import random
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from .models import Profile, Message
from django.contrib import messages

# 1. BOSH SAHIFA
def home(request):
    return render(request, 'home.html')


# 2. RO'YXATDAN O'TISH
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu username band!")
            return redirect('signup')

        u = User.objects.create_user(username=username, email=email, password=password)

        code = str(random.randint(100000, 999999))

        # PROFILE YARATISH (MUHIM FIX)
        Profile.objects.create(user=u, verification_code=code)

        print(f"VERIFICATION CODE: {code}")

        send_mail(
            'EduSwap kod',
            f'Kod: {code}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=True,
        )

        request.session['u_id'] = u.id
        return redirect('verify')

    return render(request, 'signup.html')


# 3. VERIFY
def verify(request):
    if request.method == 'POST':
        try:
            u = User.objects.get(id=request.session['u_id'])

            if u.profile.verification_code == request.POST['code']:
                u.profile.is_verified = True
                u.profile.save()
                return redirect('login')
            else:
                return render(request, 'verify.html', {'error': 'Kod noto‘g‘ri'})

        except:
            return redirect('signup')

    return render(request, 'verify.html')


# 4. SEARCH
@login_required
def search(request):
    q = request.GET.get('q', '')
    res = Profile.objects.filter(teaches__icontains=q).exclude(user=request.user)
    return render(request, 'search.html', {'res': res, 'q': q})


# 5. EDIT PROFILE (ENG MUHIM FIX SHU YERDA)
@login_required
def edit_profile(request):
    # 🔥 PROFILE YO'Q BO'LSA YARATADI
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.teaches = request.POST.get('teaches')
        profile.learns = request.POST.get('learns')
        profile.save()

        messages.success(request, "Profil saqlandi!")
        return redirect('home')

    return render(request, 'edit_profile.html', {
        'profile': profile
    })


# 6. CHAT
@login_required
def chat(request, user_id):
    receiver = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        text = request.POST.get('text')
        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            text=text
        )
        return redirect('chat', user_id=user_id)

    messages_list = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) |
        Q(sender=receiver, receiver=request.user)
    ).order_by('created_at')

    return render(request, 'chat.html', {
        'receiver': receiver,
        'messages': messages_list
    })