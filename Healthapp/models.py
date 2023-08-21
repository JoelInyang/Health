from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .managers import CustomUserManager
# Create your models here.

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    user_type = models.CharField(max_length=20)
    objects = CustomUserManager()
    
    
    groups = models.ManyToManyField(Group, related_name='custom_users', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custome_users', blank=True)
    
    
class PatientRecord(models.Model):
    #user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_records')
    Full_name = models.CharField(max_length=50)
    Date_of_birth = models.DateField()
    Gender = models.CharField(max_length=25)
    Address = models.CharField(max_length=80)
    phone_no = models.CharField(max_length=25)
    Medical_conditions = models.TextField()
    Emergency_contact_no = models.CharField(max_length=25)
    
class Appointment(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments_as_patient')
    health_worker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments_as_health_worker')
    appointment_date = models.DateTimeField()
    is_accepted = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    
    
    def __str__(self):
        return f"Appointment with {self.health_worker} on {self.appointment_date}"