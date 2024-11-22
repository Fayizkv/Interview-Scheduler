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

def round_start_time(dt):
    """Round the start time upwards to the next available :00 or :30."""
    if dt.minute < 30:
        return dt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)  # Round up to next hour if less than 30
    else:
        return dt.replace(minute=30, second=0, microsecond=0)  # Round up to next :30 if 30 or more

def round_end_time(dt):
    """Round the end time downwards to the previous available :00 or :30."""
    if dt.minute < 30:
        return dt.replace(minute=0, second=0, microsecond=0)  # Round down to nearest hour if less than 30
    else:
        return dt.replace(minute=30, second=0, microsecond=0)  # Round down to nearest :30 if 30 or more

def hr_dashboard(request):
    context = {}
    if 'candidate_id' in request.GET and 'interviewer_id' in request.GET:
        candidate_id = request.GET['candidate_id']
        interviewer_id = request.GET['interviewer_id']

        candidate_slots = Availability.objects.filter(user_type="Candidate", user_id=candidate_id)
        interviewer_slots = Availability.objects.filter(user_type="Interviewer", user_id=interviewer_id)

        possible_slots = []
        added_slots = set()  # To keep track of added slots

        for c_slot in candidate_slots:
            for i_slot in interviewer_slots:
                if c_slot.date == i_slot.date:
                    candidate_start = datetime.combine(c_slot.date, c_slot.start_time)
                    candidate_end = datetime.combine(c_slot.date, c_slot.end_time)
                    interviewer_start = datetime.combine(i_slot.date, i_slot.start_time)
                    interviewer_end = datetime.combine(i_slot.date, i_slot.end_time)

                    # Round the times
                    candidate_start = round_start_time(candidate_start)
                    candidate_end = round_end_time(candidate_end)
                    interviewer_start = round_start_time(interviewer_start)
                    interviewer_end = round_end_time(interviewer_end)

                    # Get the start and end times for both candidate and interviewer (after rounding)
                    overlap_start = max(candidate_start, interviewer_start)
                    overlap_end = min(candidate_end, interviewer_end)

                    # Generate 30-minute slots between the rounded start and end times
                    candidate_slots = []
                    interviewer_slots = []

                    # Add 30-minute intervals from candidate start to candidate end
                    while overlap_start < candidate_end:
                        candidate_slots.append(overlap_start.time())
                        overlap_start += timedelta(minutes=30)

                    # Reset overlap_start for interviewer and generate slots for interviewer
                    overlap_start = max(candidate_start, interviewer_start)
                    while overlap_start < interviewer_end:
                        interviewer_slots.append(overlap_start.time())
                        overlap_start += timedelta(minutes=30)

                    # Find the intersection of available slots between candidate and interviewer
                    common_slots = set(candidate_slots) & set(interviewer_slots)

                    # Add the common slots to possible_slots if they are not already in added_slots
                    for slot in common_slots:
                        if slot not in added_slots:
                            possible_slots.append(slot)
                            added_slots.add(slot)

        context['possible_slots'] = sorted(possible_slots)

    context['candidates'] = Candidate.objects.all()
    context['interviewers'] = Interviewer.objects.all()
    return render(request, 'hr.html', context)

def round_start_time(dt):
    """Round the start time upwards to the next :30 or :00"""
    if dt.minute < 30:
        return dt.replace(minute=30, second=0, microsecond=0)
    else:
        return dt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1) 

def round_end_time(dt):
    """Round the end time downwards to the previous :00 or :30"""
    if dt.minute < 30:
        return dt.replace(minute=0, second=0, microsecond=0)  
    else:
        return dt.replace(minute=30, second=0, microsecond=0)  

def hr_dashboard(request):
    context = {}
    if 'candidate_id' in request.GET and 'interviewer_id' in request.GET:
        candidate_id = request.GET['candidate_id']
        interviewer_id = request.GET['interviewer_id']

        candidate_slots = Availability.objects.filter(user_type="Candidate", user_id=candidate_id)
        interviewer_slots = Availability.objects.filter(user_type="Interviewer", user_id=interviewer_id)

        possible_slots = []
        added_slots = set() 

        for c_slot in candidate_slots:
            for i_slot in interviewer_slots:
                if c_slot.date == i_slot.date:
                    candidate_start = datetime.combine(c_slot.date, c_slot.start_time)
                    candidate_end = datetime.combine(c_slot.date, c_slot.end_time)
                    interviewer_start = datetime.combine(i_slot.date, i_slot.start_time)
                    interviewer_end = datetime.combine(i_slot.date, i_slot.end_time)

                    candidate_start = round_start_time(candidate_start)
                    candidate_end = round_end_time(candidate_end)
                    interviewer_start = round_start_time(interviewer_start)
                    interviewer_end = round_end_time(interviewer_end)


                    overlap_start = max(candidate_start, interviewer_start)
                    overlap_end = min(candidate_end, interviewer_end)

                    current_time = overlap_start
                    while current_time + timedelta(hours=1) <= overlap_end:
                        start_time = current_time.time()
                        end_time = (current_time + timedelta(hours=1)).time()


                        if (start_time, end_time) not in added_slots:
                            possible_slots.append((start_time, end_time))
                            added_slots.add((start_time, end_time))

                        current_time += timedelta(minutes=30)

        context['possible_slots'] = possible_slots

    context['candidates'] = Candidate.objects.all()
    context['interviewers'] = Interviewer.objects.all()
    return render(request, 'hr.html', context)
