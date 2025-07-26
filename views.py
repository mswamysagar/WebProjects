from django.shortcuts import render

# Create your views here.
from .serializers import GroupSerailizer,PermessionSerializer,GroupPermissionUpdateSerializer
from django.contrib.auth.models import Group,Permission
from rest_framework.views import APIView
from core import messages
from rest_framework import status
from core.response import Response
from rest_framework.exceptions import ValidationError

# Create your views here.
class Permissions(APIView):
    def get(self,request):
        context={
            "success":1,
            "message":messages.DATA_FOUND,
            "data":{}
        }
        try:
            queryset = Permission.objects.all()
            serializer_class = PermessionSerializer(queryset,many=True)
            context['data'] = serializer_class.data
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    
class GroupList(APIView):
    def get(self,request):
        context={
            "success":1,
            "message":messages.DATA_FOUND,
            "data":{}
        }
        try:
            queryset = Group.objects.all()
            serializer_class = GroupSerailizer(queryset,many=True)
            context['data'] = serializer_class.data
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    
class GroupDetail(APIView):
    def get(self,request,pk):
        context={
            "success":1,
            "message":messages.DATA_FOUND,
            "data":{}
        }
        try:
            queryset = Group.objects.get(pk=pk)
            serializer_class = GroupSerailizer(queryset)
            context['data'] = serializer_class.data
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    
class GroupPostView(APIView):
    def post(self, request):
        context = {
            "success": 1,
            "message": "Data processed successfully.",
            "data": {}
        }
        try:
            data = request.data
            groupupdate = data.get('groupupdate')
            if groupupdate is None:
                raise ValidationError("The groupupdate field is required.")
            if not isinstance(groupupdate, list):
                raise ValidationError("The groupupdate field must be a list.")
            if not groupupdate:
                raise ValidationError("The groupupdate list cannot be empty.")
            for group_id in groupupdate:
                if not isinstance(group_id, int):
                    raise ValidationError(f"Invalid group ID: {group_id}. Must be an integer.")
                if group_id <= 0:
                    raise ValidationError(f"Invalid group ID: {group_id}. Must be a positive integer.")
            context['data'] = {"groupupdate": groupupdate}
            return Response(context, status=status.HTTP_200_OK)
        except ValidationError as e:
            context['success'] = 0
            context['message'] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GroupPermissionUpdateView(APIView):
    def get(self,request,pk):
        context={
            "success":1,
            "message":messages.DATA_FOUND,
            "data":{}
        }
        try:
            queryset = Group.objects.get(pk=pk)
            serializer_class = GroupSerailizer(queryset)
            context['data'] = serializer_class.data
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    def patch(self, request, pk):
        context={
            "success":1,
            "message":messages.DATA_SAVED,
            "data":{}
        }
        try:
            group = Group.objects.filter(pk=pk).first()
        except Exception as e:
            context["success"]=0
            context["message"]=str(e)
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        serializer = GroupPermissionUpdateSerializer(data=request.data)
        if serializer.is_valid():
            permissions = serializer.validated_data.get('permissions', [])
            current_permissions = list(group.permissions.all())
            permissions_to_add = []
            for permission_id in permissions:
                permission = Permission.objects.get(id=permission_id)
                if permission not in current_permissions:
                    permissions_to_add.append(permission)
            group.permissions.add(*permissions_to_add)
            return Response(context, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PermissionUpdateView(APIView):
    def get(self,request,pk):
        context={
            "success":1,
            "message":messages.DATA_FOUND,
            "data":{}
        }
        try:
            queryset = Group.objects.get(pk=pk)
            serializer_class = GroupSerailizer(queryset)
            context['data'] = serializer_class.data
        except Exception as e:
            context['success'] = 0
            context['message'] = str(e)
        return Response(context)
    def patch(self,request,pk):
        context={
            "success":1,
            "message":messages.DATA_SAVED,
            "data":{}
        }
        try:
            group = Group.objects.filter(pk=pk).first()
        except Exception as e:
            context["success"]=0
            context["message"]=str(e)
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        serializer = GroupPermissionUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(group, serializer.validated_data)
            return Response(context, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)