import os
from jinja2 import Template

def getDependecies():
    currentDir = os.path.abspath(os.path.dirname(__file__))
    # print(currentDir)
    # print (__file__)
    # print (os.path.join(os.path.dirname(__file__), '..'))
    # print (os.path.dirname(os.path.realpath(__file__)))
    # print ( )
    dependenciesPath = "{}/dependencies.html".format(currentDir)
    staticDir = "{}/../static/".format(currentDir)

    data = ''
    with open(dependenciesPath,'r') as f:
        data = f.read()

    tabsCSS = ''
    viewQuillCSS = ''
    tabsJS = ''
    editorJS = ''
    with open('{}tabs/tabs.css'.format(staticDir),'r') as f:
        tabsCSS = f.read()
    with open('{}editor/view-quill.css'.format(staticDir),'r') as f:
        viewQuillCSS = f.read()
    with open('{}tabs/tabs.js'.format(staticDir),'r') as f:
        tabsJS = f.read()
    with open('{}editor/editor.js'.format(staticDir),'r') as f:
        editorJS = f.read()

    tm = Template(data)
    msg = tm.render(tabsCSS=tabsCSS, tabsJS=tabsJS, editorJS=editorJS, viewQuillCSS=viewQuillCSS)

    return msg