from django import forms
from .models import Candidate, Interviewer

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'mobile', 'email', 'available_date', 'available_time']

class InterviewerForm(forms.ModelForm):
    class Meta:
        model = Interviewer
        fields = ['name', 'mobile', 'email', 'available_date', 'available_time']
