from django.db.models import get_model
from django.contrib import admin
from widgets import TinyMCE
import settings

FIELDS = settings.ADMIN_FIELDS.copy()

for k,v in FIELDS.items():
    if isinstance(k, basestring):
        FIELDS[get_model(*k.split('.'))] = v
        del FIELDS[k]
        
class TinyMCEAdmin(admin.ModelAdmin):
    fidgets = ()
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.fidgets:
            return db_field.formfield(widget=TinyMCE(attrs={'cols': 40, 'rows': 20}))
        return super(TinyMCEAdmin, self).formfield_for_dbfield(db_field, **kwargs)

for model,modeladmin in admin.site._registry.items():
    if model in FIELDS:
        admin.site.unregister(model)
        admin.site.register(model, type('newadmin', (TinyMCEAdmin, modeladmin.__class__), {'fidgets': FIELDS[model]}))