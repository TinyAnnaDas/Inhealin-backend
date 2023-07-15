
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework import permissions, status

from .serializers import  SubsriptionSerializer, CreateSubscriptionSerializer, CreateClientAdditionalDetails, ChatSerializer
from client.serializers import ClientSerializer
from therapist.serializers import TherapistSerializer, TherapistAvailabilitySerializer

from django.contrib.auth import get_user_model
User = get_user_model()
from .models import SubscriptionPlans, Group, Chat
from therapist.models import TherapistAvailability, Therapist
from client.models import ClientAdditionalDetails, Client, Subscriptions

from django.db.models import Q

from agora_token_builder import RtcTokenBuilder
import random
import time

from .models import RoomMember


class ListClientAPI(GenericAPIView, ListModelMixin):
    permission_classes = [permissions.IsAdminUser]

    queryset = User.objects.exclude(Q(is_superuser=True) | Q(type='THERAPIST'))
    serializer_class = ClientSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



class RUDClientAPI(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = User.objects.exclude(Q(is_superuser=True) | Q(type='THERAPIST'))
    serializer_class = ClientSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


from datetime import datetime

class ListTherapistAPI(GenericAPIView, ListModelMixin):
    permission_classes = [permissions.IsAdminUser] # commenting 

    queryset = User.objects.exclude(Q(is_superuser=True) | Q(type='CLIENT')).order_by('created_at')
    serializer_class = TherapistSerializer

    def get(self, request, *args, **kwargs):
        all_therapists =  self.list(request, *args, **kwargs)

        for item in all_therapists.data:

            availability = TherapistAvailability.objects.filter(therapist_id=item['id'], session_booked=False, date_time__gte=datetime.now()
            ).order_by('date_time').first()

            serializer = TherapistAvailabilitySerializer(availability)

            



            if (availability):
                print(serializer.data["date_time"])
        
                item['next_available'] = serializer.data["date_time"]
            else:
                item['next_available'] = None

        return Response(all_therapists.data, status=status.HTTP_200_OK)
        


class RUDTherapistAPI(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    # permission_classes = [permissions.IsAdminUser]

    queryset = User.objects.exclude(Q(is_superuser=True) | Q(type='CLIENT'))
    serializer_class = TherapistSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)





class LCSubscriptionAPI(GenericAPIView, ListModelMixin, CreateModelMixin):
    
    permission_classes = [permissions.IsAdminUser]

    queryset = SubscriptionPlans.objects.all()
    serializer_class = SubsriptionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ListSubscriptionAPI(GenericAPIView, ListModelMixin): # writing it seperately since, it is needed in the front-end without any permissions
    queryset = SubscriptionPlans.objects.all().order_by('id')
    serializer_class = SubsriptionSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RUDSubscriptionAPI(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    permission_classes = [permissions.IsAdminUser]

    queryset = SubscriptionPlans.objects.all()
    serializer_class = SubsriptionSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class RetrieveSubscription(GenericAPIView, RetrieveModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SubscriptionPlans.objects.all()
    serializer_class = SubsriptionSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        print(user)
        additional_details_client = ClientAdditionalDetails.objects.filter(client_id=user.id).first()
       
        already_existing_subscription = additional_details_client.subscription_id
        print(already_existing_subscription)
        return self.retrieve(request, *args, **kwargs)













class TherapistsDetailsView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        therapist = User.objects.exclude(Q(is_superuser=True) | Q(type='CLIENT'))
     
        therapist = TherapistSerializer(therapist, many=True)

        return Response(therapist.data, status = status.HTTP_200_OK)






class ProcessOrder(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        # print(request.data)
        subscription_id = request.data['subscriptionPlanId']
        subscription = SubscriptionPlans.objects.get(id=subscription_id)
        available_sessions = subscription.sessions_available
        # print(subscription)
        client = request.user

        client_additional_details = ClientAdditionalDetails.objects.filter(client=client).first()

        serializer = CreateClientAdditionalDetails(instance=client_additional_details, data={
            "subscription": subscription_id,
            "sessions_available":available_sessions

        }, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        


        payment_id = request.data['paymentId']

        serializer = CreateSubscriptionSerializer(data={
            "subscription_plan": subscription_id,
            "client": client.id,
            "payment_id": payment_id
            })

        if not serializer.is_valid():
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
       
        return Response(serializer.data, status=status.HTTP_200_OK)

class RetriveChat(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, group_name):

        group = Group.objects.filter(name=group_name).first()
        if group:
            chats = Chat.objects.filter(group=group)
            chats = ChatSerializer(chats, many=True)
        else:
            group = Group(name=group_name)
            group.save()
        
        print(group_name)

        return Response(chats.data, status=status.HTTP_200_OK)



class getToken(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, session_id):
        appId = "c0bbf989c6494704a30b03f758f7ffb1"
        appCertificate = "c7736f9ac606497a9cee8c721c059bfc"
        print(session_id)
        channelName = str(session_id)
        uid = random.randint(1, 230)
        expirationTimeInSeconds = 3600 * 24 
        currentTimeStamp = int(time.time())
        privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
        role = 1

        token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName,  uid, role, privilegeExpiredTs)
        print("uid...", uid)

        return Response({"token":token, "uid": uid}, status=status.HTTP_200_OK)

class createMember(APIView):

    def post(self, request):

        print(request.data)

        member, created = RoomMember.objects.get_or_create(

            name = request.data['name'],
            uid = request.data['uid'],
            room_name = request.data['room_name']

        )


        return Response({'name':request.data['name'], 'uid': request.data['uid']})

class GetMember(APIView):

    def get(self, request, uid, room_name):
        member = RoomMember.objects.get(
            uid=uid,
            room_name=room_name
        )
        name = member.name

        return Response({"name": name})

from client.models import TherapySessions
class DeleteMember(APIView):
    def delete(self, request, uid, room_name, name):
        therapy_session = TherapySessions.objects.filter(id=room_name).first()
        print(therapy_session)
        therapy_session.is_completed = True
        therapy_session.save()
        user = request.user
        print(user.type)

        if user.type == "CLIENT":
            client = user
            client_additional_details = ClientAdditionalDetails.objects.filter(client_id=client.id).first()
            print(type(client_additional_details.sessions_available))
            client_additional_details.sessions_available -= 1
            client_additional_details.subscription = None
            print(client_additional_details.sessions_available)
            client_additional_details.save()




       
        
        print(uid)      
        print(room_name)
        print(name)
        member = RoomMember.objects.filter(
            name=name,
            uid=uid,
            room_name=room_name
        ).first()
        member.delete()
        return Response('Member deleted')


class GetCount(APIView):
    def get(self,request):
        signed_in_users_count = Client.objects.all().count()
        print("signed_in_user", signed_in_users_count)
        user_with_subscription = Subscriptions.objects.values('client_id').distinct()
        print("user_with_subscription ", user_with_subscription)
        therapist_count = Therapist.objects.all().count()
        print("therapist_count ", therapist_count)
        return Response({'signed_in_user': signed_in_users_count,'user_with_subscription': user_with_subscription,'therapist_count': therapist_count})

class ClientPlanStatistics(APIView):
    def get(self, request):
        subscription_plans = SubscriptionPlans.objects.all()
        data = {
            'subscription_plans': [],
            'client_count': []
        }

        for plan in subscription_plans:
            client_count = Subscriptions.objects.filter(subscription_plan_id=plan.id).count()
            data['subscription_plans'].append(plan.type)
            data['client_count'].append(client_count)

        return Response(data)









