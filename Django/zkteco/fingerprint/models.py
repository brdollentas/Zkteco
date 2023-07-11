from django.db import models

# Create your models here.
class Fingerprints(models.Model): 
    biometric_id = models.BigIntegerField()
    finger_number = models.SmallIntegerField()
    class Meta:
        db_table = 'fingerprints'


class BiometricDevices(models.Model):
    host = models.CharField(max_length=129)
    port = models.CharField(max_length=20)
    status = models.SmallIntegerField() 
    objects = models.Manager()
    def __str__(self):
        return self.host
    class Meta:
        db_table = 'biometric_devices'


class BiometricRfidUsers(models.Model):
    user_id = models.BigIntegerField()
    device_user_id = models.BigIntegerField()
    unique_id = models.CharField(max_length=9)
    class Meta:
        db_table = 'biometric_rfid_users'

class Users(models.Model):
    name = models.CharField(max_length=191)
    class Meta:
        db_table = 'users'

Users.objects = Users.objects.using('nkti')

    

    
