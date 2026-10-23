from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import F, Q
# Create your models here.
class Event(models.Model):
    STATUS_CHOICES = [
    ('upcoming', 'Upcoming'),
    ('ongoing', 'Ongoing'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
    ]

    title           = models.CharField(max_length=200, blank=False )
    venue           = models.CharField(max_length=200, blank=False)
    date            = models.DateField(blank=False)
    total_seats     = models.PositiveIntegerField(blank=False, validators=[MinValueValidator(1)])
    available_seats = models.PositiveIntegerField(blank=False)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.venue}"

    class Meta:
        ordering = ['date']
        constraints = [
            models.CheckConstraint(
                # Enforces that total_seats must be greater than equal to available_seats
                condition=Q(total_seats__gte=F('available_seats')),
                name='total_and_available_seats_validation'
            )
        ]


class Reservation(models.Model):

    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    event          = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reservations')
    attendee_name  = models.CharField(max_length=200, blank=False)
    attendee_email = models.EmailField(blank=False)
    seats_reserved = models.PositiveIntegerField(blank=False)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attendee_name} - {self.event.title} ({self.seats_reserved} seats)"

    class Meta:
        ordering = ['-created_at']
