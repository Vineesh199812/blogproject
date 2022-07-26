from django.db import models


# Create your models here.


class Blogs(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    liked_by = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Mobiles(models.Model):
    name = models.CharField(max_length=120, unique=True)
    price = models.PositiveIntegerField(default=5000)
    band = models.CharField(max_length=100, default='4g')
    display = models.CharField(max_length=120)
    processor = models.CharField(max_length=120)

    def __str__(self):
        return self.name

# orm query for creating a resource ==>
# modelname.objects.create(field1=value1,field2=value2.........)
#   so here  ==> Blogs.objects.create(title="good morning",content="hello",author="ram",liked_by="hari")

# to open the shell ==> python manage.py shell

#  orm query for fetching all objects
#  qs=modelname.objects.all()
#  so here  ==> qs=Blogs.objects.all()

#  detail view of an specific object
#  qs=modelname.objects.get(id={id number})
#    so here  blog=Blogs.objects.get(id=1)
#        to delete a blog=> (ex) blog=Blogs.objects.get(id=2).delete()          ===>>>>>refer cls 22/07/2022

# to filter
# fetch all 4g mobiles  >> qs=Mobiles.filter(band="4g")
# fetch all snapdragon prcs mobiles >> qs=Mobiles.filter(processor="snapdragon")

# print all mobiles price < 32000 >> qs=Mobiles.objects.filter(price__lt=32000)    {lt=>> lessthan} and {gt=>> greaterthan} or lte32000 ot gre32000
# non 5g mobiles >> qs=Mobiles.objects.all().exclude(band="5g")

# count of 5g mobiles >> qs=Mobiles.objects.filter(band="5g").count()