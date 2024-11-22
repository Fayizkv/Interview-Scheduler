from django.db import models

# Create your models here.
class Candidate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Interviewer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Interview(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    time_slot = models.DateTimeField()

    def __str__(self):
        return f"Interview with {self.candidate} and {self.interviewer} at {self.time_slot}"
