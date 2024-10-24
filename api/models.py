from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
import uuid

class CustomUser(AbstractUser):
    STATUS = (
        ('employee', 'employee'),
        ('client', 'client'),
        ('admin', 'admin'),
    )
    description = models.TextField(max_length=600)
    phone_number = models.CharField(max_length=12, null=True)
    status = models.CharField(max_length=10, choices=STATUS)

    def __str__(self):
        return self.username

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='api_images/')
    slug = models.SlugField(max_length=200, unique=True, null=True)

    def save(self, *args, **kwargs) :
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = f'{base_slug}-{uuid.uuid4().hex[:6]}'

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
