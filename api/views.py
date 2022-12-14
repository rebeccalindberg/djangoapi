from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.response import Response
from django.views import View
from django.http import HttpResponse
from django.utils import timezone
from .serializers import MessageSerializer, UserSerializer
from .models import Message, User, PreviousFetch
import json

# Fetch all messages
class MessageList(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = Message.objects.all()
        
        # Om get har en queryparameter för /user, hämta alla messages för den usern. Ex: messages/?user=1
        location = self.request.query_params.get('user')
        if location is not None:
            queryset = queryset.filter(itemLocation = location)
        return queryset

# Single message, with RUD 
class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

# Fetch all users
class UserList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

# Single user, with RUD
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

# Delete multiple messages
class DeleteMessages(View):
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        if request.method=="POST":
            json_ids = json.loads(request.body)
            messages = Message.objects.filter(id__in=json_ids["id"])
            for message in messages:
                message.delete()
            serializer = MessageSerializer(messages, many=True)
            return HttpResponse(serializer.data)

# Only fetch new messages
class LatestMessages(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = Message.objects.all()
        # Hämta senaste fetch tiden från databasen
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
        records = Message.objects.filter(
        date_sent__gte=start_time,
        date_sent__lte=stop_time
        ).order_by('date_sent')

        serializer = MessageSerializer(records, many=True)
        return Response(serializer.data)
