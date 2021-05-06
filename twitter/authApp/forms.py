from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    city = forms.CharField(required=False)
    country = forms.CharField(required=False)

    class Meta:
        model = Profile
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update(
            {
                "class": "form-control",
                "style": "max-width: 350px, margin-top: 20px",
                "autofocus": '""',
            }
        )
        self.fields["last_name"].widget.attrs.update({"class": "form-control"})
        self.fields["city"].widget.attrs.update({"class": "form-control"})
        self.fields["country"].widget.attrs.update({"class": "form-control"})
