# Generated by Django 5.1.3 on 2024-11-22 03:07

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelsdb', '0006_myperson_supplier'),
    ]

    operations = [
        migrations.CreateModel(
            name='Piece',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='OrderedPerson',
            fields=[
            ],
            options={
                'ordering': ['shirt_size'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('modelsdb.person',),
        ),
        migrations.RenameField(
            model_name='blog',
            old_name='slug',
            new_name='tagline',
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('article_piece', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='modelsdb.piece')),
            ],
            bases=('modelsdb.piece',),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_piece', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='modelsdb.piece')),
            ],
            bases=('modelsdb.piece',),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=255)),
                ('body_text', models.TextField()),
                ('pub_date', models.DateField()),
                ('mod_date', models.DateField(default=datetime.date.today)),
                ('number_of_comments', models.IntegerField(default=0)),
                ('number_of_pingbacks', models.IntegerField(default=0)),
                ('rating', models.IntegerField(default=5)),
                ('authors', models.ManyToManyField(to='modelsdb.author')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelsdb.blog')),
            ],
        ),
        migrations.CreateModel(
            name='BookReview',
            fields=[
                ('article_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='modelsdb.article')),
                ('book_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='modelsdb.book')),
            ],
            bases=('modelsdb.book', 'modelsdb.article'),
        ),
    ]
