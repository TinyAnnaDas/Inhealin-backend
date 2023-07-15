"""
URL configuration for inhealin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



from client.models import ClientAdditionalDetails, TherapySessions


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        if user.type == "CLIENT":
            try:
                client_additional_details = ClientAdditionalDetails.objects.get(client=user)
                if client_additional_details.subscription_id is not None:
                    token['subscription'] = client_additional_details.subscription.type
                else:
                    token['subscription'] = None
            except:
                pass

      
        session = TherapySessions.objects.filter(client=user).first()
        if session:
            token['therapy_session'] = session.id
        else: 
            pass
        
            

        # Add custom claims
        token['name'] = user.name
        token['is_superuser'] = user.is_superuser
        token['type'] = user.type
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer







from cadmin.views import ProcessOrder, RetriveChat, ListSubscriptionAPI, RetrieveSubscription
from therapist.views import RetrievePreSignedUrlView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    
    path("order-summary/process-order/", ProcessOrder.as_view()),
    path("retrieve-chat/<str:group_name>/", RetriveChat.as_view()),
    path("list-all-subscriptions/", ListSubscriptionAPI.as_view() ),
    path("retrieve-subscription/<str:pk>/", RetrieveSubscription.as_view() ), 

    path('api/therapist/', include('therapist.urls')),
    path('api/client/', include('client.urls')),
    path('admin/', include('cadmin.urls')),

    path('dj-admin/', admin.site.urls),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
