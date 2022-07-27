from django.shortcuts import render

# Create your views here.


from blogapi.models import Mobiles
from rest_framework.views import APIView
from rest_framework.response import Response
from blogapi.serializers import MobileSerializer

#url: localhost:8000/oxygen/mobiles/
#get: list all mobiles
#post: create a mobile

class MobileView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Mobiles.objects.all()
        #serialization and deserialization
        serializer=MobileSerializer(qs,many=True)
        return Response(data=serializer.data)

    def post(self,request,*args,**kwargs):
        serializer=MobileSerializer(data=request.data)
        if serializer.is_valid():
            Mobiles.objects.create(**serializer.validated_data)
            return Response(data=serializer.data)
