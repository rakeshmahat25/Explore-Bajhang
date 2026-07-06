from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['sort_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Destination(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField(max_length=300)
    description = models.TextField()
    history = models.TextField(blank=True)
    culture = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to='destinations/hero/')
    thumbnail_image = models.ImageField(upload_to='destinations/thumbnails/', blank=True)
    location = models.CharField(max_length=200, blank=True)
    best_season = models.CharField(max_length=100, blank=True)
    travel_tips = models.TextField(blank=True)
    things_to_do = models.TextField(blank=True)
    nearby_attractions = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    weather_info = models.TextField(blank=True, help_text="Weather placeholder")
    is_featured = models.BooleanField(default=False)
    is_weekly_featured = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    visit_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-is_featured', 'sort_order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.thumbnail_image and self.hero_image:
            self.thumbnail_image = self.hero_image
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class DestinationImage(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='destinations/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    caption = models.CharField(max_length=300, blank=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.destination.title} - Image {self.id}"


class DestinationFaq(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=300)
    answer = models.TextField()
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Destination FAQ"

    def __str__(self):
        return self.question


class Adventure(BaseModel):
    ACTIVITY_TYPES = [
        ('trekking', 'Trekking'),
        ('camping', 'Camping'),
        ('cycling', 'Cycling'),
        ('hiking', 'Hiking'),
        ('photography', 'Photography'),
        ('bird_watching', 'Bird Watching'),
        ('river_activities', 'River Activities'),
        ('other', 'Other'),
    ]

    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('hard', 'Hard'),
        ('expert', 'Expert'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    duration = models.CharField(max_length=100, help_text="e.g., 3-5 days")
    equipment = models.TextField(blank=True)
    safety_info = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    description = models.TextField()
    hero_image = models.ImageField(upload_to='adventures/')
    price_range = models.CharField(max_length=100, blank=True)
    best_season = models.CharField(max_length=100, blank=True)
    guide_available = models.BooleanField(default=False)
    guide_info = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_featured', 'sort_order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class AdventureImage(models.Model):
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='adventures/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']


class Culture(BaseModel):
    CULTURE_TYPES = [
        ('traditional_dress', 'Traditional Dress'),
        ('festival', 'Festival'),
        ('food', 'Food'),
        ('music', 'Music'),
        ('dance', 'Dance'),
        ('language', 'Language'),
        ('history', 'History'),
        ('religion', 'Religion'),
        ('tradition', 'Local Tradition'),
        ('handicraft', 'Handicraft'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    culture_type = models.CharField(max_length=50, choices=CULTURE_TYPES)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    image = models.ImageField(upload_to='culture/')
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_featured', 'sort_order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Event(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='events/')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200)
    registration_url = models.URLField(blank=True, help_text="Registration placeholder URL")
    is_upcoming = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogCategory(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Blog Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Blog(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='blogs')
    tags = models.ManyToManyField(Tag, blank=True, related_name='blogs')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    featured_image = models.ImageField(upload_to='blog/')
    thumbnail_image = models.ImageField(upload_to='blog/thumbnails/', blank=True)
    short_description = models.TextField(max_length=300)
    content = models.TextField()
    reading_time = models.IntegerField(help_text="Reading time in minutes", default=5)
    is_featured = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    published_at = models.DateTimeField(default=timezone.now)
    visit_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-published_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.thumbnail_image and self.featured_image:
            self.thumbnail_image = self.featured_image
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Gallery(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='gallery/covers/')

    class Meta:
        verbose_name_plural = "Galleries"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery/')
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    caption = models.TextField(blank=True)
    sort_order = models.IntegerField(default=0)
    is_video = models.BooleanField(default=False)
    video_url = models.URLField(blank=True, help_text="YouTube/Vimeo URL for video items")

    class Meta:
        ordering = ['sort_order']


class VideoHighlight(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_url = models.URLField(help_text="YouTube/Vimeo URL")
    thumbnail = models.ImageField(upload_to='videos/thumbnails/', blank=True)
    is_featured = models.BooleanField(default=False)
    duration = models.CharField(max_length=20, blank=True, help_text="e.g., 3:45")

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.title


class Testimonial(BaseModel):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200, blank=True, help_text="e.g., Traveler from Kathmandu")
    avatar = models.ImageField(upload_to='testimonials/', blank=True)
    content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject or 'No Subject'}"


class CommunityStory(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    content = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    cover_image = models.ImageField(upload_to='stories/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Community Stories"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class StoryImage(models.Model):
    story = models.ForeignKey(CommunityStory, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='stories/gallery/')
    caption = models.CharField(max_length=300, blank=True)


class BusinessCategory(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Business Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Business(BaseModel):
    LISTING_TYPES = [
        ('hotel', 'Hotel'),
        ('homestay', 'Homestay'),
        ('restaurant', 'Restaurant'),
        ('travel_agency', 'Travel Agency'),
        ('vehicle_rental', 'Vehicle Rental'),
        ('guide', 'Guide'),
        ('adventure_operator', 'Adventure Operator'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    listing_type = models.CharField(max_length=50, choices=LISTING_TYPES)
    category = models.ForeignKey(BusinessCategory, on_delete=models.SET_NULL, null=True, related_name='businesses')
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    logo = models.ImageField(upload_to='business/logos/', blank=True)
    cover_image = models.ImageField(upload_to='business/covers/')
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    address = models.CharField(max_length=300, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_sponsored = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    review_count = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Businesses"
        ordering = ['-is_featured', '-is_premium', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BusinessImage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='business/gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']


class BusinessReview(BaseModel):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='reviews')
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author_name} - {self.business.title}"


class TravelPackage(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, related_name='packages')
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='packages/')
    duration = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    includes = models.TextField(blank=True, help_text="Comma-separated list of inclusions")
    itinerary = models.TextField(blank=True)
    max_people = models.IntegerField(default=10)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_featured', 'sort_order']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BookingInquiry(models.Model):
    package = models.ForeignKey(TravelPackage, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    guests = models.IntegerField(default=1)
    message = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Booking inquiries"

    def __str__(self):
        return f"{self.name} - {self.package or 'General Inquiry'}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribe_token = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


class MonthlyTheme(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    month = models.CharField(max_length=20, help_text="Month name e.g., January")
    year = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='themes/', blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.month} {self.year}"


class WeeklyTheme(BaseModel):
    monthly_theme = models.ForeignKey(MonthlyTheme, on_delete=models.CASCADE, related_name='weekly_themes')
    title = models.CharField(max_length=200)
    week_number = models.IntegerField(help_text="1-4 for week of month")
    description = models.TextField()
    image = models.ImageField(upload_to='themes/weekly/', blank=True)

    class Meta:
        ordering = ['week_number']

    def __str__(self):
        return f"Week {self.week_number}: {self.title}"


class SocialMediaPost(BaseModel):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
    ]

    POST_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('carousel', 'Carousel'),
        ('story', 'Story'),
        ('text', 'Text Post'),
        ('reel', 'Reel'),
        ('short', 'Short'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    post_type = models.CharField(max_length=20, choices=POST_TYPES)
    topic = models.CharField(max_length=200, blank=True)
    caption = models.TextField(blank=True)
    hashtags = models.CharField(max_length=500, blank=True)
    media_file = models.FileField(upload_to='social/', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_date = models.DateTimeField(null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    repurposed_from = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='repurposed_posts')

    class Meta:
        ordering = ['-scheduled_date', '-created_at']

    def __str__(self):
        return f"{self.get_platform_display()} - {self.title}"


class Poll(BaseModel):
    question = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)
    ends_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.question


class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=200)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return self.text


class Quiz(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order']


class PhotoContest(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='contests/')
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    is_winner = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    vote_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-vote_count', '-created_at']

    def __str__(self):
        return self.title


class AdSpace(BaseModel):
    POSITION_CHOICES = [
        ('header', 'Header'),
        ('sidebar', 'Sidebar'),
        ('footer', 'Footer'),
        ('between_content', 'Between Content'),
    ]

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='ads/')
    url = models.URLField()
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return self.title


class SiteSetting(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['key']

    def __str__(self):
        return self.key

    @classmethod
    def get_setting(cls, key, default=''):
        try:
            return cls.objects.get(key=key).value
        except cls.DoesNotExist:
            return default


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.name} on {self.blog.title}"


class Rating(models.Model):
    content_type = models.CharField(max_length=50, help_text="e.g., destination, adventure")
    content_id = models.IntegerField()
    user_name = models.CharField(max_length=100)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.content_type} #{self.content_id} - {self.rating}/5"
