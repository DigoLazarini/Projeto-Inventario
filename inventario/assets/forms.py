from django import forms

from .models import Asset


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
