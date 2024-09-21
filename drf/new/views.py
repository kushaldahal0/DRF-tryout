from django.shortcuts import render
from rest_framework.views import APIView
from .models import NewModel
from .serializer import NewModelSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status , generics, mixins, viewsets

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication

from .test import Message
from new import serializer

# Create your views here.
def index(request):
    all_models = NewModel.objects.all()
    context = {
      'all_models': all_models
    }
    return render(request, 'new/index.html',context)

#for api
@api_view(['GET','POST'])
# #for authentication and it is decorator based
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication, SessionAuthentication, TokenAuthentication])
def modellist(request):


  all_models = NewModel.objects.all()
  serializer_class = NewModelSerializer(all_models, many=True)
  context = {
    'serializer_class_data':serializer_class.data,
  }
  # return render(request, 'new/index.html', context)
  return Response(serializer_class.data)



@api_view(['GET','POST'])
#for authentication
@permission_classes([IsAuthenticated])
def message(request):
  msg = Message(email='xcvkp@example.com', content='Hello World from the message class')
  #not iterable so no many=True
  serializer_class = MessageSerializer(msg)
  return Response(serializer_class.data)

#Class based view for api
class modelclist(APIView):
  #for local or view specific authentication and it is class based levels
  authentication_classes= (BasicAuthentication, SessionAuthentication)
  permission_classes = (IsAuthenticated,)
  #R all
  def get(self, request):
    all_models = NewModel.objects.all()
    serializer_class = NewModelSerializer(all_models, many=True)
    return Response(serializer_class.data)

  #C
  def post(self, request):
    serializer_obj = NewModelSerializer(data= request.data)
    if serializer_obj.is_valid(raise_exception=True):
      model_saved = serializer_obj.save()
      return Response({"Success":"Model '{}' successfully saved".format(model_saved.name)})
    return Response(serializer_obj.errors,status=status.HTTP_400_BAD_REQUEST)

#Class based view for api
class singlemodelclist(APIView):
  #crud operation
  #R
  def get(self, request, mid):
    all_models = NewModel.objects.filter(id = mid)
    serializer_class = NewModelSerializer(all_models, many=True)
    return Response(serializer_class.data)

  #U
  def put(self, request, mid):
    model_obj = NewModel.objects.get(id = mid)
    serializer_obj = NewModelSerializer(model_obj,data= request.data)
    if serializer_obj.is_valid(raise_exception=True):
      model_saved = serializer_obj.save()
      return Response({"Success":"Model '{}' successfully saved".format(model_saved.name)})
    return Response(serializer_obj.errors,status=status.HTTP_400_BAD_REQUEST)

  #D
  def delete(self, request, mid):
    model_obj = NewModel.objects.get(id = mid)
    model_obj.delete()
    return Response({"Success":"Model '{}' successfully deleted".format(model_obj.name)},status=status.HTTP_200_OK)



#now for generic views and mixins

class ListModelMixins(mixins.ListModelMixin, generics.GenericAPIView):
  #queryset is exact variable needed and cannot be changed
  queryset = NewModel.objects.all()
  serializer_class = NewModelSerializer
  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

class SingleModelMixins(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
  queryset = NewModel.objects.all()
  serializer_class = NewModelSerializer
  
  def get(self, request, *args, **kwargs):
    return self.retrieve(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

  def put(self, request, *args, **kwargs):
    return self.update(request, *args, **kwargs)
  
  def delete(self, request, *args, **kwargs):
    return self.destroy(request, *args, **kwargs)

#now for just generic crud 
# class ListModelGenerics(generics.ListAPIView):
                      #can also do list and create at once too
class ListModelGenerics(generics.ListCreateAPIView):

  queryset = NewModel.objects.all()
  serializer_class = NewModelSerializer

class SingleModelGenerics(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    #RUD at once or seperately too
                          # generics.RetrieveAPIView,
                          # generics.UpdateAPIView,
                          # generics.DestroyAPIView):
  queryset = NewModel.objects.all()
  serializer_class = NewModelSerializer

class ModelViewSet(viewsets.ModelViewSet):


  queryset = NewModel.objects.all()
  serializer_class = NewModelSerializer
  
