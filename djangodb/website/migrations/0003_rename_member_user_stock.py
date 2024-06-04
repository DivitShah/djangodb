# Generated by Django 4.2.13 on 2024-06-04 05:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_rename_members_member'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Member',
            new_name='User',
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ticker', models.CharField(max_length=10)),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.user')),
            ],
        ),
    ]
