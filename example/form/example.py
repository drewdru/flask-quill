from wtforms import (
    Form,
    FormField,
    FileField,
    BooleanField,
    StringField,
    SelectField,
    FieldList,
    DecimalField,
    HiddenField,
)
from wtforms.validators import Optional
from flask_quill.fields.wysiwyg import WysiwygField
from flask_quill.fields.tabs import TabField
from flask_quill.widgets.tabs import TabWidget

from wtforms import fields, widgets

LANGUAGE = [
    ('en', u"English"),
    ('ru', u"Russian"),
]


class ArticleFileUploadForm(Form):
    """Upload Article image"""

    file = FileField("File")
    is_previe = BooleanField("Is preview")

class ArticleFileDeleteForm(Form):
    """Delete Article image"""

    id = DecimalField("ID")
    url = StringField("Url")

class ArticleListForm(Form):
    """Change active on Article methods list"""
    
    language = SelectField("Language", choices=LANGUAGE)
    title = StringField(u"Title")
    content = StringField(u"Content")
    content_preview = StringField(u"Content preview")
    active = BooleanField("Active")
    
class EditListForm(Form):
    language = HiddenField()
    title = StringField(u"Title")
    content = WysiwygField(u"Content")
    content_preview = StringField(u"Content preview")
    # active = BooleanField("Active")
    # widget = Tab()


class ArticleEditForm(Form):
    """Change active on Article methods list"""

    active = BooleanField("Active")
    tabs = TabField(FormField(EditListForm),
                    tabs=LANGUAGE,
                    wysiwyg_fields=['content'],
                    tabs_field='language')



    