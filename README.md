# Lead SLA CRM API

A production-minded Django REST Framework API for lead assignment, outreach tracking, conversion workflows, and 24-hour SLA enforcement.

This project demonstrates explicit business rules, service-layer architecture, selector-based queries, OpenAPI documentation, and automated testing.

## Tech Stack

* Python 3.13
* Django 5.x
* Django REST Framework
* PostgreSQL
* pytest
* drf-spectacular (OpenAPI / Swagger)
* Ruff

---

## Features

* Lead management (CRUD)
* UUID primary keys
* Soft delete support
* Lead assignment
* Contact attempt logging
* Lead conversion
* SLA deadline calculation
* Business rule validation
* OpenAPI (Swagger & ReDoc)
* Automated tests with pytest

---

## Business Rules Implemented

### Lead Creation

* SLA deadline is automatically set to **24 hours** after lead creation.

### Assignment

* Only **NEW** and **ASSIGNED** leads can be assigned.
* Assigning a lead sets:

  * `assigned_advisor`
  * `status = ASSIGNED`

### Contact Attempts

* Only **ASSIGNED** and **CONTACTED** leads accept contact attempts.
* **CONVERTED** and **CLOSED_LOST** leads reject new contact attempts.
* The first contact attempt with outcome **REACHED**:

  * sets `first_contacted_at`
  * changes status to `CONTACTED`
* Subsequent successful contact attempts do **not** modify `first_contacted_at`.

### Conversion

* Only **CONTACTED** leads can be converted.
* Conversion sets:

  * `status = CONVERTED`
  * `converted_at`

### Soft Delete

Deleted leads are excluded from list endpoints while remaining stored in the database.

---

## Assumption

The specification leaves reassignment behavior intentionally ambiguous.

**Decision:**

Reassigning a lead **does not reset the SLA deadline**, even if the lead has previous contact attempts that were not successful.

Reasoning:

The SLA measures the time between lead creation and the first successful contact, not advisor ownership. Resetting the deadline would allow bypassing the SLA simply by reassigning the lead.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/amiradmin/lead-sla-crm.git
cd lead-sla-crm
```

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements/local.txt
```

---

## Database

The project includes a Docker Compose configuration for PostgreSQL.

Start the database:

```bash
docker compose up -d
```

Run migrations:

```bash
python manage.py migrate
```

Create a superuser (optional):

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

---

## Running Tests

```bash
pytest
```

or

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -p django
```

---

## API Documentation

Generate the OpenAPI schema:

```bash
python manage.py spectacular --file schema.yml
```

Swagger UI:

```
/api/docs/
```

ReDoc:

```
/api/redoc/
```

OpenAPI schema:

```
/api/schema/
```

---

## Project Structure

```
apps/
└── leads/
    ├── models.py
    ├── services.py
    ├── selectors.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── tests/
```

Business logic is implemented in the **service layer**, while database queries are isolated in **selectors**.



---

## Architecture highlights

- Business workflows are implemented in a dedicated service layer.
- Read-oriented database access is isolated in selectors.
- API contracts are documented with OpenAPI, Swagger UI, and ReDoc.
- State transitions and SLA rules are covered by automated tests.
- UUID identifiers and soft deletion support production-oriented data handling.

## Collaboration

Questions, code reviews, improvement proposals, and focused pull requests are welcome. Please open an issue before making a substantial architectural change.

For broader backend, industrial AI, or open-source collaboration, join the [ForgeMind Discussions](https://github.com/amiradmin/ForgeMind/discussions).
