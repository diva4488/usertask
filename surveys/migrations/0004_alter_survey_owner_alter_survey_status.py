# Generated by Django 5.0.4 on 2024-05-27 08:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("surveys", "0003_alter_user_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="survey",
            name="owner",
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name="survey",
            name="status",
            field=models.CharField(max_length=50),
        ),
    ]
