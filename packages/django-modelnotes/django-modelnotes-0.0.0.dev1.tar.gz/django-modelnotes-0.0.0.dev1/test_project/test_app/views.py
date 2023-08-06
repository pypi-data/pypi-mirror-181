from django.shortcuts import render
from handyhelpers.views import HandyHelperListView

from test_app.models import Order


class ListOrders(HandyHelperListView):
    """ list available Order entries """
    queryset = Order.objects.all().select_related('product').prefetch_related('notes')
    title = 'Orders'
    page_description = ''
    table = 'test_app/table/orders.htm'
    modals = 'modelnotes/form/create_note.htm'
