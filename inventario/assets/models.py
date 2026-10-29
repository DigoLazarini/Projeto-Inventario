from django.db import models
from django.utils import timezone


class Asset(models.Model):
    """Representa um equipamento controlado pelo inventário de TI."""

    # Os valores seguem os status usados na planilha original.
    STATUS_CHOICES = [
        ("Em uso", "Em uso"),
        ("Estoque", "Estoque"),
        ("Manutenção", "Manutenção"),
        ("Obsoleto", "Obsoleto"),
        ("RPMA", "RPMA"),
        ("RPMA SERVIDOR", "RPMA servidor"),
    ]

    # Identificação e pessoa responsável pelo equipamento.
    hostname = models.CharField("hostname / patrimônio", max_length=120, unique=True)
    username = models.CharField("usuário", max_length=160, blank=True)
    name = models.CharField("nome", max_length=160, blank=True)
    email = models.EmailField("e-mail", blank=True)
    # Especificações físicas e datas de controle.
    processor = models.CharField("processador", max_length=255, blank=True)
    ram = models.CharField("RAM", max_length=40, blank=True)
    model = models.CharField("modelo", max_length=120, blank=True)
    purchase_date = models.DateField("data de compra", null=True, blank=True)
    warranty_date = models.DateField("data de garantia", null=True, blank=True)
    # Campos administrativos e observações operacionais.
    rmm = models.CharField(max_length=80, blank=True)
    status = models.CharField("status / local", max_length=40, choices=STATUS_CHOICES, blank=True)
    notes = models.TextField("observação", blank=True)
    milvus = models.CharField(max_length=80, blank=True)
    xsolutions = models.TextField("informações XSolutions", blank=True)
    nucleo = models.CharField("núcleo", max_length=160, blank=True)
    term = models.CharField("termo", max_length=40, blank=True)
    serial_number = models.CharField("número de série", max_length=160, blank=True)
    source_age_months = models.PositiveIntegerField("idade importada (meses)", null=True, blank=True)
    imported_age = models.CharField("anos e meses importado", max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["hostname"]
        verbose_name = "ativo"
        verbose_name_plural = "ativos"

    def __str__(self):
        return f"{self.hostname} - {self.model or 'Sem modelo'}"

    @property
    def age_months(self):
        # A planilha já traz a idade calculada na data da importação. Mantemos esse valor
        # para preservar a referência legada e calculamos a idade para novos cadastros.
        if self.source_age_months is not None:
            return self.source_age_months
        if not self.purchase_date:
            return None
        today = timezone.localdate()
        # O cálculo em meses evita arredondar anos incompletos para cima.
        months = (today.year - self.purchase_date.year) * 12
        months += today.month - self.purchase_date.month
        if today.day < self.purchase_date.day:
            months -= 1
        return max(months, 0)

    @property
    def age_label(self):
        if self.age_months is None:
            return "Não informada"
        years, months = divmod(self.age_months, 12)
        return f"{years}a {months}m"


class HostingService(models.Model):
    """Registra domínio, hospedagem e renovação como ativo não físico."""

    domain = models.CharField("domínio", max_length=255)
    site = models.CharField("site / situação", max_length=255, blank=True)
    provider = models.CharField("serviço / provedor", max_length=120)
    management_url = models.URLField("link de gerenciamento", max_length=500, blank=True)
    renewal_date = models.DateField("vencimento", null=True, blank=True)
    renewal_note = models.CharField("informação de vencimento", max_length=80, blank=True)
    cost = models.DecimalField("valor", max_digits=12, decimal_places=2, null=True, blank=True)
    cost_label = models.CharField("valor original da planilha", max_length=80, blank=True)
    billing_cycle = models.CharField("ciclo da assinatura", max_length=80, blank=True)
    notes = models.TextField("observações", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["domain", "provider", "renewal_date"]
        verbose_name = "hospedagem / domínio"
        verbose_name_plural = "hospedagens e domínios"

    def __str__(self):
        return f"{self.domain} - {self.provider}"

    @property
    def renewal_display(self):
        if self.renewal_date:
            return self.renewal_date.strftime("%d/%m/%Y")
        return self.renewal_note or "Não informado"

    @property
    def cost_display(self):
        if self.cost_label:
            return self.cost_label
        if self.cost is None:
            return "Não informado"
        return f"R$ {self.cost:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @property
    def status_label(self):
        today = timezone.localdate()
        if "inativo" in self.site.casefold():
            return "Inativo"
        if "expirado" in self.renewal_note.casefold() or "expirado" in self.billing_cycle.casefold():
            return "Expirado"
        if not self.renewal_date:
            return "Sem vencimento"
        if self.renewal_date < today:
            return "Vencido"
        if (self.renewal_date - today).days <= 30:
            return "Vence em até 30 dias"
        return "Ativo"


class OfficeLicense(models.Model):
    """Registra as licenças Office com os quatro campos selecionados da planilha."""

    version = models.CharField("VERSÃO", max_length=255)
    key = models.TextField("Key", blank=True)
    company = models.CharField("EMPRESA", max_length=255, blank=True)
    user = models.CharField("USUÁRIO", max_length=255, blank=True)

    class Meta:
        ordering = ["version", "company", "user"]
        verbose_name = "licença Office"
        verbose_name_plural = "licenças Office"

    def __str__(self):
        return f"{self.version} - {self.company or self.user or 'Sem atribuição'}"
