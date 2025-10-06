from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

class Order(models.Model):
    FORMATTING_STYLE = [
        ('apa', 'APA'),
        ('mla', 'MLA'),
        ('harvard', 'Harvard'),
        ('chicago', 'Chicago'),
        ('oscola', 'OSCOLA'),
    ]
    ASSIGNMENT_TYPE = [
        ('essay', 'Essay'),
        ('dissertation', 'Dissertation'),
        ('proposal', 'Proposal'),
        ('term_paper', 'Term Paper'),
    ]
    STATUS = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('revision', 'Revision'),
        ('submitted', 'Submitted'),
        ('completed', 'Completed'),
        ('paid', 'Paid'),
    ]
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    formating_style = models.CharField(max_length=120, choices=FORMATTING_STYLE, default='apa')
    assignment_type = models.CharField(max_length=120, choices=ASSIGNMENT_TYPE)
    pages = models.FloatField()
    status = models.CharField(max_length=120, choices=STATUS)
    amount_per_page = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    due_date = models.DateTimeField()
    file = models.FileField(upload_to='documents/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.id} {self.title} is due at {self.due_date}"


# Create your models here.
