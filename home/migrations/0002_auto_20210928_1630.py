# Generated by Django 3.2.4 on 2021-09-28 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_address',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='student_gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default=1, max_length=10),
            preserve_default=False,
        ),
    ]
