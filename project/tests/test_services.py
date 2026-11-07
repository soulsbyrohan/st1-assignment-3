
# Stage 6 and Stage 7 Services Tests

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus, Appointment
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)

# =========================================================
# STAGE 6 - APPOINTMENT CANCELLATION TESTS
# =========================================================

def test_cancel_scheduled_appointment() -> None:
    # check if a scheduled appointment can be cancelled

    data_store = SmartCareDataStore()

    PatientService(data_store).register_patient('P1', 'Alex Example')
    PractitionerService(data_store).register_practitioner(
        'D1', 'Taylor Example', 'General'
    )
    appointment_service = AppointmentService(data_store)

    appointment = appointment_service.book_appointment(
        'A1',
        'P1',
        'D1',
        datetime(2026, 10, 1, 9),
    )

    cancelled = appointment_service.cancel_appointment('A1')

    assert cancelled.status is AppointmentStatus.CANCELLED
    assert cancelled is appointment
    assert appointment_service.find_appointment('A1') is appointment
    assert appointment in data_store.list_appointments()


def test_cancel_already_cancelled_appointment() -> None:
    # test if an already cancelled appointment can be cancelled

    data_store = SmartCareDataStore()

    PatientService(data_store).register_patient('P1', 'Alex Example')
    PractitionerService(data_store).register_practitioner(
        'D1', 'Taylor Example', 'General'
    )
    appointment_service = AppointmentService(data_store)

    appointment = appointment_service.book_appointment(
        'A1',
        'P1',
        'D1',
        datetime(2026, 10, 1, 9),
    )

    cancelled = appointment_service.cancel_appointment('A1')

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A1')

    assert cancelled.status is AppointmentStatus.CANCELLED
    assert cancelled is appointment
    assert appointment_service.find_appointment('A1') is appointment


def test_cancel_completed_appointment() -> None:
    # test the cancellation of a completed appointment is rejected

    data_store = SmartCareDataStore()

    patient = PatientService(data_store).register_patient(
        'P1', 'Alex Example'
    )
    practitioner = PractitionerService(data_store).register_practitioner(
        'D1', 'Taylor Example', 'General'
    )
    appointment_service = AppointmentService(data_store)

    appointment = Appointment(
        'A1',
        patient,
        practitioner,
        datetime(2026, 10, 1, 9),
        AppointmentStatus.COMPLETED
    )

    data_store.add_appointment(appointment)

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A1')

    assert appointment.status is AppointmentStatus.COMPLETED
    assert appointment_service.find_appointment('A1') is appointment


def test_cancel_unknown_appointment_id() -> None:
    # test cancellation of an appointment that doesn't exist

    data_store = SmartCareDataStore()
    appointment_service = AppointmentService(data_store)

    with pytest.raises(LookupError):
        appointment_service.cancel_appointment('A1000')


def test_cancel_blank_appointment_id() -> None:
    # testing blank appointment ID

    data_store = SmartCareDataStore()
    service = AppointmentService(data_store)

    with pytest.raises(ValueError):
        service.cancel_appointment('   ')


def test_cancel_invalid_appointment_id_type() -> None:
    # testing invalid appointment ID type

    data_store = SmartCareDataStore()
    service = AppointmentService(data_store)

    with pytest.raises(ValueError):
        service.cancel_appointment(None)


def test_booking_after_cancellation() -> None:
    # check if cancelling an appointment frees a time slot

    data_store = SmartCareDataStore()

    PatientService(data_store).register_patient('P1', 'Alex Example')
    PractitionerService(data_store).register_practitioner(
        'D1', 'Taylor Example', 'General'
    )
    appointment_service = AppointmentService(data_store)

    when = datetime(2026, 10, 1, 9)

    original = appointment_service.book_appointment(
        'A1', 'P1', 'D1', when
    )

    appointment_service.cancel_appointment('A1')

    replacement = appointment_service.book_appointment(
        'A2', 'P1', 'D1', when
    )

    assert original.status is AppointmentStatus.CANCELLED
    assert replacement.status is AppointmentStatus.SCHEDULED
    assert appointment_service.find_appointment('A1') is original
    assert appointment_service.find_appointment('A2') is replacement


# =========================================================
# STAGE 6 - PATIENT LOOKUP TESTS
# =========================================================

def test_find_patient_returns_patient():
    data_store = SmartCareDataStore()
    service = PatientService(data_store)

    patient = service.register_patient('P1', 'Alex Example')

    search = service.find_patient('P1')

    assert search is patient


def test_find_patient_unknown_id_raises_lookup_error():
    data_store = SmartCareDataStore()
    service = PatientService(data_store)

    with pytest.raises(LookupError):
        service.find_patient('P99')


def test_find_patient_trimmed():
    data_store = SmartCareDataStore()
    service = PatientService(data_store)

    patient = service.register_patient('P1', 'Alex Example')

    search = service.find_patient('   P1   ')

    assert search is patient


def test_find_patient_blank_id():
    data_store = SmartCareDataStore()
    service = PatientService(data_store)

    with pytest.raises(ValueError):
        service.find_patient('')


def test_find_patient_case_sensitive():
    data_store = SmartCareDataStore()
    service = PatientService(data_store)

    service.register_patient('P1', 'Alex Example')

    with pytest.raises(LookupError):
        service.find_patient('p1')


def test_find_patient_invalid_id_type():
    data_store = SmartCareDataStore()
    service = PatientService(data_store)

    with pytest.raises(ValueError):
        service.find_patient(None)


# =========================================================
# STAGE 6 - PRACTITIONER LOOKUP TESTS
# =========================================================

def test_find_existing_practitioner():
    store = SmartCareDataStore()
    service = PractitionerService(store)

    practitioner = service.register_practitioner(
        'D1', 'Dr Smith', 'Cardiology'
    )

    result = service.find_practitioner('D1')

    assert result is practitioner


def test_find_unknown_practitioner():
    store = SmartCareDataStore()
    service = PractitionerService(store)

    with pytest.raises(LookupError):
        service.find_practitioner('D999')


def test_find_blank_practitioner_id():
    store = SmartCareDataStore()
    service = PractitionerService(store)

    with pytest.raises(ValueError):
        service.find_practitioner('   ')


def test_find_practitioner_with_spaces():
    store = SmartCareDataStore()
    service = PractitionerService(store)

    practitioner = service.register_practitioner(
        'D1', 'Dr Smith', 'Cardiology'
    )

    result = service.find_practitioner('  D1  ')

    assert result is practitioner


def test_find_practitioner_case_sensitive():
    store = SmartCareDataStore()
    service = PractitionerService(store)

    service.register_practitioner(
        'D1', 'Dr Smith', 'Cardiology'
    )

    with pytest.raises(LookupError):
        service.find_practitioner('d1')


def test_find_invalid_practitioner_id_type():
    store = SmartCareDataStore()
    service = PractitionerService(store)

    with pytest.raises(ValueError):
        service.find_practitioner(None)

# Use the same appointment time in all FR-07 service tests.
FR07_WHEN = datetime(2026, 10, 1, 9)


def make_registered_services():
    # Create a new, empty data store for each test.
    store = SmartCareDataStore()

    # Register a patient in the store.
    patient = PatientService(store).register_patient(
        'P1', 'Alex Example'
    )

    # Register a practitioner in the same store.
    practitioner = PractitionerService(store).register_practitioner(
        'D1', 'Taylor Example', 'General'
    )

    # Create an appointment service using the same store.
    service = AppointmentService(store)

    # Return all four objects needed by the tests.
    return store, patient, practitioner, service

# Test 1: A cancelled appointment should stay saved in the system.
def test_fr07_cancelled_history_is_found_by_id_and_in_list():
    # Create the patient, practitioner and appointment service
    store, _, _, service = make_registered_services()

    # Book an appointment that is scheduled for 9 am
    original = service.book_appointment('A1', 'P1', 'D1', FR07_WHEN)

    # Cancel appointment
    cancelled = service.cancel_appointment('A1')

    # Check that the cancelled appointment is the exact same original object
    assert cancelled is original

    # Check the status has changed to CANCELLED
    assert original.status is AppointmentStatus.CANCELLED

    # Check we can still find the appointment by its ID
    assert service.find_appointment('A1') is original
    assert store.find_appointment('A1') is original

    # Check the cancelled appointment is still in the stored list
    assert store.list_appointments() == [original]


# Test 2: Booking the freed time slot should not delete cancelled history.
def test_fr07_rebooking_does_not_erase_cancelled_history():
    # Set up a new data store and book the first appointment.
    store, _, _, service = make_registered_services()
    original = service.book_appointment('A1', 'P1', 'D1', FR07_WHEN)

    # Cancel it so the time slot is available again.
    service.cancel_appointment('A1')

    # Book a new appointment at the same time, but with a new ID.
    replacement = service.book_appointment('A2', 'P1', 'D1', FR07_WHEN)

    # Check these are two different appointments.
    assert original is not replacement

    # Check the old one is cancelled and the new one is scheduled.
    assert original.status is AppointmentStatus.CANCELLED
    assert replacement.status is AppointmentStatus.SCHEDULED

    # Check both appointments can still be found using their IDs.
    assert service.find_appointment('A1') is original
    assert service.find_appointment('A2') is replacement

    # Check both records are still saved in the appointment list.
    assert len(store.list_appointments()) == 2
    assert original in store.list_appointments()
    assert replacement in store.list_appointments()

# Test 3: Cancelling an already cancelled appointment must not delete it.
def test_fr07_repeated_cancellation_preserves_history():
    
    # Create and cancel an appointment once.
    store, _, _, service = make_registered_services()
    original = service.book_appointment('A1', 'P1', 'D1', FR07_WHEN)
    service.cancel_appointment('A1')

    # Save the existing list so we can check it has not changed.
    previous_history = store.list_appointments()

    # Try to cancel it again. This should raise a ValueError.
    with pytest.raises(ValueError):
        service.cancel_appointment('A1')

    # Check its status is still CANCELLED and the record is still saved.
    assert original.status is AppointmentStatus.CANCELLED
    assert service.find_appointment('A1') is original
    assert store.list_appointments() == previous_history == [original]


# Test 4: A COMPLETED appointment should not be cancelled or deleted.
def test_fr07_completed_cancel_rejection_retains_record():

    # Set up a new system with a registered patient and practitioner.
    store, patient, practitioner, service = make_registered_services()

    # Create an appointment that has already been marked COMPLETED.
    original = Appointment('A1', patient, practitioner, FR07_WHEN, AppointmentStatus.COMPLETED)
    store.add_appointment(original)

    # Try to cancel the completed appointment. This should be rejected.
    with pytest.raises(ValueError):
        service.cancel_appointment('A1')

    # Check its status and stored record have not changed.
    assert original.status is AppointmentStatus.COMPLETED
    assert service.find_appointment('A1') is original
    assert store.list_appointments() == [original]



# Test 5: A request to cancel an unknown appointment must not affect history.
def test_fr07_unknown_cancellation_does_not_mutate_history():

    # Book and cancel a real appointment, so there is history to protect.
    store, _, _, service = make_registered_services()
    original = service.book_appointment('A1', 'P1', 'D1', FR07_WHEN)
    service.cancel_appointment('A1')

    # Try to cancel A999, which does not exist in our data store.
    with pytest.raises(LookupError):
        service.cancel_appointment('A999')

    # Check the real cancelled appointment was not removed or changed.
    assert store.list_appointments() == [original]
    assert service.find_appointment('A1') is original
    assert original.status is AppointmentStatus.CANCELLED

# Test 6: Invalid IDs must be rejected without changing saved history.
# Pytest runs this same test three times: empty ID, spaces-only ID, and None.
@pytest.mark.parametrize('invalid_id', ['', '   ', None])
def test_fr07_invalid_id_cannot_mutate_history(invalid_id):
    # Create a real appointment and cancel it once.
    store, _, _, service = make_registered_services()
    original = service.book_appointment('A1', 'P1', 'D1', FR07_WHEN)
    service.cancel_appointment('A1')

    # Try an invalid ID. SmartCare should raise ValueError.
    with pytest.raises(ValueError):
        service.cancel_appointment(invalid_id)

    # Check the real appointment is still stored and remains CANCELLED.
    assert store.list_appointments() == [original]
    assert service.find_appointment('A1') is original
    assert original.status is AppointmentStatus.CANCELLED


# =========================================================
# STAGE 7 - FR-05 PRACTITIONER BOOKING CONFLICT TESTS
# PERSON 2
# =========================================================

def test_fr05_available_practitioner_booking():
    """TEST-FR05-01: An available practitioner can be booked."""

    store = SmartCareDataStore()

    patient = PatientService(store).register_patient(
        'P1', 'Alex Example'
    )
    practitioner = PractitionerService(store).register_practitioner(
        'D1', 'Dr Smith', 'General'
    )
    service = AppointmentService(store)

    when = datetime(2026, 12, 1, 9, 0)

    appointment = service.book_appointment(
        'A1', 'P1', 'D1', when
    )

    assert appointment.status is AppointmentStatus.SCHEDULED
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.date_time == when
    assert service.find_appointment('A1') is appointment


def test_fr05_same_practitioner_same_time_rejected():
    """TEST-FR05-02: A practitioner cannot be double-booked."""

    store = SmartCareDataStore()

    PatientService(store).register_patient(
        'P1', 'Alex Example'
    )
    PatientService(store).register_patient(
        'P2', 'Sam Example'
    )
    PractitionerService(store).register_practitioner(
        'D1', 'Dr Smith', 'General'
    )

    service = AppointmentService(store)
    when = datetime(2026, 12, 1, 9, 0)

    original = service.book_appointment(
        'A1', 'P1', 'D1', when
    )

    with pytest.raises(ValueError, match='Practitioner already has'):
        service.book_appointment(
            'A2', 'P2', 'D1', when
        )

    assert service.find_appointment('A1') is original
    assert original.status is AppointmentStatus.SCHEDULED
    assert store.find_appointment('A2') is None
    assert len(store.list_appointments()) == 1


def test_fr05_different_practitioners_same_time_allowed():
    """TEST-FR05-03: Different practitioners can share a time slot."""

    store = SmartCareDataStore()

    PatientService(store).register_patient(
        'P1', 'Alex Example'
    )
    PatientService(store).register_patient(
        'P2', 'Sam Example'
    )

    PractitionerService(store).register_practitioner(
        'D1', 'Dr Smith', 'General'
    )
    PractitionerService(store).register_practitioner(
        'D2', 'Dr Jones', 'Cardiology'
    )

    service = AppointmentService(store)
    when = datetime(2026, 12, 1, 9, 0)

    first = service.book_appointment(
        'A1', 'P1', 'D1', when
    )
    second = service.book_appointment(
        'A2', 'P2', 'D2', when
    )

    assert first.status is AppointmentStatus.SCHEDULED
    assert second.status is AppointmentStatus.SCHEDULED
    assert first.date_time == second.date_time
    assert first.practitioner.practitioner_id == 'D1'
    assert second.practitioner.practitioner_id == 'D2'
    assert len(store.list_appointments()) == 2


def test_fr05_same_practitioner_different_times_allowed():
    """TEST-FR05-04: The same practitioner can have different time slots."""

    store = SmartCareDataStore()

    PatientService(store).register_patient(
        'P1', 'Alex Example'
    )
    PatientService(store).register_patient(
        'P2', 'Sam Example'
    )
    PractitionerService(store).register_practitioner(
        'D1', 'Dr Smith', 'General'
    )

    service = AppointmentService(store)

    first = service.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 12, 1, 9, 0)
    )
    second = service.book_appointment(
        'A2', 'P2', 'D1', datetime(2026, 12, 1, 9, 1)
    )

    assert first.status is AppointmentStatus.SCHEDULED
    assert second.status is AppointmentStatus.SCHEDULED
    assert first.date_time != second.date_time
    assert len(store.list_appointments()) == 2


def test_fr05_cancelled_slot_can_be_rebooked():
    """TEST-FR05-05: A cancelled appointment does not block its slot."""

    store = SmartCareDataStore()

    PatientService(store).register_patient(
        'P1', 'Alex Example'
    )
    PatientService(store).register_patient(
        'P2', 'Sam Example'
    )
    PractitionerService(store).register_practitioner(
        'D1', 'Dr Smith', 'General'
    )

    service = AppointmentService(store)
    when = datetime(2026, 12, 1, 9, 0)

    original = service.book_appointment(
        'A1', 'P1', 'D1', when
    )

    service.cancel_appointment('A1')

    replacement = service.book_appointment(
        'A2', 'P2', 'D1', when
    )

    assert original.status is AppointmentStatus.CANCELLED
    assert replacement.status is AppointmentStatus.SCHEDULED
    assert service.find_appointment('A1') is original
    assert service.find_appointment('A2') is replacement
    assert len(store.list_appointments()) == 2


def test_fr05_conflict_does_not_modify_existing_booking():
    """TEST-FR05-06: Rejected bookings must not mutate stored records."""

    store = SmartCareDataStore()

    PatientService(store).register_patient(
        'P1', 'Alex Example'
    )
    PatientService(store).register_patient(
        'P2', 'Sam Example'
    )
    PractitionerService(store).register_practitioner(
        'D1', 'Dr Smith', 'General'
    )

    service = AppointmentService(store)
    when = datetime(2026, 12, 1, 9, 0)

    original = service.book_appointment(
        'A1', 'P1', 'D1', when
    )

    with pytest.raises(ValueError):
        service.book_appointment(
            'A2', 'P2', 'D1', when
        )

    assert original.appointment_id == 'A1'
    assert original.patient.patient_id == 'P1'
    assert original.practitioner.practitioner_id == 'D1'
    assert original.date_time == when
    assert original.status is AppointmentStatus.SCHEDULED
    assert store.list_appointments() == [original]
    
    
def test_register_patient_valid_patient_unused_id_is_stored():
    data_store = SmartCareDataStore()  
    service = PatientService(data_store)

    patient = service.register_patient('P1', 'Alex Example')

    search = service.find_patient('P1')
    
    assert patient is search


def test_duplicate_patient_id_is_rejected():
    data_store = SmartCareDataStore()  
    service = PatientService(data_store)
     
    original = service.register_patient('P1', 'Alex Example')

    with pytest.raises(ValueError):
        service.register_patient('P1', 'Bob Example')

    assert service.find_patient('P1') is original
    assert original.name == 'Alex Example'
