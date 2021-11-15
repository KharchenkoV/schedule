from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, PROTECT
from datetime import timedelta
from django.db.models import Q
# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=10, verbose_name='назва')

    class Meta:
        verbose_name = 'група'
        verbose_name_plural = 'групи'

    def __str__(self):
        return self.name
        



class UserProfile(models.Model):
    ROLES = (
        ('student', 'Студент'),
        ('teacher', 'Викладач'),
    )
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, verbose_name='користувач')
    role = models.CharField(max_length=10, choices=ROLES, verbose_name='роль')
    group = models.ForeignKey(Group, on_delete=CASCADE, verbose_name='група', null=True, default=None, blank=True)

    class Meta:
        verbose_name_plural = 'профілі'
        verbose_name = 'profile'


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name='назва')
    hours_lecture = models.IntegerField(verbose_name='лекційні години')
    hours_practical = models.IntegerField(verbose_name='години практики')

    class Meta:
        verbose_name_plural = 'предмети'
        verbose_name = 'предмет'

    def __str__(self):
        return self.name


class Audience(models.Model):
    TYPE = (
        ('л', 'лекційна'),
        ('п', 'практична'),
    )
    room_number = models.IntegerField(verbose_name='номер')
    room_type = models.CharField(max_length=10, choices=TYPE, default='л', verbose_name='вид')
    count_places = models.IntegerField(verbose_name='кількість місць')

    class Meta:
        verbose_name_plural = 'аудиторії'
        verbose_name = 'аудиторія'

    def __str__(self):
        return str(self.room_number)


class Schedule(models.Model):
    subject = models.ForeignKey(Subject, on_delete=PROTECT, verbose_name='предмет')
    audience = models.ForeignKey(Audience, on_delete=PROTECT, verbose_name='аудиторія')
    group = models.ForeignKey(Group, on_delete=PROTECT, verbose_name='група')
    teacher = models.ForeignKey(User, on_delete=PROTECT, verbose_name='викладач')
    start_date = models.DateTimeField(verbose_name='початок пари')
    end_date = models.DateTimeField(verbose_name='кінець пари', editable=False, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'розклад'
        verbose_name = 'розклад'

    def clean(self):
        start = self.start_date
        end = start + timedelta(hours=1, minutes=20)
        cond1 = Q(end_date__range=(start, end)) | Q(start_date__range=(start, end))
        cond2 = Q(audience=self.audience) | Q(group=self.group) | Q(teacher=self.teacher)
        check = Schedule.objects.filter(cond1 & cond2).exists()
        if check:
            raise ValidationError('В даний час у викладача, групи або в аудиторії проходить пара')
            

    def save(self, *args, **kwargs):
        self.end_date = self.start_date + timedelta(hours=1, minutes=20)
        super(Schedule, self).save(*args, **kwargs)
        