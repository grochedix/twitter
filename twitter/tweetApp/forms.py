from django import forms

from .models import Tweet


class TweetForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    content = forms.CharField(required=True, max_length=280, widget=forms.Textarea)

    class Meta:
        model = Tweet
        fields = ["content", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget.attrs.update(
            {
                "class": "form-control",
                "rows": "3",
                "style": "max-width: 450px; margin-top:5px",
                "autofocus": '""',
                "placeholder": "What's going on?",
            }
        )
        self.fields["image"].widget.attrs.update(
            {
                "class": "form-control",
                "style": "max-width: 350px; margin-top:10px;",
            }
        )
