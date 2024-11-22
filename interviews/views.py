from django.shortcuts import render, redirect
from .models import Candidate, Interviewer, Availability
from datetime import datetime, timedelta

def index(request):
    return render(request, 'index.html')

def availability_register(request):
    if request.method == "POST":
        user_type = request.POST['user_type']
        user_id = request.POST['user_id']
        date = request.POST['date']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        Availability.objects.create(
            user_type=user_type,
            user_id=user_id,
            date=date,
            start_time=start_time,
            end_time=end_time
        )
        return redirect('availability')
    return render(request, 'availability.html', {
        'candidates': Candidate.objects.all(),
        'interviewers': Interviewer.objects.all(),
    })

def hr_dashboard(request):
    context = {}
    if 'candidate_id' in request.GET and 'interviewer_id' in request.GET:
        candidate_id = request.GET['candidate_id']
        interviewer_id = request.GET['interviewer_id']

        candidate_slots = Availability.objects.filter(user_type="Candidate", user_id=candidate_id)
        interviewer_slots = Availability.objects.filter(user_type="Interviewer", user_id=interviewer_id)

        possible_slots = []

        for c_slot in candidate_slots:
            for i_slot in interviewer_slots:
                if c_slot.date == i_slot.date:
                    candidate_start = datetime.combine(c_slot.date, c_slot.start_time)
                    candidate_end = datetime.combine(c_slot.date, c_slot.end_time)
                    interviewer_start = datetime.combine(i_slot.date, i_slot.start_time)
                    interviewer_end = datetime.combine(i_slot.date, i_slot.end_time)

                    overlap_start = max(candidate_start, interviewer_start)
                    overlap_end = min(candidate_end, interviewer_end)

                    while overlap_start + timedelta(hours=1) <= overlap_end:
                        possible_slots.append((overlap_start.time(), (overlap_start + timedelta(hours=1)).time()))
                        overlap_start += timedelta(hours=1)

        context['possible_slots'] = possible_slots

    context['candidates'] = Candidate.objects.all()
    context['interviewers'] = Interviewer.objects.all()
    return render(request, 'hr.html', context)
