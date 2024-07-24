from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView

from application.custom_classes import AdminRequiredMixin, AjayDatatableView
from apps.service.forms import CreateServiceForm
from apps.service.models import Service


# Create your views here.


class CreateServiceView(SuccessMessageMixin, CreateView):
    model = Service
    form_class = CreateServiceForm
    template_name = 'service/form.html'
    success_message = "Service created successfully"
    success_url = reverse_lazy('service-list')


class ListServiceView(TemplateView):
    template_name = 'service/list.html'


class ListServiceViewJson(AdminRequiredMixin, AjayDatatableView):
    model = Service
    columns = ["service_name", "payment_terms", "service_price", "service_package", "service_tax", "service_image", "active", "actions"]
    exclude_from_search_columns = ['actions']

    def get_initial_queryset(self):
        return self.model.objects.all()

    def render_column(self, row, column):
        if column == 'active':
            if row.active:
                return '<span class="badge badge-success">Active</span>'
            else:
                return '<span class="badge badge-danger">Inactive</span>'

        if column == 'actions':
            # detail_action = '<a href={} role="button" class="btn btn-info btn-xs mr-1 text-white">Detail</a>'.format(
            #     reverse('admin-user-detail', kwargs={'pk': row.pk}))
            edit_action = '<a href={} role="button" class="btn btn-warning btn-xs mr-1 text-white">Edit</a>'.format(
                reverse('service-edit', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-xs" data-url={} role="button">Delete</a>'.format(
                reverse('service-delete', kwargs={'pk': row.pk}))
            return edit_action + delete_action
        else:
            return super(ListServiceViewJson, self).render_column(row, column)


class UpdateServiceView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Service
    form_class = CreateServiceForm
    template_name = 'service/form.html'
    success_message = "Service updated successfully"
    success_url = reverse_lazy('service-list')


class DeleteServiceView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Service
    success_url = reverse_lazy('service-list')