from django import forms
from .models import UserProfile


class GuestForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('nric_number', 'name', 'mobile_number', 'company', 'photo', 'is_pdpa_checked')
