from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import NewUser,FamilyMember,Event,Invite,AddressChangeRequest,Announcement
from django.core.files.storage import default_storage
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import FamilyMember, NewUser
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import NewUser, FamilyMember  # adjust if needed
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.dateparse import parse_date
from .models import FamilyMember, NewUser
from django.utils import timezone  # <-- Make sure this is at the top
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    entrepreneurs = Entrepreneur.objects.filter(is_deleted=False).order_by('-id')
    events = Event.objects.filter(user_id=1, is_deleted=False).order_by('-date')
    return render(request, 'index1.html', {'entrepreneurs': entrepreneurs, 'events':events})

def committeemembers(request):
    """
    Render the index page.
    """
    return render(request, 'committeemembers.html')

def jainammembers(request):
    """
    Render the index page.
    """
    return render(request, 'jainammembers.html')

def about(request):
    """
    Render the about page.
    """
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# register a new user
def register_user(request):
    if request.method == 'POST':
        print("✅ register_user POST triggered")

        # Extract form data
        first_name = request.POST.get("firstName")
        middle_name = request.POST.get("middleName", "")
        last_name = request.POST.get("lastName")
        gotra = request.POST.get("gotra", "")
        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone")
        whatsapp_number = request.POST.get("whatsappNumber", "")
        blood_group = request.POST.get("bloodGroup", "")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")

        pant = request.POST.get("pant")
        pant_option = request.POST.get("pantOption")

        marudar_place = request.POST.get("marudarplace")
        state = request.POST.get("state")
        city = request.POST.get("current")
        pincode = request.POST.get("pincode")
        address = request.POST.get("address")

        business_name = request.POST.get("businessName")
        business_type = request.POST.get("businessType")
        industry = request.POST.get("industry")
        website = request.POST.get("website", "")
        business_address = request.POST.get("baddress")

        profile_picture = request.FILES.get("picture")

        # Validation
        if password != confirm_password:
            return render(request, 'register.html', {"error": "Passwords do not match"})

        if NewUser.objects.filter(Q(email=email) | Q(phone_number=phone)).exists():
            error_message = "A user with this "
            if NewUser.objects.filter(email=email).exists():
                error_message += "email"
            if NewUser.objects.filter(phone_number=phone).exists():
                if "email" in error_message:
                    error_message += " and "
                error_message += "phone number"
            error_message += " already exists."
            return render(request, 'register.html', {"error": error_message})

        try:
            # Save to DB
            user = NewUser.objects.create(
                username=phone,  # ✅ Assign phone number as username
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                gotra=gotra,
                DOB=parse_date(dob) if dob else None,
                gender=gender,
                email=email,
                phone_number=phone,
                whatsapp_number=whatsapp_number,
                blood_group=blood_group,
                password=make_password(password),

                pant=pant,
                pantoption=pant_option,

                marudar_place=marudar_place,
                state=state,
                city=city,
                pincode=pincode,
                residential_address=address,

                business_name=business_name,
                business_type=business_type,
                industry=industry,
                website=website,
                business_address=business_address,

                profile_picture=profile_picture,
              
            )

            messages.success(request, "Your registration was successful. Please wait until your account is approved by the admin.")
            return redirect('login')
        except IntegrityError as e:
            print(f"Error saving user: str{e}")
            return render(request,'register.html', {"error": "A user with this email or phone number already exists. Please try again with different email and phone number."})

    return render(request, 'register.html')


# Temporary in-memory store
OTP_STORE = {}

@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if phone:
            otp = str(random.randint(100000, 999999))
            OTP_STORE[phone] = otp
            print(f"OTP for {phone} is {otp}")  # Log to console for testing
            return JsonResponse({'success': True, 'message': 'OTP sent (check server console).'})
        return JsonResponse({'success': False, 'message': 'Phone number missing.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        otp = request.POST.get('otp')
        if phone and otp:
            stored_otp = OTP_STORE.get(phone)
            if stored_otp == otp:
                return JsonResponse({'success': True, 'message': 'OTP verified successfully.'})
            return JsonResponse({'success': False, 'message': 'Invalid OTP.'})
        return JsonResponse({'success': False, 'message': 'Phone or OTP missing.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})



from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

User = get_user_model()

def login_user(request):
    if request.method == 'POST':
        phone_number = request.POST.get('username')  # used as username
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(username=phone_number)
        except User.DoesNotExist:
            user_obj = None

        if user_obj:
            if not user_obj.is_active:
                # Show custom message based on user_type
                if user_obj.user_type == 'Admin':
                    messages.error(request, "Admin account is not activated. Please contact support.")
                else:
                    messages.error(request, "Your account is not active. Please contact admin.")
                return render(request, 'login.html')

            # User is active, now try to authenticate
            user = authenticate(request, username=phone_number, password=password)
            if user:
                login(request, user)
                if user.user_type == 'Admin':
                    return redirect('admin_dashboard')
                elif user.user_type == 'User':
                    return redirect('dashboard')
                else:
                    return redirect('dashboard')
            else:
                messages.error(request, "Invalid phone number or password.")
        else:
            messages.error(request, "Invalid phone number or password.")

    return render(request, 'login.html')

@login_required
def profile_view(request):
    user = request.user  # The currently logged-in user
    return render(request, 'profile.html', {'user': user})

@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get("first_name")
        user.middle_name = request.POST.get("middle_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.phone_number = request.POST.get("phone_number")
        user.DOB = request.POST.get("dob")
        user.gender = request.POST.get("gender")
        user.gotra = request.POST.get("gotra")
        user.pant = request.POST.get("pant")
        user.pantoption = request.POST.get("pantoption")
        user.city = request.POST.get("city")
        user.state = request.POST.get("state")
        user.pincode = request.POST.get("pincode")
        user.residential_address = request.POST.get("residential_address")
        user.marudar_place = request.POST.get("marudar_place")
        user.business_name = request.POST.get("business_name")
        user.business_type = request.POST.get("business_type")
        user.industry = request.POST.get("industry")
        user.website = request.POST.get("website")
        user.business_address = request.POST.get("business_address")

        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        user.save()
        return redirect('profile_view')

    return render(request, 'edit_profile.html', {'user': user})

def user_dashboard(request):
    user = request.user  # Get the logged-in user
    user_id = request.session.get('user_id')  # Get the user ID from the session
    all_users = NewUser.objects.exclude(user_type='Admin')  # Get all users for the dashboard
    admin_users = NewUser.objects.filter(user_type='Admin')
    announcements = Event.objects.filter(user__in=admin_users, is_deleted=False).order_by('-created_at')
    general_announcements = Announcement.objects.filter(user__in=admin_users, is_deleted=False).order_by('-created_at')
    invites = Invite.objects.filter(members=user).select_related('event', 'user').order_by('-invited_at')


    # Get all family members linked to the logged-in user
    family_members = FamilyMember.objects.filter(main_user=user)
    family_count = family_members.count()  # Count of family members

    # get all events for the user
    events = Event.objects.filter(user=user).order_by('-date')
    events_count = events.count()  # Count of events
    upcoming_events = events.filter(date__gte=datetime.now()).order_by('date')  # Get upcoming events
    upcoming_events_count = upcoming_events.count()  # Count of upcoming events

        # Extract filter parameters
    marudar_place = request.GET.get('marudarplace')
    state = request.GET.get('state')
    city = request.GET.get('city')
    business_type = request.GET.get('business_type')

    # Apply filters
    if marudar_place:
        all_users = all_users.filter(marudar_place__icontains=marudar_place)
    if state:
        all_users = all_users.filter(state__icontains=state)
    if city:
        all_users = all_users.filter(city__icontains=city)
    if business_type:
        all_users = all_users.filter(business_type__iexact=business_type)


    # For dropdown population (you must define how you collect marudar_places and states)
    marudar_places = NewUser.objects.values_list('marudar_place', flat=True).distinct()
    states = NewUser.objects.values_list('state', flat=True).distinct()


    context = {
        'user': user,
        'all_users': all_users,
        'marudar_places': marudar_places,
        'states': states,
        'user_id': user_id,
        'marudar_place': marudar_place,
        'family_members': family_members,
        'family_count': family_count,
        'state': state,
        'city': city,
        'events': events,
        'events_count': events_count,
        'upcoming_events': upcoming_events,
        'upcoming_events_count': upcoming_events_count,
        'announcements': announcements,
        'general_announcements' : general_announcements,
        'invites': invites

    }
    return render(request, 'user_dashboard.html', context)

# add user (head of the family) by admin
def add_member_admin(request):
    user = request.user  # Get the logged-in user
    user_id = request.session.get('user_id')  # Get the user ID from the session
    all_users = NewUser.objects.filter(added_by = 1)  # Get all users for the dashboard


    # Get all family members linked to the logged-in user
    family_members = FamilyMember.objects.filter(main_user=user)
    family_count = family_members.count()  # Count of family members

    # get all events for the user
    events = Event.objects.filter(user=user).order_by('-date')
    events_count = events.count()  # Count of events
    upcoming_events = events.filter(date__gte=datetime.now()).order_by('date')  # Get upcoming events
    upcoming_events_count = upcoming_events.count()  # Count of upcoming events

        # Extract filter parameters
    marudar_place = request.GET.get('marudarplace')
    state = request.GET.get('state')
    city = request.GET.get('city')
    business_type = request.GET.get('business_type')

    # Apply filters
    if marudar_place:
        all_users = all_users.filter(marudar_place__icontains=marudar_place)
    if state:
        all_users = all_users.filter(state__icontains=state)
    if city:
        all_users = all_users.filter(city__icontains=city)
    if business_type:
        all_users = all_users.filter(business_type__iexact=business_type)


    # For dropdown population (you must define how you collect marudar_places and states)
    marudar_places = NewUser.objects.values_list('marudar_place', flat=True).distinct()
    states = NewUser.objects.values_list('state', flat=True).distinct()


    context = {
        'user': user,
        'all_users': all_users,
        'marudar_places': marudar_places,
        'states': states,
        'user_id': user_id,
        'marudar_place': marudar_place,
        'family_members': family_members,
        'family_count': family_count,
        'state': state,
        'city': city,
        'events': events,
        'events_count': events_count,
        'upcoming_events': upcoming_events,
        'upcoming_events_count': upcoming_events_count,

    }
    return render(request, 'add_member_admin.html', context)# register a new user


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from django.contrib.auth.hashers import make_password
from .models import NewUser  # adjust this import if needed

@login_required
def add_new_user(request):
    if request.method == 'POST':
        # Read form data
        first_name = request.POST.get("firstName")
        middle_name = request.POST.get("middleName", "")
        last_name = request.POST.get("lastName")
        gotra = request.POST.get("gotra", "")
        DOB_str = str(request.POST.get("dob"))
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        whatsapp_number = request.POST.get("whatsappNumber", "")
        blood_group = request.POST.get("bloodGroup", "")

        pant = request.POST.get("pant")
        pant_option = request.POST.get("pantOption")

        marudar_place = request.POST.get("marudarplace")
        state = request.POST.get("state")
        city = request.POST.get("current")
        pincode = request.POST.get("pincode")
        address = request.POST.get("address")

        business_name = request.POST.get("businessName")
        business_type = request.POST.get("businessType")
        industry = request.POST.get("industry")
        website = request.POST.get("website", "")
        business_address = request.POST.get("baddress")

        profile_picture = request.FILES.get("picture")

        # Parse DOB
        DOB = parse_date(DOB_str)
        if not DOB:
            return render(request, 'add_new_user.html', {'error': 'Invalid DOB format'})

        # Use phone as username and password
        default_password = make_password(phone)

        # Create user
        NewUser.objects.create(
            username=phone,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            gotra=gotra,
            DOB=DOB,
            gender=gender,
            email=email,
            password=default_password,
            phone_number=phone,
            whatsapp_number=whatsapp_number,
            blood_group=blood_group,
            pant=pant,
            pantoption=pant_option,
            marudar_place=marudar_place,
            state=state,
            city=city,
            pincode=pincode,
            residential_address=address,
            business_name=business_name,
            business_type=business_type,
            industry=industry,
            website=website,
            business_address=business_address,
            profile_picture=profile_picture,
            is_active=True,
            is_deleted=False,
            added_by=request.user if request.user.is_authenticated else None,
        )
        return redirect('add_member_admin')  # Change to your actual view name

    return render(request, 'add_new_user.html')




def add_family_member_for_user(request, pk):
    main_user = get_object_or_404(NewUser, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        relationship = request.POST.get('relationship')
        birthday = request.POST.get('birthday')
        gender = request.POST.get('Gender')
        phone = request.POST.get('phone')
        whatsapp = request.POST.get('whatsappNumber')
        email = request.POST.get('email')
        blood_group = request.POST.get('blood_group', '')
        address = request.POST.get('address')
        notes = request.POST.get('notes')

        if FamilyMember.objects.filter(phone=phone).exists():
            messages.error(request, "A family member with this phone already exists.")
        else:
            family_member = FamilyMember(
                main_user=main_user,
                head_of_family=main_user,
                name=name,
                relationship=relationship,
                birthday=birthday or None,
                gender=gender,
                phone=phone,
                whatsapp=whatsapp,
                email=email,
                blood_group=blood_group,
                address=address,
                notes=notes,
            )
            family_member.set_password(phone)  # Set password as phone
            family_member.save()
            messages.success(request, f"Family member added for {main_user.first_name}.")
            return redirect('add_family_member_for_user', pk=pk)

    return render(request, 'add_member_admin.html', {'main_user': main_user})



@csrf_exempt
@login_required
def add_family_member(request):
    if request.method == "POST":
        main_user = request.user  # Authenticated user

        name = request.POST.get("name")
        relationship = request.POST.get("relationship")
        birthday_str = request.POST.get("birthday")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        whatsapp = request.POST.get("whatsappNumber")
        gender = request.POST.get("Gender")
        blood_group = request.POST.get("bloodGroup", "")
        address = request.POST.get("address")
        notes = request.POST.get("notes")

        if not phone:
            messages.error(request, "Phone number is required.")
            return redirect("dashboard")

        if FamilyMember.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists.")
            return redirect("dashboard")

        # Convert birthday string to date object
        birthday = parse_date(birthday_str) if birthday_str else None

        member = FamilyMember.objects.create(
            main_user=main_user,
            name=name,
            relationship=relationship,
            birthday=birthday,
            phone=phone,
            email=email,
            whatsapp=whatsapp,
            gender=gender,
            blood_group=blood_group,
            address=address,
            notes=notes
        )

        # Optional: if your FamilyMember model has a password field
        member.set_password(phone)
        member.save()

        messages.success(request, f"Family member '{name}' added successfully.")
        return redirect("dashboard")

    return redirect("dashboard")


@csrf_exempt  # optional, better to use @login_required and handle CSRF correctly
def edit_family_member(request, pk):
    member = get_object_or_404(FamilyMember, pk=pk)
    if request.method == "POST":
        member.name = request.POST.get("name")
        member.relationship = request.POST.get("relationship")
        member.birthday = parse_date(request.POST.get("birthday")) if request.POST.get("birthday") else None
        member.phone = request.POST.get("phone")
        member.email = request.POST.get("email")
        member.whatsapp = request.POST.get("whatsappNumber")
        member.gender = request.POST.get("Gender")
        member.address = request.POST.get("address")
        member.notes = request.POST.get("notes")
        member.save()

        messages.success(request, "Family member updated successfully.")
        return redirect("dashboard")

    return render(request, "edit_member.html", {"member": member})



def delete_family_member(request, pk):
    member = get_object_or_404(FamilyMember, pk=pk)
    member.delete()
    messages.success(request, "Family member deleted successfully.")
    return redirect("dashboard")


def admin_dashboard(request):
    user_id = request.session.get('user_id')
    users = NewUser.objects.all() # Get all users
    users_count =  users.count() # Get the count  users
    active_users = users.filter(is_active=True) # Get all active users
    active_users_count = active_users.count() # Get the count of active users
    family_members = FamilyMember.objects.all() # Get all family members
    family_members_count = family_members.count()# Get the count of family members
    pending_users = users.filter(is_active=False) # Get all pending users
    pending_users_count = pending_users.count() # Get the count of pending users
    event = Event.objects.all() # Get all events
    upcoming_events = event.filter(date__gte=datetime.now()).order_by('date') # Get upcoming events
    upcoming_events_count = upcoming_events.count() # Get the count of upcoming events
    event_count = event.count() # Get the count of events

    context ={
        'users': users,
        'users_count': users_count,
        'active_users': active_users,
        'active_users_count': active_users_count,
        'family_members': family_members,
        'family_members_count': family_members_count,
        'pending_users': pending_users,
        'pending_users_count': pending_users_count,
        'user_id': user_id,
        'event': event,
        'event_count': event_count,
        'upcoming_events': upcoming_events,
        'upcoming_events_count': upcoming_events_count,
    }

    return render(request, 'admin_dashboard.html', context)


def request_list(request):


    # Start with all users except Admins
    pending_users = NewUser.objects.exclude(user_type='Admin')

    # Extract filter parameters
    marudar_place = request.GET.get('marudarplace')
    state = request.GET.get('state')
    city = request.GET.get('city')
    business_type = request.GET.get('business_type')

    # Apply filters
    if marudar_place:
        pending_users = pending_users.filter(marudar_place__icontains=marudar_place)
    if state:
        pending_users = pending_users.filter(state__icontains=state)
    if city:
        pending_users = pending_users.filter(city__icontains=city)
    if business_type:
        pending_users = pending_users.filter(business_type__iexact=business_type)

    pending_users_count = pending_users.count()

    # For dropdown population (you must define how you collect marudar_places and states)
    marudar_places = NewUser.objects.values_list('marudar_place', flat=True).distinct()
    states = NewUser.objects.values_list('state', flat=True).distinct()

    context = {
        'pending_users': pending_users,
        'pending_users_count': pending_users_count,
        'marudar_places': marudar_places,
        'states': states,
    }
    return render(request, 'request_list.html', context)



def request_list1(request):


    # Start with all users except Admins
    pending_users = NewUser.objects.exclude(user_type='Admin')

    # Extract filter parameters
    marudar_place = request.GET.get('marudarplace')
    state = request.GET.get('state')
    city = request.GET.get('city')
    business_type = request.GET.get('business_type')

    # Apply filters
    if marudar_place:
        pending_users = pending_users.filter(marudar_place__icontains=marudar_place)
    if state:
        pending_users = pending_users.filter(state__icontains=state)
    if city:
        pending_users = pending_users.filter(city__icontains=city)
    if business_type:
        pending_users = pending_users.filter(business_type__iexact=business_type)

    pending_users_count = pending_users.count()

    # For dropdown population (you must define how you collect marudar_places and states)
    marudar_places = NewUser.objects.values_list('marudar_place', flat=True).distinct()
    states = NewUser.objects.values_list('state', flat=True).distinct()

    context = {
        'pending_users': pending_users,
        'pending_users_count': pending_users_count,
        'marudar_places': marudar_places,
        'states': states,
    }
    return render(request, 'request_list1.html', context)


def activate_user(request, user_id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(NewUser, id=user_id)
            user.is_active = True
            user.save()
            messages.success(request, f'User {user.email} activated successfully.')
        except Exception as e:
            messages.error(request, f'Failed to activate user: {str(e)}')
    return redirect('search_members')

def deactivate_user(request, user_id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(NewUser, id=user_id)
            user.is_active = False
            user.save()
            messages.success(request, f'User {user.email} deactivated successfully.')
        except Exception as e:
            messages.error(request, f'Failed to deactivate user: {str(e)}')
    return redirect('search_members')


def get_member_details(request, user_id):
    try:
        member = NewUser.objects.get(id=user_id)

        # Get related family members using related_name
        family_members = member.family_members.all()

        family_list = [
            {
                'id': fm.id,
                'name': fm.name,
                'relationship': fm.relationship,
                'birthday': fm.birthday.strftime('%d %B %Y') if fm.birthday else '',
                'gender': fm.gender,
                'phone': fm.phone,
                'whatsapp': fm.whatsapp,
                'blood_group': fm.blood_group,
                'email': fm.email,
                'address': fm.address,
                'notes': fm.notes,
            }
            for fm in family_members
        ]

        data = {
            "username": member.username,
            "user_type": member.user_type,
            "first_name": member.first_name,
            "middle_name": member.middle_name,
            "last_name": member.last_name,
            "gotra": member.gotra,
            "DOB": member.DOB.strftime('%d %B %Y') if member.DOB else '',
            "gender": member.gender,
            "profile_picture": member.profile_picture.url if member.profile_picture else '',
            "email": member.email,
            "phone_number": member.phone_number,
            "whatsapp_number": member.whatsapp_number,
            "blood_group": member.blood_group,
            "pant": member.pant,
            "pantoption": member.pantoption,
            "marudar_place": member.marudar_place,
            "state": member.state,
            "city": member.city,
            "pincode": member.pincode,
            "residential_address": member.residential_address,
            "business_name": member.business_name,
            "business_type": member.business_type,
            "industry": member.industry,
            "website": member.website,
            "business_address": member.business_address,
            "is_active": member.is_active,
            "date_joined": member.date_joined.strftime('%d %B %Y %H:%M'),
            "last_login": member.last_login.strftime('%d %B %Y %H:%M') if member.last_login else '',
            "family_members": family_list,
        }

        return JsonResponse(data)

    except NewUser.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)


def get_member_details_user(request, user_id):
    try:
        member = NewUser.objects.get(id=user_id)
        data = {
            'name': member.first_name,

            'dob': member.DOB.strftime('%d %B %Y') if member.DOB else '',

            'phone': member.phone_number,
            'email': member.email,
            'address': member.residential_address,

        }
        return JsonResponse(data)
    except FamilyMember.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)

@csrf_exempt
def logout_user(request):
    """Log out the user by clearing the session.

    """
    request.session.flush()  # Clear the session
    return redirect('login')  # Redirect to the login page


"""Event functions"""

@csrf_exempt
@login_required(login_url='login')  # Redirects to login if not authenticated
def add_event(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to add an event.")
            return redirect('login')  # redirect to login instead of dashboard

        main_user = request.user  # Directly use authenticated user

        title = request.POST.get("title")
        date_str = request.POST.get("date")
        time_str = request.POST.get("time")
        location = request.POST.get("location", "")
        description = request.POST.get("description", "")

        # Basic validation
        if not title or not date_str or not time_str:
            messages.error(request, "Title, date, and time are required.")
            return redirect('dashboard')

        # Parse date and time
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            messages.error(request, "Invalid date or time format.")
            return redirect('dashboard')

        # Save event
        Event.objects.create(
            user=main_user,
            title=title,
            date=date,
            time=time,
            location=location,
            description=description
        )

        

        messages.success(request, f"Event '{title}' added successfully.")
        return redirect('event_list')

    return redirect('event_list')

@csrf_exempt
@login_required(login_url='login')  # Redirects to login if not authenticated
def add_event_admin(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to add an event.")
            return redirect('login')  # redirect to login instead of dashboard

        main_user = request.user  # Directly use authenticated user

        title = request.POST.get("title")
        date_str = request.POST.get("date")
        time_str = request.POST.get("time")
        location = request.POST.get("location", "")
        description = request.POST.get("description", "")

        # Basic validation
        if not title or not date_str or not time_str:
            messages.error(request, "Title, date, and time are required.")
            return redirect('admin_dashboard')

        # Parse date and time
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            messages.error(request, "Invalid date or time format.")
            return redirect('admin_dashboard')

        # Save event
        Event.objects.create(
            user=main_user,
            title=title,
            date=date,
            time=time,
            location=location,
            description=description
        )

        messages.success(request, f"Event '{title}' added successfully.")
        return redirect('event_list_admin')

    return redirect('event_list_admin')


@csrf_exempt
def update_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('id')
        try:
            event = Event.objects.get(pk=event_id)
            event.title = request.POST.get('title')
            event.date = request.POST.get('date')
            event.time = request.POST.get('time')
            event.location = request.POST.get('location')
            event.description = request.POST.get('description')
            event.save()
            return JsonResponse({'status': 'success'})
        except Event.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Event not found'}, status=404)
        
@csrf_exempt
def soft_delete_event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
        event.soft_delete()
        return JsonResponse({'status': 'success'})
    except Event.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Not found'}, status=404)
    
from .models import Entrepreneur

def entrepreneur_list(request):
    entrepreneurs = Entrepreneur.objects.filter(is_deleted=False).order_by('-id')
    return render(request, 'el.html', {'entrepreneurs': entrepreneurs})

@csrf_exempt
def add_entrepreneur(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        company_name = request.POST.get('company_name')
        designation = request.POST.get('designation')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        profile_picture = request.FILES.get('profile_picture')
        website = request.POST.get('website', '')

        Entrepreneur.objects.create(
            name=name,
            company_name=company_name,
            designation=designation,
            phone=phone,
            email=email,
            address=address,
            profile_picture=profile_picture,
            website =website,
            added_by=request.user if request.user.is_authenticated else None
        )
        return JsonResponse({'message': 'Entrepreneur added successfully'})
    return JsonResponse({'error': 'Invalid method'}, status=400)

@csrf_exempt
def edit_entrepreneur(request):
    if request.method == 'POST':
        eid = request.POST.get('id')
        print("✅ edit_entrepreneur called with id:", eid)
        entrepreneur = Entrepreneur.objects.get(id=eid)

        entrepreneur.name = request.POST.get('name')
        entrepreneur.company_name = request.POST.get('company_name')
        entrepreneur.designation = request.POST.get('designation')
        entrepreneur.phone = request.POST.get('phone')
        entrepreneur.email = request.POST.get('email')
        entrepreneur.website = request.POST.get('website')
        entrepreneur.address = request.POST.get('address')

        if request.FILES.get('profile_picture'):
            entrepreneur.profile_picture = request.FILES.get('profile_picture')

        entrepreneur.save()
        return JsonResponse({'message': 'Entrepreneur updated successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def soft_delete_entrepreneur(request, pk):
    entrepreneur = get_object_or_404(Entrepreneur, pk=pk)
    entrepreneur.soft_delete()
    messages.success(request, f"{entrepreneur.name} was soft deleted.")
    return redirect('entrepreneur_list')



def get_event_details(request, event_id):
    # ✅ Step 1: Check if user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    try:
        # ✅ Step 2: Only fetch events belonging to the logged-in user
        event = Event.objects.get(id=event_id, user=request.user)
        data = {
            "title": event.title,
            "date": event.date.strftime("%Y-%m-%d"),
            "time": event.time.strftime("%H:%M"),
            "location": event.location,
            "description": event.description,
        }
        return JsonResponse(data)
    except Event.DoesNotExist:
        return JsonResponse({"error": "Event not found"}, status=404)

def get_entreprenuers_details(request, event_id):
    # ✅ Step 1: Check if user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    try:
        # ✅ Step 2: Only fetch events belonging to the logged-in user
        event = Entrepreneur.objects.get(id=event_id, user=request.user)
        data = {
            "name": event.name,
            "company": event.company_name,
            "phone": event.phone,
            "location": event.address,
        }
        return JsonResponse(data)
    except Event.DoesNotExist:
        return JsonResponse({"error": "Event not found"}, status=404)


def delete_event(request, event_id):
    if request.method == 'POST':
        try:
            event = Event.objects.get(id=event_id, user=request.user)
            event.delete()
            messages.success(request, "Event deleted successfully.")
        except Event.DoesNotExist:
            messages.error(request, "Event not found.")
    return redirect('dashboard')


def delete_entre(request, event_id):
    if request.method == 'POST':
        try:
            event = Entrepreneur.objects.get(id=event_id, added_by_id=request.user.id)
            event.delete()
            messages.success(request, "Entrepreneur deleted successfully.")
        except Event.DoesNotExist:
            messages.error(request, "Event not found.")
    return redirect('entrepreneur_list')

from django.shortcuts import render, redirect
from .models import Event
from django.contrib.auth.decorators import login_required

@login_required
def event_list(request):
    # Filter only the events of the logged-in user
    events = Event.objects.filter(user=request.user)

    # Extract filter parameters
    title = request.GET.get('title')
    location = request.GET.get('location')

    # Apply filters
    if title:
        events = events.filter(title__icontains=title)
    if location:
        events = events.filter(location__icontains=location)

    events_count = events.count()

    # For dropdown: distinct location values
    locations = Event.objects.values_list('location', flat=True).distinct()

    context = {
        'events': events,
        'events_count': events_count,
        'location': locations,
        'title': title or '',
    }
    return render(request, 'event_list.html', context)

@login_required
def event_list_admin(request):
    # Filter only the events of the logged-in user
    events = Event.objects.filter(user=request.user, is_deleted=False).order_by('-date')

    # Extract filter parameters
    title = request.GET.get('title')
    location = request.GET.get('location')

    # Apply filters
    if title:
        events = events.filter(title__icontains=title)
    if location:
        events = events.filter(location__icontains=location)

    events_count = events.count()

    # For dropdown: distinct location values
    locations = Event.objects.values_list('location', flat=True).distinct()

    context = {
        'events': events,
        'events_count': events_count,
        'location': locations,
        'title': title or '',
    }
    return render(request, 'event_list_admin.html', context)




@login_required
def invite_member(request, event_id):
    

    selected_event = get_object_or_404(Event, id=event_id)
    events = Event.objects.all().order_by('-date')

    # Base QuerySet: exclude Admins
    members = NewUser.objects.exclude(user_type='Admin').exclude(id=request.user.id)


    # Extract filters from GET params
    marudar_place = request.GET.get('marudarplace')
    state = request.GET.get('state')
    city = request.GET.get('city')
    business_type = request.GET.get('business_type')

    # Apply filters if present
    if marudar_place:
        members = members.filter(marudar_place__icontains=marudar_place)
    if state:
        members = members.filter(state__icontains=state)
    if city:
        members = members.filter(city__icontains=city)
    if business_type:
        members = members.filter(business_type__iexact=business_type)

    # Populate filter dropdowns
    marudar_places = NewUser.objects.values_list('marudar_place', flat=True).distinct()
    states = NewUser.objects.values_list('state', flat=True).distinct()

    context = {
        'selected_event': selected_event,
        'events': events,
        'members': members,
        'marudar_places': marudar_places,
        'states': states,
        # For retaining search values in the template
        'selected_marudar_place': marudar_place or '',
        'selected_state': state or '',
        'selected_city': city or '',
        'selected_business_type': business_type or '',
    }

    return render(request, 'invite_member.html', context)

@login_required
def search_members_events(request, event_id):
    
    event = get_object_or_404(Event, id=event_id)

    members = NewUser.objects.exclude(user_type='Admin')

    # Filter params
    marudar_place = request.GET.get('marudarplace')
    state = request.GET.get('state')
    city = request.GET.get('city')
    business_type = request.GET.get('business_type')

    if marudar_place:
        members = members.filter(marudar_place__icontains=marudar_place)
    if state:
        members = members.filter(state__icontains=state)
    if city:
        members = members.filter(city__icontains=city)
    if business_type:
        members = members.filter(business_type__iexact=business_type)

    # For dropdowns
    marudar_places = NewUser.objects.values_list('marudar_place', flat=True).distinct()
    states = NewUser.objects.values_list('state', flat=True).distinct()

    context = {
        'members': members,
        'event': event,  # For showing event title etc.
        'events': event,  # If you used 'events' in template
        'marudar_places': marudar_places,
        'states': states,
        'marudar_place': marudar_place,
        'state': state,
        'city': city,
        'business_type': business_type,
    }

    return render(request, 'invite_member.html', context)

# adjust if models are in different places

@login_required
def send_invites(request, event_id):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('members')
        event = get_object_or_404(Event, id=event_id)

        if not selected_ids:
            messages.warning(request, "No members selected.")
            return redirect('invite_members', event_id=event.id)

        invited_members = NewUser.objects.filter(id__in=selected_ids)

        # Create or get Invite object
        invite, created = Invite.objects.get_or_create(
            user=request.user,
            event=event
        )
        invite.members.set(invited_members)
        invite.save()

        messages.success(request, f"Successfully invited {invited_members.count()} members to {event.title}.")
        return redirect('invite_member', event_id=event.id)

    return redirect('event_list')

from django.shortcuts import render, get_object_or_404
from .models import Invite, Event

@login_required
def invited_members_list(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    try:
        invite = Invite.objects.get(user=request.user, event=event)
        invited_members = invite.members.all()
    except Invite.DoesNotExist:
        invited_members = []

    return render(request, 'invited_members_list.html', {
        'event': event,
        'invited_members': invited_members
    })




def search_people(request):
    query = Q()
    marudarplace = request.GET.get("marudarplace")
    state = request.GET.get("state")
    city = request.GET.get("city")
    business_type = request.GET.get("business_type")


    if marudarplace:
        query &= Q(marudar_place__icontains=marudarplace)
    if state:
        query &= Q(state__icontains=state)
    if city:
        query &= Q(city__icontains=city)
    if business_type:
        query &= Q(business_type__icontains=business_type)

    pending_users = NewUser.objects.filter(query, is_active=False) if request.GET else []

    context = {
        "pending_users": pending_users,
        "pending_users_count": len(pending_users),
        "marudar_places": NewUser.objects.values_list('marudar_place', flat=True).distinct(),
        "states": NewUser.objects.values_list('state', flat=True).distinct(),
    }
    return render(request, 'search_people.html', context)


def delete_family_member(request, pk):
    member = get_object_or_404(FamilyMember, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, "Family member deleted successfully.")
        return redirect('dashboard')  # change this to the page you redirect after deletion

@login_required
def request_address_change(request):
    if request.method == 'POST':
        new_address = request.POST.get('new_address')
        user = request.user
        old_address = user.residential_address  # assuming address is a field in your User model

        AddressChangeRequest.objects.create(
            user=user,
            old_address=old_address,
            new_address=new_address,
        )
        messages.success(request, "Address change request submitted successfully.")
        return redirect('profile_view')  # or wherever appropriate

    return render(request, 'request_address_change.html')

@login_required
def request_address_change1(request):
    if request.method == 'POST':
        new_address = request.POST.get('new_address')
        field_name = request.POST.get('field_name')  # 'residential' or 'business'
        user = request.user
        old_address = user.business_address  # assuming address is a field in your User model

        AddressChangeRequest.objects.create(
            user=user,
            old_address=old_address,
            new_address=new_address,
            field_name=field_name,  # 'residential' or 'business'
        )
        messages.success(request, "Address change request submitted successfully.")
        return redirect('profile_view')  # or wherever appropriate

    return render(request, 'request_address_change1.html')
# views.py

def review_address_requests(request):
    requests = AddressChangeRequest.objects.all().order_by('-created_at')
    return render(request, 'review_requests.html', {'requests': requests})



def approve_request(request, req_id):
    req = get_object_or_404(AddressChangeRequest, id=req_id)
    req.status = 'approved'
    req.reviewed_at = timezone.now()
    req.save()

    user = req.user  # Use user reference for cleaner code

    if req.field_name == 'residential_address':
        user.residential_address = req.new_address
    elif req.field_name == 'business_address':
        user.business_address = req.new_address
    
    user.save()

    messages.success(request, "Request approved and address updated.")
    return redirect('review_requests')



def reject_request(request, req_id):
    req = get_object_or_404(AddressChangeRequest, id=req_id)
    req.status = 'rejected'
    req.reviewed_at = timezone.now()
    req.save()

    messages.info(request, "Request rejected.")
    return redirect('review_requests')

def manage_announcements(request):
    all_announcements = Announcement.objects.filter(is_deleted=False)

    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get("image")
        message = request.POST.get('message')

        Announcement.objects.create(
            user=request.user,
            title=title,
            image=image,
            message=message,
            )
        messages.info(request,"announcement created")
        return redirect('manage_announcements')
    return render(request,'manage_announcements.html',{'all_announcements': all_announcements})

@login_required
def delete_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id, is_deleted=False)


    announcement.is_deleted = True
    announcement.save()
    return redirect('manage_announcements')  # change this to your actual redirect view name