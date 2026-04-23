from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import ShortenedURL, ClickRecord
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import qrcode
from io import BytesIO
import base64

# Homepage view - where users shorten URLs
def home(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        
        # Validate URL
        validator = URLValidator()
        try:
            validator(original_url)
        except ValidationError:
            messages.error(request, 'Please enter a valid URL (include http:// or https://)')
            return render(request, 'shortener/home.html')
        
        # Create shortened URL
        if request.user.is_authenticated:
            # User is logged in - save to their account
            short_url = ShortenedURL.objects.create(
                original_url=original_url,
                created_by=request.user
            )
        else:
            # Anonymous user - save without user association
            short_url = ShortenedURL.objects.create(
                original_url=original_url
            )
        
        # Get the full short URL
        full_short_url = request.build_absolute_uri('/' + short_url.short_code)

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(full_short_url)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")

# Convert to base64 for displaying in HTML
        buffer = BytesIO()
        qr_image.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        messages.success(request, f'URL shortened successfully!')
        
        return render(request, 'shortener/home.html', {
            'short_url': full_short_url,
            'original_url': original_url,
            'short_code': short_url.short_code,
            'qr_code': qr_base64
        })
    
    return render(request, 'shortener/home.html')

# This is the magic - redirects short URL to original
def redirect_to_original(request, short_code):
    # Find the link or show 404
    short_url = get_object_or_404(ShortenedURL, short_code=short_code, is_active=True)
    
    # Check if link expired
    if short_url.is_expired():
        raise Http404("This link has expired")
    
    # Rest of your code remains the same...
    short_url.increment_clicks()
    
    ClickRecord.objects.create(
        shortened_url=short_url,
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        ip_address=request.META.get('REMOTE_ADDR', ''),
        referrer=request.META.get('HTTP_REFERER', '')
    )
    
    return redirect(short_url.original_url)

# Dashboard - shows all links created by logged-in user
@login_required
def dashboard(request):
    user_links = ShortenedURL.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Add full short URL to each link
    for link in user_links:
        link.full_short_url = request.build_absolute_uri('/' + link.short_code)
    
    return render(request, 'shortener/dashboard.html', {
        'links': user_links
    })

# Delete a link
@login_required
def delete_link(request, link_id):
    link = get_object_or_404(ShortenedURL, id=link_id, created_by=request.user)
    link.delete()
    messages.success(request, 'Link deleted successfully!')
    return redirect('dashboard')


from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'shortener/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'shortener/signup.html')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters')
            return render(request, 'shortener/signup.html')
        
        # Create user
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        messages.success(request, f'Account created! Welcome {username}')
        return redirect('home')
    
    return render(request, 'shortener/signup.html')


from django.contrib.auth import login as auth_login

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'shortener/login.html')


from django.contrib.auth import logout as auth_logout

def custom_logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')