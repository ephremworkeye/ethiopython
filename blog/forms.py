from django import forms
from .models import Comment


class PostEmailShareForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=250)
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    message = forms.CharField(required=False, widget=forms.Textarea)
