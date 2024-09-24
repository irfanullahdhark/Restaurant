# Generated by Django 4.2.1 on 2023-07-12 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_site', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='post_sub',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='galerymodel',
            name='title',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='orderaddress',
            name='address',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='orderaddress',
            name='street',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='product',
            name='info',
            field=models.TextField(),
        ),
    ]
