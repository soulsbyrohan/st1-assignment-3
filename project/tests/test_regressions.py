##Stage 8 F8-01 regression tests for practitioner booking conflicts.

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import AppointmentService, PatientService, PractitionerService


def make_f8_01_services():
    # Each test gets its own empty store so the tests do not affect each other.
    store = SmartCareDataStore()
    patients = PatientService(store)
    practitioners = PractitionerService(store)

    patients.register_patient("P1", "Alex Example")
    patients.register_patient("P2", "Sam Example")
    practitioners.register_practitioner("D1", "Taylor Example", "General")
    practitioners.register_practitioner("D2", "Jordan Example", "Cardiology")

    return store, AppointmentService(store)


def test_f8_01_same_practitioner_same_time_is_rejected():
    # Book one appointment for practitioner D1 at 9 am.
    store, service = make_f8_01_services()
    when = datetime(2026, 10, 1, 9, 0)
    original = service.book_appointment("A1", "P1", "D1", when)

    # The same practitioner must not be booked again at the same time.
    with pytest.raises(ValueError, match="Practitioner already has"):
        service.book_appointment("A2", "P2", "D1", when)

    # Assert: The failed booking must not change or add stored appointments.
    assert service.find_appointment("A1") is original
    assert original.status is AppointmentStatus.SCHEDULED
    assert store.find_appointment("A2") is None
    assert store.list_appointments() == [original]
