from django import template
from django.template.loader import get_template
import imp

register = template.Library()

@register.filter
def app_links(app, request):
    try:
        app_info = imp.find_module(app)
        loaded_app = imp.load_module(app, *app_info)
        app_links_info = imp.find_module('app_links', loaded_app.__path__)
        links = imp.load_module('app_links', *app_links_info)
        return links.app_links(request)
    except ImportError:
        return ''

@register.simple_tag
def collapsed_admin_list_filter(cl, spec):
    tpl = get_template(spec.template)
    return tpl.render({
        'title': spec.title,
        'choices': list(spec.choices(cl)),
        'selected_choices': list(spec.selected_choices(cl)),
        'spec': spec,
    })
