# Inventário Web

Sistema de inventário de ativos de TI construído com Django e PostgreSQL, baseado na planilha legada fornecida.

## Como o projeto funciona

O fluxo principal do Django é: **URL -> view -> modelo -> template**.

- `inventario/assets/models.py`: define o que é um ativo e como a vida útil é calculada.
- `inventario/assets/views.py`: recebe a requisição do navegador, aplica filtros e escolhe a página.
- `inventario/assets/forms.py`: transforma o modelo em formulário e valida os dados enviados.
- `templates/assets/`: contém o HTML que o usuário vê no navegador.
- `static/css/app.css`: contém o visual e as regras de adaptação para telas menores.
- `inventario/assets/management/commands/import_assets.py`: converte a planilha legada para registros no banco.
- `inventario/settings.py`: configura banco, idioma, horário e aplicações instaladas.

O campo `hostname` identifica cada ativo e é único. A coluna `NÚCLEO` representa o gerente ou diretor responsável. A idade importada da planilha é mantida em meses; novos ativos usam a data de compra. A meta operacional é de até 60 meses (5 anos).

## Primeiro contato com o código

1. Execute o projeto com SQLite usando o passo a passo abaixo.
2. Abra `/` para o dashboard e `/admin/` para a administração do Django.
3. Leia `models.py` para entender os dados, depois `views.py` para acompanhar uma requisição.
4. Altere o modelo somente quando a estrutura dos dados mudar; alterações de modelo exigem nova migration.
5. Depois de qualquer alteração, rode `py manage.py check` antes de iniciar o servidor.

Os comentários no código destacam decisões de negócio e pontos de configuração. Nomes simples e docstrings explicam a responsabilidade de cada parte sem repetir o que a própria linha já deixa claro.

## Desenvolvimento rápido com SQLite

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:USE_SQLITE="True"
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```

Acesse `http://127.0.0.1:8000/`.

## PostgreSQL

Copie `.env.example` para `.env`, ajuste as credenciais e remova `USE_SQLITE` do ambiente. Crie o banco `inventario` no PostgreSQL e execute `py manage.py migrate`.

## Importar a planilha

```powershell
py manage.py import_assets "caminho\Modelo Base Inventario(Base inventario).csv"
```

Para importar novamente e atualizar registros existentes pelo hostname, use `--atualizar`. O comando também aceita arquivos `.xlsx`.

## Hospedagem gratuita

O projeto está preparado para um serviço web Python e um PostgreSQL compatível com plano gratuito. O arquivo `render.yaml` contém o build e o comando de inicialização para o Render.

No serviço web, configure `DATABASE_URL`, `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False` e `DJANGO_ALLOWED_HOSTS` com o domínio fornecido. O build instala as dependências, coleta os arquivos estáticos e executa as migrations. Planos gratuitos podem suspender a aplicação sem acessos e ter limites de armazenamento, tráfego ou duração; confirme os limites atuais do provedor antes de usar em produção.

Para criar o primeiro usuário após o deploy, execute no Shell do provedor:

```bash
python manage.py createsuperuser
```
