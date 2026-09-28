from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0004_alter_books_author_alter_books_genre'),
    ]
    operations = [
        migrations.AlterField(
            model_name='borrowabooks',
            name='employee',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='borrow_books',
                to='users.employee',
            ),
        ),
    ]
