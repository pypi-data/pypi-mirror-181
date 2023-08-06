import json

from django.conf import settings
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.http import require_GET

from modelnotes.views.action import check_managability

# import models
if 'auditlog' in settings.INSTALLED_APPS:
    from auditlog.models import LogEntry
from modelnotes.models import Note


@require_GET
def get_note_details(request):
    """
    Description:
        get details for a given Note.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'client_response' in request.GET:
            object_id = request.GET['client_response']
            obj = Note.objects.get(id=object_id)
            if not check_managability(request.user, obj, 'read'):
                return HttpResponse('Insufficient permissions', status=403)
            template = loader.get_template('modelnotes/ajax/detail_note.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'object': obj})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)


@require_GET
def get_note_auditlog(request):
    """
    Description:
        get AuditLog for a given Note.
    Args:
        request: AJAX request object.
    Returns:
        HttpResponse: JSON formatted response.
    """
    if (request.is_ajax()) and (request.method == 'GET'):
        if 'auditlog' not in settings.INSTALLED_APPS:
            return HttpResponse('auditlog is not installed', status=400)
        if 'client_response' in request.GET:
            obj_id = request.GET['client_response']
            queryset = LogEntry.objects.filter(content_type__model='note',
                                               object_id=obj_id)
            template = loader.get_template('handyhelpers/ajax/show_audit_log.htm')
            return HttpResponse(json.dumps({'server_response': template.render({'queryset': queryset})}),
                                content_type='application/javascript')
        else:
            return HttpResponse('Invalid request inputs', status=400)
    else:
        return HttpResponse('Invalid request', status=400)
