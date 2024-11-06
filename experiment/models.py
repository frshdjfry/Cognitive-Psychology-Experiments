from django.db import models

# Create your models here.
from django.db import models

class Participant(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.CharField(max_length=1, choices=[('A', 'Group A'), ('B', 'Group B')])

class Response(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    question_id = models.CharField(max_length=50)
    answer = models.TextField()
    response_time = models.DurationField(null=True, blank=True)  # New field for time tracking
    created_at = models.DateTimeField(auto_now_add=True)


class TwoFourSixFinalGuess(models.Model):
    """Model to store the final guess for the 2-4-6 experiment."""
    final_guess = models.CharField(max_length=255, blank=True, null=True)

class TwoFourSixSequenceAttempt(models.Model):
    """Model to store each sequence attempt in the 2-4-6 experiment."""
    final_guess = models.ForeignKey(TwoFourSixFinalGuess, on_delete=models.CASCADE)
    sequence = models.CharField(max_length=20)  # Store as a string, e.g., "2,4,6"
    fits_rule = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)