from django.db.models.signals import post_save,post_delete
from . import models
from django.dispatch import receiver
from api import models as api_models

@receiver(post_save,sender=models.CustomUser)
def staff_extractor(sender,instance,created,**kwargs):
    # print('from signals = ',instance.user_type)
    # print(instance)
    if created:
        if instance.user_type == 'staff':
            pass
            # print('saving new stafff')
            # # add this user/instance details to staff table
            # name=instance.full_name
            # mobile = instance.mobile
            # email=instance.email
            # user_type=instance.user_type
            # # created_at=instance.created_at
            # # updated_at=instance.modified_at
            # instanse = api_models.Staff(name=name,mobile=mobile,email=email,user_type=user_type)
            # instanse.save()
        if instance.user_type is not None:
            # send email and password to any type of user through EMAIL
            pass
