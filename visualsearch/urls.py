# coding: utf-8

from django.conf.urls import url
from views import get_matched_items

urlpatterns = [
    url('^get_matched_items/$',
        view=get_matched_items,
        name='get_matched_items'),
    ]
