# StoryWeave 📚✨

A full-stack AI-powered interactive storytelling platform that combines story generation with social media features.

![StoryWeave Banner](https://placeholder-image-url.com/storyweave-banner.jpg)

## 🌟 Features

### AI Story Generation
Generate unique stories by selecting emotions, themes, length, and situational elements:

![AI Story Generation](https://placeholder-image-url.com/ai-story-demo.gif)

```
Example parameters:
- Emotion: Suspenseful
- Length: Medium
- Theme: Mystery
- Situation: "A detective finds an unusual object at a crime scene"
```

### Collaborative Storytelling
Invite others to co-create stories with real-time collaboration:

![Collaboration Demo](https://placeholder-image-url.com/collaboration-demo.gif)

### Dynamic Emotional Theming
Interface adapts to match story emotions:

| Emotion | Theme Preview |
|---------|---------------|
| Romantic | ![Romantic Theme](https://placeholder-image-url.com/romantic-theme.jpg) |
| Horror | ![Horror Theme](https://placeholder-image-url.com/horror-theme.jpg) |
| Adventure | ![Adventure Theme](https://placeholder-image-url.com/adventure-theme.jpg) |

### Social Features
- Like stories
- Track views
- Discover trending content
- Follow favorite authors

![Social Features](https://placeholder-image-url.com/social-features.gif)

### Accessibility Features
- Translate stories to any language
- Text-to-speech narration
- Download as PDF

![Accessibility Demo](https://placeholder-image-url.com/accessibility-demo.gif)

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Django 4.0+
- Node.js 14+
- PostgreSQL

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/storyweave.git
   cd storyweave
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment variables**
   Create a `.env` file in the root directory:
   ```
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   DATABASE_URL=postgresql://user:password@localhost/storyweave
   HUGGINGFACE_API_KEY=your_huggingface_api_key
   UNSPLASH_ACCESS_KEY=your_unsplash_key
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your_email@example.com
   EMAIL_HOST_PASSWORD=your_email_password
   ```

5. **Database setup**
   ```bash
   python manage.py migrate
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 📊 Project Structure

```
storyweave/
├── authentication/      # User authentication, profiles, admin views
├── Mystory/             # Core story models and main user functionality
├── aistory/             # AI story generation and enhanced features
├── static/              # CSS, JS, images
│   ├── css/             # Stylesheets including emotional themes
│   ├── js/              # JavaScript files
│   └── images/          # Static images and icons
├── templates/           # HTML templates
└── manage.py            # Django management script
```

## 🧩 Core Components

### Models
- User: Authentication and profile information
- Story: Central story content and metadata
- StoryLike: Tracks likes on stories
- StoryView: Tracks views on stories
- CollaborationInvite: Manages collaboration invitations
- Profile: Extended user profile information

### Key Views
- AI story generation workflow
- Story editing and collaboration
- Exploration and discovery
- Translation and text-to-speech
- Social interaction (likes, views)

## 🔧 API Integration

### HuggingFace AI
Uses the Falcon-7b-instruct model for story generation:

```python
def generate_story(prompt):
    API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
    headers = {
        "Authorization": f"Bearer {access_token}"
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
    if response.status_code == 200:
        data = response.json()
        return data[0]["generated_text"]
    else:
        return "Error: Couldn't generate story."
```

### Unsplash API
Fetches relevant images for story covers:

```python
def get_unsplash_image(query):
    access_key = 'your_unsplash_access_key'  
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={access_key}"    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        image_url = data['urls']['regular']
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            return ContentFile(image_response.content)  
    return None
```

### Google Translator
Provides multi-language support:

```python
def translate_story(story_content, target_language):
    return GoogleTranslator(source='auto', target=target_language).translate(story_content)
```

## 🖌️ Emotional Theming

The `emotion_theme` context processor determines the appropriate theme based on story emotions:

```python
def emotion_theme(request):
    theme_class = 'theme-neutral'
    theme_emoji = '😊'
    
    story_id = request.resolver_match.kwargs.get('story_id')
    
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
                # Additional emotion mappings...
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
```

## 👥 Contributing

We welcome contributions to StoryWeave!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📬 Contact

Project Link: [https://github.com/yourusername/storyweave](https://github.com/yourusername/storyweave)

## 🙏 Acknowledgements

- [Django](https://www.djangoproject.com/)
- [HuggingFace](https://huggingface.co/)
- [Unsplash](https://unsplash.com/)
- [Google Translator](https://cloud.google.com/translate)
- [gTTS](https://gtts.readthedocs.io/)