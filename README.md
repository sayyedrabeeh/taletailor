# 🌟 Tail Tailor: AI Story Generator + Story Social Media 🌟

![Tail Tailor Banner](https://placeholder-image-url.com/tail-tailor-banner.jpg)

## ✨ Welcome to Tail Tailor

Tail Tailor is a revolutionary full-stack platform that brings together cutting-edge AI story generation with vibrant social media features, creating a dynamic ecosystem for storytellers and readers alike. Create, collaborate, share, and experience stories in ways never before possible!

![Story Generation Demo](https://placeholder-image-url.com/story-generation-demo.gif)

## 🚀 Features

### 🤖 AI-Powered Story Generation
Transform your ideas into captivating narratives with our advanced AI engine:

- **Emotion Selection**: Set the emotional tone of your story (happy, sad, suspenseful, scary, etc.)
- **Theme Selection**: Choose from genres like fantasy, mystery, sci-fi, romance, horror, and more
- **Length Customization**: Create short stories, medium-length tales, or epic sagas
- **Plot Twists**: Opt for unexpected turns that keep readers on the edge of their seats
- **Character Development**: Specify number of characters and their relationships
- **Situational Prompts**: Start with a specific scenario and watch the AI expand it into a full story

![Emotion Selection Interface](https://placeholder-image-url.com/emotion-selection.jpg)

### 📝 Story Creation & Management
Express yourself through our intuitive story creation tools:

- **Rich Text Editor**: Craft your stories with a powerful formatting toolkit
- **Draft Saving**: Never lose your work with automatic saving
- **Public/Private Options**: Choose whether to share your story with the world or keep it personal
- **Word Count Tracking**: Monitor your story's length as you write
- **Custom Cover Images**: Each story gets a unique cover image based on its title

![Story Editor Interface](https://placeholder-image-url.com/story-editor.jpg)

### 👥 Collaborative Storytelling
Create together with friends, family, or new connections:

- **Collaboration Invitations**: Invite others to contribute to your story
- **Collaborative Editing**: Work together until the story is ready for publication
- **Permission Management**: Control who can edit your collaborative stories
- **Publication Control**: Once published, stories become read-only for collaborators
- **Contribution Tracking**: See who wrote what in collaborative works

![Collaboration Demo](https://placeholder-image-url.com/collaboration-demo.gif)

### 🌈 Dynamic Emotional Theming
Experience stories in a completely immersive way:

- **Mood-Based Interfaces**: The entire UI adapts to match your story's emotional tone
- **Romantic Stories**: Soft pink backgrounds with heart motifs
- **Horror Tales**: Dark mode with spooky elements
- **Adventure Narratives**: Vibrant earth tones with exploration themes
- **Each Emotion Unique**: Every emotional category has its own color scheme and visual elements

| Emotion | Theme Preview |
|---------|---------------|
| Romantic | ![Romantic Theme](https://placeholder-image-url.com/romantic-theme.jpg) |
| Horror | ![Horror Theme](https://placeholder-image-url.com/horror-theme.jpg) |
| Adventure | ![Adventure Theme](https://placeholder-image-url.com/adventure-theme.jpg) |

### 🔍 Discover & Explore
Find your next favorite story with our advanced discovery features:

- **Story Feed**: Browse public stories in a familiar social media format
- **Search Functionality**: Find stories by title, author, or content
- **Filter System**: Sort by emotion, length, theme, and more
- **Trending Section**: Discover the most popular stories on the platform
- **Similar Stories**: Get recommendations based on your reading history

![Discovery Interface](https://placeholder-image-url.com/discovery-interface.jpg)

### 💬 Social Engagement
Connect with a community of storytellers and readers:

- **Like System**: Show appreciation for stories you enjoy
- **View Tracking**: See how many people have read your stories
- **User Profiles**: Customize your profile with bio and profile picture
- **Follow Authors**: Keep up with your favorite storytellers
- **Story Stats**: Track engagement metrics for your published works

![Social Features](https://placeholder-image-url.com/social-features.jpg)

### 🌐 Accessibility Features
Make stories accessible to everyone:

- **One-Click Translation**: Translate stories into multiple languages
- **Text-to-Speech**: Listen to stories with natural-sounding narration
- **Responsive Design**: Perfect experience on any device
- **PDF Export**: Download stories as beautifully formatted documents
- **Reading Time Estimates**: Know how long a story will take to read

![Accessibility Features](https://placeholder-image-url.com/accessibility-features.jpg)

### 👤 User Authentication & Profiles
Secure and personalized experience:

- **Email Verification**: Secure signup with OTP verification
- **Profile Customization**: Add your bio, profile picture, and more
- **Story Collection**: All your stories in one place
- **Activity Tracking**: See your interactions across the platform
- **Account Settings**: Manage your preferences and privacy options

![User Profile](https://placeholder-image-url.com/user-profile.jpg)

### 👑 Administrative Tools
Powerful tools for platform management:

- **User Management**: Block/unblock users when necessary
- **Content Moderation**: Review and manage reported content
- **Analytics Dashboard**: Monitor platform metrics and growth
- **Story Management**: Feature exceptional stories or remove inappropriate content
- **System Health Monitoring**: Keep the platform running smoothly

![Admin Dashboard](https://placeholder-image-url.com/admin-dashboard.jpg)

## 🛠️ Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL
- **AI Integration**: HuggingFace Falcon-7b-instruct model
- **External APIs**: Unsplash (images), Google Translator, gTTS (text-to-speech)

## 📊 Project Structure

```
tail-tailor/
├── authentication/      # User authentication, profiles, admin controls
├── Mystory/             # Core story models and functionality
├── aistory/             # AI story generation features
├── static/              # CSS, JS, images
│   ├── css/             # Stylesheets with emotional themes
│   ├── js/              # JavaScript files
│   └── images/          # Static images and assets
├── templates/           # HTML templates
└── manage.py            # Django management script
```

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Django 4.0+
- PostgreSQL
- Node.js (for frontend build tools)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/tail-tailor.git
   cd tail-tailor
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory with the following variables:
   ```
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   DATABASE_URL=postgresql://user:password@localhost/tailtailor
   HUGGINGFACE_API_KEY=your_huggingface_api_key
   UNSPLASH_ACCESS_KEY=your_unsplash_access_key
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your_email@example.com
   EMAIL_HOST_PASSWORD=your_email_password
   ```

5. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   Open your browser and go to `http://127.0.0.1:8000/`

## 🌟 Key Components

### Models
- `User`: Authentication and profile information
- `Story`: Central story content and metadata
- `StoryLike`: Tracks likes on stories
- `StoryView`: Records story views
- `CollaborationInvite`: Manages collaboration invitations
- `Profile`: Extended user profile information

### Views
- AI story generation flow
- Story creation and editing
- Collaborative storytelling
- Social interaction features
- Translation and accessibility functions

### Core Functionality

#### Story Generation
```python
def generate_story(prompt):
    API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
    headers = {"Authorization": f"Bearer {access_token}"}
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

#### Dynamic Theming
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
                # Additional emotions...
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

## 📱 Mobile-Friendly Design

Tail Tailor is designed with responsiveness in mind:

- **Adaptive Layout**: Automatically adjusts to any screen size
- **Touch-Friendly Controls**: Easy to use on mobile devices
- **Optimized Reading Experience**: Comfortable story consumption on any device
- **Consistent Theming**: Emotional themes work seamlessly across all devices

![Mobile Interface](https://placeholder-image-url.com/mobile-interface.jpg)

## 🔮 Future Enhancements

We're continuously working to improve Tail Tailor with exciting new features:

- **Audio Stories**: Record your voice for narrated stories
- **Story Challenges**: Themed writing competitions
- **Enhanced AI Models**: More powerful and nuanced story generation
- **Community Groups**: Create writing circles and book clubs
- **Interactive Stories**: Choose-your-own-adventure style narratives
- **Merchandising**: Turn popular stories into physical books

## 👥 Contributing

We welcome contributions to make Tail Tailor even better!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Django](https://www.djangoproject.com/)
- [HuggingFace](https://huggingface.co/)
- [Unsplash](https://unsplash.com/)
- [Google Translator](https://cloud.google.com/translate)
- [gTTS](https://gtts.readthedocs.io/)

## 📬 Contact

- Project Link: [https://github.com/yourusername/tail-tailor](https://github.com/yourusername/tail-tailor)
- Website: [https://tailtailor.com](https://tailtailor.com)
- Email: contact@tailtailor.com

---

### 💫 "Where AI and Human Creativity Weave Tales Together" 💫

![Footer Image](https://placeholder-image-url.com/tail-tailor-footer.jpg)