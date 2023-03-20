# Generated by Django 4.1.3 on 2023-03-15 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0007_suppliers_kpp_suppliers_ogrn_suppliers_post_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileForSearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_file', models.FileField(upload_to='for_1C/from_site/%Y/%m/%d/', verbose_name='Файл')),
                ('hash_file', models.TextField(verbose_name='Хэсумма')),
            ],
            options={
                'verbose_name': 'Файл для поиска',
                'verbose_name_plural': 'Файлы для поиска',
            },
        ),
    ]