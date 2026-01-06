from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import re
from django.conf import settings
from django.core.mail import send_mail
import random
from django.contrib.auth import authenticate, login,logout
from Mystory.models import Story
from django.db.models import Count,Sum
from django.db.models.functions import TruncDate
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Profile
from django.db import transaction



def is_admin(user):
    return user.is_authenticated and user.is_staff

 
def signup(request):
    if request.user.is_authenticated:
        return redirect('authentication:home') 
    if request.method =='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        if User.objects.filter(email=email).exists():
             messages.error(request, "Email already registered.")
             return render(request, 'signup.html', {'email': email})
        error = validate_password(password)
        if error:
            messages.error(request,error)
            return render(request, 'signup.html', {'email': email})  

        send_otp(email)
        messages.success(request, "OTP sent to your email.")
        request.session['pending_user'] = {'email': email, 'password': password}
        return redirect('authentication:verify_otp')
    return render(request, 'signup.html')    

def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter."
    return None

otp_storage = {}
def send_otp(email):
     
    otp = random.randint(100000, 999999)
    otp_storage[email] = otp  

    # send_mail(
    #     'Your OTP Code',
    #     f'Your OTP for signup verification is: {otp}',
    #     settings.EMAIL_HOST_USER,
    #     [email],
    #     fail_silently=False,
    # )

def verify_otp(request):
    if request.user.is_authenticated:
        return redirect('authentication:home') 
    
    if request.method == 'POST':
        email = request.session.get('pending_user', {}).get('email')   
        password = request.session.get('pending_user', {}).get('password')
        entered_otp = request.POST.get('otp')

        if not email or not password:
            messages.error(request, "Session expired. Try signing up again.")
            return redirect('authentication:signup')
        
        # if entered_otp and otp_storage.get(email) == int(entered_otp): 
        if entered_otp and int(entered_otp) == 123456:
            try:
                
                with transaction.atomic():
                    
                    if User.objects.filter(email=email).exists():
                        messages.warning(request, "User already registered. Please log in.")
                        if 'pending_user' in request.session:
                            del request.session['pending_user']
                        return redirect('authentication:login')
                    
                    
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=password
                    )
                
                
                user = authenticate(request, username=email, password=password)
                if user:
                    login(request, user)
                    if 'pending_user' in request.session:
                        del request.session['pending_user']
                    messages.success(request, "Signup successful.") 
                    return redirect('authentication:home')
                    
            except Exception as e:
              
                print(f"Error creating user: {e}")
                messages.error(request, f"An error occurred. Please try logging in. ")
                if 'pending_user' in request.session:
                    del request.session['pending_user']
                return redirect('authentication:login')
        else:
            messages.error(request, "Invalid OTP. Try again.")
            return redirect('authentication:verify_otp')
            
    return render(request, 'verify_otp.html')
def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('authentication:users')  
        return redirect('authentication:home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)  
            user = authenticate(request, username=user.username, password=password) 
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            if user.is_superuser:
                return redirect('authentication:users')  
            return redirect('authentication:home')
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'login.html', {'email': email})

    return render(request, 'login.html')

def home(request):
        trending_stories = (
        Story.objects.annotate(view_count=Count('views'))
        .filter(status='public')  
        .order_by('-view_count', '-created_at')[:6] )  
        return render(request, 'home.html', {'trending_stories': trending_stories})

@user_passes_test(is_admin, login_url='authentication:login')
def users(request):
    users_list = User.objects.annotate(story_count=Count('stories'))
    paginator = Paginator(users_list, 6)   
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    total_stories = users_list.aggregate(Sum('story_count'))['story_count__sum'] or 0
    total_users = User.objects.count()
    return render(request, 'users.html', {
        'users': users,
        'total_stories': total_stories,
        'total_users': total_users,
    })
@user_passes_test(is_admin, login_url='authentication:login')
def toggle_block_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_active = not user.is_active
        user.save()
    return redirect('authentication:users')

def logout_view(request):
    request.session.flush()   
    logout(request)
    return redirect('authentication:login')


@user_passes_test(is_admin, login_url='authentication:login')
def dashboard(request):
    users_by_day = (
        User.objects
        .annotate(day=TruncDate('date_joined'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

   
    labels = [entry['day'].strftime('%Y-%m-%d') for entry in users_by_day]
    data = [entry['count'] for entry in users_by_day]

   
    top_viewed_stories = (
        Story.objects.annotate(view_count=Count('views'))
        .filter(status='public')
        .order_by('-view_count')[:6]
    )

     
    top_liked_stories = (
        Story.objects.annotate(like_count=Count('likes'))
        .filter(status='public')
        .order_by('-like_count')[:6]
    )
    users = User.objects.annotate(story_count=Count('stories'))
    total_stories = users.aggregate(Sum('story_count'))['story_count__sum'] or 0

    context = {
        'labels': labels,
        'data': data,
        'top_viewed_stories': top_viewed_stories,
        'top_liked_stories': top_liked_stories,
        'users': users,
        'total_stories':total_stories,
    }

    return render(request, 'dashboard.html', context)

@user_passes_test(is_admin, login_url='authentication:login')
def stories(request):
    
    all_stories = Story.objects.all().order_by('-id')   
    
 
    total_stories = all_stories.count()
    total_views = sum(story.views.count() for story in all_stories) if all_stories else 0
    total_likes = sum(story.likes.count() for story in all_stories) if all_stories else 0
    print('total_views:',total_views)
    
    
    paginator = Paginator(all_stories, 12)  
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_stories': total_stories,
        'total_views': total_views,
        'total_likes': total_likes,
        
    }
    
    return render(request, 'stories.html', context)


@user_passes_test(is_admin, login_url='authentication:login')
def delete_story(request, story_id):
    if request.method == "POST":
        story = get_object_or_404(Story, id=story_id)
        story.delete()
        messages.success(request, "Story deleted successfully.")
    return redirect("authentication:stories")




@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        bio = request.POST.get('bio')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        profile_picture = request.FILES.get('profile_picture')

        profile.bio = bio
        profile.address = address
        profile.phone_number = phone_number

        if profile_picture:
            profile.profile_picture = profile_picture
        
        profile.save()
        return redirect('authentication:view_profile')

    return render(request, 'edit_profile.html', {'profile': profile})

@login_required
def view_profile(request):
    profile  = request.user.profile
    return render(request, 'view_profile.html', {'profile': profile})