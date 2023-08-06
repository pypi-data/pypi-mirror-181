from django.apps import apps
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.views.generic import View, DeleteView
from braces.views import LoginRequiredMixin


# import models
from django.contrib.auth.models import Group
from modelnotes.models import (Scope, Permission, Note)


def check_managability(user, note, action):
    """
    Determine if user can edit or delete this note. This note can be edited or deleted if at least one of the
    following criteria is met:
        - user is an admin
        - user is the author of the note
        - user is member of a group in groups AND note is proper permission is set
        - note is public and proper permission is set

    Args:
        user: django User object
        note: Note object
        action: (str) name of action to check for (edit or delete)

    Returns (bool):
        True if this note can be managed by the provided user
        False if this note can not be managed by the provided user
    """
    if action not in 'readeditdelete':
        return False
    if user.is_superuser:
        return True
    if note.author == user:
        return True
    if note.scope.name == 'group' and \
            any(i in user.groups.all() for i in note.groups.all()) and \
            action in [i.name for i in note.public_permissions.all()]:
        return True
    if note.scope.name == 'public' and action in [i.name for i in note.public_permissions.all()]:
        return True
    return False


class CreateNote(LoginRequiredMixin, View):
    """ create a note """
    def post(self, request, *args, **kwargs):
        """ process POST request """
        label = self.request.GET.dict().get('model', None)
        obj_id = self.request.GET.dict().get('id', None)
        title = self.request.GET.dict().get('title', None)
        scope_name = self.request.GET.dict().get('scope', None)
        groups = self.request.GET.dict().get('groups', None)
        permissions = self.request.GET.dict().get('permissions', None)
        content = self.request.GET.dict().get('content', None)

        try:
            if scope_name:
                scope = Scope.objects.get(name=scope_name)
            else:
                scope = None
            note = Note.objects.create(
                title=title,
                author=request.user,
                scope=scope,
                content=content,
                content_type=ContentType.objects.get(app_label=label.split('.')[0], model=label.split('.')[1]),
                object_id=obj_id,
            )

            if scope.name == 'group':
                group_list = Group.objects.filter(name__in=groups.split(','))
                for group in group_list:
                    if group not in note.groups.all():
                        note.groups.add(group)

            elif scope.name == 'public':
                permission_list = Permission.objects.filter(name__in=permissions.split(','))
                for permission in permission_list:
                    if permission not in note.public_permissions.all():
                        note.public_permissions.add(permission)

            messages.add_message(self.request, messages.INFO, f'note {note} successfully created',
                                 extra_tags='alert-info')
        except Exception as err:
            messages.add_message(request, messages.ERROR, str(err), extra_tags='alert-danger')
        return redirect(self.request.META.get('HTTP_REFERER'))


class UpdateNote(LoginRequiredMixin, View):
    """ update a note """
    def post(self, request, *args, **kwargs):
        """ process POST request """
        obj_id = self.request.GET.dict().get('id', None)
        title = self.request.GET.dict().get('title', None)
        scope_name = self.request.GET.dict().get('scope', None)
        groups = self.request.GET.dict().get('groups', None)
        permissions = self.request.GET.dict().get('permissions', None)
        content = self.request.GET.dict().get('content', None)
        new_groups = Group.objects.filter(name__in=groups.split(','))
        new_permissions = Permission.objects.filter(name__in=permissions.split(','))
        try:
            note = Note.objects.get_object_or_none(id=obj_id)
            scope = Scope.objects.get(name=scope_name)
            if check_managability(request.user, note, 'edit'):
                note.title = title
                note.scope = scope
                note.content = content

                # remove attached groups if note scope is not group
                if scope.name != 'group':
                    note.groups.remove(*note.groups.all())

                # remove attached public_permissions if note scope is not public
                if scope.name != 'public':
                    note.public_permissions.remove(*note.public_permissions.all())

                if scope.name == 'group':
                    for group in new_groups:
                        if group not in note.groups.all():
                            note.groups.add(group)
                    for group in note.groups.all():
                        if group not in new_groups:
                            note.groups.remove(group)

                if scope.name == 'public':
                    for permission in new_permissions:
                        if permission not in note.public_permissions.all():
                            note.public_permissions.add(permission)
                    for permission in note.public_permissions.all():
                        if permission not in new_permissions:
                            note.public_permissions.remove(permission)

                note.save()
                messages.add_message(self.request, messages.INFO, 'note successfully updated', extra_tags='alert-info')
            else:
                messages.add_message(self.request, messages.ERROR, f'This note can not be updated by {request.user}',
                                     extra_tags='alert-danger')
        except Exception as err:
            messages.add_message(request, messages.ERROR, err, extra_tags='alert-danger')
        return redirect(self.request.META.get('HTTP_REFERER'))


class DeleteNote(LoginRequiredMixin, DeleteView):
    """ delete a note (by pk) and return to the referring page """
    def delete(self, request, *args, **kwargs):
        note = Note.objects.get(**kwargs)
        if check_managability(request.user, note, 'delete'):
            note.delete()
            messages.add_message(self.request, messages.INFO, 'note successfully deleted', extra_tags='alert-info')
        else:
            messages.add_message(self.request, messages.ERROR, f'This note can not be deleted by {request.user}',
                                 extra_tags='alert-danger')
        return redirect(self.request.META.get('HTTP_REFERER'))
