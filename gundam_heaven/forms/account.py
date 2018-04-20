from django import forms
from gundam_heaven.models import UserInfo, SEX_CHOICES



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