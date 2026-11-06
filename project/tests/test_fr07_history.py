"""Stage 7: FR-07 / AC-05.2 cancelled appointment history integration tests.
"""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import AppointmentService, PatientService, PractitionerService


WHEN = datetime(2026, 10, 1, 9, 0)


def make_registered_services():
    """Create independent participants in one shared store for each test."""
    store = SmartCareDataStore()
    patient = PatientService(store).register_patient('P1', 'Alex Example')
    practitioner = PractitionerService(store).register_practitioner(
        'D1', 'Taylor Example', 'General'
    )
    return store, patient, practitioner, AppointmentService(store)


def test_fr07_cancelled_history_is_found_by_id_and_in_list():
    """TEST-FR07-01: cancelling preserves the same stored appointment."""
    store, _, _, service = make_registered_services()
    original = service.book_appointment('A1', 'P1', 'D1', WHEN)

    cancelled = service.cancel_appointment('A1')

    assert cancelled is original
    assert original.status is AppointmentStatus.CANCELLED
    assert service.find_appointment('A1') is original
    assert store.find_appointment('A1') is original
    assert store.list_appointments() == [original]


def test_fr07_rebooking_does_not_erase_cancelled_history():
    """TEST-FR07-02: old CANCELLED and new SCHEDULED records coexist."""
    store, _, _, service = make_registered_services()
    original = service.book_appointment('A1', 'P1', 'D1', WHEN)
    service.cancel_appointment('A1')

    replacement = service.book_appointment('A2', 'P1', 'D1', WHEN)

    assert original is not replacement
    assert original.status is AppointmentStatus.CANCELLED
    assert replacement.status is AppointmentStatus.SCHEDULED
    assert service.find_appointment('A1') is original
    assert service.find_appointment('A2') is replacement
    assert len(store.list_appointments()) == 2
    assert original in store.list_appointments()
    assert replacement in store.list_appointments()


def test_fr07_repeated_cancellation_preserves_history():
    """TEST-FR07-03: a rejected second cancellation changes nothing."""
    store, _, _, service = make_registered_services()
    original = service.book_appointment('A1', 'P1', 'D1', WHEN)
    service.cancel_appointment('A1')
    previous_history = store.list_appointments()

    with pytest.raises(ValueError):
        service.cancel_appointment('A1')

    assert original.status is AppointmentStatus.CANCELLED
    assert service.find_appointment('A1') is original
    assert store.list_appointments() == previous_history == [original]


def test_fr07_completed_cancel_rejection_retains_record():
    """TEST-FR07-04: illegal COMPLETED transition keeps stored history."""
    store, patient, practitioner, service = make_registered_services()
    original = Appointment('A1', patient, practitioner, WHEN, AppointmentStatus.COMPLETED)
    store.add_appointment(original)

    with pytest.raises(ValueError):
        service.cancel_appointment('A1')

    assert original.status is AppointmentStatus.COMPLETED
    assert service.find_appointment('A1') is original
    assert store.list_appointments() == [original]


def test_fr07_unknown_cancellation_does_not_mutate_history():
    """TEST-FR07-05: unknown valid IDs must not delete existing history."""
    store, _, _, service = make_registered_services()
    original = service.book_appointment('A1', 'P1', 'D1', WHEN)
    service.cancel_appointment('A1')

    with pytest.raises(LookupError):
        service.cancel_appointment('A999')

    assert store.list_appointments() == [original]
    assert service.find_appointment('A1') is original
    assert original.status is AppointmentStatus.CANCELLED


@pytest.mark.parametrize('invalid_id', ['', '   ', None])
def test_fr07_invalid_id_cannot_mutate_history(invalid_id):
    """TEST-FR07-06: invalid/whitespace IDs reject without state changes."""
    store, _, _, service = make_registered_services()
    original = service.book_appointment('A1', 'P1', 'D1', WHEN)
    service.cancel_appointment('A1')

    with pytest.raises(ValueError):
        service.cancel_appointment(invalid_id)

    assert store.list_appointments() == [original]
    assert service.find_appointment('A1') is original
    assert original.status is AppointmentStatus.CANCELLED
