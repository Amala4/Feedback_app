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
    personal_question = models.CharField(max_length=200, default="What exactly do you like about me")
    business_question = models.CharField(max_length=200, default="Did my business serve you well, please let me know")
    purpose = models.CharField(max_length=50, choices=type_choices, default='private')


    class Meta:
        verbose_name_plural = "Messages"

    def __str__(self):
        return self.message




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False, help_text= "Checks if user has paid")
    total_response = models.IntegerField(default=0)
    personal_question = models.CharField(max_length=200, default="What exactly do you like about me")
    business_question = models.CharField(max_length=200, default="Did my business serve you well, please let me know")


    class Meta:
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.user.username



class WebStat(models.Model):

    homePage = models.IntegerField("Home Page views", default=0, editable = False)
    contact_admin = models.IntegerField("Contact admin views", default=0, editable = False)
    profile = models.IntegerField("profile", default=0, editable = False)
    privacy_policy = models.IntegerField("privacy policy views", default=0, editable = False)
    personal_quest_edit = models.IntegerField("Number of personal question edits", default=0, editable = False)
    personal_message_open = models.IntegerField("Number of personal messsage opens", default=0, editable = False)
    personal_message_post = models.IntegerField("Number of personal messsage posts", default=0, editable = False)
    business_quest_edit = models.IntegerField("Number of business question edits", default=0, editable = False)
    business_message_open = models.IntegerField("Number of business messsage opens", default=0, editable = False)
    business_message_post = models.IntegerField("Number of business messsage posts", default=0, editable = False)
    period = models.CharField(max_length=300,null=True, blank=True, editable = False)

    class Meta:
        verbose_name_plural = "Website Statistics"

    def __str__(self):
        return str(self.homePage)



