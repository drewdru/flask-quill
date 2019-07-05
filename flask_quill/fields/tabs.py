from wtforms import fields

from flask_quill.widgets.tabs import TabWidget

class TabField(fields.FieldList):
    widget = TabWidget()

    def __init__(self, unbound_field, label=None, validators=None,
                 min_entries=0, max_entries=None, tabs=[],
                 wysiwyg_fields=['content'], tabs_field='language',
                 default=tuple(), **kwargs):
        super(TabField, self).__init__(unbound_field,
                                       label=label,
                                       validators=validators,
                                       default=default,
                                       **kwargs)
        self.min_entries = len(tabs)
        self.widget = TabWidget(tabs=tabs,
                                wysiwyg_fields=wysiwyg_fields,
                                tabs_field=tabs_field)
        
        

