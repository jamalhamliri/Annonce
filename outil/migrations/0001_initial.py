# Generated by Django 4.1.5 on 2023-03-11 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Etat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Etat')),
            ],
        ),
        migrations.CreateModel(
            name='Kilometrage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Kilometrage')),
            ],
        ),
        migrations.CreateModel(
            name='Origine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Origine')),
            ],
        ),
        migrations.CreateModel(
            name='Puissance_fiscale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Puissance fiscale')),
            ],
        ),
        migrations.CreateModel(
            name='Stockage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='capacite de stockage')),
            ],
        ),
        migrations.CreateModel(
            name='Telephone_Marque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Telephone Marque')),
                ('image', models.ImageField(blank=True, upload_to='media/Telephone_Marque/')),
            ],
        ),
        migrations.CreateModel(
            name='Type_Carburants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Type de carburant')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle_Marque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Marque')),
                ('image', models.ImageField(blank=True, upload_to='media/Vehicle_Marque/')),
            ],
        ),
        migrations.CreateModel(
            name='Voyage_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Type de voyage')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle_Modele',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Modele')),
                ('Marque', models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='outil.vehicle_marque')),
            ],
        ),
        migrations.CreateModel(
            name='Telephone_Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Telephone Modele')),
                ('marque', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='outil.telephone_marque')),
            ],
        ),
    ]