from django.shortcuts import render
from rest_framework import generics, viewsets, views, status
from rest_framework.response import Response
from django.views import View
from django.http import HttpResponse
from django.utils import timezone
from .serializers import MessageSerializer, UserSerializer
from .models import Message, User, PreviousFetch
import json

def index(request):
    return render(request, 'landingpage.html')

# Fetch all messages
class MessageList(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = Message.objects.all()
        
        #Eg: message/?user=1
        user = self.request.query_params.get('user')
        if user is not None:
            queryset = queryset.filter(recipient = user)
        return queryset

# Single message, RUD 
class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

# Fetch all users
class UserList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

# Single user, RUD
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

# Only fetch new messages
class LatestMessages(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = Message.objects.all()

        last_fetch_time = PreviousFetch.objects.values_list('time', flat=True).last()

        if last_fetch_time is not None:
            queryset = queryset.filter(date_sent__gt=last_fetch_time)

        current_time = timezone.now()
        previous_fetch = PreviousFetch(time=current_time)
        previous_fetch.save()
        return queryset

# Get all messages in a specific date range, ordered by time
class MessagesInDateRange(viewsets.ViewSet):
    def list(self, request):
        # Example url ?start_date=2022-12-14T00:00:00Z&end_date=2022-12-15T00:00:00Z
        # Parse the start and stop values from the query parameters
        start_time = request.query_params.get('start_date')
        stop_time = request.query_params.get('end_date')
        # Fetch all records from the database in date range, ordered by time
        messages = Message.objects.filter(
        date_sent__gte=start_time,
        date_sent__lte=stop_time
        ).order_by('date_sent')

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

# Delete multiple messages /message/delete/?id=1,2
class DeleteMessagessView(views.APIView):
    def delete(self, request):
        messages = request.query_params.get('id')
        # Split the string of comma-separated IDs on the comma character
        messages = messages.split(',')
        # Convert each individual ID to an integer
        messages = [int(message) for message in messages]
        items = Message.objects.filter(id__in=messages)
        for item in items:
            item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)