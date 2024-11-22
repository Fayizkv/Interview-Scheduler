from django import forms
from .models import Candidate, Interviewer, Interview

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'email']

class InterviewerForm(forms.ModelForm):
    class Meta:
        model = Interviewer
        fields = ['name', 'email']

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['candidate', 'interviewer', 'time_slot']
