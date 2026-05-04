from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('verify/', views.verify, name='verify'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('search/', views.search, name='search'),
    path('chat/<int:user_id>/', views.chat, name='chat'),
]
