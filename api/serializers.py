from rest_framework import serializers
from Healthapp.models import CustomUser, PatientRecord, Appointment
from rest_framework.validators import UniqueValidator

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)
    
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'phone_number', 'user_type')
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email = validated_data['email'],
           
            phone_number = validated_data['phone_number'],
            user_type = validated_data['user_type']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
    
    
class PatientRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRecord
        fields = '__all__'
        
        
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

