"""Stage 09 service-level tests for practitioner appointment listing."""
from datetime import datetime
import pytest
from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import AppointmentService, PatientService, PractitionerService


@pytest.fixture
def listing_setup():
    # A new store prevents tests from interfering with each other.
    store = SmartCareDataStore()
    patients = PatientService(store)
    practitioners = PractitionerService(store)
    patients.register_patient('P1', 'Alex Example')
    second_patient = patients.register_patient('P2', 'Sam Example')
    first_practitioner = practitioners.register_practitioner('D1', 'Taylor Example', 'General')
    practitioners.register_practitioner('D2', 'Jordan Example', 'Cardiology')
    return store, AppointmentService(store), second_patient, first_practitioner


def make_appointments(listing_setup):
    store, service, second_patient, first_practitioner = listing_setup
    nine = datetime(2026, 10, 1, 9)
    ten = datetime(2026, 10, 1, 10)
    eleven = datetime(2026, 10, 1, 11)
    # Insert the later booking first, so a correct listing must reorder results.
    later = service.book_appointment('A9', 'P1', 'D1', ten)
    cancelled = service.book_appointment('A2', 'P1', 'D1', nine)
    service.cancel_appointment('A2')
    replacement = service.book_appointment('A1', 'P2', 'D1', nine)
    completed = Appointment('A5', second_patient, first_practitioner,
                            eleven, AppointmentStatus.COMPLETED)
    store.add_appointment(completed)
    other = service.book_appointment('B1', 'P2', 'D2', nine)
    return store, service, replacement, cancelled, later, completed, other


def test_listing_known_practitioner_with_no_appointments(listing_setup):
    store, service, _, _ = listing_setup
    assert service.list_practitioner_appointments('D1') == []
    assert store.list_appointments() == []


def test_listing_unknown_practitioner_raises_lookup_error(listing_setup):
    store, service, _, _ = listing_setup
    with pytest.raises(LookupError):
        service.list_practitioner_appointments('D999')
    assert store.list_appointments() == []


@pytest.mark.parametrize('invalid_id', ['', '   ', None, 42])
def test_listing_invalid_practitioner_id_raises_value_error(listing_setup, invalid_id):
    store, service, _, _ = listing_setup
    with pytest.raises(ValueError):
        service.list_practitioner_appointments(invalid_id)
    assert store.list_appointments() == []


@pytest.mark.parametrize('invalid_status', ['scheduled', '', 1, False])
def test_listing_invalid_status_raises_value_error(listing_setup, invalid_status):
    store, service, _, _ = listing_setup
    with pytest.raises(ValueError):
        service.list_practitioner_appointments('D1', invalid_status)
    assert store.list_appointments() == []


def test_listing_trims_id_but_remains_case_sensitive(listing_setup):
    store, service, _, _ = listing_setup
    appointment = service.book_appointment('A1', 'P1', 'D1', datetime(2026, 10, 1, 9))
    assert service.list_practitioner_appointments(' D1 ') == [appointment]
    with pytest.raises(LookupError):
        service.list_practitioner_appointments('d1')
    assert store.list_appointments() == [appointment]


def test_listing_defaults_to_all_statuses_and_sorts_by_time_then_id(listing_setup):
    store, service, replacement, cancelled, later, completed, other = make_appointments(listing_setup)
    original_order = store.list_appointments()
    result = service.list_practitioner_appointments('D1')
    # A1 and A2 tie at 9 am, so the appointment ID breaks the tie.
    assert [item.appointment_id for item in result] == ['A1', 'A2', 'A9', 'A5']
    assert result == [replacement, cancelled, later, completed]
    assert other not in result
    assert store.list_appointments() == original_order


def test_listing_filters_every_enum_status(listing_setup):
    store, service, replacement, cancelled, later, completed, _ = make_appointments(listing_setup)
    original_order = store.list_appointments()
    assert service.list_practitioner_appointments('D1', AppointmentStatus.SCHEDULED) == [replacement, later]
    assert service.list_practitioner_appointments('D1', AppointmentStatus.CANCELLED) == [cancelled]
    assert service.list_practitioner_appointments('D1', AppointmentStatus.COMPLETED) == [completed]
    assert store.list_appointments() == original_order


def test_listing_returns_fresh_list_and_original_objects(listing_setup):
    store, service, replacement, cancelled, later, completed, _ = make_appointments(listing_setup)
    original_order = store.list_appointments()
    first = service.list_practitioner_appointments('D1')
    second = service.list_practitioner_appointments('D1')
    assert first is not second
    assert first == second
    assert first[0] is replacement
    assert cancelled.status is AppointmentStatus.CANCELLED
    assert completed.status is AppointmentStatus.COMPLETED
    assert later.status is AppointmentStatus.SCHEDULED
    assert store.list_appointments() == original_order
