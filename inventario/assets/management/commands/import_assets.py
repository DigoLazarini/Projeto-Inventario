import csv
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from inventario.assets.models import Asset


class Command(BaseCommand):
    """Comando para migrar o cadastro da planilha para o modelo Asset."""

    help = "Importa ativos de CSV separado por ponto e vírgula ou XLSX."

    def add_arguments(self, parser):
        parser.add_argument("arquivo", type=str)
        parser.add_argument("--atualizar", action="store_true", help="Atualiza ativos existentes pelo hostname.")

    def handle(self, *args, **options):
        path = Path(options["arquivo"])
        if not path.exists():
            raise CommandError(f"Arquivo não encontrado: {path}")
        rows = self._read_rows(path)
        created = updated = skipped = 0
        for row in rows:
            # Linhas vazias da planilha são ignoradas; o hostname identifica o ativo.
            hostname = self._value(row, "Hostname")
            if not hostname:
                skipped += 1
                continue
            # Estes nomes traduzem o layout legado para os campos normalizados do modelo.
            defaults = {
                "username": self._value(row, "Usuário", "Usuario"),
                "name": self._value(row, "Nome"),
                "email": self._value(row, "Email"),
                "processor": self._value(row, "Processador"),
                "ram": self._value(row, "Ram", "RAM"),
                "model": self._value(row, "Modelo"),
                "purchase_date": self._date(self._value(row, "Data de Compra")),
                "warranty_date": self._date(self._value(row, "Data de Garantia")),
                "rmm": self._value(row, "RMM"),
                "status": self._value(row, "Local"),
                "notes": self._value(row, "Observação", "Observacao"),
                "milvus": self._value(row, "MILVUS"),
                "xsolutions": self._value(row, "INFORMAÇÕES XSOLUTIONS", "INFORMACOES XSOLUTIONS"),
                "nucleo": self._value(row, "NÚCLEO", "NUCLEO"),
                "term": self._value(row, "TERMO"),
                "serial_number": self._value(row, "Nº de Série", "N° de Série", "N de Serie"),
                "source_age_months": self._integer(self._value(row, "Idade (meses)")),
                "imported_age": self._value(row, "Anos e meses"),
            }
            asset, was_created = Asset.objects.get_or_create(hostname=hostname, defaults=defaults)
            if was_created:
                created += 1
            elif options["atualizar"]:
                for key, value in defaults.items():
                    setattr(asset, key, value)
                asset.save()
                updated += 1
            else:
                skipped += 1
        self.stdout.write(self.style.SUCCESS(f"Importação concluída: {created} criados, {updated} atualizados, {skipped} ignorados."))

    def _read_rows(self, path):
        """Lê XLSX ou CSV e devolve cada linha como um dicionário de colunas."""
        if path.suffix.lower() == ".xlsx":
            # O modo somente leitura permite importar planilhas grandes sem carregá-las
            # integralmente como objetos editáveis do openpyxl.
            from openpyxl import load_workbook
            sheet = load_workbook(path, read_only=True, data_only=True).active
            values = list(sheet.values)
            headers = [str(value or "").strip() for value in values[0]]
            return [dict(zip(headers, row)) for row in values[1:]]
        # O CSV fornecido usa separador ; e a codificação típica do Excel no Windows.
        with path.open("r", encoding="cp1252", newline="") as file:
            return list(csv.DictReader(file, delimiter=";"))

    @staticmethod
    def _value(row, *keys):
        """Busca a primeira coluna disponível, aceitando variações de acentuação."""
        for key in keys:
            if key in row and row[key] is not None:
                value = str(row[key]).strip()
                if value:
                    return value
        return ""

    @staticmethod
    def _date(value):
        """Converte datas comuns da planilha; valores inválidos ficam vazios."""
        if not value:
            return None
        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
        return None

    @staticmethod
    def _integer(value):
        """Converte idade com vírgula decimal para meses inteiros."""
        try:
            return int(float(value.replace(",", "."))) if value else None
        except ValueError:
            return None
