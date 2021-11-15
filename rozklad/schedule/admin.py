from django.contrib import admin
from django import forms
from django.db.models.query import QuerySet
from .models import *
# Register your models here.

class ScheduleForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset= User.objects.filter(profile__role = 'teacher'))



class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'group')
    list_display_links = ()

class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    
    class Meta:
        verbose_name = 'ueaf'


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'hours_lecture', 'hours_practical')

class AudienceAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'count_places')


class ScheduleAdmin(admin.ModelAdmin):
    form = ScheduleForm
    list_display = ('start_date', 'end_date','subject', 'group', 'audience', 'teacher')
    class Meta:
        verbose_name = "розкладів"

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Audience, AudienceAdmin)
admin.site.register(Schedule, ScheduleAdmin)