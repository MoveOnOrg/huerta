# Huerta

Huerta is a set of templates and template-related functionality for Django sites, customizable with any [Bootstrap](https://getbootstrap.com/)-based CSS.

## Using

* Add `huerta` to `INSTALLED_APPS` in `settings.py`
* Add `'huerta.context_processors.theme_settings'` to `context_processors` in `settings.py`.

## Customizing

Huerta will read the following settings from the Django site's `settings.py`:

* *SITE_NAME*: the name of the site, to put in `<title>`.
* *HUERTA_EXTRA_HEAD*: HTML to put in `<head>`.
* *HUERTA_EXTRA_FOOTER*: HTML to put in `<footer>`.
* *HUERTA_EXTRA_STATIC_CSS*: paths to local static CSS files, relative to the static directory path.

## App links

Huerta allows each Django app to supply its own admin navigation links. To add links to the admin navigation:

* Create a file in your app named `app_links.py` with a function named `app_links` that takes the request and returns relevant links wrapped in `<li>`, e.g.:

```
def app_links(request):
    user = request.user
    links = []
    if user.has_perm('special.permission'):
      links.append('<li><a href="%s">Special Page</a></li>' % reverse('special:page'))
    return ''.join(links)
```

## Model Admin Display Options

Huerta adds some options to model admin displays, i.e. classes extending admin.ModelAdmin. Here's an example using all options:

```from huerta.filters import CollapsedListFilter, textinputfilter_factory

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_filter = (('venue', CollapsedListFilter),
                   textinputfilter_factory('Email',
                            'email'))
    change_list_template = "admin/change_list_filters_top.html"
    filters_collapsable = True
    filters_require_submit = True
    disable_list_headers = True
    list_striped = True
```

### CollapsedListFilter

CollapsedListFilter is a filter type that shows multiple options in a drop-down.

### textinputfilter_factory(title, parameter_name)

Creates a text input filter where parameter_name is searched by `__icontains`

### change_list_filters_top.html

This template moves filters above results.

### filters_collapsable = True

This option makes the entire filters panel collaspable.

### filters_require_submit = True

This option makes filters no longer submit on select, and instead adds a "Filter" button for submitting.

### disable_list_headers = True

This option removes headers from the results list.

### list_striped = True

This option makes the results list table striped.
