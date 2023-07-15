from django.urls import path
from .views import RegisterClientView,RetrieveClientView, RetrieveSubscriptionDetails,MoodJoural, LCTherapySessionAPI, RTherapySessiosTherapistAPI, RTherapySessiosClientAPI, RetrieveUpcomingSubscriptionClient, UpdateTherapySessionAPI, CancelTherapySessionAPI, RetrieveCompletedSubscriptionClient, RemoveTheAvailableSessionByOne

urlpatterns = [
    path('register', RegisterClientView.as_view()),
    path('me', RetrieveClientView.as_view()),
    path('retrieve-subscription/', RetrieveSubscriptionDetails.as_view()),
    path('mood-journal/', MoodJoural.as_view()),

    path('list-create-therapy-session/', LCTherapySessionAPI.as_view()),
    path('retrieve-therapy-sessions-therapist/<int:pk>/', RTherapySessiosTherapistAPI.as_view()),
    path('retrieve-therapy-sessions-client/<int:pk>/', RTherapySessiosClientAPI.as_view()),
    path('retrieve-completed-therapy-session-client/', RetrieveCompletedSubscriptionClient.as_view() ),
    path('retrieve-upcoming-therapy-session-client/', RetrieveUpcomingSubscriptionClient.as_view() ),
    path('update-therapy-session/<int:id>/', UpdateTherapySessionAPI.as_view() ),
    path('delete-therapy-session/<int:pk>/', CancelTherapySessionAPI.as_view() ),

    path('reduce-the-available-session-by-one/', RemoveTheAvailableSessionByOne.as_view() ),

   
  

]