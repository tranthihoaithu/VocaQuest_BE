# Generated by Django 5.1.1 on 2024-11-08 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn_voca', '0003_userprogress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('MC', 'Multiple Choice'), ('F', 'Fill In The Blank'), ('L', 'Listen And Choice')], default='MC', max_length=2),
        ),
    ]