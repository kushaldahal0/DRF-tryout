from django.urls import path
# from rest_framework import routers
from new import views
from new.views import modelclist,singlemodelclist,  ListModelMixins, SingleModelMixins , ListModelGenerics, SingleModelGenerics, ModelViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(
    'modelviewset', ModelViewSet, basename='models'
)


urlpatterns = [
    path('', views.index, name='index'),
    path('modellist/', views.modellist, name='modellist'),
    path('message/', views.message, name='message'),
    path('modelclist/', modelclist.as_view(), name='modelclist'),
    path('singlemodelclist/<int:mid>', singlemodelclist.as_view(), name='singlemodelclist'),
    #generics and mixinscrud
    path('mixinslist/', ListModelMixins.as_view(), name='mixinslist'),
    #pk = primary key
    path('mixinssingle/<int:pk>/', SingleModelMixins.as_view(), name='mixinssingle'),
    #generics crud
    path('genericslist/', ListModelGenerics.as_view(), name='genericslist'),
    path('genericssingle/<int:pk>', SingleModelGenerics.as_view(), name='genericssingle'),
]+router.urls
