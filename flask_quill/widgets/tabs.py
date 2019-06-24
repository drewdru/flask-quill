from wtforms import widgets

class TabWidget(object):
    
    def __init__(self, tabs=[]):
        self.tabs = tabs

    def __call__(self, fields, wysiwyg_field='content', **kwargs):
        kwargs.setdefault('id', fields.id)
        
        # kwargs.setdefault('class', 'tab')
        if kwargs.get('class'):
            kwargs['class'] += ' tabwidget'
        else:
            kwargs.setdefault('class', 'tabwidget')

        html = ['<div {}>'.format(widgets.core.html_params(**kwargs))]
        html = ['<div class="tab">']
        
        for tab in self.tabs:
            html.append("""<button type="button" class="tablinks" onclick="openTab(event, '{}')">
{}</button>""".format(tab[0], tab[1]))
        html.append('</div>')

        # field_list = ''
        # for subfield in fields:
        #     field_list += '{} {}'.format(subfield(), subfield.label)
        for index, tab in enumerate(self.tabs):
            subfield = fields[index]
            content_id = "{}-{}".format(subfield.id, wysiwyg_field)
            subfield.id = "{}-language__{}".format(subfield.id, tab[0])

            html.append("""<div id="{}" class="tabcontent">
{}</div><input type="hidden" id="hidden-{}" name="{}" value="{}">""".format(
                tab[0],
                subfield(),
                content_id,
                content_id,
                subfield.data[wysiwyg_field]))

        html.append('</div>')
        return widgets.HTMLString(''.join(html))
        # return widgets.HTMLString('<div {}>{}</div>'.format(
        #     widgets.html_params(name=field.name, **kwargs)),
        #     data
        # )