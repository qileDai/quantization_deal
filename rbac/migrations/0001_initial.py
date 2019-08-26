# Generated by Django 2.2.4 on 2019-08-16 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='菜单标题')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Menu', verbose_name='自关联')),
            ],
            options={
                'verbose_name_plural': '菜单表',
                'db_table': 'menu',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='权限标题')),
                ('url', models.CharField(max_length=128, unique=True, verbose_name='含正则的URL')),
                ('menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Menu', verbose_name='关联菜单')),
            ],
            options={
                'verbose_name_plural': '权限表',
                'db_table': 'permission',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='角色标题')),
                ('permissions', models.ManyToManyField(to='rbac.Permission', verbose_name='关联用户')),
            ],
            options={
                'verbose_name_plural': '角色表',
                'db_table': 'role',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('nickname', models.CharField(max_length=32, verbose_name='昵称')),
                ('email', models.EmailField(max_length=254)),
                ('roles', models.ManyToManyField(to='rbac.Role', verbose_name='关联角色')),
            ],
            options={
                'verbose_name_plural': '用户表',
                'db_table': 'userinfo',
            },
        ),
    ]
