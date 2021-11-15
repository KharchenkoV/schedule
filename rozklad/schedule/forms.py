from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Group, UserProfile


class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('teacher', 'Викладач'),
    ]
    GROUP_CHICES = [('','-')]
    for g in Group.objects.all():
        temp = (g.name, g.name)
        GROUP_CHICES.append(temp)
    role = forms.CharField(widget=forms.RadioSelect(choices=ROLE_CHOICES), label='Виберіть студент ви чи викладач')
    group = forms.ChoiceField(choices=GROUP_CHICES, label='Якщо ви студент виберіть групу')

    def save(self, commit=True):
        instance = super().save(commit=True)
        if (self.cleaned_data['role'] == 'student'):
            temp = Group.objects.get(name=self.cleaned_data['group'])
            profile = UserProfile(user=instance, role=self.cleaned_data['role'], group=temp)
        else:
            profile = UserProfile(user=instance, role=self.cleaned_data['role'])
        profile.save()
        return instance 