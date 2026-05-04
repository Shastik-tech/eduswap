from django.contrib import admin
from .models import Profile, Message

# Profilni admin panelda ko'rsatish
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'teaches', 'learns', 'rating', 'is_verified')
    list_editable = ('is_verified', 'rating') # To'g'ridan-to'g'ri o'zgartirish
    search_fields = ('user__username', 'teaches')

# Xabarlarni admin panelda ko'rsatish
admin.site.register(Message)
