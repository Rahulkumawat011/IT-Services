from apps.service.views import CreateServiceView, ListServiceView, ListServiceViewJson, UpdateServiceView, \
    DeleteServiceView
from django.urls import path

urlpatterns = [
    path('service/add', CreateServiceView.as_view(), name='service-add'),
    path('service/list', ListServiceView.as_view(), name='service-list'),
    path('service/list/ajax', ListServiceViewJson.as_view(), name='service-list-ajax'),
    path('service/edit/<int:pk>', UpdateServiceView.as_view(), name='service-edit'),
    path('service/delete/<int:pk>', DeleteServiceView.as_view(), name='service-delete'),

]