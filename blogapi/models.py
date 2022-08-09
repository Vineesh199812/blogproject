from django.db import models


# Create your models here.
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

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
    def average_rating(self):
        reviews=self.reviews_set.all()
        if reviews:
            ratings=[rv.rating for rv in reviews]
            total=sum(ratings)
            return total/len(reviews)
        else:
            return 0
    def total_reviews(self):
        return self.reviews_set.all().count()

#
class Reviews(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Mobiles,on_delete=models.CASCADE)
    review=models.CharField(max_length=120)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    date=models.DateField(auto_now_add=True)

    class Meta:
        unique_together=("author","product")

    def __str__(self):
        return self.review

class Carts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Mobiles,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    options=(
        ("incart","incart"),
        ("order-placed","order-placed"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=120,choices=options,default="incart")
class Orders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Mobiles,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    options=(
        ("order_placed","incart"),
        ("order_placed","order_placed"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=120,choices=options,default="order_placed")



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

#to update or edit object ==>> get the id that we wanna update ==>> (ex)    qs=Blogs.objects.get(id=3)
# then ==>> qs.content="hi all"  ==>> qs.save()  ==>> qs.content(to view the updated object)

#user.reviews_set.create(product=mob,review='good',rating=4)

#to list reviews ==> qs=Reviews.objects.filter(author=user) or user.reviews_set.all()