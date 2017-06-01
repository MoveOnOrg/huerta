from django.conf import settings

def theme_settings(request):
    """
    Returns context variables required by apps that use huerta.
    """

    return {'apps': settings.INSTALLED_APPS,
            'extrastaticcss': getattr(settings, 'HUERTA_EXTRA_STATIC_CSS', None),
            'site_name': getattr(settings, 'SITE_NAME', None),
            'extrahead': getattr(settings, 'HUERTA_EXTRA_HEAD', None),
            'extrafooter': getattr(settings, 'HUERTA_EXTRA_FOOTER', None)}
