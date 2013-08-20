import operator, json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models.loading import get_model
from django.db import models
from .admin import construct_search

@login_required
def get_matched_items(request):
    facet = request.GET.get('facet')
    searchTerm = request.GET.get('searchTerm')
    app_label = request.GET.get('app_label')
    model_name = request.GET.get('model_name')
    model = get_model(app_label, model_name)

    or_queries = []
    if facet.find('__') != -1:
        field = facet.split('__')[0]
        field_cls = model._meta.get_field_by_name(field)[0]
        model = field_cls.related.parent_model
        subfields = facet.split('__')[1:]
        orm_lookups = [construct_search(str(subfield))
                       for subfield in subfields]
        for orm_lookup in orm_lookups:
            or_queries.append(
                models.Q(
                    **{orm_lookup: searchTerm}
                )
            )
    else:
        subfields = [facet]
        or_queries.append(
            models.Q(
                **{construct_search(facet): searchTerm}
            )
        )
    results = model.objects.filter(reduce(operator.or_, or_queries))

    def get_field_value(obj, field):
        val = getattr(obj, field)
        if val:
            return val
        return u''

    result = [
        {
            'label': ' '.join([get_field_value(result, field) for field in subfields]),
            'value': unicode(result.pk)
        }
            for result in results[:10]
    ]
    return HttpResponse(json.dumps(result))