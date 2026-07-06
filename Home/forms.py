from django import forms
from .models import ContactMessage, NewsletterSubscriber, CommunityStory, BookingInquiry, BusinessReview, BlogComment, PhotoContest


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your Message'}),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        }


class StoryForm(forms.ModelForm):
    class Meta:
        model = CommunityStory
        fields = ['title', 'author_name', 'author_email', 'short_description', 'content', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Story Title'}),
            'author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'author_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Short summary'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Your story...'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = BookingInquiry
        fields = ['name', 'email', 'phone', 'package', 'check_in', 'check_out', 'guests', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'package': forms.Select(attrs={'class': 'form-select'}),
            'check_in': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = BusinessReview
        fields = ['author_name', 'author_email', 'rating', 'comment']
        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form-control'}),
            'author_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-select'}, choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['name', 'email', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your comment'}),
        }


class PhotoContestForm(forms.ModelForm):
    class Meta:
        model = PhotoContest
        fields = ['title', 'description', 'image', 'author_name', 'author_email']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'author_name': forms.TextInput(attrs={'class': 'form-control'}),
            'author_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
