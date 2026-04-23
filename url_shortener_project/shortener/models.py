from django.db import models
from django.contrib.auth.models import User
import random
import string

# Function to generate unique short code
def generate_short_code():
    length = 6
    while True:
        # Generate random 6-character code (letters + numbers)
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        # Make sure it's unique
        if not ShortenedURL.objects.filter(short_code=code).exists():
            return code

# Your main model - this creates the database table
class ShortenedURL(models.Model):
    # The original long URL the user wants to shorten
    original_url = models.URLField(max_length=2000, help_text="Paste your long URL here")
    
    # The unique short code (like "abc123")
    short_code = models.CharField(max_length=10, unique=True, default=generate_short_code, editable=False)
    
    # Who created this link? (links user to Django's User model)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # When was this link created?
    created_at = models.DateTimeField(auto_now_add=True)
    
    # When does this link expire? (optional, None means never expires)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # How many total clicks?
    total_clicks = models.IntegerField(default=0)
    
    # Is this link active?
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.short_code} -> {self.original_url[:50]}"
    
    def increment_clicks(self):
        """Increase click count by 1"""
        self.total_clicks += 1
        self.save(update_fields=['total_clicks'])

    def is_expired(self):
        """Check if the link has expired"""
        from django.utils import timezone
        if self.expires_at:
            return self.expires_at < timezone.now()
        return False

# This model tracks EVERY individual click for analytics
class ClickRecord(models.Model):
    # Which link was clicked?
    shortened_url = models.ForeignKey(ShortenedURL, on_delete=models.CASCADE, related_name='clicks')
    
    # When was it clicked?
    clicked_at = models.DateTimeField(auto_now_add=True)
    
    # Where did the click come from? (browser, OS, device info)
    user_agent = models.TextField(blank=True, null=True)
    
    # IP address of the person who clicked
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    # Referrer (which website sent this click)
    referrer = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"Click on {self.shortened_url.short_code} at {self.clicked_at}"
    

    