# Generated by Django 4.2.4 on 2023-11-14 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0017_remove_comentario_usuario_alter_comentario_nombre'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instrumento',
            options={'ordering': ['usuario', '-fechaPublicacion']},
        ),
    ]