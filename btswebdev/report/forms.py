from django import forms

from .models import Report


class ReportForm(forms.ModelForm):
	report_title = forms.CharField()

	class Meta:
		model = Report
		fields = [
			'report_title'
		]