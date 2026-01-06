from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Story
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.urls import reverse
from django.core.paginator import Paginator
from .models import CollaborationInvite, User
from Mystory.models import CollaborationInvite, Notification
from django.contrib.auth.decorators import login_required
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from io import BytesIO
import textwrap
import uuid
from django.utils.html import escape
from django.core.files.base import ContentFile
import requests
from django.conf import settings
from django.templatetags.static import static
import os
from dotenv import load_dotenv
from  .models import Follower
import requests
from django.core.files.base import ContentFile
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
from django.db.models import Q 
from django.core.files.base import ContentFile
import requests

load_dotenv()
 

@login_required(login_url='authentication:login') 
def yourownstory(request):
    query = request.GET.get("q", "")

    stories = Story.objects.filter(user=request.user)
    story = stories.first() if stories.exists() else None

     
    my_stories = Story.objects.filter(user=request.user, is_collaborated=False)
    if query:
        my_stories = my_stories.filter(Q(title__icontains=query) | Q(content__icontains=query))
    my_stories = my_stories.order_by('-id')[:3]

     
    you_created_and_collaborated = Story.objects.filter(user=request.user, is_collaborated=True)
    you_were_invited = Story.objects.filter(collaborators=request.user)
    collaborated_stories = (you_created_and_collaborated | you_were_invited).distinct()

    if query:
        collaborated_stories = collaborated_stories.filter(Q(title__icontains=query) | Q(content__icontains=query))
    collaborated_stories = collaborated_stories.order_by('-id')[:3]

    return render(request, "yourownstory.html", {
        "my_stories": my_stories,
        "stories": stories,
        "story": story,
        "colla_stories": collaborated_stories,
        "query": query
    })


# @login_required(login_url='authentication:login') 
# def get_unsplash_image(query):
#     access_key = 'sx-HxKDsbMy5QCfZfQhhgu7Vu3m9CtkZkZKk1NtaGm4'  
#     url = f"https://api.unsplash.com/photos/random?query={query}&client_id={access_key}"    
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         image_url = data['urls']['regular']
#         image_response = requests.get(image_url)
#         if image_response.status_code == 200:
#             return ContentFile(image_response.content)  
#     return None

import cloudinary.uploader

def get_unsplash_image(query):
    access_key = os.getenv("UNSPLASH_ACCESS_KEY")
    if not access_key:
        print("Unsplash key missing")
        return None

    url = "https://api.unsplash.com/photos/random"
    headers = {
        "Authorization": f"Client-ID {access_key}",
        "Accept-Version": "v1"
    }
    params = {
        "query": query,
        "orientation": "landscape"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code != 200:
            print("Unsplash error:", response.text)
            return None

        data = response.json()
        image_url = data["urls"]["regular"]

        upload_result = cloudinary.uploader.upload(
            image_url,
            folder="story_images"
        )

        return upload_result["public_id"]   

    except Exception as e:
        print("Unsplash/Cloudinary error:", e)
        return None

@login_required(login_url='authentication:login') 
def edit_story(request, story_id=None):    
    if not story_id:
        if request.method == "POST":
            post_type = request.POST.get("post_type")
            new_title = request.POST.get("title", "")
            new_content = request.POST.get("story", "")
            story_length = request.POST.get("length", "medium")
            emotions = request.POST.getlist("emotion")
            theme = request.POST.get("theme", "")
            word_count = len(new_content.split())
            if not new_title.strip() or not new_content.strip():
                messages.error(request, "Title and content cannot be empty.")
                return render(request, "edityourownstory.html", {"title": new_title, "story11": new_content})
            if word_count < 300:
                messages.error(request, f"Your story must have at least 300 words. (Currently {word_count} words)")
                return render(request, "edityourownstory.html", {"title": new_title, "story11": new_content})
            if post_type in ["public", "private"]:
                    normalized_title = new_title.strip().lower()
                    normalized_content = new_content.strip().lower()
                    
                    duplicate_stories = Story.objects.filter(
                         user=request.user,
                         title__iexact=normalized_title,
                         status=post_type
                     )
                     
                    duplicate_exists = any(
                         s.content.strip().lower() == normalized_content for s in duplicate_stories
                     )
                     
                    
                    if duplicate_exists:
                        messages.warning(request, "You've already submitted this story.")
                        return redirect("mystory:yourownstory")
                    story= Story.objects.create(
                       user=request.user,
                       title=new_title,
                       content=new_content,
                       status=post_type,
                       length=story_length,
                       emotions=", ".join(emotions),
                     )
                    public_id = get_unsplash_image(new_title)
                    
                    if public_id:
                        story.image = public_id
                        story.save(update_fields=["image"])
                    
                    if post_type == "public":
                          notify_followers(request.user, story,action="posted")
                    messages.success(request, f"Story Created Successfully as {post_type.capitalize()}.")
                    return redirect("mystory:yourownstory")
        return render(request, "edityourownstory.html", {})
    story = get_object_or_404(Story, id=story_id)
    if story.user != request.user and not story.collaborators.filter(id=request.user.id).exists():
        messages.error(request, "You do not have permission to edit this story.")
        return redirect("mystory:yourownstory")
    is_owner = story.user == request.user
    is_collaborator = story.collaborators.filter(id=request.user.id).exists()
    if request.method == "POST":
        post_type = request.POST.get("post_type")
        update_action = request.POST.get("update")
        new_title = request.POST.get("title", story.title)
        new_content = request.POST.get("story", story.content)
        word_count = len(new_content.split())
        if not new_title.strip() or not new_content.strip():
            messages.error(request, "Title and content cannot be empty.")
            return render(request, "edityourownstory.html", {
                "title": new_title, 
                "story11": new_content,
                "sid": story.id,
                "is_collaborator": is_collaborator,
                "is_owner": is_owner,
                "status": story.status,
            })
        if word_count < 300:
            messages.error(request, f"Your story must have at least 300 words. (Currently {word_count} words)")
            return render(request, "edityourownstory.html", {
                "title": new_title, 
                "story11": new_content,
                "sid": story.id,
                "is_collaborator": is_collaborator,
                "is_owner": is_owner,
                "status": story.status,
            })
        if is_owner and post_type in ["public", "private"]:
            story.title = new_title
            story.content = new_content
            story.status = post_type
            story.save()
            if post_type == "public":
                     notify_followers(request.user, story,action="Updated")
            public_id = get_unsplash_image(new_title)

            if public_id:
                 story.image = public_id
                 story.save(update_fields=["image"])

      
            messages.success(request, f"Story posted {post_type.capitalize()} successfully!")
            return redirect("mystory:yourownstory")
        elif update_action is not None:
            story.title = new_title
            story.content = new_content
            story.save()
            messages.success(request, "Story updated successfully!")
            return redirect("mystory:edit_story", story_id=story.id)
        else:
           messages.error(request, "Invalid action. Please use one of the provided buttons.")
           return render(request, "edityourownstory.html", {
            "title": new_title, 
            "story11": new_content,
            "sid": story.id,
            "is_collaborator": is_collaborator,
            "is_owner": is_owner,
            "status": story.status,
           })
    return render(request, "edityourownstory.html", {
        "story": story, 
        "story11": story.content,
        "title": story.title,
        "sid": story.id,
        "is_collaborator": is_collaborator,
        "is_owner": is_owner,
        "status": story.status,
    })

def send_story_email_to_followers(story, followers, action="posted"):
    subject = f"{story.user.username} has {action} a new story: {story.title}"
    from_email = settings.EMAIL_HOST_USER
    story_url = f"http://127.0.0.1:9000/Aistories/view_story/{story.id}/"  

    html_content = render_to_string("email/story_notification.html", {
        "author": story.user.username,
        "story": story,
        "story_url": story_url,
        "action": action
    })

    for follower in followers:
        follower_user = follower.follower
        msg = EmailMultiAlternatives(subject, "", from_email, [follower_user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

@login_required(login_url='authentication:login') 
def share_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    share_url = request.build_absolute_uri(f"/Aistories/view_story/{story.id}/")
    return render(request, "share_story.html", {"share_url": share_url, "story": story})

@login_required(login_url='authentication:login') 


def download_story(request, story_id):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch
    from io import BytesIO
    import os
    from datetime import datetime
    
    story = get_object_or_404(Story, id=story_id)
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    elements = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=1,  
        spaceAfter=20
    )
    try:

        logo_path = os.path.join('static', 'images', 'company_logo.jpg')
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=2*inch, height=1*inch)
            elements.append(logo)
    except:

        header_style = ParagraphStyle(
            name='Header',
            parent=styles['Heading2'],
            fontSize=14,
            alignment=1,
            textColor=colors.darkblue
        )
        elements.append(Paragraph("OFFICIAL DOCUMENT", header_style))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(story.title, title_style))
    data = [
        ["Document ID:", f"STORY-{story_id}"],
        ["Date:", datetime.now().strftime("%B %d, %Y")],
        ["Author:", getattr(story, 'author', 'Unknown')]
    ]
    metadata_table = Table(data, colWidths=[1.5*inch, 4*inch])
    metadata_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.darkblue),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(metadata_table)
    elements.append(Spacer(1, 0.3*inch))
    content_style = ParagraphStyle(
        name='Content',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        firstLineIndent=20
    )
    for paragraph in story.content.split('\n\n'):
        if paragraph.strip():
            elements.append(Paragraph(paragraph, content_style))
            elements.append(Spacer(1, 0.1*inch))
    footer_style = ParagraphStyle(
        name='Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1
    )
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("This is an official document. All rights reserved.", footer_style))
    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{story.title}.pdf"'
    return response

def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.darkblue)
    canvas.setFillColor(colors.darkblue)
    canvas.rect(72, 730, 450, 20, fill=1)
    canvas.setStrokeColor(colors.darkblue)
    canvas.setFillColor(colors.darkblue)
    canvas.rect(72, 50, 450, 2, fill=1)
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.black)
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.drawRightString(540, 30, text)
    canvas.setFont("Helvetica", 60)
    canvas.setFillColor(colors.lightgrey.clone(alpha=0.2))
    canvas.rotate(45)
    canvas.drawCentredString(350, 50, "OFFICIAL")
    canvas.restoreState()

@login_required(login_url='authentication:login') 
def story_detail_view(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    story=story.content
    return render(request, "edityourownstory.html", {"stor11": story})

@login_required(login_url='authentication:login') 
def invite_collaborator(request):
    users = User.objects.exclude(id=request.user.id)
    search_query = request.GET.get('q', '')
    if search_query:
        users = users.filter(username__icontains=search_query)
    paginator = Paginator(users, 5)
    page_number = request.GET.get('page')
    page_users = paginator.get_page(page_number)
    if request.method == "POST":
        selected_user_ids = request.POST.getlist("selected_users")
        new_story = Story.objects.create(
            user=request.user,
            title="New Collaborative Story",
            content="Start your collaborative journey here!",
            status=None,
            is_collaborated=True,
        )
        for user_id in selected_user_ids:
            receiver = User.objects.get(id=user_id)
            CollaborationInvite.objects.create(
                story=new_story,
                sender=request.user,
                receiver=receiver
            )
        messages.success(request, f"Story created and invitations sent!")
        return redirect("mystory:edit_story", story_id=new_story.id)
    return render(request, "invite_collaborator.html", {
        "users": page_users,
        "search_query": search_query
    })

@login_required(login_url='authentication:login')
def collaboration_requests(request):
    print('hi')
    pending_invites = CollaborationInvite.objects.filter(receiver=request.user, status="pending")
    notifications = Notification.objects.filter(user=request.user,is_read=False)
    Notification.objects.filter(id__in=[n.id for n in notifications]).update(is_read=True)
    print('notification:',notifications)
    for i in notifications:
        print('notification:',i)
    context = {
        "pending_invites": pending_invites,
        'notifications': notifications
               }
    return render(request, "collaboration_requests.html",context )

@login_required(login_url='authentication:login') 
def view_invites(request):
    return render(request, "view_invites.html")
 
@login_required(login_url='authentication:login') 
def accept_invite(request, invite_id):
    invite = get_object_or_404(CollaborationInvite, id=invite_id, receiver=request.user)
    invite.accept()
    messages.success(request, f"You are now a collaborator on '{invite.story.title}'!")
    return redirect("mystory:edit_story", story_id=invite.story.id)
 
def reject_invite(request, invite_id):
    invite = get_object_or_404(CollaborationInvite, id=invite_id, receiver=request.user)
    invite.reject()
    messages.info(request, f"Collaboration invite for '{invite.story.title}' rejected.")
    return redirect("mystory:collaboration_requests")

@login_required(login_url='authentication:login') 
def my_collaborations(request):
    stories = request.user.collaborations.all()   
    return render(request, "my_collaborations.html", {"stories": stories})

@login_required(login_url='authentication:login') 
def mystory1(request):
    query = request.GET.get('search', '')
    stories = Story.objects.filter(
        Q(user=request.user) | Q(collaborators=request.user)
    ).distinct()

    if query:
        stories = stories.filter(
            Q(title__icontains=query) |
            Q(user__username__icontains=query) |
            Q(genre__icontains=query)
        )

    paginator = Paginator(stories, 5)   
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'mystory.html', {'stories': page_obj, 'query': query})

@login_required(login_url='authentication:login') 
def delete_story(request, story_id):
    if request.method == "POST":
        story = get_object_or_404(Story, id=story_id)
        story.delete()
        messages.success(request, "Story deleted successfully.")
    return redirect("mystory:mystory1")

def author_profile(request,username):
    author = get_object_or_404(User,username=username)
    stories = Story.objects.filter(user=author)
    collabrated = Story.objects.filter(collaborators = author).exclude( user=author)
    total_stories = stories.count()
    total_collab =collabrated.count()
    is_following = Follower.objects.filter(follower=request.user, following=author).exists() if request.user.is_authenticated else False
   
    if hasattr(author, 'profile') and author.profile.profile_picture:
        profile_pic_url = author.profile.profile_picture.url
    else:
        profile_pic_url = static('images/logo4.webp')
    return render(request,'author_profile.html',{
        "author": author,
        "stories": stories,
        "collaborated": collabrated,
        "total_stories": total_stories,
        "total_collab": total_collab,
        "is_following": is_following,
        "profile_pic_url": profile_pic_url,
         
    })
@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    if request.user != target_user:
        follow, created = Follower.objects.get_or_create(follower=request.user, following=target_user)
        if created:
            username = escape(request.user.username)
            user_link = f'<a href="/Mystory/author/{username}/">{username}</a>'
            Notification.objects.create(
                user=target_user,
                message=f"{user_link} started following you."
            )
    return redirect('mystory:author_profile', username=target_user)

@login_required
def unfollow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    if request.user != target_user:
        Follower.objects.filter(follower=request.user, following=target_user).delete()
    return redirect('mystory:author_profile', username=username)

def user_followers(request, username):
    user = get_object_or_404(User, username=username)
    followers = user.followers.select_related('follower')
    return render(request, 'follow_list.html', {'user': user, 'follows': followers,'view_type': 'followers'})

def user_following(request, username):
    user = get_object_or_404(User, username=username)
    following = user.following.select_related('following')
    return render(request, 'follow_list.html', {'user': user, 'follows': following,'view_type': 'following'})



def notify_followers(user, story,action="posted"):
    followers = Follower.objects.filter(following=user).select_related("follower")
    username = escape(user.username)
    story_title = escape(story.title)

    user_link = f'<a href="/Mystory/author/{username}/">{username}</a>'
    story_link = f'<a href="/Aistories/view_story/{story.id}/">{story_title}</a>'
    message = f"{user_link} posted a new story: '{story_link}'."
    send_story_email_to_followers(story, followers, action)

    for follower_relation in followers:
        Notification.objects.create(
            user=follower_relation.follower,
            message=message
        )
