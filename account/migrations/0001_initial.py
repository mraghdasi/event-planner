# Generated by Django 4.2.10 on 2024-03-02 22:12

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import image_optimizer.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('image', image_optimizer.fields.OptimizedImageField(blank=True, null=True, upload_to='Profile')),
                ('phone_number', models.CharField(max_length=11)),
                ('role', models.CharField(choices=[('a', 'admin'), ('u', 'user')], max_length=2)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('users', models.ManyToManyField(related_name='teams', to='account.profile')),
            ],
        ),
    ]
