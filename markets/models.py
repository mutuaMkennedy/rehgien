from django.db import models
from django.contrib.gis.db import models
from django.conf import settings
from django.urls import reverse
from multiselectfield import MultiSelectField
from django.contrib.postgres.fields import ArrayField
from django.utils.safestring import mark_safe
from profiles import models as profile_models
from location import models as location_models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from notifications.signals import notify
from app_notifications import push_notifications, models as app_ntf_models

User = get_user_model()


# Request are published as leads
class JobPost(models.Model):
    PROJECT_SIZE = (
        ('LARGE',mark_safe(
            u'<span>Large</span> <small>Mostly a longer term activity with a series of complex multiple requirements.' +
            '<br>Example: Designing and building a house. </small>'
            )
        ),
        ('MEDIUM',mark_safe(
            u'<span>Medium</span><small> A moderately complex activity with a well defined time frame.' +
            '<br>Example: Home value assessment. </small>'
            )
        ),
        ('SMALL',mark_safe(
            u'<span>Small</span> <small>A relatively quick activity with less complex steps which can ussually be done in a small time frame.' +
            '<br>Examples: Cleaning service, Moving service etc. </small>'
            )
        ),
    )
    PROJECT_DURATION_CHOICES = (
        ('1', mark_safe(u'<span>less than a week</span>')),
        ('2', mark_safe(u'<span>less than 1 month</span>')),
        ('3', mark_safe(u'<span>1 to 3 months</span>')),
        ('4', mark_safe(u'<span>3 to 6 months</span>')),
        ('5', mark_safe(u'<span>more than 6 months</span>')),
    )

    title = models.CharField(max_length = 100, blank=False )
    description = models.TextField(blank = False)
    project_size = models.CharField(max_length = 20, choices = PROJECT_SIZE , blank = False)
    project_duration =  models.CharField(max_length = 20, choices = PROJECT_DURATION_CHOICES , blank = False)
    skill_areas = ArrayField(models.CharField(max_length=100, blank=True),blank=True, null=True)
    verified = models.BooleanField(default = False)
    active = models.BooleanField(default=True)
    location = ArrayField(models.CharField(max_length=100, blank=True),blank=True, null=True)
    job_viewers = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='job_viewer', blank=True)
    job_creation_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    job_update_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    job_poster = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='job_poster', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'JobPosts'

    def get_absolute_url(self):
        return reverse( 'rehgien_pro:job_detail', kwargs={'pk':self.pk})

class JobPostProposal(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='job_post_proposal', null=True, blank=True)
    message = models.TextField()
    proposal_sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='job_post_responder', on_delete=models.CASCADE, default=None, null=True)
    proposal_send_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'JobPostProposals'

"""
A project is a job that is submitted by a client to a specific service
provider who then gets to respond with a project quote or reject the job.
"""
class Project(models.Model):
    RESPONSE_STATE = (
    ('ACCEPTED', 'accepted'),
    ('PENDING', 'pending'),
    ('REJECTED','rejected')
    )
    PROJECT_STATE = (
    ('ACTIVE', 'active'),
    ('COMPLETED', 'completed'),
    ('CANCELLED','cancelled')
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='project_owner', on_delete=models.CASCADE, default=None, null=True)
    client_message = models.TextField()
    requested_service = models.ForeignKey(profile_models.ProfessionalService, on_delete=models.SET_NULL,\
                default = None, related_name='project_service', null =True, blank=True)
    project_status = models.CharField(choices=PROJECT_STATE, default='ACTIVE', null=True, max_length=20)
    # Check should be made to ensure on users who are pros can respond
    pro_contacted =  models.ForeignKey(settings.AUTH_USER_MODEL, related_name='project_contacted_pro', on_delete=models.CASCADE, default=None, null=True)
    pro_response_state = models.CharField(choices=RESPONSE_STATE, default='PENDING', null=True, max_length=20)
    publishdate = models.DateTimeField(auto_now=False, auto_now_add=True)

    __original_pro_reponse = None
    __original_project_status = None

    def __str__(self):
        return (self.requested_service.service_name if self.requested_service.service_name else "") + " " + self.pro_response_state

    class Meta:
        verbose_name_plural = 'Project'

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        self.__original_pro_reponse = self.pro_response_state
        self.__original_project_status = self.project_status

   
# A new project is treated as a lead that professionals can engage with
# TO DO: decouple code using helper function
def new_lead_notification(sender, instance, created, **kwargs):
    recipient = instance.pro_contacted
    recipient_name = recipient.pro_business_profile.business_name if recipient.pro_business_profile else 'there'
    service_name = instance.requested_service.service_name
    user = User.objects.get(pk=instance.owner.pk)
    # check if pro response state field has been updated
    if instance._Project__original_pro_reponse != instance.pro_response_state:
        """
        Field has been updated, so, now check if status has been 
        updated to rejected and send a notification to the sender.
        """            
        notification_created = False
        if instance.pro_response_state == "REJECTED":
            try:
                # save the notification to the notification model
                notify.send(instance, recipient=user,
                            verb=f'{recipient_name} is currently unavailable to take on your project. Please look for a different service provider.',
                            target = instance,
                            type = 'Project'
                            )
                notification_created = True
            except Exception as e:
                print(f'Something went wrong! Notification not sent {e}')

        if notification_created:
            # send push notification to user's device
            try:
                devices = user.user_device.all()

                # Using expo push notification SDK
                if devices:
                    for dvc in devices:
                        if dvc.expo_token:
                            push_notifications.send_push_message(
                                        token = dvc.expo_token,
                                        title = f'{service_name} project update.',
                                        message = f'{recipient_name} is currently unavailable to take on your project. Please look for a different service provider.',
                                        extra = {'type':'Project','target':instance.pk},
                                        )
            except:
                print('Something went wrong!')

    # check if project status has been updated
    if instance._Project__original_project_status != instance.project_status:
        """
        An update has occured so check what type of update this is and send the
        right notification message
        """
        notification_title = ''
        if instance.project_status == 'ACTIVE':
            notification_title = f'Hi {recipient_name}, you have a new lead.'
            notification_body = f'You\'ve got a new job for your {service_name} service.'
        if instance.project_status == 'COMPLETED':
            notification_title = f'{service_name} project update.'
            notification_body = 'This project has been marked as complete by the owner.'
        if instance.project_status == 'CANCELLED':
            notification_title = f'{service_name} project update.'
            notification_body = 'This project has been cancelled by the owner.'

        sent = False
        try:
            notify.send(instance, recipient=recipient,
                        verb=notification_title,
                        target = instance,
                        type = 'Project lead'
                        )
            sent = True
        except:
            pass
        if sent:
            try:
                devices = recipient.user_device.all()
                # Using expo push notification SDK
                if devices:
                    for dvc in devices:
                        if dvc.expo_token:
                            push_notifications.send_push_message(
                                        token = dvc.expo_token,
                                        title = notification_title,
                                        message = notification_body,
                                        extra = {'type':'Project lead','target':instance.pk},
                                        )
                else:
                    print("No device found")
            except Exception as e:
                print(f'Something went wrong! Notification not sent {e}')
    else:
        """It's a new projec so send new lead notification by default"""
        sent = False
        try:
            notify.send(instance, recipient=recipient,
                        verb=f'Hi {recipient_name}, you have a new lead.',
                        target = instance,
                        type = 'Project lead'
                        )
            sent = True
        except:
            pass
        if sent:
            try:
                devices = recipient.user_device.all()
                # Using expo push notification SDK
                if devices:
                    for dvc in devices:
                        if dvc.expo_token:
                            push_notifications.send_push_message(
                                        token = dvc.expo_token,
                                        title = f'Hi {recipient_name}, you have a new lead.',
                                        message = f'You\'ve got a new job for your {service_name} service.',
                                        extra = {'type':'Project lead','target':instance.pk},
                                        )
                else:
                    print("No device found")
            except Exception as e:
                print(f'Something went wrong! Notification not sent {e}')

post_save.connect(new_lead_notification, sender=Project)

# Project details allow the client to state the specifics of the type of job they have
class ProjectDetails(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_details', null=True, blank=True)
    location = models.ForeignKey(location_models.KenyaTown, blank = False, \
                on_delete=models.SET_NULL, null=True, related_name='location_of_project')

    def __str__(self):
        return self.project.requested_service.service_name

    class Meta:
        verbose_name_plural = 'Project Details'

class ProjectQuestion(models.Model):
    project_details = models.ForeignKey(ProjectDetails, on_delete=models.CASCADE, \
                related_name='project_questions', null=True, blank=True)
    question = models.ForeignKey(profile_models.Question, on_delete=models.CASCADE,\
                default = None, related_name='project_question')
    answer = models.ManyToManyField(profile_models.QuestionOptions, blank=True, \
                related_name='project_question_answer')

    class Meta:
        verbose_name_plural = 'Project Questions'

# The contacted service provider is the one who gets to respond to the job by sending a quote
class ProjectQuote(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_quote', null=True, blank=True)
    message = models.TextField()
    price = models.PositiveIntegerField(default=0)
    negotiable = models.BooleanField(default=False, null=True, blank=True)
    quote_sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='project_quote_sender', on_delete=models.SET_NULL, default=None, null=True)
    quote_send_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Project Quote'

    def __str__(self):
        return self.project.requested_service.service_name

def project_quote_sent_notification(sender, instance, created, **kwargs):
    user = User.objects.get(pk=instance.project.owner.pk)
    quote_sender = instance.quote_sender.pro_business_profile.business_name if instance.quote_sender.pro_business_profile else instance.quote_sender.username
    service_name = instance.project.requested_service.service_name
    sent = False
    try:
        notify.send(instance, recipient=user,
                    verb=f'{quote_sender} sent you a quote',
                    target = instance.project,
                    type = 'Project'
                    )
        sent = True
    except:
        pass
    if sent:
        try:
            devices = user.user_device.all()

            # Using expo push notification SDK
            if devices:
                for dvc in devices:
                    if dvc.expo_token:
                        push_notifications.send_push_message(
                                    token = dvc.expo_token,
                                    title = f'{quote_sender} sent you a quote',
                                    message = instance.message,
                                    extra = {'type':'Project','target':instance.project.pk},
                                    )
        except:
            print('Something went wrong!')

post_save.connect(project_quote_sent_notification, sender=ProjectQuote)

"""
Project models end here
"""
