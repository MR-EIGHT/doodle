from django.db import models




class webDoc(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    url = models.URLField()
    

