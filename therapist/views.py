# from django.shortcuts import render

# # Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from .models import TherapistAdditionalDetails, Therapist, TherapistAvailability
from client.models import  Client, TherapySessions
from client.serializers import  ClientSerializer, TherapySessionsSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from  inhealin import s3
import json
from .serializers import TherapistAdditionalDetailsSerializer, CreateTherapistSerializer, TherapistSerializer, TherapistAvailabilitySerializer


class RetrieveUpcomingSubscriptionTherapist(APIView):
     permission_classes = [permissions.IsAuthenticated]
     def get(self, request):
        therapist = request.user
        print(therapist.name)
        upcoming_therapy_session = TherapySessions.objects.filter(therapist=therapist.id, is_completed=False).first()
        if upcoming_therapy_session:
            session_serializer = TherapySessionsSerializer(upcoming_therapy_session)
            client = upcoming_therapy_session.client
            client_serializer = ClientSerializer(client)

            response_data = {
                'session': session_serializer.data,
                'therapist': client_serializer.data
            }
        else:
            return Response({"session" : "No Session"}, status=status.HTTP_200_OK)
      

        return Response(response_data, status=status.HTTP_200_OK)


class RetrieveCompletedSubscriptionTherapist(GenericAPIView, ListModelMixin ):
     permission_classes = [permissions.IsAuthenticated]
     serializer_class = TherapySessionsSerializer

     def get_queryset(self):
        queryset = TherapySessions.objects.filter(therapist=self.request.user.id, is_completed=True)
        return queryset

     def get(self, request, *args, **kwargs):
        all_completed_sessions =  self.list(request, *args, **kwargs)

        for item in all_completed_sessions.data:
            print(item)
            client = Client.objects.filter(id=item['client']).first()
            print(client.name)
            # serializer = TherapistSerializer(therapist)
            item["therapist_name"] = client.name

        
        return Response(all_completed_sessions.data)





class CancelTherapySessionTherapist(GenericAPIView, UpdateModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TherapySessions.objects.all()
    serializer_class = TherapySessionsSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class RetrieveTherapySessionsTherapistAPI(GenericAPIView, ListModelMixin):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = TherapySessionsSerializer

    def get_queryset(self):
        therapist_id = self.request.user.id
        print(therapist_id)
        queryset = TherapySessions.objects.filter(therapist=therapist_id, cancelled_by_therapist=False, is_completed=False)
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset() 

        serializer = self.get_serializer(queryset, many=True)
        for item in serializer.data:
            print(item["is_completed"])
            client = Client.objects.filter(id=item['client']).first()
            item['client_name'] = client.name

        return Response(serializer.data)

    # return Response("Message:Success")
    

class ListAllApprovedTherapists(GenericAPIView, ListModelMixin):
    queryset = Therapist.objects.filter(status='approved')
    serializer_class = TherapistSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveTheapistAdditionalDetailsAPI(APIView):
     def get(self, request, pk):
        theapist_additional_details = TherapistAdditionalDetails.objects.filter(therapist=pk).first()
        print(theapist_additional_details)
        serializer = TherapistAdditionalDetailsSerializer(theapist_additional_details)
        availability = TherapistAvailability.objects.filter(therapist=pk, session_booked=False, date_time__gte=datetime.now()).order_by('date_time').first()
        availability_serializer = TherapistAvailabilitySerializer(availability)
        print(availability_serializer.data["date_time"])
        therapist = Therapist.objects.filter(id=pk).first()
        therapist_serializer = TherapistSerializer(therapist)
        

        response_data = {
            "additional_details": serializer.data,
            "availability":availability_serializer.data["date_time"],
            "therapist":therapist_serializer.data
        }

        # print(serializer.data)

        return Response(response_data, status=status.HTTP_200_OK)



from datetime import datetime
class ListTherapistAdditionalDetailsAPI(GenericAPIView, ListModelMixin):
    serializer_class = TherapistAdditionalDetailsSerializer
    queryset = TherapistAdditionalDetails.objects.filter(
    therapist__status='listed'
    )
    def get(self, request, *args, **kwargs):
        therapist_additional_details = self.list(request, *args, **kwargs)


       

        # availability = TherapistAvailability.objects.all()
        # print(availability.date_timef)
        # serialzier = TherapistAvailabilitySerializer(availability, many=True)

        for item in therapist_additional_details.data:
            print(item['therapist'])

            availability = TherapistAvailability.objects.filter(therapist=item['therapist'], session_booked=False, date_time__gte=datetime.now()
            ).order_by('date_time').first()


           

            # 

            # datetime_obj = datetime.strptime(availability.date_time, "%Y-%m-%dT%H:%M:%SZ")
            # sprint(datetime_obj)
            # formatted_datetime = datetime_obj.strftime("%b %d, %Y, %I:%M %p")
            # print(formatted_datetime)

            if (availability):
                availability_serializer = TherapistAvailabilitySerializer(availability)
                print(availability_serializer.data)
                # datetime_obj = datetime.strptime(availability.date_time, "%Y-%m-%dT%H:%M:%SZ")
                # datetime_string=availability.date_time.strftime("%b %d, %Y %I:%M %p")
                # print(datetime_string)
                # formatted_datetime = datetime_obj.strftime("%b %d, %Y, %I:%M %p")
                item['next_available'] = availability_serializer.data["date_time"]
                # item['next_available'] = formatted_datetime
        for item in therapist_additional_details.data:

            print(item['therapist'])
            therapist = Therapist.objects.filter(id=item['therapist']).first()
            item['therapist_name'] = therapist.name

            # print(availability)
            
            # item['next_available'] = availability.date_time

        # print(therapist_additional_details.data)
        # response_data = {
        #     'therapist_additional_details': therapist_additional_details.data,
        #     # 'availability': serialzier.data
        # }

        return Response(therapist_additional_details.data, status=status.HTTP_200_OK)



class RetrievePreSignedUrlView(APIView):
    def get(self, request):
        url = s3.create_presigned_url()
        # print(url)
        return Response(url, status = status.HTTP_200_OK)

class RegisterTherapistView(APIView):
    def post(self, request):
        # print(request.data)
        name = request.data['name'] 
       
        email = request.data['email'] 
       
        phone = request.data['phone'] 
       
        password = request.data['password'] 

        serializer = CreateTherapistSerializer(data={
            "name":name,
            "email": email,
            "phone":phone,
            "password":password
        })

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        therapist = serializer.create(serializer.validated_data)
        # print(therapist)
        specialization = request.data['specialization'] 
        specializations = specialization.split(',')
        # print(specializations)

        technique = request.data['technique']
        techniques = technique.split(',')
        # print(techniques)

        fluency_data = []
        for key, value in request.data.items():
            if key.startswith('fluency'):
                fluency_data.append(value)
        #  print(fluency_data)

        additional_details = {
            'therapist':therapist.id,
            'age':request.data['age'], 
            'gender': request.data['gender'],
            'qualification': request.data['qualification'],
            'experience': request.data['experience'],
            'hoursPerWeek': request.data['hoursPerWeek'],
            'experience': request.data['experience'],
            'specialization': specializations,
            'technique': techniques,
            'describeYourSelf': request.data['describeYourSelf'],
            "fluency":fluency_data,
            'videoCallInfrastructure': request.data['videoCallInfrastructure'],
            'chat2to3TimesADay': request.data['chat2to3TimesADay'],
            'sessionPreferredTime': request.data['sessionPreferredTime'],
            'resume': request.data['resume'] 

        }
        serializer = TherapistAdditionalDetailsSerializer(data=additional_details)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        

        
       

        # print(describeYourSelf)
        # fluency = request.data['fluency'][0] 
        # parsed_fluency = json.loads(fluency)
        # print(fluency)
        
    

        return Response(serializer.data, status = status.HTTP_200_OK)

class LCTherapistAvailability(GenericAPIView, ListModelMixin, CreateModelMixin):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = TherapistAvailabilitySerializer
    queryset = TherapistAvailability.objects.all()


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

from datetime import datetime
class RetrieveTherapistAvailability(APIView):
    def get(self, request, date_time):
        print(request.user)
        thrapist = request.user
        print(date_time)
        availability = TherapistAvailability.objects.filter(date_time__date=date_time, therapist=thrapist.id).first()
        serialzier = TherapistAvailabilitySerializer(availability)
        # print(availability.date_time)
        # print(availability.date)
        # print(availability.time)

        return Response (serialzier.data, status=status.HTTP_200_OK)



# class RUDTherapistAvailability(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = TherapistAvailabilitySerializer
#     queryset = TherapistAvailability.objects.all()
#     lookup_field = 'date_time' 

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         datetime_value = self.request.query_params.get('date_time')
#         if datetime_value:
#             print(datetime_value)
#             datetime_obj = datetime.strptime(datetime_value, '%Y-%m-%dT%H:%M:%S')
#             queryset = queryset.filter(date_time=datetime_obj)
#             print(queryset)
#         return queryset


#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
