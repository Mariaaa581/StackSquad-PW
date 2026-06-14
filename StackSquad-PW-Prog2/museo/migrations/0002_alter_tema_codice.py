from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tema',
            name='codice',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
