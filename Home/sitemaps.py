from django.contrib import sitemaps
from django.urls import reverse
from .models import Blog, Destination


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['Home:home', 'Home:about', 'Home:gallery', 'Home:contact',
                'Home:destination_list', 'Home:adventure_list', 'Home:culture_list',
                'Home:event_list', 'Home:blog_list', 'Home:story_list',
                'Home:business_list', 'Home:package_list']

    def location(self, item):
        return reverse(item)


class BlogSitemap(sitemaps.Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Blog.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class DestinationSitemap(sitemaps.Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Destination.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at
