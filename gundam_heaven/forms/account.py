from django import forms
from gundam_heaven.models import UserInfo

from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='this email will be used for password reset, please input an valid one.')

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email')


class FileUploadForm(forms.ModelForm):
    # file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    class Meta:
        model = UserInfo
        fields = ['photo']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

# class UserInfoChangeForm(forms.Form):
#     nickname = forms.CharField(max_length=150)
#     age = forms.IntegerField(min_value=17)
#     sex = forms.ChoiceField(widget=forms.RadioSelect(), choices=SEX_CHOICES)
#     email = forms.EmailField()