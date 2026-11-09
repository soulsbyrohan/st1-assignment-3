
from datetime import datetime

import pytest

from smartcare.console import parse_date_time, format_appointment
from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


# Test 1: Valid date and time input
def test_console_valid_date_time():
    when = parse_date_time('2026-10-01 09:00')

    assert when == datetime(2026, 10, 1, 9, 0)


# Test 2: Invalid calendar date
def test_console_invalid_date():
    with pytest.raises(ValueError):
        parse_date_time('2026-02-30 09:00')


# Test 3: Invalid date/time format
def test_console_invalid_date_format():
    with pytest.raises(ValueError):
        parse_date_time('01/10/2026 09:00')


# Test 4: Format a scheduled appointment
def test_console_format_booking():
    store = SmartCareDataStore()

    PatientService(store).register_patient('P1', 'Alex Example')
    PractitionerService(store).register_practitioner(
        'D1', 'Taylor Example', 'General'
    )
    service = AppointmentService(store)

    appointment = service.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 10, 1, 9)
    )

    result = format_appointment(appointment)

    assert 'A1' in result
    assert 'P1' in result
    assert 'D1' in result
    assert '2026-10-01 09:00' in result
    assert 'scheduled' in result


# Test 5: Format a cancelled appointment
def test_console_format_cancellation():
    store = SmartCareDataStore()

    PatientService(store).register_patient('P1', 'Alex Example')
    PractitionerService(store).register_practitioner(
        'D1', 'Taylor Example', 'General'
    )
    service = AppointmentService(store)

    original = service.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 10, 1, 9)
    )

    cancelled = service.cancel_appointment('A1')

    result = format_appointment(cancelled)

    assert cancelled is original
    assert cancelled.status is AppointmentStatus.CANCELLED
    assert service.find_appointment('A1') is original
    assert 'A1' in result
    assert 'cancelled' in result
