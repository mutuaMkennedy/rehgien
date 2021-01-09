from django import forms
from . import models

class JobPostForm(forms.ModelForm):
    project_size = forms.ChoiceField(required = False, choices =models.JobPost.PROJECT_SIZE, widget=forms.RadioSelect())
    project_duration = forms.ChoiceField(required = False, choices =models.JobPost.PROJECT_DURATION_CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = models.JobPost
        fields = '__all__'
        exclude = ["job_viewers","job_creation_date","job_update_date",
                    "job_poster"
                   ]
