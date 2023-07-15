
from django.urls import path
from .views import RetrievePreSignedUrlView, RegisterTherapistView, ListTherapistAdditionalDetailsAPI, RetrieveTheapistAdditionalDetailsAPI,ListAllApprovedTherapists, LCTherapistAvailability, RetrieveTherapistAvailability, RetrieveTherapySessionsTherapistAPI, CancelTherapySessionTherapist, RetrieveUpcomingSubscriptionTherapist, RetrieveCompletedSubscriptionTherapist

urlpatterns = [
     path('pre-signed-url/', RetrievePreSignedUrlView.as_view()),
      path('register-therapist/', RegisterTherapistView.as_view()),
      path ('therapist-additional-details/', ListTherapistAdditionalDetailsAPI.as_view()),
      path ('retrieve-therapist-additional-details/<int:pk>', RetrieveTheapistAdditionalDetailsAPI.as_view()),
     path('all-approved-therapist/', ListAllApprovedTherapists.as_view()),
     path('list-create-therapist-availability/', LCTherapistAvailability.as_view()),
     path('retrieve-therapist-availability/<str:date_time>/', RetrieveTherapistAvailability.as_view()),
     path('retrieve-therapy-sessions-therapist/', RetrieveTherapySessionsTherapistAPI.as_view()),
     path('cancel-therapy-session-therapist/<int:pk>/', CancelTherapySessionTherapist.as_view()), 
     path('retrieve-upcoming-therapy-session-therapist/', RetrieveUpcomingSubscriptionTherapist.as_view() ),
     path('retrieve-completed-therapy-session-therapist/', RetrieveCompletedSubscriptionTherapist.as_view() ),

     




]