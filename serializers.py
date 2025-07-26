from rest_framework import serializers
from django.contrib.auth.models import Permission,Group


class PermessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id','name', 'codename']

class GroupSerailizer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = ['id','name','permissions']
    def get_permissions(self,obj):
        permissions = obj.permissions.all()
        return PermessionSerializer(permissions,many=True).data
    
class GroupPermissionUpdateSerializer(serializers.Serializer):
    permissions = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        allow_null=False
    )
    def update(self, instance, validated_data):
        permissions = validated_data.get('permissions')
        if permissions is not None:
            permission_objects = Permission.objects.filter(id__in=permissions)
            instance.permissions.set(permission_objects)
        return instance
