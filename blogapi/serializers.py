

from rest_framework import serializers
from blogapi.models import Mobiles,Reviews
from django.contrib.auth.models import User

class MobileSerializer(serializers.Serializer):
    id=serializers.CharField(read_only=True)
    name=serializers.CharField()
    price=serializers.IntegerField()
    band=serializers.CharField()
    display=serializers.CharField()
    processor=serializers.CharField()

    def validate(self,data):
        cost=data.get("price")
        if cost<0:
            raise serializers.ValidationError("invalid price")
        return data

class MobileModelSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=Mobiles
        fields=["id",
                "name",
                "price",
                "band",
                "display",
                "processor"]
        #fields="__all__"  >> we can also write this instead
    def validate(self,data):
        price=data.get("price")
        if price<0:
            raise serializers.ValidationError("invalid_price")
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=[
            "username",
            "first_name",
            "last_name",
            "email",
            "password"
        ]
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

#api/v6/oxygen/mobiles/{pid}/add_review
#method post
#data ={rating:4,review:"gd"}

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reviews
        fields=["review","rating"]

    def create(self, validated_data):
        user=self.context.get("user")
        product=self.context.get("product")
        return Reviews.objects.create(author=user,product=product,**validated_data)
