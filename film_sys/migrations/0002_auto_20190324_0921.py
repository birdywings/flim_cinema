# Generated by Django 2.0.2 on 2019-03-24 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('film_sys', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='index_label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='label', to='film_sys.IndexLabel', verbose_name='index_label'),
        ),
    ]
