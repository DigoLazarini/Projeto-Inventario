from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AssetForm
from .models import Asset


@login_required
def dashboard(request):
    """Lista ativos e calcula indicadores sobre o conjunto atualmente filtrado."""
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    age_filter = request.GET.get("age", "").strip()
    assets = Asset.objects.all()
    if query:
        assets = assets.filter(
            Q(hostname__icontains=query) | Q(name__icontains=query) |
            Q(username__icontains=query) | Q(serial_number__icontains=query) |
            Q(model__icontains=query)
        )
    if status:
        assets = assets.filter(status=status)
    # A idade é uma propriedade Python porque combina a idade legada com a data de compra.
    # Por isso o filtro é aplicado depois da consulta ao banco e antes da paginação.
    if age_filter == "up_to_5":
        assets = [asset for asset in assets if asset.age_months is not None and asset.age_months <= 60]
    elif age_filter == "over_5":
        assets = [asset for asset in assets if asset.age_months is not None and asset.age_months > 60]
    ages = [asset.age_months for asset in assets if asset.age_months is not None]
    # Sessenta meses representa a meta de vida útil definida para os equipamentos.
    average_age = round(sum(ages) / len(ages)) if ages else None
    average_age_label = "-"
    if average_age is not None:
        years, months = divmod(average_age, 12)
        average_age_label = f"{years} anos e {months} meses"
    paginator = Paginator(assets, 25)
    page = paginator.get_page(request.GET.get("page"))
    context = {
        "page": page,
        "query": query,
        "selected_status": status,
        "statuses": Asset.STATUS_CHOICES,
        "total": len(assets),
        "in_use": sum(asset.status == "Em uso" for asset in assets),
        "stock": sum(asset.status == "Estoque" for asset in assets),
        "maintenance": sum(asset.status == "Manutenção" for asset in assets),
        "average_age_label": average_age_label,
        "selected_age": age_filter,
        "age_choices": [("up_to_5", "Até 5 anos"), ("over_5", "Acima de 5 anos")],
    }
    return render(request, "assets/dashboard.html", context)


@login_required
def asset_detail(request, pk):
    """Exibe um ativo; 404 é retornado quando o identificador não existe."""
    return render(request, "assets/detail.html", {"asset": get_object_or_404(Asset, pk=pk)})


@login_required
def asset_create(request):
    """Mostra o formulário vazio e cria um ativo quando os dados são válidos."""
    form = AssetForm(request.POST or None)
    if form.is_valid():
        asset = form.save()
        messages.success(request, "Ativo cadastrado com sucesso.")
        return redirect("assets:detail", pk=asset.pk)
    return render(request, "assets/form.html", {"form": form, "title": "Novo ativo"})


@login_required
def asset_update(request, pk):
    """Edita um ativo existente usando a mesma validação do cadastro."""
    asset = get_object_or_404(Asset, pk=pk)
    form = AssetForm(request.POST or None, instance=asset)
    if form.is_valid():
        form.save()
        messages.success(request, "Ativo atualizado com sucesso.")
        return redirect("assets:detail", pk=asset.pk)
    return render(request, "assets/form.html", {"form": form, "title": "Editar ativo", "asset": asset})


@login_required
def asset_delete(request, pk):
    """Exige confirmação via POST antes de remover um registro."""
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == "POST":
        asset.delete()
        messages.success(request, "Ativo excluído.")
        return redirect("assets:dashboard")
    return render(request, "assets/delete.html", {"asset": asset})
