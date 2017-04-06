from __future__ import absolute_import
from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('end_time', 'created_at')
