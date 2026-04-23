from django.urls import path
from . import views

urlpatterns = [
    # Homepage - where you paste URL to shorten
    path('', views.home, name='home'),
    
    # Dashboard - MUST come before the redirect route
    path('dashboard/', views.dashboard, name='dashboard'),

    path('signup/', views.signup, name='signup'),

    path('login/', views.custom_login, name='login'),

    path('logout/', views.custom_logout, name='logout'),
    
    # Delete link
    path('delete/<int:link_id>/', views.delete_link, name='delete'),
    
    # The redirect link - MUST be LAST (catches everything else)
    path('<str:short_code>/', views.redirect_to_original, name='redirect'),

    
]