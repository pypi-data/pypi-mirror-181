from django.conf import settings
from django.shortcuts import render
from django.views.generic import (ListView)
from django.db.models import Q

from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
from handyhelpers.mixins.view_mixins import FilterByQueryParamsMixin


# import models
from django.contrib.auth.models import Group
from modelnotes.models import Note, Permission


class ListNotesBaseView(LoginRequiredMixin, FilterByQueryParamsMixin, ListView):
    base_template = getattr(settings, 'BASE_TEMPLATE', 'handyhelpers/handyhelpers_base_bs5.htm')
    template = 'handyhelpers/generic/bs5/generic_list.html'


class ListMyNotes(ListNotesBaseView):
    """ get modelnotes where user is the author """
    def get(self, request, *args, **kwargs):
        context = dict()
        self.queryset = Note.objects.filter(author=request.user).distinct().order_by('-updated_at').\
            select_related('author', 'scope', 'content_type').\
            prefetch_related('public_permissions', 'groups', 'content_object')
        context['base_template'] = self.base_template
        context['queryset'] = self.filter_by_query_params()
        context['title'] = 'Notes'
        context['subtitle'] = request.user.username
        context['table'] = 'modelnotes/table/list_notes.htm'
        context['modals'] = 'modelnotes/form/update_note.htm'
        context['groups'] = Group.objects.all()
        context['permissions'] = Permission.objects.all()
        return render(request, self.template, context=context)


class ListGroupNotes(ListNotesBaseView):
    """ get modelnotes with a scope of 'group' and authored by a member of a group user is also a member of """
    def get(self, request, *args, **kwargs):
        context = dict()
        self.queryset = Note.objects.filter(groups__user=request.user, scope__name='group').distinct()\
            .order_by('-updated_at'). \
            select_related('author', 'scope', 'content_type'). \
            prefetch_related('public_permissions', 'groups', 'content_object')
        context['base_template'] = self.base_template
        context['queryset'] = self.filter_by_query_params()
        context['title'] = 'Notes'
        context['subtitle'] = request.user.username + '\'s groups'
        context['table'] = 'modelnotes/table/list_notes.htm'
        context['modals'] = 'modelnotes/form/update_note.htm'
        context['groups'] = Group.objects.all()
        context['permissions'] = Permission.objects.all()
        return render(request, self.template, context=context)


class ListReadableNotes(ListNotesBaseView):
    """ get modelnotes that current user can read:
        - authored by user
        - with a scope of 'group' and authored by a member of a group user is also a member of
        - with a scope of 'public'
    """
    def get(self, request, *args, **kwargs):
        context = dict()
        self.queryset = Note.objects.filter(
            Q(author=request.user) |
            Q(groups__user=request.user, scope__name='group') |
            Q(scope__name='public')
        ).distinct().order_by('-updated_at'). \
            select_related('author', 'scope', 'content_type'). \
            prefetch_related('public_permissions', 'groups', 'content_object')
        context['base_template'] = self.base_template
        context['queryset'] = self.filter_by_query_params()
        context['title'] = 'Notes'
        context['subtitle'] = None
        context['table'] = 'modelnotes/table/list_notes.htm'
        context['modals'] = 'modelnotes/form/update_note.htm'
        context['groups'] = Group.objects.all()
        context['permissions'] = Permission.objects.all()
        return render(request, self.template, context=context)


class ListAllNotes(ListNotesBaseView, SuperuserRequiredMixin):
    """ get modelnotes all modelnotes (only available to superusers) """
    def get(self, request, *args, **kwargs):
        context = dict()
        self.queryset = Note.objects.all().distinct().order_by('-updated_at'). \
            select_related('author', 'scope', 'content_type'). \
            prefetch_related('public_permissions', 'groups', 'content_object')
        context['base_template'] = self.base_template
        context['queryset'] = self.filter_by_query_params()
        context['title'] = 'Notes'
        context['subtitle'] = 'all modelnotes'
        context['table'] = 'modelnotes/table/list_notes.htm'
        context['modals'] = 'modelnotes/form/update_note.htm'
        context['groups'] = Group.objects.all()
        context['permissions'] = Permission.objects.all()
        return render(request, self.template, context=context)
