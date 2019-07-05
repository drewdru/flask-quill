import os
import html
import base64

from flask import request
from flask import Flask, render_template
from jinja2 import Template

from flask_quill.templates.template import getDependecies


from example.form.example import ArticleEditForm

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/uploaded_editor_files/', methods=('POST',))
def uploaded_editor_files():
    # TODO: save your image and return url
    image = request.files['image']  
    if image:
        image.filename = html.escape(image.filename, True)
        ext = os.path.splitext(image.filename)[1].replace(".", "")
        content_type = image.content_type
        size = len(image.read())
        # Put file cursor to initial position
        image.seek(0)
        print(image.filename, ext, content_type, size)

        data = image.read()
        # data:image/png
        # return base64.b64encode(data)
        return "data:{};base64,{}".format(content_type, base64.b64encode(data).decode("utf-8"))
    return request.form.image.data

@app.route('/delete_file_by_url/', methods=('DELETE',))
def delete_files():
    # TODO: save your image and return url
    return 'Image was deleted'
    

@app.route('/', methods=('GET', 'POST'))
def myobject_route():
    data = {
        'active': True,
        'tabs': [
            {
                'language': 'ru',
                'title': 'Test',
                'content': '<p>TEST!</p>',
                'content_preview': 'Test',
            },
            {
                'language': 'en',
                'title': 'Test2',
                'content': '<p>TEST2!</p>',
                'content_preview': 'Test2',
            },
        ]
    }
    form = ArticleEditForm(data=data)
    if request.method == "POST":
        form.process(request.form)
        if form.validate():
            active = form.data['active']
            for tab in form.tabs:
                language = tab.data['language'],
                title = tab.data['title']
                content = tab.data['content']
                content_preview = tab.data['content_preview']
                # TODO: save data
    
    return render_template(
        'edit.html',
        form=form,
        flask_quill_dependencies=getDependecies(),
    )