 
from django.contrib import admin
from django.urls import path 

from .views import ( yourownstory  ,edit_story,download_story,share_story,
story_detail_view,invite_collaborator,collaboration_requests, accept_invite, reject_invite, my_collaborations,
view_invites ,mystory1,delete_story,author_profile,follow_user, unfollow_user,user_following,user_followers )

app_name = 'mystory' 

urlpatterns = [

    path('yourownstory/',yourownstory,name='yourownstory'),
    path('mystory1/',mystory1,name='mystory1'),
    path('story/edit/<int:story_id>/', edit_story, name='edit_story'),
    path('story/edit/', edit_story, name='edit_story'),
    path("download/<int:story_id>/", download_story, name="download_story"),
    path("share/<int:story_id>/", share_story, name="share_story"),
    path("story/<int:story_id>/", story_detail_view, name="story_detail"),
    path("invites/", view_invites, name="view_invites"),
    path('invite-collaborator/<int:story_id>/', invite_collaborator, name='invite_collaborator'),
    path("invite-collaborator/",  invite_collaborator, name="invite_collaborator"),
    path("collaboration-requests/", collaboration_requests, name="collaboration_requests"),
    path("accept-invite/<int:invite_id>/", accept_invite, name="accept_invite"),
    path("reject-invite/<int:invite_id>/", reject_invite, name="reject_invite"),
    path("my-collaborations/", my_collaborations, name="my_collaborations"),
    path("stories/delete/<int:story_id>/", delete_story, name="delete_story"),
    path("author/<str:username>/", author_profile, name="author_profile"),

    path('follow/<str:username>/', follow_user, name='follow_user'),
    path('unfollow/<str:username>/',  unfollow_user, name='unfollow_user'),
    path('<str:username>/followers/', user_followers, name='user-followers'),
    path('<str:username>/following/', user_following, name='user-following'),
]
