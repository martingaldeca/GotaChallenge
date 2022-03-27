# Generated by Django 3.2.12 on 2022-03-27 16:08

import core.helpers.handle_storage
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Action',
                'verbose_name_plural': 'Actions',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('active', models.BooleanField(blank=True, help_text='Field that shows if the model is active(True) or deactivated (False)', null=True, verbose_name='Active')),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.helpers.handle_storage.handle_storage, verbose_name='Image')),
            ],
            options={
                'verbose_name': 'Device',
                'verbose_name_plural': 'Devices',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.helpers.handle_storage.handle_storage, verbose_name='Image')),
                ('food_type', models.CharField(blank=True, choices=[('fruit', 'Fruit'), ('vegetable', 'Vegetable'), ('meat', 'Meat'), ('fish', 'Fish'), ('cereal', 'Cereal'), ('legume', 'Legume'), ('nut', 'Nut'), ('tuber', 'Tuber'), ('dairy', 'Dairy'), ('egg', 'Egg')], db_index=True, max_length=20, null=True, verbose_name='Food type')),
                ('calories', models.FloatField(blank=True, help_text='Calories of the ingredient for each 100 gr of it', null=True, verbose_name='Calories')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Price')),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients',
            },
        ),
        migrations.CreateModel(
            name='RecipyStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.helpers.handle_storage.handle_storage, verbose_name='Image')),
                ('time', models.FloatField(help_text='Time required to complete the recipy step. All Recipy steps must have a defined time. All the times are in seconds', verbose_name='Time')),
                ('ordinal', models.IntegerField(blank=True, help_text='The ordinal number of the step in the recipy', null=True, verbose_name='Ordinal')),
                ('action', models.ForeignKey(help_text='The action to use in the recipy step. Only one action per step is allowed. All the recipy steps will require an action.', on_delete=django.db.models.deletion.PROTECT, related_name='recipy_steps', to='core.action', verbose_name='Action')),
                ('device', models.ForeignKey(blank=True, help_text='The device to use in the recipy step. Only one device per step is allowed. If the step does not require any device it will be None.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipy_steps', to='core.device', verbose_name='Device')),
            ],
            options={
                'verbose_name': 'Recipy step',
                'verbose_name_plural': 'Recipy steps',
            },
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.CreateModel(
            name='StepIngredientRelationShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('quantity', models.FloatField(help_text='The quantity required for the recipy step. All will be in gr.', verbose_name='Quantity')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ingredient')),
                ('recipy_step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.recipystep')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='recipystep',
            name='ingredients',
            field=models.ManyToManyField(help_text='All the needed ingredients in the recipy step', related_name='ingredients', through='core.StepIngredientRelationShip', to='core.Ingredient', verbose_name='Ingredients'),
        ),
        migrations.CreateModel(
            name='Recipy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.helpers.handle_storage.handle_storage, verbose_name='Image')),
                ('recipy_steps', models.ManyToManyField(help_text='All the recipy steps to follow in order to complete the recipy.', to='core.RecipyStep', verbose_name='Recipy steps')),
            ],
            options={
                'verbose_name': 'Recipy',
                'verbose_name_plural': 'Recipies',
            },
        ),
        migrations.CreateModel(
            name='DeviceActionRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(blank=True, help_text='Field that shows if the model is active(True) or deactivated (False)', null=True, verbose_name='Active')),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.action')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.device')),
            ],
            options={
                'verbose_name': 'Device action relation',
                'verbose_name_plural': 'Device action relations',
            },
        ),
        migrations.AddField(
            model_name='device',
            name='allowed_actions',
            field=models.ManyToManyField(blank=True, help_text='Allowed actions for the device. The actions can be active or not, you can check that info looking the through model.', related_name='allowed_actions', through='core.DeviceActionRelationship', to='core.Action', verbose_name='Allowed actions'),
        ),
    ]
