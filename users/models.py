from django.db import models

# Create your models here.
class user_tbl(models.Model):
    fname = models.CharField(max_length=50)
    pnum = models.IntegerField()
    email = models.EmailField()
    passw = models.CharField(max_length=12)
    

