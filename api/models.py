from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.username

class Message(models.Model):
    subject = models.CharField(max_length=100)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    #Cascade gör att när en user deletas, så deletas alla kopplade messages till det också
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject

class PreviousFetch(models.Model):
    time = models.DateTimeField()