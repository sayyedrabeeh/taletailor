 
from django.contrib import admin
from django.urls import path 
from .views import signup,verify_otp,home,login_view,logout_view,users,toggle_block_user,dashboard,stories,delete_story,edit_profile,view_profile

app_name = 'authentication' 

urlpatterns = [
    path('',signup,name='signup'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('home/',home,name='home'),
    path('stories/',stories,name='stories'),
    path("stories/delete/<int:story_id>/", delete_story, name="delete_story"),

    path('users/', users, name='users'),
    path('dashboard/', dashboard, name='dashboard'),
    path('verify_otp/',verify_otp,name='verify_otp'),
   path('toggle-block/<int:user_id>/', toggle_block_user, name='toggle_block_user'),
   path('profile/',  view_profile, name='view_profile'),
    path('profile/edit/',  edit_profile, name='edit_profile'),
     
]
