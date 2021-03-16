from homey.celery import app
from celery.schedules import crontab
from contact import views as contact_views

@app.task(name="send_connection_request_email")
def send_connection_request_email(requestor_business_profile_pk, receiver_business_profile_pk):
    return contact_views.request_team_connection(requestor_business_profile_pk, receiver_business_profile_pk)

@app.task(name="send_connection_accepted_email")
def send_connection_accepted_email(requestor_business_profile_pk, receiver_business_profile_pk):
    return contact_views.team_connection_request_acccepted(requestor_business_profile_pk, receiver_business_profile_pk)

@app.task(name="send_pro_profile_completion_progress_message")
def send_pro_profile_completion_progress_message():
    return contact_views.send_pro_profile_completion_progress()
