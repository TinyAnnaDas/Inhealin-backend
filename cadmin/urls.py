from django.urls import path

from .views import   ListTherapistAPI, RUDTherapistAPI, ListClientAPI, RUDClientAPI, LCSubscriptionAPI, RUDSubscriptionAPI, getToken, createMember, GetMember,DeleteMember, GetCount, ClientPlanStatistics


urlpatterns = [
    path('list-all-clients/', ListClientAPI.as_view()),
    path('retreive-update-delete-client/<int:pk>/', RUDClientAPI.as_view()),

    path('list-all-therapists/', ListTherapistAPI.as_view()),
    path('retreive-update-delete-therapist/<int:pk>/', RUDTherapistAPI.as_view()),

   

    path('list-create-subscription-plans/', LCSubscriptionAPI.as_view(), name="all_subscriptions"),
    path('retreive-update-delete-subscription-plans/<int:pk>/', RUDSubscriptionAPI.as_view() ),

    path ('get-token/<int:session_id>/', getToken.as_view()),
    path('create_member/', createMember.as_view()),
    path('get_member/<int:uid>/<str:room_name>/', GetMember.as_view()),
    path('delete_member/<int:uid>/<str:room_name>/<str:name>/', DeleteMember.as_view()),

    path('get_count/', GetCount.as_view()),
    path('get_client_plan_statistics/', ClientPlanStatistics.as_view()),

    
    
   
   

]