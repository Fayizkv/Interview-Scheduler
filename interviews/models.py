from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Interviewer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Availability(models.Model):
    user_type = models.CharField(max_length=20)  # "Candidate" or "Interviewer"
    user_id = models.IntegerField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.user_type} {self.user_id}: {self.date} {self.start_time}-{self.end_time}"
