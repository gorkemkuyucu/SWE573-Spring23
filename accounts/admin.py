from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile

# Register your models here.

#Unregister Groups
admin.site.unregister(Group)

class ProfileInLine(admin.StackedInline):
    model = Profile

#Change user model to show wanted fields (imports from modeladmin) + add profile inline with admin user page
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username","first_name", "last_name", "email","date_joined"]
    inlines = [ProfileInLine]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)
#admin.site.register(Profile)  //profiller user içine konduğu için gerek yok





