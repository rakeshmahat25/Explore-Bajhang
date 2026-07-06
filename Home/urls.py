from django.urls import path
from . import views
from .feeds import BlogFeed

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),

    # Destinations
    path('destinations/', views.destination_list, name='destination_list'),
    path('destination/<slug:slug>/', views.destination_detail, name='destination_detail'),
    path('destination/', views.destination_list, name='destination'),

    # Adventures
    path('adventures/', views.adventure_list, name='adventure_list'),
    path('adventure/<slug:slug>/', views.adventure_detail, name='adventure_detail'),

    # Culture
    path('culture/', views.culture_list, name='culture_list'),
    path('culture/<slug:slug>/', views.culture_detail, name='culture_detail'),

    # Events
    path('events/', views.event_list, name='event_list'),
    path('event/<slug:slug>/', views.event_detail, name='event_detail'),

    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/feed/', BlogFeed(), name='blog_feed'),

    # Stories
    path('stories/', views.story_list, name='story_list'),
    path('story/<slug:slug>/', views.story_detail, name='story_detail'),
    path('submit-story/', views.submit_story, name='submit_story'),

    # Business Directory
    path('businesses/', views.business_list, name='business_list'),
    path('business/<slug:slug>/', views.business_detail, name='business_detail'),

    # Packages
    path('packages/', views.package_list, name='package_list'),
    path('package/<slug:slug>/', views.package_detail, name='package_detail'),

    # Features
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('search/', views.search, name='search'),
    path('photo-contest/', views.photo_contest, name='photo_contest'),
    path('polls/', views.poll_list, name='poll_list'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
]
