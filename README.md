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
- `inventario/assets/management/commands/import_hostings.py`: importa domínios e hospedagens da planilha de serviços.
- `inventario/settings.py`: configura banco, idioma, horário e aplicações instaladas.

O campo `hostname` identifica cada ativo e é único. A coluna `NÚCLEO` representa o gerente ou diretor responsável. A idade importada da planilha é mantida em meses; novos ativos usam a data de compra. A meta operacional é de até 60 meses (5 anos).

## Primeiro contato com o código

1. Execute o projeto com SQLite usando o passo a passo abaixo.
2. Abra `/login/` e entre com uma conta Django; depois acesse o inventário em `/inventario/`.
3. Leia `models.py` para entender os dados, depois `views.py` para acompanhar uma requisição.
4. Altere o modelo somente quando a estrutura dos dados mudar; alterações de modelo exigem nova migration.
5. Depois de qualquer alteração, rode `py manage.py check` antes de iniciar o servidor.

Os comentários no código destacam decisões de negócio e pontos de configuração. Nomes simples e docstrings explicam a responsabilidade de cada parte sem repetir o que a própria linha já deixa claro.

## Desenvolvimento local com SQLite

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:USE_SQLITE="True"
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```

O banco local fica em `data/inventario.sqlite3`. A pasta é criada automaticamente e ignorada pelo Git. Para escolher outro arquivo, configure `SQLITE_PATH`.

Acesse `http://127.0.0.1:8000/`.

Na primeira execução, crie uma conta administrativa para entrar no sistema:

```powershell
py manage.py createsuperuser
```

Use essa conta em `/login/`. Usuários autenticados podem consultar os dados; criar, editar e excluir exige as permissões padrão de adicionar, alterar e excluir ativos ou hospedagens. Um administrador pode criar usuários e atribuir essas permissões em `/admin/`.

## PostgreSQL

Copie `.env.example` para `.env`, ajuste as credenciais e remova `USE_SQLITE` do ambiente. Crie o banco `inventario` no PostgreSQL e execute `py manage.py migrate`.

## Importar a planilha

```powershell
py manage.py import_assets "caminho\Modelo Base Inventario(Base inventario).csv"
```

Para importar novamente e atualizar registros existentes pelo hostname, use `--atualizar`. O comando também aceita arquivos `.xlsx`.

## Hospedagens e domínios

Os serviços não físicos ficam em uma tabela separada dos equipamentos. Acesse `/hospedagens/` para listar, pesquisar, cadastrar, editar ou excluir esses registros. Para carregar a planilha de referência:

```powershell
py manage.py import_hostings "caminho\Base serviços de Hospedagens.xlsx"
```

O importador encontra a linha de cabeçalho automaticamente, preserva textos como `Expirado` e valores não numéricos como `***`, e pode ser executado novamente para atualizar registros correspondentes.

## Licenças Office

A tabela `/licencas-office/` importa somente `VERSÃO`, `Key`, `EMPRESA` e `USUÁRIO` da aba `Licenças Office`; as demais colunas da planilha são ignoradas. Para importar ou sincronizar novas linhas:

```powershell
py manage.py import_office_licenses "caminho\Inventário de máquinas.xlsx"
```

## Hospedagem gratuita

O projeto está preparado para um serviço web Python e um banco PostgreSQL no Render. O arquivo `render.yaml` contém o build e o comando de inicialização.

Antes de criar o serviço web, crie um PostgreSQL no Render e forneça sua Internal Database URL como `DATABASE_URL` ao configurar o Blueprint (`sync: false`). O `render.yaml` gera `DJANGO_SECRET_KEY` e configura `DJANGO_DEBUG=False`; o serviço recebe o host Render automaticamente. Para domínio personalizado, inclua o domínio em `DJANGO_ALLOWED_HOSTS` e sua origem HTTPS em `DJANGO_CSRF_TRUSTED_ORIGINS`, separados por vírgulas. O build instala as dependências, coleta os arquivos estáticos e executa as migrations.

O deploy executa migrations, mas não importa as planilhas. Uma base de produção nova começa sem registros de equipamentos, hospedagens ou licenças; importe somente dados reais depois do deploy. O SQLite local, arquivos `.env` e planilhas não devem ser enviados ao repositório.

Para criar o primeiro usuário após o deploy, execute no Shell do provedor:

```bash
python manage.py createsuperuser
```

