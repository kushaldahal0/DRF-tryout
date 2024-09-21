from rest_framework import serializers

from .models import NewModel

# this is a model based serializer
class NewModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = NewModel
    fields = '__all__'
      # for selective fields
    # fields = ['name','age','email','phone','address']


# this is simple serializer
class MessageSerializer(serializers.Serializer):
  email = serializers.EmailField()
  content = serializers.CharField(max_length = 200)
  created = serializers.DateTimeField()
    