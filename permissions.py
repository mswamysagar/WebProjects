from rest_framework import permissions
from authentication.models import CustomUser

class IsMedchoiceUser(permissions.BasePermission):
    
    def has_permission(self, request, view) -> bool:
        return bool(request.user and (request.user.user_type == CustomUser.UserType.SUPER_ADMIN 
                                      or request.user.user_type == CustomUser.UserType.STAFF or
                                        request.user.user_type == CustomUser.UserType.USER))
    
class HasMedchoice(permissions.BasePermission):

    message = "Staff is not assigned with any medchoice. Please contact admin."
    
    def has_permission(self, request, view) -> bool:
        return True if request.user.medchoice else False