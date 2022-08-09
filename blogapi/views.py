from django.shortcuts import render

# Create your views here.


from blogapi.models import Mobiles,Reviews,Carts
from rest_framework.views import APIView
from rest_framework.response import Response
from blogapi.serializers import MobileSerializer,MobileModelSerializer,UserSerializer,ReviewSerializer,CartSerializer,OrderSerializer
from rest_framework import status,viewsets
from django.contrib.auth.models import User
from rest_framework import authentication,permissions
from rest_framework.decorators import action

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

#Viewset
class MobilesViewSetView(viewsets.ViewSet):
    def list(self,request,*args,**kwargs):
        qs=Mobiles.objects.all()
        serializer=MobileModelSerializer(qs,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def create(self,request,*args,**kwargs):
        serializer=MobileModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_404_NOT_FOUND)

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")  # pk =>> primary key (instead of "id")
        object=Mobiles.objects.get(id=id)
        serializer=MobileModelSerializer(object)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Mobiles.objects.get(id=id)
        serializer=MobileModelSerializer(data=request.data,instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Mobiles.objects.get(id=id)
        object.delete()
        return Response({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)

#modelViewset
class MobilesModelViewSetView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = MobileModelSerializer
    queryset = Mobiles.objects.all()


    @action(methods=["post"],detail=True)
    def add_review(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        mobile=Mobiles.objects.get(id=id)
        user=request.user
        serializer=ReviewSerializer(data=request.data,context={"user":user,"product":mobile})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    #api/v4/oxygen/mobiles/{pid}/get_reviews
    @action(methods=["get"],detail=True)
    def get_reviews(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        mobile=Mobiles.objects.get(id=id)
        reviews=mobile.reviews_set.all()
        serializer=ReviewSerializer(reviews,many=True)
        return Response(data=serializer.data)

    @action(methods=["post"],detail=True)
    def add_to_cart(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        mobile=Mobiles.objects.get(id=id)
        user=request.user
        serializer=CartSerializer(data=request.data,context={"user":user,"product":mobile})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    @action(methods=["post"],detail=True)
    def order(self,request,*args,**kwargs):
        user=request.user
        id=kwargs.get("pk")
        mobile=Mobiles.objects.get(id=id)
        serializer=OrderSerializer(data=request.data,context={"user":user,"product":mobile})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    # @action(methods=["get"],detail=True)
    # def view_cart(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     user=User.objects.get(id=id)
    #     cart=user.carts_set.all()
    #     serializer=CartSerializer(cart,many=True)       *we don't have to use this here coz cart is not only related
    #     return Response(data=serializer.data)            - to Mobiles field instead we create a class with token authentication

    # @action(methods=["get"],detail=False)
    # def my_cart(self,request,*args,**kwargs):
    #    qs=Carts.objects.filter(user=request.user)
    #    serializer=CartSerializer(qs,many=True)
    #    return Response(data=serializer.data)

class UserRegistrationView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#class ReviewView(viewsets.ModelViewSet):
    #serializer_class = ReviewSerializer
    #queryset = Reviews.objects.all()

class CartsView(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Carts.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user)