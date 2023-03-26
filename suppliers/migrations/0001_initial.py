# Generated by Django 4.1.3 on 2023-03-25 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileForSearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_file', models.FileField(upload_to='for_1C/from_site/%Y/%m/%d/', verbose_name='Файл')),
                ('hash_file', models.TextField(verbose_name='Хэшсумма')),
            ],
            options={
                'verbose_name': 'Файл для поиска',
                'verbose_name_plural': 'Файлы для поиска',
            },
        ),
        migrations.CreateModel(
            name='Suppliers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('INN', models.CharField(max_length=32, verbose_name='ИНН')),
                ('KPP', models.CharField(max_length=32, verbose_name='КПП')),
                ('OGRN', models.CharField(max_length=32, verbose_name='ОГРН')),
                ('title', models.CharField(max_length=320, verbose_name='Название')),
                ('full_title', models.CharField(default='', max_length=1320, verbose_name='Полное название')),
                ('email', models.EmailField(max_length=254, verbose_name='Електронная почта')),
                ('address', models.CharField(max_length=1320, verbose_name='Адрес фактический')),
                ('post_address', models.CharField(max_length=1320, verbose_name='Адрес почтовый')),
                ('type', models.CharField(max_length=32, verbose_name='Тип')),
                ('phone', models.TextField(verbose_name='Номер телефона')),
                ('site_url', models.URLField(max_length=320, verbose_name='Сайт')),
                ('price', models.FileField(blank=True, null=True, upload_to='', verbose_name='Прайс-лист')),
            ],
            options={
                'verbose_name': 'Поставщик',
                'verbose_name_plural': 'Поставщики',
            },
        ),
    ]