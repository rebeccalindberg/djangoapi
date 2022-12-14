from rest_framework import serializers
from .models import User, Message, PreviousFetch

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('__all__')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')

class PreviousFetch(serializers.ModelSerializer):
    class Meta:
        model = PreviousFetch
        fields = ('__all__')