 
from django.contrib import admin
from django.urls import path 
from .views import  explore,view_story,like_story,aimake1,aimake2,post_private_story,translate_story 

app_name = 'aistory' 

urlpatterns = [
    
    path("explore/", explore, name="explore"),
    path("aimake1/", aimake1, name="aimake1"),
    path("aimake2/", aimake2, name="aimake2"),
    path("view_story/<int:story_id>/", view_story, name="view_story"),
     path('like/<int:story_id>/',  like_story, name='like_story'),
    path("post-private/",  post_private_story, name="post_private_story"),
    path('story/<int:story_id>/translate/', translate_story, name='translate_story'),
 

]
