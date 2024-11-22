from django.shortcuts import render, redirect
from .models import Candidate, Interviewer, Interview
from .forms import CandidateForm, InterviewerForm

# Index Page
def index(request):
    return render(request, 'scheduler/index.html')

# Candidate View
def candidate_view(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CandidateForm()
    return render(request, 'scheduler/candidate_schedule.html', {'form': form})

# Interviewer View
def interviewer_view(request):
    if request.method == 'POST':
        form = InterviewerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = InterviewerForm()
    return render(request, 'scheduler/interviewer_schedule.html', {'form': form})

# HR Dashboard
def hr_dashboard(request):
    candidates = Candidate.objects.filter(is_scheduled=False)
    interviewers = Interviewer.objects.filter(is_scheduled=False)
    interviews = Interview.objects.all()

    if request.method == 'POST' and 'schedule' in request.POST:
        candidate_id = request.POST.get('candidate_id')
        interviewer_id = request.POST.get('interviewer_id')
        candidate = Candidate.objects.get(id=candidate_id)
        interviewer = Interviewer.objects.get(id=interviewer_id)
        
        # Schedule the interview
        interview = Interview.objects.create(
            candidate=candidate,
            interviewer=interviewer,
            scheduled_date=candidate.available_date,
            scheduled_time=candidate.available_time,
        )
        candidate.is_scheduled = True
        interviewer.is_scheduled = True
        candidate.save()
        interviewer.save()

    return render(request, 'scheduler/hr_dashboard.html', {
        'candidates': candidates,
        'interviewers': interviewers,
        'interviews': interviews,
    })
