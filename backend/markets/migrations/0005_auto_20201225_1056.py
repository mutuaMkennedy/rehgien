# Generated by Django 2.2.12 on 2020-12-25 07:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('markets', '0004_auto_20201224_0104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agentpropertyrequest',
            name='claimer',
        ),
        migrations.RemoveField(
            model_name='agentpropertyrequest',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='agentpropertyrequest',
            name='referrer',
        ),
        migrations.RemoveField(
            model_name='otherservicelead',
            name='claimer',
        ),
        migrations.RemoveField(
            model_name='otherservicelead',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='otherservicelead',
            name='referrer',
        ),
        migrations.RemoveField(
            model_name='proffesionalrequestlead',
            name='claimer',
        ),
        migrations.RemoveField(
            model_name='proffesionalrequestlead',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='proffesionalrequestlead',
            name='referrer',
        ),
        migrations.RemoveField(
            model_name='propertyrequestlead',
            name='claimer',
        ),
        migrations.RemoveField(
            model_name='propertyrequestlead',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='propertyrequestlead',
            name='referrer',
        ),
        migrations.AddField(
            model_name='jobpostproposal',
            name='proposal_sender',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_post_responder', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='jobpostproposal',
            name='job_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_post_proposal', to='markets.JobPost'),
        ),
        migrations.DeleteModel(
            name='AgentLeadRequest',
        ),
        migrations.DeleteModel(
            name='AgentPropertyRequest',
        ),
        migrations.DeleteModel(
            name='OtherServiceLead',
        ),
        migrations.DeleteModel(
            name='ProffesionalRequestLead',
        ),
        migrations.DeleteModel(
            name='PropertyRequestLead',
        ),
    ]