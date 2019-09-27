from django.contrib import admin
# django
from camplist.models import CampWeek, CampTheme, CampPrice, Child

# Register your models here.

@admin.register(CampWeek)
class CampWeekAdmin(admin.ModelAdmin):
    pass

class ChildInline(admin.StackedInline):
    model = Child.camps.through
    extra = 1

@admin.register(CampTheme)
class CampThemeAdmin(admin.ModelAdmin):
    list_display = ('theme', 'week_date', 'field_trip')
    inlines=[ChildInline]

admin.site.register(CampPrice)


class ChildAdmin(admin.ModelAdmin):
    list_display=('first_name', 'last_name', 'dob', 'grade_in_fall', 'parent', 'display_camps')
    fields = ['first_name', 'last_name', 'dob', 'grade_in_fall', 'parent', 'camps']
    filter_horizontal=("camps",)

admin.site.register(Child, ChildAdmin)
