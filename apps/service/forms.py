from django import forms

from apps.service.models import Service


class CreateServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["service_name", "payment_terms", "service_price", "service_package", "service_tax", "service_image", "active"]