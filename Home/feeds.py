from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Blog


class BlogFeed(Feed):
    title = "Explore Bajhang Blog"
    link = "/blog/"
    description = "Latest blog posts about Bajhang, Nepal"

    def items(self):
        return Blog.objects.filter(is_active=True)[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.short_description

    def item_link(self, item):
        return reverse('Home:blog_detail', args=[item.slug])
