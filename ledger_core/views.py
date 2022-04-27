import json
from django.http import HttpResponse
from django.views import View
from django.db.models import QuerySet


def _to_dict(data):
    if isinstance(data, list) or isinstance(data, QuerySet):
        return json.dumps([_to_dict(item) for item in data], sort_keys=True, default=str)
    else:
        to_dict = getattr(data, 'to_dict', None)
        if callable(to_dict):
            return to_dict()
        else:
            return getattr(data, '__dict__', data)


class APIBaseView(View):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        return HttpResponse(content_type="application/json", content=json.dumps(_to_dict(response), sort_keys=True, default=str))
