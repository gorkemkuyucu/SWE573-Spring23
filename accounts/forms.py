from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from .models import Profile


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email','password1','password2']
    terms_conditions = forms.BooleanField(required=True, label=mark_safe(("I have read and agree with the "
                                                      "<a href='terms_conditions'>Terms and Conditions</a>")), error_messages={'required': 'You must agree to the terms and conditions'})
#    is_verified = forms.BooleanField(default=False)


class UpdateProfileForm(forms.ModelForm):
#    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = Profile
        fields = ['about_me', 'profile_picture']

class ChangePasswordForm(PasswordChangeForm):
    pass

