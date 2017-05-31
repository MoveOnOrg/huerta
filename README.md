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

### App links

Huerta allows each Django app to supply its own admin navigation links. To add links to the admin navigation:

* Create a file in your app named `app_links.py` with a function named `app_links` that takes the request and returns relevant links wrapped in `<li>`, e.g.:

```def app_links(request):
    user = request.user
    links = []
    if user.has_perm('special.permission'):
      links.append('<li><a href="%s">Special Page</a></li>' % reverse('special:page'))
    return ''.join(links)
```
