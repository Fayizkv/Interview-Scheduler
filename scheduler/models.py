from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    available_date = models.DateField()
    available_time = models.TimeField()
    is_scheduled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.available_date} at {self.available_time}"

class Interviewer(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    available_date = models.DateField()
    available_time = models.TimeField()
    is_scheduled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.available_date} at {self.available_time}"

class Interview(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()

    def __str__(self):
        return f"Interview on {self.scheduled_date} at {self.scheduled_time}"
