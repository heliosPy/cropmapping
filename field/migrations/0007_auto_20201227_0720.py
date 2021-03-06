# Generated by Django 3.0.11 on 2020-12-27 07:20

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('field', '0006_cropndvi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='mandal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crop_fields', to='field.Mandals'),
        ),
        migrations.CreateModel(
            name='NewFieldModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('farmer', models.CharField(max_length=50)),
                ('village', models.CharField(blank=True, max_length=100)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=7756)),
                ('crop', models.CharField(choices=[('Rice', 'Rice'), ('Vegetables', 'Vegetables'), ('Cotton', 'Cotton'), ('Maize', 'Maize'), ('Cerials', 'Cerials'), ('Others', 'Others')], max_length=30)),
                ('mandal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='field.Mandals')),
            ],
        ),
        migrations.CreateModel(
            name='IndicesModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('NDVI', 'NDVI'), ('EVI', 'EVI'), ('LSWI', 'LSWI'), ('Others', 'Others')], max_length=10)),
                ('date', models.DateField()),
                ('value', models.DecimalField(decimal_places=3, max_digits=4)),
                ('crop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ndvi_values', to='field.NewFieldModel')),
            ],
        ),
    ]
