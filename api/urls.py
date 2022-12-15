from django.urls import path, include
from .views import MessageList, MessageDetail, UserList, UserDetail, LatestMessages, MessagesInDateRange, DeleteMessagessView
from rest_framework import routers

# Create a router and register the viewset with it
router = routers.DefaultRouter()
router.register('messagesbydate', MessagesInDateRange, 'messagesbydate')

urlpatterns = [
    path('', include(router.urls)),
    path('message/', MessageList.as_view()),
    path('message/<int:pk>/', MessageDetail.as_view()),
    path('message/delete/', DeleteMessagessView.as_view(), name='delete_records'),
    path('user/', UserList.as_view()),
    path('user/<int:pk>/', UserDetail.as_view()),
    path('latestmessages/', LatestMessages.as_view()),
]