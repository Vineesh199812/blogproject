from django.shortcuts import render

# Create your views here.


from blogapi.models import Mobiles
from rest_framework.views import APIView
from rest_framework.response import Response
from blogapi.serializers import MobileSerializer,MobileModelSerializer
from rest_framework import status

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
        else:
            return Response(serializer.errors)

# to know about a specific mobile
# url: oxygen/mobiles/{id}
#put
#delete

class MobileDetailsView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        try:
            qs=Mobiles.objects.get(id=id)
            serializer=MobileSerializer(qs)   # here we take only one value so there is no need of many=True
            return Response(data=serializer.data)
        except:
            return Response({"msg":"doesn't exist"},status=status.HTTP_404_NOT_FOUND)
    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        try:
            object=Mobiles.objects.get(id=id)
            serializer=MobileSerializer(data=request.data)
            if serializer.is_valid():
                object.name=serializer.validated_data.get("name")
                object.price=serializer.validated_data.get("price")
                object.band=serializer.validated_data.get("band")
                object.display=serializer.validated_data.get("display")
                object.processor=serializer.validated_data.get("processor")
                object.save()
                return Response(data=serializer.data)
            else:
                return Response(serializer.errors)
        except:
            return Response({"msg":"doesn't exist"},status=status.HTTP_404_NOT_FOUND)
    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        try:
            object=Mobiles.objects.get(id=id)
            object.delete()
            return Response({"msg":"deleted"})
        except:
            return Response({"msg":"doesn't exist"},status=status.HTTP_404_NOT_FOUND)

#model serializer

class MobileModelView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Mobiles.objects.all()
        serializer=MobileModelSerializer(qs,many=True)
        return Response(data=serializer.data)
    def post(self,request,*args,**kwargs):
        serializer=MobileModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class MobileDetailModelView(APIView):
    def get(self,req,*args,**kwargs):
        id=kwargs.get("id")
        try:
            qs=Mobiles.objects.get(id=id)
            serializer=MobileModelSerializer(qs)
            return Response(data=serializer.data)
        except:
            return Response({"msg":"doesn't exist"},status=status.HTTP_404_NOT_FOUND)
    def put(self,req,*args,**kwargs):
        id=kwargs.get("id")
        try:
            instance=Mobiles.objects.get(id=id)
            serializer=MobileModelSerializer(data=req.data,instance=instance)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
        except:
            return Response({"msg":"doesn't exist"},status=status.HTTP_404_NOT_FOUND)
    def delete(self,req,*args,**kwargs):
        id=kwargs.get("id")
        qs=Mobiles.objects.get(id=id)
        qs.delete()
        return Response({"msg":"deleted"})

