from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from queue_app.models import CustomUser
from .models import Service
from .models import Booking

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'full_name', 'phone_number', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('full_name', 'phone_number', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('full_name', 'phone_number', 'profile_picture')}),
    )
    search_fields = ('username', 'email','full_name','queue_number','phone_number')
    ordering = ('username',)

class BookingAdmin(admin.ModelAdmin):
    list_display =  ('user','queue_number','date_time','service')
    search_fields = ('queue_number',)



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Service)
admin.site.register(Booking,BookingAdmin)

