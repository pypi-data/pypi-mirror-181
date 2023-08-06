from django.contrib import admin

# import models
from modelnotes.models import (Note, Permission)


def set_private(modeladmin, request, queryset):
    for item in queryset:
        item.scope = 'private'
        item.save()


def set_public(modeladmin, request, queryset):
    for item in queryset:
        item.scope = 'public'
        item.save()


set_private.short_description = 'set scope to private'
set_public.short_description = 'set scope to public'


class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'scope', 'content', 'content_type', 'object_id', 'object_repr', 'created_at', 'updated_at',]
    search_fields = ['title', 'scope', 'content', 'object_id', 'object_repr']
    list_filter = ['author', 'scope']
    actions = [set_private, set_public]

    def save_related(self, request, form, formsets, change):
        super(NoteAdmin, self).save_related(request, form, formsets, change)
        form.instance.public_permissions.add(Permission.objects.get_or_create(name='read')[0])


# register models
admin.site.register(Note, NoteAdmin)
