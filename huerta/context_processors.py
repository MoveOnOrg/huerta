from django.conf import settings

def theme_settings(request):
    """
    Returns context variables required by apps that use huerta.
    """

    return {'apps': settings.INSTALLED_APPS,
            'extrastaticcss': getattr(settings, 'HUERTA_EXTRA_STATIC_CSS', ''),
            'site_name': getattr(settings, 'SITE_NAME', ''),
            'extrahead': getattr(settings, 'HUERTA_EXTRA_HEAD',
                                 """
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
                  integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u"
                  crossorigin="anonymous" />
                                 """),
            'extrafooter': getattr(settings, 'HUERTA_EXTRA_FOOTER', '')}
