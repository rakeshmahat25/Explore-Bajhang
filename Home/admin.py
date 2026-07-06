from django.contrib import admin
from .models import *

class DestinationImageInline(admin.TabularInline):
    model = DestinationImage
    extra = 1

class DestinationFaqInline(admin.TabularInline):
    model = DestinationFaq
    extra = 1

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'is_weekly_featured', 'visit_count', 'sort_order']
    list_filter = ['is_featured', 'is_weekly_featured', 'is_active']
    search_fields = ['title', 'description', 'location']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [DestinationImageInline, DestinationFaqInline]

@admin.register(Adventure)
class AdventureAdmin(admin.ModelAdmin):
    list_display = ['title', 'activity_type', 'difficulty', 'duration', 'is_featured']
    list_filter = ['activity_type', 'difficulty', 'is_featured', 'is_active']
    search_fields = ['title', 'location']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Culture)
class CultureAdmin(admin.ModelAdmin):
    list_display = ['title', 'culture_type', 'is_featured']
    list_filter = ['culture_type', 'is_featured', 'is_active']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'location', 'is_upcoming', 'is_featured']
    list_filter = ['is_upcoming', 'is_featured', 'is_active']
    search_fields = ['title', 'location']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'published_at', 'is_featured', 'visit_count']
    list_filter = ['category', 'is_featured', 'is_active', 'published_at']
    search_fields = ['title', 'content', 'short_description']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['gallery', 'alt_text', 'is_video', 'sort_order']
    list_filter = ['gallery', 'is_video']

@admin.register(VideoHighlight)
class VideoHighlightAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration', 'is_featured']
    list_filter = ['is_featured', 'is_active']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'rating', 'is_featured']
    list_filter = ['rating', 'is_featured', 'is_active']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read']
    search_fields = ['name', 'email', 'subject', 'message']

@admin.register(CommunityStory)
class CommunityStoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_name', 'status', 'is_featured', 'created_at']
    list_filter = ['status', 'is_featured']
    search_fields = ['title', 'author_name', 'content']

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['title', 'listing_type', 'is_featured', 'is_premium', 'average_rating']
    list_filter = ['listing_type', 'is_featured', 'is_premium', 'is_active']
    search_fields = ['title', 'description', 'address']

@admin.register(BusinessCategory)
class BusinessCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BusinessReview)
class BusinessReviewAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'business', 'rating', 'is_approved']
    list_filter = ['rating', 'is_approved']

@admin.register(TravelPackage)
class TravelPackageAdmin(admin.ModelAdmin):
    list_display = ['title', 'destination', 'duration', 'price', 'discounted_price', 'is_featured']
    list_filter = ['destination', 'is_featured']

@admin.register(BookingInquiry)
class BookingInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'package', 'guests', 'is_read', 'created_at']
    list_filter = ['is_read']

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active']

@admin.register(MonthlyTheme)
class MonthlyThemeAdmin(admin.ModelAdmin):
    list_display = ['title', 'month', 'year', 'is_active']
    list_filter = ['is_active', 'month', 'year']

@admin.register(WeeklyTheme)
class WeeklyThemeAdmin(admin.ModelAdmin):
    list_display = ['title', 'monthly_theme', 'week_number']
    list_filter = ['monthly_theme']

@admin.register(SocialMediaPost)
class SocialMediaPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'platform', 'post_type', 'status', 'scheduled_date']
    list_filter = ['platform', 'post_type', 'status']

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['question', 'is_active', 'ends_at']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']

@admin.register(PhotoContest)
class PhotoContestAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_name', 'is_winner', 'is_approved', 'vote_count']
    list_filter = ['is_winner', 'is_approved']

@admin.register(AdSpace)
class AdSpaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'is_active', 'start_date', 'end_date']
    list_filter = ['position', 'is_active']

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']
    search_fields = ['key']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'blog', 'is_approved', 'created_at']
    list_filter = ['is_approved']
