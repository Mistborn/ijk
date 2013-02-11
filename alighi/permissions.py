from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.forms.models import fields_for_model

def flatten(seqofseqs):
    if seqofseqs is None:
        return None
    result = []
    for item in seqofseqs:
        if isinstance(item, (list, tuple)):
            result.extend(item)
        else:
            result.append(item)

class SpecialPermissionsChangeList(admin.views.main.ChangeList):
    def __init__(self, request, model, list_display, list_display_links,
            list_filter, date_hierarchy, search_fields, list_select_related,
            list_per_page, list_max_show_all, list_editable, model_admin):
        if model_admin.is_readonly(request):
            list_editable = []
        elif not model_admin.can_change_all(request):
            list_editable = [field for field in list_editable
                if field in model_admin.get_changeable_fields(request)]
            print list_editable
        super(SpecialPermissionsChangeList, self).__init__(
            request, model, list_display, list_display_links,
            list_filter, date_hierarchy, search_fields, list_select_related,
            list_per_page, list_max_show_all, list_editable, model_admin)
            
class SpecialPermissionsAdmin(admin.options.BaseModelAdmin):
    def get_view_permission(self):
        for (perm, desc) in self.model._meta.permissions:
            if perm.startswith('view_'):
                return perm
        return None
    def can_change_all(self, request):
        change_perm = 'alighi.{}'.format(
            self.model._meta.get_change_permission())
        return request.user.has_perm(change_perm)
    def can_change_any(self, request):
        return (self.can_change_all(request) or
                bool(self.get_changeable_fields(request)))
    def is_readonly(self, request):
        view_perm = 'alighi.{}'.format(self.get_view_permission())
        return (request.user.has_perm(view_perm) and not
                self.can_change_any(request))
    def get_readonly_fields(self, request, obj=None):
        fields = flatten(self.fields) or fields_for_model(self.model)
        sup = super(SpecialPermissionsAdmin, self).get_readonly_fields(
            request, obj)
        allfields = set(fields) | set(sup)
        if self.is_readonly(request):
            fields = allfields
        elif not self.can_change_all(request):
            fields = [f for f in allfields
                if f not in self.get_changeable_fields(request, obj)]
        else:
            fields = sup
        return fields
    def get_changeable_fields(self, request, obj=None):
        prefix = '{}.change_{}_'.format(
            self.model._meta.app_label,
            self.model._meta.module_name)
        perms = [(prefix+f, f)
            for f in self.model._meta.get_all_field_names()]
        return [field for (perm, field) in perms
                      if request.user.has_perm(perm)]
    def has_change_permission(self, request, obj=None):
        sup = super(SpecialPermissionsAdmin, self).has_change_permission(
            request, obj)
        return (sup or request.user.has_perm(
                    'alighi.{}'.format(self.get_view_permission())) or
                self.can_change_any(request))
    def get_changelist(self, request, **kw):
        return SpecialPermissionsChangeList
    def changelist_view(self, request, extra_context=None):
        if self.is_readonly(request) and request.method == 'POST':
            raise PermissionDenied
        return super(SpecialPermissionsAdmin, self).changelist_view(
            request, extra_context=extra_context)
    def change_view(self, request, object_id, form_url='', extra_context=None):
        if self.is_readonly(request) and request.method == 'POST':
            raise PermissionDenied
        return super(SpecialPermissionsAdmin, self).change_view(
            request, object_id,
            form_url=form_url, extra_context=extra_context)
    def save_model(self, request, obj, form, change):
        if change and obj.pk and not self.can_change_all(request):
            old_obj = obj.__class__.objects.get(pk=obj.pk)
            field_diff = [field
                    for field in obj._meta.get_all_field_names()
                    if getattr(obj, field) != getattr(old_obj, field)]
            if set(field_diff) - set(self.get_changeable_fields(request, obj)):
                raise PermissionDenied
        return super(SpecialPermissionsAdmin, self).save_model(
            request, obj, form, change)

