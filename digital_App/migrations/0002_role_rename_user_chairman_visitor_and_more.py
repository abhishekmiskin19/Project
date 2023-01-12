# Generated by Django 4.1.3 on 2023-01-05 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("digital_App", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Role",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "Role_Type",
                    models.CharField(
                        blank=True,
                        choices=[("M", "members"), ("C", "chairmans")],
                        default="",
                        max_length=5,
                    ),
                ),
            ],
            options={"db_table": "role",},
        ),
        migrations.RenameField(
            model_name="chairman", old_name="User", new_name="Visitor",
        ),
        migrations.RenameField(
            model_name="member", old_name="User", new_name="Visitor",
        ),
        migrations.RemoveField(model_name="chairman", name="FullName",),
        migrations.RemoveField(model_name="chairman", name="Gender",),
        migrations.RemoveField(model_name="chairman", name="Mobile",),
        migrations.RemoveField(model_name="member", name="Birthday",),
        migrations.RemoveField(model_name="member", name="FullName",),
        migrations.RemoveField(model_name="member", name="Gender",),
        migrations.RemoveField(model_name="member", name="Mobile",),
        migrations.RemoveField(model_name="watchman", name="User",),
        migrations.AddField(
            model_name="visitor",
            name="Birthday",
            field=models.DateField(default="2022-11-20"),
        ),
        migrations.AlterField(
            model_name="visitor",
            name="FullName",
            field=models.CharField(blank=True, default="", max_length=15),
        ),
    ]