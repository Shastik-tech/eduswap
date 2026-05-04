import random
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from .models import Profile, Message
from django.contrib import messages
from django.http import HttpResponse

# 1. BOSH SAHIFA
def home(request):
    return render(request, 'home.html')

# 2. RO'YXATDAN O'TISH (Professional HTML xat bilan)
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu username band!")
            return redirect('signup')

        u = User.objects.create_user(username=username, email=email, password=password)
        code = str(random.randint(100000, 999999))
        Profile.objects.create(user=u, verification_code=code)

        # CHIROYLI EMAIL YUBORISH
        subject = 'EduSwap | Tasdiqlash kodi'
        html_content = render_to_string('verify_email.html', {'code': code, 'username': username})
        text_content = strip_tags(html_content)

        try:
            msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except:
            pass

        request.session['u_id'] = u.id
        return redirect('verify')

    return render(request, 'signup.html')

# 3. VERIFY (OTP inputlar uchun moslangan)
def verify(request):
    if request.method == 'POST':
        try:
            u = User.objects.get(id=request.session.get('u_id'))
            user_code = request.POST.get('code') # JS yuborgan 6 xonali kod

            if u.profile.verification_code == user_code:
                u.profile.is_verified = True
                u.profile.save()
                return redirect('login')
            else:
                return render(request, 'verify.html', {'error': 'Kod noto‘g‘ri yoki muddati tugagan'})
        except:
            return redirect('signup')
    return render(request, 'verify.html')

# 4. ADMIN YARATISH (Faqat bir marta ishlatish uchun)
def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'shastik595@gmail.com', 'admin123')
        return HttpResponse("Admin yaratildi! Login: admin, Parol: admin123")
    return HttpResponse("Admin allaqachon bor.")

# 5. SEARCH, EDIT_PROFILE VA CHAT QISMLARI (O'zgarmadi)
@login_required
def search(request):
    q = request.GET.get('q', '')
    res = Profile.objects.filter(teaches__icontains=q).exclude(user=request.user)
    return render(request, 'search.html', {'res': res, 'q': q})

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.teaches = request.POST.get('teaches')
        profile.learns = request.POST.get('learns')
        profile.save()
        messages.success(request, "Profil saqlandi!")
        return redirect('home')
    return render(request, 'edit_profile.html', {'profile': profile})

@login_required
def chat(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        Message.objects.create(sender=request.user, receiver=receiver, text=text)
        return redirect('chat', user_id=user_id)
    
    messages_list = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user)
    ).order_by('created_at')
    return render(request, 'chat.html', {'receiver': receiver, 'messages': messages_list})
