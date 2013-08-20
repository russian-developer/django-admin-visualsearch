
import operator
from django.core.exceptions import SuspiciousOperation, ImproperlyConfigured
from django.contrib.admin.options import IncorrectLookupParameters
from django.contrib.admin.views.main import ChangeList, SEARCH_VAR, PAGE_VAR
from django.db import models
import json

def construct_search(field_name):
    if field_name.startswith('^'):
        return "%s__istartswith" % field_name[1:]
    elif field_name.startswith('='):
        return "%s__iexact" % field_name[1:]
    elif field_name.startswith('@'):
        return "%s__search" % field_name[1:]
    else:
        return "%s__icontains" % field_name

class VisualSearchChangeList(ChangeList):

    def __init__(self, request, *a, **k):
        super(VisualSearchChangeList, self).__init__(request, *a, **k)
        try:
            self.page_num = int(request.POST.get(PAGE_VAR, 0))
        except ValueError:
            self.page_num = 0

    def get_query_set(self, request):
        (self.filter_specs, self.has_filters, remaining_lookup_params,
         use_distinct) = self.get_filters(request)
        qs = self.root_query_set
        for filter_spec in self.filter_specs:
            new_qs = filter_spec.queryset(request, qs)
            if new_qs is not None:
                qs = new_qs
        try:
            qs = qs.filter(**remaining_lookup_params)
        except (SuspiciousOperation, ImproperlyConfigured):
            raise
        except Exception as e:
            raise IncorrectLookupParameters(e)
        if not qs.query.select_related:
            if self.list_select_related:
                qs = qs.select_related()
            else:
                for field_name in self.list_display:
                    try:
                        field = self.lookup_opts.get_field(field_name)
                    except models.FieldDoesNotExist:
                        pass
                    else:
                        if isinstance(field.rel, models.ManyToOneRel):
                            qs = qs.select_related()
                            break
        ordering = self.get_ordering(request, qs)
        qs = qs.order_by(*ordering)

        self.visualsearch_query = request.POST.get(SEARCH_VAR, '')
        try:
            self.visualsearch_query = json.loads(self.visualsearch_query)
        except ValueError:
            self.visualsearch_query = None
        if self.search_fields and self.visualsearch_query:
            and_queries = []
            for bit in self.visualsearch_query:
                if bit['key'] in self.search_fields:
                    if bit['key'].find('__') != -1:
                        field = bit['key'].split('__')[0]
                        field_cls = qs.model._meta.get_field_by_name(field)[0]
                        model = field_cls.related.parent_model
                        model.objects.get(pk=bit['object_pk'])
                        and_queries.append(models.Q(**{field: model.objects.get(pk=bit['object_pk'])}))
                    else:
                        and_queries.append(
                            models.Q(pk=bit['object_pk'])
                        )
            qs = qs.filter(reduce(operator.and_, and_queries))
        return qs


class VisualSearchAdmin(object):
    change_list_template = 'admin/visualsearch/change_list.html'

    def __init__(self, *a, **k):
        self.search_fields = self.visualsearch_fields.keys()
        super(VisualSearchAdmin, self).__init__(*a, **k)

    def get_changelist(self, request, **k):
        return VisualSearchChangeList

    class Media:
        css = {
            'all': ('css/visualsearch-datauri.css',)
        }
        js = ('js/dependencies.js', 'js/visualsearch.js')