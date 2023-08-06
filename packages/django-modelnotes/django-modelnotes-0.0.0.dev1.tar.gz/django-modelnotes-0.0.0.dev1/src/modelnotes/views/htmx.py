from django.shortcuts import render
from django.views.generic import (View)

# import models
from modelnotes.models import Permission


class GetScopeFields(View):
    """ get groups or permissions based on scope and build dropdown for create/edit modelnote form """
    def get(self, request):
        context = dict()
        scope = request.GET.get('scope')

        # set defaults
        context['option_list'] = None
        context['field'] = None
        context['multiple'] = None

        if scope == 'group':
            context['option_list'] = request.user.groups.all()
            context['select_id'] = 'id_group_select'
            context['multiple'] = True
        elif scope == 'public':
            context['option_list'] = Permission.objects.all()
            context['select_id'] = 'id_permission_select'
            context['multiple'] = True

        return render(request, template_name='modelnotes/snippet/select_options.htm', context=context)
