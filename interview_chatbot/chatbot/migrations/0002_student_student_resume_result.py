# Generated by Django 4.1.2 on 2022-10-14 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_resume_result',
            field=models.CharField(default='', max_length=50),
        ),
    ]
