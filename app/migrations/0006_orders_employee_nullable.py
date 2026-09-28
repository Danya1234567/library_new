from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('app', '0005_borrowabooks_employee_nullable')]
    operations = [
        migrations.AlterField(
            model_name='orders',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='users.employee'),
        ),
    ]
