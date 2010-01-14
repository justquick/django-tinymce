from django.db.models import get_model
from django.contrib import admin
from django import forms
from widgets import TinyMCE
import settings

FIELDS = settings.ADMIN_FIELDS.copy()

for k,v in FIELDS.items():
    if isinstance(k, basestring):
        FIELDS[get_model(*k.split('.'))] = v
        del FIELDS[k]
        
class TinyMCEAdmin(admin.ModelAdmin):
    editor_fields = ()
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.editor_fields:
            return db_field.formfield(widget=TinyMCE())
        return super(TinyMCEAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        
for model,modeladmin in admin.site._registry.items():
    if model in FIELDS:
        admin.site.unregister(model)
        admin.site.register(model, type('newadmin', (TinyMCEAdmin, modeladmin.__class__), {
            'editor_fields': FIELDS[model],
        }))