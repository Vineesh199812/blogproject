

from rest_framework import serializers
from blogapi.models import Mobiles

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