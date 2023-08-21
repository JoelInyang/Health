from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer, LoginSerializer, PatientRecordSerializer, CustomUserSerializer, AppointmentSerializer
from django.contrib.auth import authenticate
from Healthapp.models import PatientRecord, CustomUser, Appointment
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Q
from django.utils import timezone
from datetime import datetime

class RegistrationView(APIView):
    """
    The registration view class that inherit from APIView and handles the signup of users on the application
    """
    def post(self, request):
        """
        This handles the post request, since signing up is a post request. 
        JWT is involved that has refresh and access token respectively
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
               
                'refresh' : str(refresh),
                'access' : str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    This is the LoginView class that logs in the user after providing correct email and password using the JWTtokens for authentication
    """
    def post(self, request):
        """
        The post method of the LoginView, since the login is a post request by submitting the correct credentials
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email'].strip()  # Remove whitespace
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                #print('Hi')
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                })
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'detail': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)
    
    
class PatientRecordView(APIView):
    """
    This class for the Patient record that allows users to fill their medical information
    """
    
    def get(self, request):
        """
        returns the data present
        """
        records = PatientRecord.objects.filter(user=request.user)
        serializer = PatientRecordSerializer(records, many=True)
        return Response(serializer.data)
        
        
    def post(self, request):
        """
        post request, return the data submitted
        """
        
        data = request.data.copy()  # Copy the request data to modify
        data['user'] = request.user.id  # Set the user field to the authenticated user's ID
        serializer = PatientRecordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class RecordStatistic(APIView):
    """
    This class handles the display of medical records gotten from user, that users with a particular illness such as Ebola
    """
    
    def get(self, request):
        """
        returns the count data that is no of people with the sickness
        So it checks for the count of those with Ebola and gives the count which will be used to form a chart on the frontend
        """
        
        count = PatientRecord.objects.filter(Medical_conditions='Ebola').count()
        return Response({'count': count})
    
class UserStatistic(APIView):
    """
    This class provides data of all users present and their relevant medical records
    """
    def get(self, request):
        """
        returns User data available user data in database
        """
        if not request.user:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        users = CustomUser.objects.filter(user_type='medical_practitioner')
        user_serializer = CustomUserSerializer(users, many=True)
        
        records = PatientRecord.objects.all()
        record_serializer = PatientRecordSerializer(records, many=True)
        
        data = {'users': user_serializer.data, 'records': record_serializer.data}
        return Response(data)

    
class FilteredUsers(APIView):
    """
    This class filter users with only a particular sickness like malaria
    """
    
    def get(self, request):
        """
        This return users with the specified illness
        """
        medical_condition = request.query_params.get('medical_condition')

        if not medical_condition:
            return Response({'detail': 'Specify a medical condition'}, status=status.HTTP_400_BAD_REQUEST)

        medical_condition = medical_condition.strip()
        #print(f"Medical Condition: {medical_condition}")

        patients_with_condition = PatientRecord.objects.filter(Medical_conditions__contains=medical_condition)
        #print(patients_with_condition)
        #print(f"Queryset: {patients_with_condition}")

        filtered_patients = [
            {'full_name': patient.Full_name, 'phone_number': patient.phone_no}
            for patient in patients_with_condition
        ]

        return Response(filtered_patients)
    
    
    
class CreateAppointment(APIView):
    """
    Create Appointment class books an appointment with the medical practitioner 
    and sends the appointment to the mail of the medical practitioner
    """
    print('Hi')
    #permission_classes = [IsAuthenticated]
    
    print('Hiiiiii')
    def post(self, request):
        """
        Saves the appointment credentials and sends the appointment
        """
        print('Helo')
        print(request.META.get('HTTP_AUTHORIZATION'))
        print('Hi')
        health_worker_id = request.data.get('health_worker_id')
        appointment_date = request.data.get('appointment_date')
        user = request.user.id
        
        print(f"User: {user}")

        if not health_worker_id or not appointment_date:
            return Response({'detail': 'Provide health worker ID and appointment date'}, status=status.HTTP_400_BAD_REQUEST)

        # Remove leading and trailing whitespaces using strip()
        health_worker_id = health_worker_id.strip()

        try:
            health_worker = CustomUser.objects.get(id=health_worker_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Health worker not found'}, status=status.HTTP_404_NOT_FOUND)

        appointment = Appointment.objects.create(patient=request.user, health_worker=health_worker, appointment_date=appointment_date)

        # Send email notification to health worker
        subject = 'New Appointment Request'
        context = {
            'appointment': appointment,
            'patient': request.user,
            'health_worker': health_worker,
        }
        message = render_to_string('appointment_email_body.txt', context)
        plain_message = strip_tags(message)
        from_email = 'villateam@gmail.com'
        to_email = health_worker.email
        send_mail(subject, plain_message, from_email, [to_email], html_message=message)

        return Response({'detail': 'Appointment created and email sent, The concerned medical_practitioner will contact you accordingly'}, status=status.HTTP_201_CREATED)
        
class SearchHealthWorkers(APIView):
    """
    This class search for health practitioner
    """
    def get(self, request):
        """"
        returns the search result
        """
        search_term = request.query_params.get('search_term')

        if not search_term:
            return Response({'detail': 'Specify a search term'}, status=status.HTTP_400_BAD_REQUEST)

        health_workers = CustomUser.objects.filter(user_type='medical_practitioner', email__icontains=search_term) #Just type the medical_practitioner first name to search
        user_serializer = CustomUserSerializer(health_workers, many=True)

        return Response(user_serializer.data)
    
    
    
    
class ManageAppointment(APIView):
    """
    This class manages the appoint recieved by the health practitioner
    """
    
    def post(self, request, appointment_id):
        """Returns the response of the medical practitioner"""
        try:
            appointment = Appointment.objects.get(id=appointment_id, health_worker=request.user, status='pending')
        except Appointment.DoesNotExist:
            return Response({'detail': 'Appointment not found or already processed'}, status=status.HTTP_400_BAD_REQUEST)

        action = request.data.get('action')  # 'accept' or 'reject'
        if action == 'accept':
            appointment.status = 'accepted'
            appointment.save()

            # Send an email to the patient informing them of the accepted appointment
            patient_email = appointment.patient.email
            subject = 'Appointment Accepted'
            context = {'appointment': appointment}
            message = render_to_string('appointment_accepted_email_body.txt', context)
            plain_message = strip_tags(message)
            from_email = 'villateam@gmail.com'  # Update with your email
            send_mail(subject, plain_message, from_email, [patient_email], html_message=message)

        elif action == 'reject':
            appointment.status = 'rejected'
            appointment.save()

            # Send an email to the patient informing them of the rejected appointment
            patient_email = appointment.patient.email
            subject = 'Appointment Rejected'
            context = {'appointment': appointment}
            message = render_to_string('appointment_rejected_email_body.txt', context)
            plain_message = strip_tags(message)
            from_email = 'villateam@gmail.com'  # Update with your email
            send_mail(subject, plain_message, from_email, [patient_email], html_message=message)

        return Response({'detail': 'Appointment updated successfully'}, status=status.HTTP_200_OK)
    

class AppointmentsStats(APIView):
    "This class get the total number of appointments along with the one accepted and rejected "
    def get(self, request):
        """Returns the total number of appointments along with the one accepted and rejected"""
        # Get the current month and year
        current_month = timezone.now().month
        current_year = timezone.now().year

        # Calculate the total appointments booked and rejected for the current month
        appointments = Appointment.objects.filter(
            appointment_date__month=current_month, appointment_date__year=current_year
        )
        total_booked = appointments.filter(is_accepted=True).count()
        total_rejected = appointments.filter(is_accepted=False).count()

        # Return the stats as a response
        return Response({
            'total_booked': total_booked,
            'total_rejected': total_rejected
        })