from django.db import models

class RealityPost(models.Model):
    title = models.TextField()
    description = models.TextField()
    source = models.TextField()
    image_url = models.URLField(default=None, null=True)
    link_url = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.IntegerField()
    date_updated = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

