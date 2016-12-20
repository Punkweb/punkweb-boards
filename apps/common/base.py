from django.shortcuts import render
from django.views.generic.base import TemplateView


class BaseQuery:
    def get_name(self):
        return 'BaseQuery'

    def get_context(self):
        return {}


class QueryView(TemplateView):
    template_name = 'base.html'

    def get_queries(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(QueryView, self).get_context_data(**kwargs)
        for query in self.get_queries():
            context.update({query.get_name(): query.get_context()})
        return context
