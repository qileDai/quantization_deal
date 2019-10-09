#encoding: utf-8
from rest_framework import serializers
from .models import Role,UserInfo,Menu,Permission

class RoleSerializer(serializers.ModelSerializer):
    permission = Permission.title
    class Meta:
        model = Role
        fields = ('id','rolename','permission')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('id','title','accesskey','secretkey','users_id','platform')

class PermissonSerializer(serializers.ModelSerializer):
    menu = Menu.title
    class Meta:
        model = Permission
        fields = ('id','title','url','menu')

class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ('id','title','url','parent')



