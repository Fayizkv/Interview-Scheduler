from django.shortcuts import render, redirect
from .forms import CandidateForm, InterviewerForm, InterviewForm
from .models import Interview

def candidate_schedule(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hr_dashboard')
    else:
        form = CandidateForm()
    return render(request, 'candidate_schedule.html', {'form': form})

def interviewer_schedule(request):
    if request.method == 'POST':
        form = InterviewerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hr_dashboard')
    else:
        form = InterviewerForm()
    return render(request, 'interviewer_schedule.html', {'form': form})

def hr_dashboard(request):
    interviews = Interview.objects.all()
    return render(request, 'hr_dashboard.html', {'interviews': interviews})
