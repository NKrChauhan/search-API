from django.db import models

class Anime(models.Model):
    name = models.CharField(unique = True,max_length=120,null=True,blank=True)
    rating = models.DecimalField(decimal_places=2,max_digits=4,null=True,blank=True)
    created = models.DateTimeField(null=True,blank=True)
    description = models.CharField(null=True,blank=True,max_length=400)
    poster = models.URLField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name