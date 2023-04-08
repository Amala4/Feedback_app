from django.db import models
from django.contrib.auth.models import User



class Message(models.Model):
    type_choices = (
       ('private', 'private'),
       ('business', 'business')
    )


    message = models.TextField(editable = False)
    belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedbacks", editable = False)
    post_date = models.DateTimeField(auto_now_add=True)
    purpose = models.CharField(max_length=50, choices=type_choices, default='private')

    class Meta:
        verbose_name_plural = "Messages"

    def __str__(self):
        return self.message




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False, help_text= "Checks if user has paid")
    total_response = models.IntegerField(default=0)


    class Meta:
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.user.username
    
    




