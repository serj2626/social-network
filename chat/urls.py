from django.urls import path
from .views import ChatListView, ChatCreateView, ChatDetailView, MessageDeleteView

urlpatterns = [

    path('chat-list', ChatListView.as_view(), name='chat_list'),
    path('chat/create/<slug:slug>', ChatCreateView.as_view(), name='chat_create'),
    path('chat-detail/<int:pk>', ChatDetailView.as_view(), name='chat_detail'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),





]
