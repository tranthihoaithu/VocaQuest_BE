# Generated by Django 5.1.1 on 2024-11-19 15:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn_voca', '0005_question_correct_answer_useranswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='uploads/%Y/%m'),
            preserve_default=False,
        ),
    ]
