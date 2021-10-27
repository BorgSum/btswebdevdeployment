from django import forms

from .models import Entry, EntryImage

#class RawEntryForm(forms.Form):
#	entry_title = forms.CharField()
#	entry_content = forms.CharField()

class EntryForm(forms.ModelForm):
	entry_title = forms.CharField(widget=forms.Textarea(attrs={'rows':1,'class': "form-control", 'style': 'resize: none'}))
	entry_content = forms.CharField(widget=forms.Textarea(attrs={'rows':5, 'cols':80, 'class': "form-control", 'style': 'resize: none'}))
	class Meta:
		model = Entry
		fields = [
			'entry_title',
			'entry_content'
		]

class EntryImageForm(forms.ModelForm):
	entry_image_file = widget=forms.ClearableFileInput(attrs={'multiple': True})
	class Meta:
		model = EntryImage
		fields = [
			'entry_image_file',
			'entry_image_desc'
		]


# 