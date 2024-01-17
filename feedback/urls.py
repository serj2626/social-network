from django.urls import path
from .views import FeedbackCreateView, NewsletterCreateView

urlpatterns = [

    path('', FeedbackCreateView.as_view(), name='feedback'),
    path('newsletter', NewsletterCreateView.as_view(), name='newsletter')
]
