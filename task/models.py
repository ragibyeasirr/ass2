from django.db import models
from django.contrib.auth.models import User
class category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)

    time = models.TimeField()
   
    category = models.ForeignKey(category, on_delete=models.CASCADE, related_name="event")
    image= models.ImageField(upload_to='event',  blank=True, null=True,
                              default="event/default.jpg")
    participent= models.ManyToManyField(
        User,
        related_name="rsvped_events",
        blank=True
    )

    def __str__(self):
        return self.name


   