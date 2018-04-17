from django import forms
from gundam_heaven.models import UserInfo



class FileUploadForm(forms.ModelForm):
    # file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    class Meta:
        model = UserInfo
        fields = ['photo']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class UserInfoChangeForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['nickname', 'age', 'sex']