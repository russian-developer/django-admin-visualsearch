from django.contrib.admin.views.main import SEARCH_VAR, PAGE_VAR
from django.template import Library
import json

register = Library()

@register.inclusion_tag('admin/visualsearch/visual_search.html')
def visual_search(cl):
    return {
        'cl': cl,
        'query': json.dumps(cl.visualsearch_query).replace("'", "\'"),
        'keys': cl.model_admin.visualsearch_fields,
        'app_label': cl.model._meta.app_label,
        'model_name': cl.model.__name__,
        'show_result_count': cl.result_count != cl.full_result_count,
        'search_var': SEARCH_VAR,
        'page_var': PAGE_VAR
    } 