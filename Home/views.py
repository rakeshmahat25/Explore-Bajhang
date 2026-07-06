from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Count
from .models import *
from .forms import *


def home(request):
    destinations = Destination.objects.filter(is_active=True, is_featured=True)[:6]
    adventures = Adventure.objects.filter(is_active=True, is_featured=True)[:3]
    cultures = Culture.objects.filter(is_active=True, is_featured=True)[:4]
    events = Event.objects.filter(is_active=True, is_upcoming=True)[:3]
    blogs = Blog.objects.filter(is_active=True)[:3]
    testimonials = Testimonial.objects.filter(is_active=True, is_featured=True)[:5]
    galleries = Gallery.objects.filter(is_active=True)[:3]
    videos = VideoHighlight.objects.filter(is_active=True)[:3]
    weekly_featured = Destination.objects.filter(is_active=True, is_weekly_featured=True).first()
    stories = CommunityStory.objects.filter(is_active=True, status='approved')[:3]
    packages = TravelPackage.objects.filter(is_active=True, is_featured=True)[:3]
    monthly_theme = MonthlyTheme.objects.filter(is_active=True).first()

    context = {
        'destinations': destinations,
        'adventures': adventures,
        'cultures': cultures,
        'events': events,
        'blogs': blogs,
        'testimonials': testimonials,
        'galleries': galleries,
        'videos': videos,
        'weekly_featured': weekly_featured,
        'stories': stories,
        'packages': packages,
        'monthly_theme': monthly_theme,
        'contact_form': ContactForm(),
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'index.html', context)


def destination_list(request):
    destinations = Destination.objects.filter(is_active=True)
    query = request.GET.get('q')
    if query:
        destinations = destinations.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query)
        )
    context = {'destinations': destinations}
    return render(request, 'destination_list.html', context)


def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug, is_active=True)
    destination.visit_count += 1
    destination.save(update_fields=['visit_count'])
    related = Destination.objects.filter(is_active=True).exclude(id=destination.id)[:3]
    context = {
        'destination': destination,
        'related_destinations': related,
    }
    return render(request, 'destination_detail.html', context)


def adventure_list(request):
    adventures = Adventure.objects.filter(is_active=True)
    activity = request.GET.get('activity')
    if activity:
        adventures = adventures.filter(activity_type=activity)
    context = {
        'adventures': adventures,
        'activity_types': Adventure.ACTIVITY_TYPES,
    }
    return render(request, 'adventure_list.html', context)


def adventure_detail(request, slug):
    adventure = get_object_or_404(Adventure, slug=slug, is_active=True)
    related = Adventure.objects.filter(is_active=True, activity_type=adventure.activity_type).exclude(id=adventure.id)[:3]
    context = {'adventure': adventure, 'related_adventures': related}
    return render(request, 'adventure_detail.html', context)


def culture_list(request):
    cultures = Culture.objects.filter(is_active=True)
    ctype = request.GET.get('type')
    if ctype:
        cultures = cultures.filter(culture_type=ctype)
    context = {
        'cultures': cultures,
        'culture_types': Culture.CULTURE_TYPES,
    }
    return render(request, 'culture_list.html', context)


def culture_detail(request, slug):
    culture = get_object_or_404(Culture, slug=slug, is_active=True)
    related = Culture.objects.filter(is_active=True, culture_type=culture.culture_type).exclude(id=culture.id)[:3]
    context = {'culture': culture, 'related_items': related}
    return render(request, 'culture_detail.html', context)


def event_list(request):
    events = Event.objects.filter(is_active=True)
    context = {'events': events}
    return render(request, 'event_list.html', context)


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_active=True)
    related = Event.objects.filter(is_active=True).exclude(id=event.id)[:3]
    context = {'event': event, 'related_events': related}
    return render(request, 'event_detail.html', context)


def about(request):
    context = {
        'testimonials': Testimonial.objects.filter(is_active=True, is_featured=True)[:3],
        'milestones': [
            {'year': '2020', 'title': 'Founded', 'description': 'Explore Bajhang was established'},
            {'year': '2021', 'title': 'First Campaign', 'description': 'Launched Discover Bajhang campaign'},
            {'year': '2022', 'title': 'Community Growth', 'description': 'Reached 10K followers'},
            {'year': '2023', 'title': 'Website Launch', 'description': 'Official website launched'},
        ],
    }
    return render(request, 'about.html', context)


def gallery(request):
    galleries = Gallery.objects.filter(is_active=True)
    images = GalleryImage.objects.filter(gallery__is_active=True)[:30]
    videos = VideoHighlight.objects.filter(is_active=True)[:6]
    context = {
        'galleries': galleries,
        'images': images,
        'videos': videos,
    }
    return render(request, 'gallery.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent.')
            return redirect('Home:contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def blog_list(request):
    blogs = Blog.objects.filter(is_active=True)
    categories = BlogCategory.objects.all()
    tags = Tag.objects.all()
    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')
    query = request.GET.get('q')

    if category_slug:
        blogs = blogs.filter(category__slug=category_slug)
    if tag_slug:
        blogs = blogs.filter(tags__slug=tag_slug)
    if query:
        blogs = blogs.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(short_description__icontains=query))

    context = {
        'blogs': blogs,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'blog_list.html', context)


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_active=True)
    blog.visit_count += 1
    blog.save(update_fields=['visit_count'])

    if request.method == 'POST' and blog.allow_comments:
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.save()
            messages.success(request, 'Your comment has been submitted for approval.')
            return redirect('Home:blog_detail', slug=blog.slug)
    else:
        form = BlogCommentForm()

    related = Blog.objects.filter(is_active=True, category=blog.category).exclude(id=blog.id)[:3]
    context = {
        'blog': blog,
        'related_blogs': related,
        'comment_form': form,
        'comments': blog.comments.filter(is_approved=True),
    }
    return render(request, 'blog_detail.html', context)


def story_list(request):
    stories = CommunityStory.objects.filter(is_active=True, status='approved')
    context = {'stories': stories}
    return render(request, 'story_list.html', context)


def story_detail(request, slug):
    story = get_object_or_404(CommunityStory, slug=slug, is_active=True, status='approved')
    related = CommunityStory.objects.filter(is_active=True, status='approved').exclude(id=story.id)[:3]
    context = {'story': story, 'related_stories': related}
    return render(request, 'story_detail.html', context)


def submit_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.status = 'pending'
            story.save()
            messages.success(request, 'Your story has been submitted! It will be reviewed by our team.')
            return redirect('Home:story_list')
    else:
        form = StoryForm()
    return render(request, 'submit_story.html', {'form': form})


def business_list(request):
    businesses = Business.objects.filter(is_active=True)
    listing_type = request.GET.get('type')
    query = request.GET.get('q')

    if listing_type:
        businesses = businesses.filter(listing_type=listing_type)
    if query:
        businesses = businesses.filter(Q(title__icontains=query) | Q(description__icontains=query))
    context = {
        'businesses': businesses,
        'listing_types': Business.LISTING_TYPES,
    }
    return render(request, 'business_list.html', context)


def business_detail(request, slug):
    business = get_object_or_404(Business, slug=slug, is_active=True)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.business = business
            review.save()
            messages.success(request, 'Thank you for your review!')
            return redirect('Home:business_detail', slug=business.slug)
    else:
        form = ReviewForm()
    context = {
        'business': business,
        'review_form': form,
        'reviews': business.reviews.filter(is_approved=True),
    }
    return render(request, 'business_detail.html', context)


def package_list(request):
    packages = TravelPackage.objects.filter(is_active=True)
    context = {'packages': packages}
    return render(request, 'package_list.html', context)


def package_detail(request, slug):
    package = get_object_or_404(TravelPackage, slug=slug, is_active=True)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.package = package
            booking.save()
            messages.success(request, 'Your inquiry has been submitted! We will contact you soon.')
            return redirect('Home:package_detail', slug=package.slug)
    else:
        form = BookingForm()
    context = {'package': package, 'booking_form': form}
    return render(request, 'package_detail.html', context)


def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully subscribed to our newsletter!')
        else:
            messages.error(request, 'This email is already subscribed or invalid.')
    return redirect(request.META.get('HTTP_REFERER', '/'))


def search(request):
    query = request.GET.get('q', '')
    results = {
        'destinations': [],
        'blogs': [],
        'events': [],
        'stories': [],
        'adventures': [],
        'businesses': [],
    }

    if query:
        results['destinations'] = Destination.objects.filter(
            is_active=True
        ).filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query))[:5]
        results['blogs'] = Blog.objects.filter(
            is_active=True
        ).filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(short_description__icontains=query))[:5]
        results['events'] = Event.objects.filter(
            is_active=True
        ).filter(Q(title__icontains=query) | Q(description__icontains=query))[:5]
        results['stories'] = CommunityStory.objects.filter(
            is_active=True, status='approved'
        ).filter(Q(title__icontains=query) | Q(content__icontains=query))[:5]
        results['adventures'] = Adventure.objects.filter(
            is_active=True
        ).filter(Q(title__icontains=query) | Q(description__icontains=query))[:5]
        results['businesses'] = Business.objects.filter(
            is_active=True
        ).filter(Q(title__icontains=query) | Q(description__icontains=query))[:5]

    context = {'query': query, 'results': results}
    return render(request, 'search.html', context)


def photo_contest(request):
    if request.method == 'POST':
        form = PhotoContestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your photo has been submitted for the contest!')
            return redirect('Home:photo_contest')
    else:
        form = PhotoContestForm()
    entries = PhotoContest.objects.filter(is_approved=True)
    context = {'form': form, 'entries': entries}
    return render(request, 'photo_contest.html', context)


def poll_list(request):
    polls = Poll.objects.filter(is_active=True)
    context = {'polls': polls}
    return render(request, 'poll_list.html', context)


def quiz_list(request):
    quizzes = Quiz.objects.filter(is_active=True)
    return render(request, 'quiz_list.html', {'quizzes': quizzes})
