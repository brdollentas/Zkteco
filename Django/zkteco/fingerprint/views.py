from django.shortcuts import render
from zk import ZK, const
from .models import *
# Create your views here.
def index(request):
    conn = None
    devices = BiometricDevices.objects.filter(status = 1)
    for device in devices:
    # create ZK instance
        zk = zkInit(device.host, int(device.port))
        other_device = BiometricDevices.objects.filter(status = 1).exclude(id = device.id)
        try:
            # connect to device
            conn = zk.connect()
            # disable device, this method ensures no activity on the device while the process is run
            conn.disable_device()
            # another commands will be here!
            #Example: Get All Users
            users = conn.get_user()
            for index, user in enumerate(users):
                print (index+1,'out of',len(users),'users fingerprints synced')
                print ('+ UID        : {}'.format(user.uid))
                print ('  Name       : {}'.format(user.name))
                print ('  User  ID   : {}'.format(user.user_id))
                index_finger = []
                for i in range(10):
                    fingerprint = conn.get_user_template(uid=user.uid, temp_id=i)
                    if fingerprint:
                       index_finger.append(fingerprint)
                for zkdevice in other_device:
                    teco = zkInit(zkdevice.host, int(zkdevice.port))
                    connect = teco.connect()
                    connect.disable_device()
                    connect.save_user_template(user, index_finger)
                    connect.enable_device()
            conn.test_voice()
            # re-enable device after all commands already executed
            conn.enable_device()
        except Exception as e:
            print ("Process terminate : {}".format(e))
        finally:
            if conn:
                conn.disconnect()
    return render(request, 'index.html')

def zkInit(host, port):
    return ZK(host, port=port, timeout=5, password=0, force_udp=False, ommit_ping=False)

def syncFingerPerUser(request):
    conn = None
    devices = BiometricDevices.objects.filter(status = 1)
    for device in devices:
        zk = zkInit(device.host, int(device.port))
        other_device = BiometricDevices.objects.filter(status = 1).exclude(id = device.id)
        try:
            # connect to device
            conn = zk.connect()
            # disable device, this method ensures no activity on the device while the process is run
            conn.disable_device()
            # another commands will be here!
            bio = BiometricRfidUsers.objects.filter(user_id = request.id)
            # user_device = UserTemplate(bio[0].device_user_id, user[0].name, bio[0].unique_id)
            users = conn.get_users()
            find_user = None
            for user in users:
                if user.uid == bio[0].device_user_id:
                   find_user = user
                   break 
            index_finger = []
            for i in range(10): 
                fingerprint = conn.get_user_template(uid=bio[0].device_user_id, temp_id=i)
                if fingerprint:
                    index_finger.append(fingerprint)
            for zkdevice in other_device:
                teco = zkInit(zkdevice.host, int(zkdevice.port))
                connect = teco.connect()
                connect.disable_device()
                connect.save_user_template(find_user, index_finger)
                connect.enable_device()
            conn.test_voice()
            # re-enable device after all commands already executed
            conn.enable_device()
        except Exception as e:
            print ("Process terminate : {}".format(e))
        finally:
            if conn:
                conn.disconnect()
    return render(request, 'index.html')