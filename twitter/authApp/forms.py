from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user", "avatar"]

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'style': 'width: 350px'})
            self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
            self.fields['city'].widget.attrs.update({'class': 'form-control'})
            self.fields['country'].widget.attrs.update({'class': 'form-control'})