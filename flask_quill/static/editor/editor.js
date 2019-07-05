class QuillWTForms {
  /**
  * @param {object} config 
  *   QuillWTForms config 
  *   {
  *     modelID: Number,
  *     uploadImageUrl: string,
  *     deleteImageUrl: string,
  *     tabFieldName: string,
  *   }
  * @param {object} handlers
  *   Quill Handlers https://quilljs.com/docs/modules/toolbar/#toolbar-module
  * @param {Array} toolbarOptions
  *   Quill toolbar options https://quilljs.com/docs/modules/toolbar/#container
  */
  constructor(config, handlers=null, toolbarOptions=null) {
    const vm = this;

    vm.modelID = config.modelID;
    vm.uploadImageUrl = config.uploadImageUrl;
    vm.deleteImageUrl = config.deleteImageUrl;
    
    vm.toolbarOptions = toolbarOptions;
    if (vm.toolbarOptions === null) {
      vm.toolbarOptions = [
        ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
        ['blockquote', 'code-block'],  
        [{ 'header': 1 }, { 'header': 2 }],               // custom button values
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
        [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
        [{ 'direction': 'rtl' }],                         // text direction  
        [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
        [ 'link', 'image', 'video' ],          // add's image support
        [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
        [{ 'font': ['Avenir', 'Sans', 'Serif', 'Monospace' ] }],
        [{ 'align': ''}, { 'align': 'center'}, { 'align': 'right'},{ 'align': 'justify'}],  
        ['clean'],                                         // remove formatting button
      ];
    }

    /**
    * Get image url from Delta
    *
    * @param {Delta} delta 
    */
    vm.getImgUrls = (delta) => {
      return delta.ops.filter(i => i.insert && i.insert.image).map(i => i.insert.image);
    }

    vm.initWysiwygWidgets = () => {
      document.querySelectorAll('.wysiwyg').forEach(item => {
        const table = item.closest('table');
        const table_data = table.getAttribute("id").split('__');
        const tab_id = table_data[0].replace('-language', '');
  
        const editor = new Quill(item, {
            modules: {
                toolbar: {
                    container: vm.toolbarOptions,
                    handlers: vm.handlers,
                },
            },
            theme: 'snow',
            attributes: {
              height: '170',
              width: '400'
            }
        });
        
        // TODO: get content element 
        const contentId = `#hidden-${item.getAttribute('id')}`; // TODO: CHANGE FOR TABS
        const content = $(contentId).val();

        let is_innerHTML = true;
        const qlEditorElem = $(item).find('.ql-editor');
        qlEditorElem[0].innerHTML = content
        setTimeout(function(){ is_innerHTML = false; }, 1000);
        
        editor.on('text-change', (delta, oldContents, source) => {
            if (is_innerHTML) return;
            if (source !== 'user') return;
  
            const inserted = vm.getImgUrls(delta);
            const deleted = vm.getImgUrls(editor.getContents().diff(oldContents));
            for (let i = 0; i < inserted.length; i++) {
                // Save Image from clipboard
                try {
                    const file = vm.b64toBlob(inserted[i]);
                    editor.setContents(oldContents);
                    saveToServer(file.file, file.filename);
                } catch (e) {
                  vm.downloadedImg = new Image;
                  vm.downloadedImg.crossOrigin = "Anonymous";
                  vm.downloadedImg.addEventListener("load", () => {
                    try {
                      let canvas = document.createElement("canvas");
                      let context = canvas.getContext("2d");

                      canvas.width = vm.downloadedImg.width;
                      canvas.height = vm.downloadedImg.height;
                      
                      context.drawImage(vm.downloadedImg, 0, 0);
                      const file = vm.b64toBlob(canvas.toDataURL("image/png"));
                      editor.setContents(oldContents);
                      saveToServer(file.file, file.filename);
                    } catch (e) {
                      console.log('error:', e);
                    }
                  }, false);
                  vm.downloadedImg.src = inserted[i];
                }
            }
            deleted.length && console.log('delete', deleted)
            for (let i = 0; i < deleted.length; i++) {
              vm.deleteFromServer(deleted[i]);
            }
            $(contentId).attr("value", item.children[0].innerHTML);
        });

        /**
        * Step1. select local image
        *
        */
        function selectLocalImage(event, args) {
          const input = document.createElement('input');
          input.setAttribute('type', 'file');
          input.click();
      
          // Listen upload local image and save to server
          input.onchange = () => {
            const file = input.files[0];
      
            // file type is only image.
            if (/^image\//.test(file.type)) {
              saveToServer(file);
            } else {
              // TODO: flash error
              console.warn('You could only upload images.');
            }
          };
        }
        /**
        * Step2. save to server
        *
        * @param {File} file
        * @param {String} filename for Blob
        */
        function saveToServer(file, filename=null) {
          const fd = new FormData();
          fd.append('id', vm.modelID);
          if (filename) {
              fd.append('image', file, filename);
          } else {
              fd.append('image', file);
          }

          const xhr = new XMLHttpRequest();      
          xhr.open('POST', `${vm.uploadImageUrl}?id=${vm.modelID}`, true);
          xhr.onload = () => {
              if (xhr.status === 200) {
                  // this is callback data: url
                  const url = xhr.responseText;
                  insertToEditor(url);
              }
          };
          xhr.send(fd);
        }
        /**
        * Step3. insert image url to rich editor.
        *
        * @param {string} url
        */
        function insertToEditor(url) {
          const range = editor.getSelection();
          const delta = editor.insertEmbed(range.index, 'image', `${url}`);
          $(contentId).attr("value", item.children[0].innerHTML);
        }

        /**
        * Base64 image string to Blob
        *
        * @param {String} dataURL
        */
        vm.b64toBlob = (dataURL) => {
            const block = dataURL.split(";");
            const contentType = block[0].split(":")[1];
            const byteString = atob(block[1].split(",")[1]);
            const ab = new ArrayBuffer(byteString.length);
            const ia = new Uint8Array(ab);
      
            for (let i = 0; i < byteString.length; i++) {
                ia[i] = byteString.charCodeAt(i);
            }
            return {
                file: new Blob([ab], { type: contentType }),
                filename: `blob.${contentType.split("/")[1]}`
            };
        }
        /**
        * Delete from server
        *
        * @param {String} path 
        */
        vm.deleteFromServer = (url) => {
          const fd = new FormData();
          fd.append('id', MODEL_ID);
          fd.append('url', url);

          const xhr = new XMLHttpRequest();
          xhr.open('DELETE', `${DELETE_IMAGE_URL}?id=${MODEL_ID}`, true);
          xhr.onload = () => {
              console.log(xhr.responseText);
              if (xhr.status === 200) {
                  console.log('Image deleted from server');
              }
          };
          xhr.send(fd);
        }

        if (handlers) {
          vm.handlers = handlers;
          if (vm.handlers.image === undefined) {
            editor.getModule("toolbar").addHandler("image", selectLocalImage);
          }
        } else {
          editor.getModule("toolbar").addHandler("image", selectLocalImage);
        }
      });
    }

    vm.initWysiwygWidgets();
  }
}

