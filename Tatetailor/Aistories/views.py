from django.shortcuts import render,get_object_or_404,redirect
from Mystory.models import Story,StoryLike,StoryView
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q
import requests
import os
from django.utils.html import strip_tags
from django.conf import settings
from Mystory.views import get_unsplash_image
from deep_translator import GoogleTranslator
from gtts import gTTS
from django.contrib.auth.decorators import login_required




 
@login_required(login_url='authentication:login') 
def explore(request):
     
    stories = Story.objects.filter(status='public').order_by('-created_at')
    stories = stories.annotate(
        view_count=Count('views', distinct=True),
        like_count=Count('likes', distinct=True)
    )
    view_mode = request.GET.get('view', '')
    search_query = request.GET.get('search', '')
    if search_query:
        stories = stories.filter(
            Q(title__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )
    selected_lengths = request.GET.getlist('length')
    if selected_lengths:
        stories = stories.filter(length__in=selected_lengths)
    selected_types = request.GET.getlist('type')
    if selected_types:
        stories = stories.filter(genre__in=selected_types)
    selected_emotions = request.GET.getlist('emotion')
    if selected_emotions:
        emotion_query = Q()
        for emotion in selected_emotions:
            emotion_query |= Q(emotions__icontains=emotion)
        if emotion_query:
            stories = stories.filter(emotion_query)
    paginator = Paginator(stories, 6)  
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    genres = ["fantasy", "mystery", "scifi", "romance", "horror", "adventure", "thriller", "comedy"]
    emotions = ["happy", "sad", "suspenseful", "scary", "emotional", "dark", "feel-good", "epic"]
    context = {
        'page_obj': page_obj,
        'genres': genres,
        'emotions': emotions,
        'total_stories': stories.count(),
        'search_query': search_query,
        'selected_lengths': selected_lengths,
        'selected_types': selected_types,
        'selected_emotions': selected_emotions,
        'view_mode': view_mode,
    }
    return render(request, "explore.html", context)


@login_required(login_url='authentication:login') 
def view_story(request,story_id):
    if  story_id:
        sid=story_id
        story = get_object_or_404(Story, id=story_id)
        emotions_list = story.emotions.split(',')
        is_liked = False
        ip = get_client_ip(request)
        user = request.user if request.user.is_authenticated else None
        if user:
             already_viewed = StoryView.objects.filter(story=story, user=user).exists()
        else:
             already_viewed = StoryView.objects.filter(story=story, ip_address=ip).exists()

        collaborators = story.collaborators.all() if story.is_collaborated else []

        if not already_viewed:
             StoryView.objects.create(story=story, user=user, ip_address=ip)

        view_count = story.views.count()
        like_count = story.likes.count()   
        similar_stories = Story.objects.filter(
            Q(emotions__contains=story.emotions) | Q(genre__exact=story.genre)
        ).exclude(id=story.id)[:6]
        
        if user:
             is_liked = StoryLike.objects.filter(story=story, user=user).exists()
        return render(request, "view_story.html",{
            'story':story,
            'emotions_list':emotions_list,
            'is_liked':is_liked,
            'view_count': view_count,
            'like_count': like_count,
            'collaborators':collaborators,
            'similar_stories':similar_stories,       
            })
    
# @login_required(login_url='authentication:login') 
def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


@login_required(login_url='authentication:login') 
def like_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    user = request.user
    if user.is_authenticated:
        existing_like = StoryLike.objects.filter(story=story, user=user)
        if existing_like.exists():
            existing_like.delete()
        else:
            StoryLike.objects.create(story=story, user=user)

    return redirect('aistory:view_story', story_id=story.id)

@login_required(login_url='authentication:login') 
def aimake1(request):
    if request.method == "POST":
        emotion = request.POST.get('emotion')
        twists = request.POST.get('twists') == 'on'
        length = request.POST.get('length')
        theme = request.POST.get('theme')
        situation = request.POST.get('situation')
        request.session['story_step1'] = {
            'emotion': emotion,
            'twists': twists,
            'length': length,
            'theme': theme,
            'situation': situation,
        }
        return redirect('aistory:aimake2')
    return render(request,'aimake1.html')

@login_required(login_url='authentication:login') 

def aimake2(request):
     
    step1_data = request.session.get("story_step1", {})
    if not step1_data:
        return redirect('aistory:aimake1')   

    if request.method == "POST":
        
        char_count = request.POST.get("char_count", "")
        char_names = request.POST.get("char_names", "")
        locations = request.POST.get("places", "")

       
        emotion = step1_data.get("emotion", "")
        twists = step1_data.get("twists", False)
        length = step1_data.get("length", "")
        theme = step1_data.get("theme", "")
        situation = step1_data.get("situation", "")

        
        prompt = f"""
        Write a {length} story with emotion '{emotion}', twists: {twists}, and this theme:
        {theme}

        Situation: {situation}
        Characters: {char_names} (Count: {char_count})
        Places: {locations}
        """

        story = generate_story(prompt)
        word_count = len(story.split())
        
        request.session.pop("story_step1", None)
        print('story:',story)
        return render(request, "story_output.html", {
            "story": story,
            "emotion": emotion,
            "length": length,
            "theme": theme,
            "situation": situation,
            "twists": twists,
             "word_count":word_count,
            })

    return render(request, "aimake2.html")


access_token = os.getenv("HUGGINGFACE_API_KEY")
def generate_story(prompt):
    import requests

    API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 700,
            "temperature": 0.9,
            "top_p": 0.95,
            "repetition_penalty": 1.2,
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    print("Response status:", response.status_code)
    print("Response text:", response.text)  

    if response.status_code == 200:
        data = response.json()
        return data[0]["generated_text"]
    else:
        return "Error: Couldn't generate story."
    
@login_required(login_url='authentication:login')  
def post_private_story(request):
    if request.method == "POST":
      
     
        story_text = strip_tags(request.POST.get("story", ""))
        
        
        print("RAW STORY TEXT LENGTH:", len(story_text))
        print("FIRST 100 CHARS:", story_text[:100])
        new_title=request.POST.get("theme", "").strip() or "Untitled"
       
        if story_text:
            try:
                 
                story = Story(
                    user=request.user,
                    content=story_text,
                    status='private',
                    emotions=request.POST.get("emotion", ""),
                    length=request.POST.get("length", "medium"),
                    title=request.POST.get("theme", "").strip() or "Untitled",
                    is_ai_generated=True,
                )
                 
                story.save(force_insert=True)
                img_file = get_unsplash_image(new_title)
                if img_file:
                     story.image.save(f"{story.id}.jpg", img_file)
                     story.save()
              
                saved_story = Story.objects.get(id=story.id)
                print(f"STORY SAVED SUCCESSFULLY. ID: {story.id}, CONTENT LENGTH: {len(saved_story.content)}")
                
                return redirect("mystory:mystory1")
            except Exception as e:
                import traceback
                print(f"ERROR SAVING STORY: {str(e)}")
                print(traceback.format_exc())   
                
                 
                try:
                    print("TRYING ALTERNATE APPROACH")
                    Story.objects.create(
                        user=request.user,
                        content="Error saving original content. Please try again.",
                        status='private',
                        title="Error Saving Story"
                    )
                    return redirect("mystory:mystory1")
                except Exception as e2:
                    print(f"SECOND ATTEMPT FAILED: {str(e2)}")
        else:
            print("NO STORY TEXT FOUND IN REQUEST")
    
    return redirect("aistory:aimake1")




@login_required(login_url='authentication:login') 


def translate_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    translated_text = None
    selected_language = None
    user = request.user if request.user.is_authenticated else None
    if request.method == 'POST':
        selected_language = request.POST.get('language')

        try:
            translated_text = GoogleTranslator(source='auto', target=selected_language).translate(story.content)
        except Exception as e:
            print("Translation error:", e)
            translated_text = "Translation failed. Try again later."
        

    view_count = story.views.count()
    like_count = story.likes.count()   
    similar_stories = Story.objects.filter(
        Q(emotions__contains=story.emotions) | Q(genre__exact=story.genre)
    ).exclude(id=story.id)[:6]
    
    if user:
        is_liked = StoryLike.objects.filter(story=story, user=user).exists()
    return render(request, 'view_story.html', {
        'story': story,
        'translated_content': translated_text,
        'language': selected_language,
        'view_count': view_count,
        'like_count': like_count,
        'similar_stories': similar_stories,
        'is_liked': is_liked,
    })


 