# Generated by Django 4.1.3 on 2023-03-04 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0004_contacts_oerder_index'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contacts',
            options={'ordering': ('order_index',), 'verbose_name': 'Контакт', 'verbose_name_plural': 'Контакты'},
        ),
        migrations.RenameField(
            model_name='contacts',
            old_name='oerder_index',
            new_name='order_index',
        ),
    ]
