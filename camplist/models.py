from datetime import date
# django
from django.conf import settings
from django.core.exceptions import ValidationError

# from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

# Create your models here.

class CampPrice(models.Model):
    duration_in_days = models.IntegerField()
    price_in_dollars = models.IntegerField(null=True)

    def __str__(self):
        return f'${self.price_in_dollars} for {self.duration_in_days} days'


class CampWeek(models.Model):
    week_num = models.IntegerField()
    date_start = models.DateField()
    date_end = models.DateField()

    class Meta:
        ordering = ['week_num']

    def __str__(self):
        return f'week #{ self.week_num } ({ self.date_start }  to  { self.date_end })'

    def check_start_end(self):
        if self.date_start >= self.date_end:
            raise ValidationError('Invalid dates.')
        return True

    def save(self, *args, **kwargs):
        if self.check_start_end():
            super().save(*args, **kwargs)

class CampTheme(models.Model):
    theme = models.CharField(max_length=200)
    field_trip = models.CharField(max_length=200)
    summary = models.TextField()
    week_date = models.OneToOneField(
        CampWeek,
        verbose_name='Week number and start date/end date',
        on_delete=models.CASCADE)
    price = models.ForeignKey(CampPrice, on_delete=models.CASCADE)

    class Meta:
        ordering = ['week_date']

    def __str__(self):
        return f'{self.theme} ({self.week_date})'

    def get_absolute_url(self):
        """Returns the url to access a detail for this camp."""
        return reverse('camp-detail', kwargs={'pk': self.pk})

    def next(self):
        # Returns the url of the camp the week after this.
        return reverse('camp-detail', args=[str(self.id + 1)])

    def previous(self):
        # Returns the url of the camp the week before this.
        return reverse('camp-detail', args=[str(self.id - 1)])


class Child(models.Model):
    first_name = models.CharField(max_length=64, blank=False)
    last_name = models.CharField(max_length=64, blank=False)
    dob = models.DateField(max_length=12, blank=False)
    grade_in_fall = models.CharField(max_length=1, blank=False)
    parent = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_query_name="parent",
                                related_name="children",)
    camps = models.ManyToManyField(CampTheme, blank=True, related_name="camper")

    class Meta:
        verbose_name_plural = "children"

    def __str__(self):
        return f'{self.first_name} {self.last_name} dob: {self.dob}'

    def get_absolute_url(self):
        return reverse('child-detail', args=[str(self.pk)])
        # args=[str(self.id)])


    def display_camps(self):
        # Create a string for Camps
        return ' | '.join([p.theme for p in self.camps.all()])
        display_camps.short_description = 'CampThemes'


    def total_price(self):
        # return aggregate([p.price for p in self.camps.all()])
        return sum([p.price.price_in_dollars for p in self.camps.all()])
        total_price.short_description = 'Dollars'
