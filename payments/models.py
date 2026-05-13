from django.db import models


class Payment(models.Model):
    encrypted_data = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)
