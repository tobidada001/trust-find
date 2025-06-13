from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth import get_user_model


User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Item(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]
    
    ITEM_STATUS_CHOICES = [
        ('active', 'Active'),
        ('resolved', 'Resolved'),
        ('expired', 'Expired'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    item_status = models.CharField(max_length=10, choices=ITEM_STATUS_CHOICES, default='active')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.CharField(max_length=400)
    image = models.ImageField(upload_to='items/')
    date_lost_found = models.DateField()
    time_lost_found = models.TimeField(blank=True, null=True)
    contact_info = models.CharField(max_length=200)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    is_approved = models.BooleanField(default=True)  # Set to False if moderation is required
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_status_display()}: {self.title}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('item_detail', kwargs={'pk': self.pk})




class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='item_images/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.item.title}"

class Message(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.sender.username} about {self.item.title}"