from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.utils.translation import ugettext
from django.http import HttpResponseRedirect
from .models import Job, validate_time, suggest_timeslot
from .forms import JobForm
from .utils import roundup, convert_time_from_int_to_str 

WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def scheduler(request):
    jobs = Job.objects.all()
    job_array = [{} for i in range(7)]

    for job in jobs:
        weekday = job.weekday
        start_time = job.start_time
        job_array[weekday][start_time] = {'duration': job.duration, 'title': str(job.title), 'location': str(job.location)}

    return render(request, "scheduler/scheduler.html", {'job_array': job_array})

def add_job(request):
    if request.method == 'POST':
        jform = JobForm(request.POST)

        if jform.is_valid():
            job_data = jform.cleaned_data
            start_time = job_data['start_time']
            duration = roundup(job_data['duration'])
            weekday = job_data['weekday']

            if validate_time(start_time, duration, weekday):
                job = jform.save()
                messages.add_message(request, messages.INFO, ugettext('Job added successfully.'))
                return HttpResponseRedirect("/")
            else:
                suggested_timeslots = suggest_timeslot(duration)
                messages.add_message(request, messages.INFO, ugettext('You are not free at this timeslot.'))
                if len(suggested_timeslots) == 0:
                    messages.add_message(request, messages.INFO, ugettext('There is no available timeslot for the job duration.'))
                else:
                    timeslot_messages = []
                    for timeslot in suggested_timeslots:
                        timestot_start_time = convert_time_from_int_to_str(timeslot['start_time'])
                        timeslot_weekday = timeslot['weekday']
                        timeslot_messages.append('%s (Start time: %s)' %(WEEKDAYS[timeslot_weekday], timestot_start_time))
                    timeslot_messages = ', '.join(timeslot_messages)
                    messages.add_message(request, messages.INFO, ugettext("Suggested timeslots: " + timeslot_messages))
    else:
        jform = JobForm()
    
    return render(request, 'scheduler/add_job.html', {'jform': jform})