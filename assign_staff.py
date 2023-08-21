from Healthapp.models import CustomUser

"""This file is to assign a particular user to be a staff/medical practitioner """



def assign_staff(email):
    user = CustomUser.objects.filter(email=email)
    user.is_staff = True
    user.save()

# Call the function with the email of the user you want to assign as staff
#assign_staff('medical@example.com') #an example