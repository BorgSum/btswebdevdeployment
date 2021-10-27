from django import forms

from .models import Comment

# Creates a comment form with the one field that is formatted as a HTML textarea and sized here.
class RawCommentForm(forms.Form):
	comment_text = forms.CharField(widget=forms.Textarea(attrs={'rows':5, 'cols':80, 'class': "form-control", 'style': 'resize: none'}))
