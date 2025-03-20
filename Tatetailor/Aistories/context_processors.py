def emotion_theme(request):
    theme_class = 'theme-neutral'
    theme_emoji = '😊'
    
    
    story_id = request.resolver_match.kwargs.get('story_id') if hasattr(request, 'resolver_match') else None
    
    if story_id:
        from Mystory.models import Story
        try:
            story = Story.objects.get(id=story_id)
            emotions = story.emotions.lower() if story and story.emotions else ''
            
             
            theme_map = {
                'happy': {'class': 'theme-happy', 'emoji': '😄'},
                'sad': {'class': 'theme-sad', 'emoji': '😢'},
                'romantic': {'class': 'theme-romantic', 'emoji': '❤️'},
                'thriller': {'class': 'theme-thriller', 'emoji': '😱'},
                'adventure': {'class': 'theme-adventure', 'emoji': '🏔️'},
                'mystery': {'class': 'theme-mystery', 'emoji': '🔍'},
                'comedy': {'class': 'theme-comedy', 'emoji': '😂'},
                'horror': {'class': 'theme-horror', 'emoji': '👻'},
                'fantasy': {'class': 'theme-fantasy', 'emoji': '🧙'},
                'scifi': {'class': 'theme-scifi', 'emoji': '🚀'},
                'inspirational': {'class': 'theme-inspirational', 'emoji': '✨'},
                'melancholy': {'class': 'theme-melancholy', 'emoji': '🌧️'},
                'anger': {'class': 'theme-anger', 'emoji': '😠'},
                'surprise': {'class': 'theme-surprise', 'emoji': '😲'},
                'fear': {'class': 'theme-fear', 'emoji': '😨'},
            }
            
  
            if ',' in emotions:
                primary_emotion = emotions.split(',')[0].strip()
                theme_data = theme_map.get(primary_emotion, {'class': 'theme-neutral', 'emoji': '😊'})
            else:
                theme_data = theme_map.get(emotions, {'class': 'theme-neutral', 'emoji': '😊'})
                
            theme_class = theme_data['class']
            theme_emoji = theme_data['emoji']
        except Story.DoesNotExist:
            pass
    
    return {
        'theme_class': theme_class,
        'theme_emoji': theme_emoji
    }