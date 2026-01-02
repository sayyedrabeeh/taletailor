def emotion_theme(request):
    """
    Enhanced context processor for emotion-based themes with audio information.
    Provides theme class, emoji, and audio characteristics for each emotion.
    """
    theme_class = 'theme-neutral'
    theme_emoji = '😊'
    audio_style = 'ambient'  # ambient, intense, calm, upbeat
    has_sfx = False
    
    story_id = request.resolver_match.kwargs.get('story_id') if hasattr(request, 'resolver_match') else None
    
    if story_id:
        from Mystory.models import Story
        try:
            story = Story.objects.get(id=story_id)
            emotions = story.emotions.lower() if story and story.emotions else ''
            
            # Comprehensive theme mapping with audio characteristics
            theme_map = {
                'happy': {
                    'class': 'theme-happy',
                    'emoji': '😄',
                    'audio_style': 'upbeat',
                    'has_sfx': True,
                    'description': 'Bright and cheerful atmosphere'
                },
                'sad': {
                    'class': 'theme-sad',
                    'emoji': '😢',
                    'audio_style': 'melancholic',
                    'has_sfx': True,
                    'description': 'Somber and reflective mood'
                },
                'romantic': {
                    'class': 'theme-romantic',
                    'emoji': '❤️',
                    'audio_style': 'gentle',
                    'has_sfx': True,
                    'description': 'Warm and intimate ambiance'
                },
                'thriller': {
                    'class': 'theme-thriller',
                    'emoji': '😱',
                    'audio_style': 'suspenseful',
                    'has_sfx': True,
                    'description': 'Tense and gripping atmosphere'
                },
                'adventure': {
                    'class': 'theme-adventure',
                    'emoji': '🏔️',
                    'audio_style': 'epic',
                    'has_sfx': True,
                    'description': 'Bold and exciting journey'
                },
                'mystery': {
                    'class': 'theme-mystery',
                    'emoji': '🔍',
                    'audio_style': 'enigmatic',
                    'has_sfx': True,
                    'description': 'Intriguing and puzzling mood'
                },
                'comedy': {
                    'class': 'theme-comedy',
                    'emoji': '😂',
                    'audio_style': 'playful',
                    'has_sfx': True,
                    'description': 'Light-hearted and humorous'
                },
                'horror': {
                    'class': 'theme-horror',
                    'emoji': '👻',
                    'audio_style': 'terrifying',
                    'has_sfx': True,
                    'description': 'Dark and frightening atmosphere with random scary sounds'
                },
                'fantasy': {
                    'class': 'theme-fantasy',
                    'emoji': '🧙',
                    'audio_style': 'magical',
                    'has_sfx': True,
                    'description': 'Enchanted and mystical realm'
                },
                'scifi': {
                    'class': 'theme-scifi',
                    'emoji': '🚀',
                    'audio_style': 'futuristic',
                    'has_sfx': True,
                    'description': 'High-tech and otherworldly'
                },
                'inspirational': {
                    'class': 'theme-inspirational',
                    'emoji': '✨',
                    'audio_style': 'uplifting',
                    'has_sfx': True,
                    'description': 'Motivating and empowering'
                },
                'melancholy': {
                    'class': 'theme-melancholy',
                    'emoji': '🌧️',
                    'audio_style': 'wistful',
                    'has_sfx': True,
                    'description': 'Bittersweet and nostalgic'
                },
                'anger': {
                    'class': 'theme-anger',
                    'emoji': '😠',
                    'audio_style': 'intense',
                    'has_sfx': True,
                    'description': 'Powerful and fierce energy'
                },
                'surprise': {
                    'class': 'theme-surprise',
                    'emoji': '😲',
                    'audio_style': 'dynamic',
                    'has_sfx': True,
                    'description': 'Unexpected and astonishing'
                },
                'fear': {
                    'class': 'theme-fear',
                    'emoji': '😨',
                    'audio_style': 'anxious',
                    'has_sfx': True,
                    'description': 'Nervous and unsettling'
                },
            }
            
            # Handle multiple emotions (comma-separated)
            if ',' in emotions:
                primary_emotion = emotions.split(',')[0].strip()
                theme_data = theme_map.get(primary_emotion, {
                    'class': 'theme-neutral',
                    'emoji': '😊',
                    'audio_style': 'ambient',
                    'has_sfx': False,
                    'description': 'Neutral atmosphere'
                })
            else:
                theme_data = theme_map.get(emotions, {
                    'class': 'theme-neutral',
                    'emoji': '😊',
                    'audio_style': 'ambient',
                    'has_sfx': False,
                    'description': 'Neutral atmosphere'
                })
            
            theme_class = theme_data['class']
            theme_emoji = theme_data['emoji']
            audio_style = theme_data['audio_style']
            has_sfx = theme_data['has_sfx']
            description = theme_data.get('description', '')
            
        except Story.DoesNotExist:
            pass
    
    return {
        'theme_class': theme_class,
        'theme_emoji': theme_emoji,
        'audio_style': audio_style,
        'has_sfx': has_sfx,
        'theme_description': description if 'description' in locals() else 'Default theme'
    }


# Additional utility function for audio management
def get_audio_settings(emotion):
    """
    Returns specific audio settings for each emotion/theme.
    Can be used in views or API endpoints.
    """
    audio_settings = {
        'happy': {
            'bg_volume': 0.5,
            'sfx_volume': 0.6,
            'loop': True,
            'fade_in': 1000,
            'fade_out': 500,
        },
        'sad': {
            'bg_volume': 0.4,
            'sfx_volume': 0.3,
            'loop': True,
            'fade_in': 2000,
            'fade_out': 2000,
        },
        'romantic': {
            'bg_volume': 0.4,
            'sfx_volume': 0.4,
            'loop': True,
            'fade_in': 1500,
            'fade_out': 1500,
        },
        'thriller': {
            'bg_volume': 0.6,
            'sfx_volume': 0.7,
            'loop': True,
            'fade_in': 500,
            'fade_out': 500,
        },
        'adventure': {
            'bg_volume': 0.6,
            'sfx_volume': 0.6,
            'loop': True,
            'fade_in': 1000,
            'fade_out': 1000,
        },
        'mystery': {
            'bg_volume': 0.5,
            'sfx_volume': 0.5,
            'loop': True,
            'fade_in': 1500,
            'fade_out': 1000,
        },
        'horror': {
            'bg_volume': 0.5,
            'sfx_volume': 0.8,
            'loop': True,
            'fade_in': 2000,
            'fade_out': 500,
            'random_sfx': True,
            'sfx_interval': 15000,  # milliseconds
        },
        'fantasy': {
            'bg_volume': 0.5,
            'sfx_volume': 0.5,
            'loop': True,
            'fade_in': 1500,
            'fade_out': 1500,
        },
        'scifi': {
            'bg_volume': 0.5,
            'sfx_volume': 0.6,
            'loop': True,
            'fade_in': 1000,
            'fade_out': 1000,
        },
        'inspirational': {
            'bg_volume': 0.5,
            'sfx_volume': 0.5,
            'loop': True,
            'fade_in': 1000,
            'fade_out': 1000,
        },
    }
    
    return audio_settings.get(emotion, {
        'bg_volume': 0.5,
        'sfx_volume': 0.5,
        'loop': True,
        'fade_in': 1000,
        'fade_out': 1000,
    })


# Template tag for audio features
from django import template

register = template.Library()

@register.simple_tag
def audio_enabled(emotion):
    """Template tag to check if audio is enabled for a theme"""
    audio_themes = ['happy', 'sad', 'romantic', 'thriller', 'adventure', 
                    'mystery', 'horror', 'fantasy', 'scifi', 'inspirational']
    return emotion.lower() in audio_themes


@register.simple_tag
def get_audio_description(emotion):
    """Get audio description for a theme"""
    descriptions = {
        'happy': 'Upbeat and cheerful background music',
        'sad': 'Melancholic piano with rain sounds',
        'romantic': 'Gentle romantic melodies',
        'thriller': 'Suspenseful and tense soundtrack',
        'adventure': 'Epic orchestral adventure themes',
        'mystery': 'Enigmatic and mysterious ambience',
        'horror': 'Scary atmosphere with random horror effects',
        'fantasy': 'Magical and enchanted soundscapes',
        'scifi': 'Futuristic electronic music',
        'inspirational': 'Uplifting and motivational tracks',
    }
    return descriptions.get(emotion.lower(), 'Ambient background music')