from django import forms

from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}


class ContactUsForm(forms.Form):
    user_email = forms.EmailField(label='Input your e-mail')
    user_subject = forms.CharField(label='Subject')
    user_message = forms.CharField(label='Input you message', widget=forms.Textarea)