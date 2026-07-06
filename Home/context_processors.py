from .models import Category, Destination, Event, Blog, Gallery
import datetime

def site_settings(request):
    settings_dict = {
        'site_title': 'Explore Bajhang',
        'site_description': 'Discover the hidden beauty of Bajhang, Nepal',
    }

    try:
        from .models import SiteSetting
        for s in SiteSetting.objects.all():
            settings_dict[s.key] = s.value
    except:
        pass

    return {
        'site_settings': settings_dict,
        'nav_categories': list(Category.objects.filter(is_active=True)[:6]),
        'featured_destinations': list(Destination.objects.filter(is_active=True, is_featured=True)[:3]),
        'upcoming_events': list(Event.objects.filter(is_active=True, is_upcoming=True)[:3]),
        'latest_blogs': list(Blog.objects.filter(is_active=True)[:3]),
        'galleries': list(Gallery.objects.filter(is_active=True)[:4]),
        'current_year': datetime.datetime.now().year,
    }