from django.apps import apps
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from handyhelpers.models import HandyHelperBaseModel


if 'auditlog' in settings.INSTALLED_APPS:
    from auditlog.registry import auditlog
    from auditlog.models import AuditlogHistoryField


def get_default_scope():
    """ get the default scope """
    data = Scope.objects.get_or_create(name='private')[0]
    return data.id


class Scope(HandyHelperBaseModel):
    """ Track the scope of a note; build-in scopes include:
        private - viewable only to the author
        group   - viewable to members of groups set in the groups field
        public  - viewable to everyone
    """
    name = models.CharField(max_length=16, unique=True, help_text='name of this scope')
    description = models.CharField(max_length=16, help_text='description of this scope')

    def __str__(self):
        return self.name


class Permission(HandyHelperBaseModel):
    """ Track the permissions of a note; build-in permissions include:
        read   - allowed to view note
        edit   - allowed to edit note
        delete - allowed to delete note
    """
    name = models.CharField(max_length=16, unique=True, help_text='permission')
    description = models.CharField(max_length=16, help_text='description of this permission')

    def __str__(self):
        return self.name


class Note(HandyHelperBaseModel):
    """
    if scope is group, any member of the group can perform actions as set in permissions
    """
    title = models.CharField(max_length=32, help_text='title for this note')
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                               help_text='user who created this note')
    scope = models.ForeignKey(Scope, blank=True, null=True, default=get_default_scope,
                              on_delete=models.SET_NULL, help_text='sets access to this note')
    public_permissions = models.ManyToManyField(Permission, blank=True, through='PublicPermission',
                                                help_text='indicated actions that can be performed on this note when '
                                                          'scope is set to public')
    groups = models.ManyToManyField(Group, blank=True, through='GroupPermission')
    content = models.TextField(help_text='the actual content of this note')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    object_repr = models.CharField(max_length=128, blank=True, null=True,
                                   help_text='string representation of an object instance')
    content_object = GenericForeignKey('content_type', 'object_id')
    if 'auditlog' in settings.INSTALLED_APPS:
        history = AuditlogHistoryField()

    def clean(self):
        """ runs validations before saving """
        def verify_object_instance_exists():
            """ Check that the instance of an object, as identified by object_id, exists. If not, do not allow
            note to be attached. """
            try:
                content_type_object = ContentType.objects.get(id=self.content_type_id)
                model_class = apps.get_model(app_label=content_type_object.app_label,
                                             model_name=content_type_object.model)
            except Exception as err:
                raise ValidationError({'object_id': f'Failed to attach note: {err}'})
            try:
                model_class.objects.get(id=self.object_id)
            except model_class.DoesNotExist:
                raise ValidationError({'object_id': 'Can not attach a note to an instance that does not exists'})

        def set_obj_repr():
            """ set the object_repr """
            try:
                content_type_object = ContentType.objects.get(id=self.content_type_id)
                model_class = apps.get_model(app_label=content_type_object.app_label,
                                             model_name=content_type_object.model)
                content_instance = model_class.objects.get(id=self.object_id)
                self.object_repr = str(content_instance)
            except Exception as err:
                pass

        verify_object_instance_exists()
        set_obj_repr()

    def set_read_permission(self):
        """ automatically add the 'read' permission if scope is set to 'public' """
        # https://www.py4u.net/discuss/204721
        if self.scope and self.scope.name == 'public':
                self.public_permissions.add(Permission.objects.get_or_create(name='read')[0])

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Note, self).save(*args, **kwargs)
        self.set_read_permission()

    def __str__(self):
        return self.title


class GroupPermission(HandyHelperBaseModel):
    """ through table to link permissions to groups on a note """
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission, blank=True,
                                         help_text='actions that can be performed on a group scoped note')


class PublicPermission(HandyHelperBaseModel):
    """ through table to link public permissions on a note """
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, blank=True, null=True, on_delete=models.SET_NULL,
                                   help_text='actions that can be performed on a public scoped note')


if 'auditlog' in settings.INSTALLED_APPS:
    auditlog.register(Note)
