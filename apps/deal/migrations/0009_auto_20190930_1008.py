# Generated by Django 2.2.3 on 2019-09-30 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deal', '0008_merge_20190930_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robot',
            name='protection',
            field=models.SmallIntegerField(choices=[(1, '保护'), (0, '解除')], default=2),
        ),
        migrations.AlterField(
            model_name='robot',
            name='status',
            field=models.SmallIntegerField(choices=[(1, '运行中'), (0, '已停止'), (2, '运行中(保护)'), (3, '停止中(保护)')], default=0),
        ),
    ]
