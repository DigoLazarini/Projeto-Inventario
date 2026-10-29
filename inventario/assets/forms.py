from django import forms

from .models import Asset, HostingService


class AssetForm(forms.ModelForm):
    """Formulário do cadastro; a validação básica vem do próprio modelo Django."""

    class Meta:
        model = Asset
        fields = [
            "hostname", "username", "name", "email", "processor", "ram", "model",
            "purchase_date", "warranty_date", "rmm", "status", "notes", "milvus",
            "xsolutions", "nucleo", "term", "serial_number",
        ]
        widgets = {
            "purchase_date": forms.DateInput(attrs={"type": "date"}),
            "warranty_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
            "xsolutions": forms.Textarea(attrs={"rows": 3}),
        }


class HostingServiceForm(forms.ModelForm):
    """Formulário para cadastrar ou atualizar domínio e hospedagem."""

    class Meta:
        model = HostingService
        fields = [
            "domain", "site", "provider", "management_url", "renewal_date",
            "renewal_note", "cost", "billing_cycle", "notes",
        ]
        widgets = {
            "renewal_date": forms.DateInput(attrs={"type": "date"}),
            "cost": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }
