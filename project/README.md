
# SmartCare — Stage 9

SmartCare is a Python-based appointment management system developed for Software Technology Assignment 3.

The application supports patient and practitioner registration, appointment booking, cancellation, lookup, and practitioner appointment listing through an interactive console.

## Requirements

- Python 3.13 or later
- pytest 8.3.5 for testing
- Python standard library for application runtime

Install development dependencies if required:

```bash
py -m pip install -r requirements-dev.txt
```

## Running SmartCare

Open a terminal inside the `project` directory.

### Interactive console

```bash
py main.py --interactive
```

The console provides the following options:

| Option | Function |
|---|---|
| 0 | Exit |
| 1 | Register patient |
| 2 | Find patient |
| 3 | Register practitioner |
| 4 | Find practitioner |
| 5 | Book appointment |
| 6 | Cancel appointment |
| 7 | Find appointment |
| 8 | List practitioner appointments |

### Standard demonstration

```bash
py main.py
```

This runs the application's predefined demonstration.

## Running Tests

Run the complete test suite:

```bash
py -m pytest -q
```

Run workflow tests only:

```bash
py -m pytest tests/test_workflows.py -v
```

The integrated Stage 12 regression run on commit
`3aa1be27cb16ca40da3732f4777c0d80b82d7376`
reported 99 passing tests.

## System Design

SmartCare separates its responsibilities across several Python modules:

- `domain.py` — domain entities, appointment statuses and business rules.
- `data_store.py` — in-memory storage for patients, practitioners and appointments.
- `services.py` — registration, booking, cancellation and lookup operations.
- `queries.py` — practitioner appointment selection, filtering and sorting.
- `console.py` — interactive user interface and input handling.
- `main.py` — application entry point.

## Appointment Rules

- Patient, practitioner and appointment IDs must be valid and unique.
- A practitioner cannot have two scheduled appointments at the same date and time.
- Different practitioners can have appointments at the same time.
- Cancelling an appointment changes its status without deleting its record.
- Cancelled appointments remain available for lookup and listing.
- Practitioner appointments can be filtered by scheduled, cancelled or completed status.
- Appointment listings are ordered chronologically.
- Invalid inputs are handled without terminating the console session.

## Date and Time Format

Appointments use the following input format:

`YYYY-MM-DD HH:MM`

Example: `2026-12-01 09:00`

## Data Storage and Limitations

SmartCare uses an in-memory data store shared by the application services during a session.

Data is not saved permanently and is lost when the application exits. Restart persistence is outside the current scope.

The application is intended for educational demonstration and testing. Use synthetic patient and practitioner information only.
