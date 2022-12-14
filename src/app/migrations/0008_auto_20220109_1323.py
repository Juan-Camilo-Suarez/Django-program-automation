# Generated by Django 3.2.9 on 2022-01-09 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0007_auto_20211219_1640"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="competence",
            options={"verbose_name": "компетенция", "verbose_name_plural": "компетенции"},
        ),
        migrations.AlterModelOptions(
            name="program",
            options={"verbose_name": "Программа", "verbose_name_plural": "Программы"},
        ),
        migrations.AlterModelOptions(
            name="thematicplanformlesson",
            options={"verbose_name": "количество часов по темам", "verbose_name_plural": "количество часов по темам"},
        ),
        migrations.AlterField(
            model_name="author",
            name="academic_tittle",
            field=models.CharField(
                choices=[("доцент", "доцент"), ("профессор", "профессор")], max_length=15, verbose_name="ученое звание"
            ),
        ),
        migrations.AlterField(
            model_name="program",
            name="form_training",
            field=models.CharField(
                choices=[("очное", "очное"), ("заочное", "заочное")], max_length=20, verbose_name="форма обучения"
            ),
        ),
        migrations.AlterField(
            model_name="program",
            name="language_choices",
            field=models.CharField(
                choices=[("русский", "русский"), ("англиский", "англиский")], max_length=20, verbose_name="язык"
            ),
        ),
        migrations.AlterField(
            model_name="program",
            name="type_discipline",
            field=models.CharField(
                choices=[("базовая", "базовая"), ("вариативная", "вариативная"), ("курс по выбору", "курс по выбору")],
                max_length=20,
                verbose_name="тип дисциплина",
            ),
        ),
        migrations.AlterField(
            model_name="thematicplanformlesson",
            name="count",
            field=models.IntegerField(verbose_name="количество часов"),
        ),
    ]
