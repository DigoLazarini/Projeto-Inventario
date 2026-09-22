# AGENTS.md

This repository is treated as a Django project unless the project structure proves otherwise. Keep changes aligned with Django conventions and favor the framework's built-in patterns over ad hoc implementations.

## Working assumptions

- Use the Django app structure: `manage.py` at the repo root, settings in a project package, app code under `apps/` or individual app folders.
- Prefer Django's ORM, forms, validation, authentication, admin, templates, and URL routing instead of custom wrappers.
- Keep business logic in app-specific modules or service helpers, not inside views unless the logic is trivial.
- Preserve project conventions for settings, environment variables, and migrations.

## Commands

Use the project’s existing Django commands when available. Typical commands for a Django repo include:

- `python manage.py check`
- `python manage.py test`
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver`
- `python manage.py collectstatic` (when static files are configured)

If the repo uses Poetry or pip-tools, follow that toolchain instead of inventing a new one. Keep dependency updates consistent with the existing project configuration.

## Code guidance

- Follow PEP 8 and keep imports organized.
- Prefer explicit, readable model and queryset code over clever shortcuts.
- Use `get_object_or_404()` for single-object fetches and validate user input before mutating data.
- For forms, rely on Django validation and model forms when appropriate.
- Keep templates, URLs, and forms in their conventional app locations.
- Add migrations only when the model structure actually changes.
- Avoid raw SQL unless the task clearly requires it.
- Do not commit secrets, environment files, or local database files.

## Security and quality

- Validate user permissions and authentication before sensitive actions.
- Use Django auth/session protections instead of custom session logic.
- Guard against CSRF and mass-assignment issues in forms and API endpoints.
- Keep database queries efficient; avoid N+1 patterns in list views and serializers.
- Prefer small, focused migrations and test coverage for model, view, and form changes.

## References

- [Django documentation](https://docs.djangoproject.com/)
- [Django tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- [Django settings](https://docs.djangoproject.com/en/stable/topics/settings/)
- [Django testing](https://docs.djangoproject.com/en/stable/topics/testing/)

## When editing this repo

- Respect the existing app boundaries and naming patterns.
- Preserve current settings split between development and production environments.
- Prefer incremental changes that fit the project’s architecture rather than introducing new frameworks or patterns.
- If a task is unclear, search for the relevant Django app and existing model/view/template conventions before making a change.
