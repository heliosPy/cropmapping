# Generated by Django 3.0.11 on 2020-12-28 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('field', '0008_auto_20201228_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newfieldmodel',
            name='crop',
            field=models.CharField(choices=[('Rice', 'Rice'), ('Vegetables', 'Vegetables'), ('Cotton', 'Cotton'), ('Maize', 'Maize'), ('Cerials', 'Cerials'), ('Mango', 'Mango'), ('Others', 'Others')], max_length=30),
        ),
    ]
