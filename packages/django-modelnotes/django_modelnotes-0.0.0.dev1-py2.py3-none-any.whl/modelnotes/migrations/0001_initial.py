from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelnotes.models


def populate(apps, schema):
    """ populate Scope and Permission data """
    Permission = apps.get_model('modelnotes', 'Permission')
    Scope = apps.get_model('modelnotes', 'Scope')

    permission_list = [
        {'name': 'read', 'description': 'allowed to view note'},
        {'name': 'edit', 'description': 'allowed to edit note'},
        {'name': 'delete', 'description': 'allowed to delete note'},
    ]

    scope_list = [
        {'name': 'group', 'description': 'viewable to members of the defined group'},
        {'name': 'private', 'description': 'viewable only to the author'},
        {'name': 'public', 'description': 'viewable to everyone'},
    ]

    for permission in permission_list:
        Permission.objects.get_or_create(name=permission['name'], defaults=permission)
    for scope in scope_list:
        Scope.objects.get_or_create(name=scope['name'], defaults=scope)



class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(help_text='title for this note', max_length=32)),
                ('content', models.TextField(help_text='the actual content of this note')),
                ('object_id', models.PositiveIntegerField()),
                ('object_repr', models.CharField(blank=True, help_text='string representation of an object instance', max_length=128, null=True)),
                ('author', models.ForeignKey(blank=True, help_text='user who created this note', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('groups', models.ManyToManyField(blank=True, through='modelnotes.GroupPermission', to='auth.Group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='permission', max_length=16, unique=True)),
                ('description', models.CharField(help_text='description of this permission', max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Scope',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='name of this scope', max_length=16, unique=True)),
                ('description', models.CharField(help_text='description of this scope', max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PublicPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelnotes.note')),
                ('permission', models.ForeignKey(blank=True, help_text='actions that can be performed on a public scoped note', null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelnotes.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='note',
            name='public_permissions',
            field=models.ManyToManyField(blank=True, help_text='indicated actions that can be performed on this note when scope is set to public', through='modelnotes.PublicPermission', to='modelnotes.Permission'),
        ),
        migrations.AddField(
            model_name='note',
            name='scope',
            field=models.ForeignKey(blank=True, default=modelnotes.models.get_default_scope, help_text='sets access to this note', null=True, on_delete=django.db.models.deletion.SET_NULL, to='modelnotes.scope'),
        ),
        migrations.AddField(
            model_name='grouppermission',
            name='note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelnotes.note'),
        ),
        migrations.AddField(
            model_name='grouppermission',
            name='permissions',
            field=models.ManyToManyField(blank=True, help_text='actions that can be performed on a group scoped note', to='modelnotes.Permission'),
        ),

        migrations.RunPython(populate),
    ]
