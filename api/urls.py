from django.urls import path
from .views import RegistrationView, LoginView, PatientRecordView, RecordStatistic,  UserStatistic, FilteredUsers, CreateAppointment, SearchHealthWorkers, ManageAppointment, AppointmentsStats


urlpatterns = [
    path('signup/', RegistrationView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='Login'),
    path('patient-records/', PatientRecordView.as_view(), name='patient-records'),
    path('rec_stat/', RecordStatistic.as_view(), name='rec_stat'),
    path('user_stat/', UserStatistic.as_view(), name='user_stat'),
    path('filtered-users/', FilteredUsers.as_view(), name='filtered-users'), #http://127.0.0.1:8000/filtered-users/?medical_condition=Malaria
    path('create-appointment/', CreateAppointment.as_view(), name='create-appointment'),
    path('search-health-workers/', SearchHealthWorkers.as_view(), name='search-health-workers'),#http://127.0.0.1:8000/search-health-workers/?search_term=peo@gmail.com (just search the the medical_practioner first name)
    path('manage-appointment/<int:appointment_id>/', ManageAppointment.as_view(), name='manage-appointment'),
    path('appointments-stats/', AppointmentsStats.as_view(), name='appointments-stats'),
]