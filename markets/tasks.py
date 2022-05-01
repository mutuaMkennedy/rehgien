from homey.celery import app
from celery.schedules import crontab
from contact import utils

@app.task(name="send_lead_notification")
def send_lead_notification(pro, service, client, email, phone, message):
    return utils.send_lead_support(pro, service, client, email, phone, message)