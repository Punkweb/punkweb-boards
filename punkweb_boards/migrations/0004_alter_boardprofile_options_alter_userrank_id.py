# Generated by Django 4.2.2 on 2023-08-20 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('punkweb_boards', '0003_remove_boardprofile_metadata_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='boardprofile',
            options={'ordering': ('user',)},
        ),
        migrations.AlterField(
            model_name='userrank',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
