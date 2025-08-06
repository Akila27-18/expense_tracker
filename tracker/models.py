from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ("food", "Food"),
        ("transport", "Transport"),
        ("housing", "Housing"),
        ("utilities", "Utilities"),
        ("entertainment", "Entertainment"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.title} - {self.amount}"
