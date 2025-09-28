from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from task.models import event 
from django.conf import settings

@receiver(m2m_changed, sender=event.participent.through)
def revp_mail(sender, instance, action, **kwargs):
    if action == 'post_add':
       

        assigned_emails = [emp.email for emp in instance.participent.all()]
        

        send_mail(
            "New event Assigned",
            f"You have been rsvp to the event: {instance.name}",
             settings.EMAIL_HOST_USER,
            assigned_emails,
            fail_silently=False,
        )