# Generated by Django 2.2.3 on 2019-10-22 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, null=True)),
                ('url', models.CharField(max_length=200, null=True)),
                ('perms', models.CharField(max_length=500, null=True)),
                ('type', models.IntegerField(choices=[(1, '目录'), (0, '菜单'), (2, '按钮')])),
                ('orderNum', models.IntegerField()),
                ('parentid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.NewMenu')),
            ],
            options={
                'ordering': ['orderNum'],
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True)),
                ('url', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rolename', models.CharField(max_length=64, unique=True)),
                ('menus', models.ManyToManyField(to='rbac.NewMenu')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('phone_number', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=128)),
                ('nickname', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
                ('status', models.SmallIntegerField(choices=[(0, '禁用'), (1, '正常')], default=1)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('roles', models.ManyToManyField(to='rbac.Role')),
            ],
            options={
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True)),
                ('url', models.CharField(max_length=32)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Menu')),
            ],
        ),
    ]
