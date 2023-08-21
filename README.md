A web app with the following requirements:
Stack: Django

Checklist
-	Users are to login with their email not username
-	Email and phone number must be unique for every user

Functionalities and corresponding endpoints
1.	Sign up page for users- A user can either sign-up as a health worker or as a normal patient.

        http://localhost:8000/signup/
        http://localhost:8000/login/

2.	A page were normal users/patients can fill in their medical information with relevant questions depending on the developer's discretion.

        http://localhost:8000/patient-records/

3.	A page that displays the statistical details of the medical records gotten from the users (all users can view this page). e.g. multi charts that shows the count for users with Ebola.

        http://127.0.0.1:8000/rec_stat/

4.	A table that displays all users and their relevant medical records (only users registered as medical practitioners can view this page).

       http://127.0.0.1:8000/user_stat/

5.	A drop-down filter to show users with specified medical records of your own discretion e.g. show only users with malaria.

       http://127.0.0.1:8000/filtered-users/?medical_condition=Malaria
       #malaria can be replaced with another sickness


6.	Users should be able to search for any health worker and be able to book appointment with him or her and the health worker should be able to receive a mail about the appointment with information about who wants to book the appointment, date and time.

        http://127.0.0.1:8000/search-health-workers/?search_term=zeo
        #where zeo is the health worker name, it can be replaced with another health worker

        http://127.0.0.1:8000/create-appointment/


7.	A health worker should be able to either accept or reject an appointment through his dashboard.

        http://127.0.0.1:8000/manage-appointment/1/
        where 1 is the appointment_id

8.	Total number of appointments booked and rejected for a particular month should be visible to a health worker when he/she logs into his dashboard


        http://127.0.0.1:8000/appointments-stats/