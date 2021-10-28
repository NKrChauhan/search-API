from django.db import models

# class Anime(models.Model):
#     name = models.CharField(unique = True,max_length=120,null=True,blank=True)
#     rating = models.DecimalField(decimal_places=2,max_digits=4,null=True,blank=True)
#     created = models.DateTimeField(null=True,blank=True)
#     description = models.CharField(null=True,blank=True,max_length=400)
#     poster = models.URLField(max_length=100,null=True,blank=True)

#     def __str__(self):
#         return self.name

# class Actor(models.Model):
#     name = models.CharField(max_length=120,null=False,blank=False)

#     def __str__(self):
#         return self.name

# class AnimeActorRel(models.Model):
#     anime = models.ForeignKey(Anime,blank=False,null=False,on_delete=models.CASCADE)
#     actor = models.ForeignKey(Actor,blank=False,null=False,on_delete=models.CASCADE)

class Movie(models.Model):
    name    = models.CharField(unique = True,max_length=120,null=True,blank=True) 
    rated   = models.CharField(max_length=10,null=True,blank=True) 
    year    = models.IntegerField()
    director= models.CharField(max_length=120,null=True,blank=True) 

    def __str__(self):
       return self.name

class Ratings(models.Model):
    movie   = models.ForeignKey(Movie,blank=False,null=False,on_delete=models.CASCADE)
    source  = models.CharField(max_length=120,null=True,blank=True)
    value   = models.CharField(max_length=120,null=True,blank=True)

    def __str__(self):
        return f"{self.movie}__{self.source}__{self.value}"