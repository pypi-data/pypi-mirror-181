from django.db import DEFAULT_DB_ALIAS
from django.contrib.contenttypes.fields import GenericRelation
from modelnotes.models import Note


class ModelNoteField(GenericRelation):
    def __init__(self, pk_indexable=True, delete_related=True, **kwargs):
        kwargs['to'] = Note

        if pk_indexable:
            kwargs['object_id_field'] = 'object_id'
        else:
            kwargs['object_id_field'] = 'object_pk'

        kwargs['content_type_field'] = 'content_type'
        self.delete_related = delete_related
        super(ModelNoteField, self).__init__(**kwargs)

    def bulk_related_objects(self, objs, using=DEFAULT_DB_ALIAS):
        if self.delete_related:
            return super(ModelNoteField, self).bulk_related_objects(objs, using)
        return []
