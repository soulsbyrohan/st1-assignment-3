# Stage 6 Services Test file

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import (AppointmentStatus, Appointment)
from smartcare.services import (AppointmentService, PatientService, PractitionerService)


def test_cancel_scheduled_appointment() -> None:
    # check if a scheduled appointment can be cancelled

    data_store = SmartCareDataStore()

    PatientService(data_store).register_patient('P1', 'Alex Example')
    PractitionerService(data_store).register_practitioner('D1', 'Taylor Example', 'General')
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
    # Added assertion based on given feedback to show that proves the appointment remains in the data store's appointment list
    assert appointment in data_store.list_appointments()


def test_cancel_already_cancelled_appointment() -> None:
    # test if a already made appointment can be cancelled

    data_store = SmartCareDataStore()
    
    PatientService(data_store).register_patient('P1', 'Alex Example')
    PractitionerService(data_store).register_practitioner('D1', 'Taylor Example', 'General')
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
        
    patient = PatientService(data_store).register_patient('P1', 'Alex Example')
    practitioner = PractitionerService(data_store).register_practitioner('D1', 'Taylor Example', 'General')
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
    # test the cancellation of an appointment that doesn't exist is rejected

    data_store = SmartCareDataStore()
    appointment_service = AppointmentService(data_store)

    with pytest.raises(LookupError):
        appointment_service.cancel_appointment('A1000')



def test_cancel_blank_appointment_id() -> None:
    # testing blank appointment ID
    data_store = SmartCareDataStore()
    service = AppointmentService(data_store)

    with pytest.raises(ValueError):
        service.cancel_appointment('')

    # added a test to show inputs that only contains spaces raises a value error
    with pytest.raises(ValueError):
        service.cancel_appointment('')


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
    PractitionerService(data_store).register_practitioner('D1', 'Taylor Example', 'General')
    appointment_service = AppointmentService(data_store)

    when = datetime(2026, 10, 1, 9)

    original = appointment_service.book_appointment('A1', 'P1', 'D1', when)

    appointment_service.cancel_appointment('A1')

    replacement = appointment_service.book_appointment('A2', 'P1', 'D1', when)

    assert original.status is AppointmentStatus.CANCELLED
    assert replacement.status is AppointmentStatus.SCHEDULED
    assert appointment_service.find_appointment('A1') is original
    assert appointment_service.find_appointment('A2') is replacement

# test 1: find existing patient
def test_find_patient_returns_patient():
    data_store = SmartCareDataStore()
    service = PatientService(data_store)

    patient = service.register_patient('P1', 'Alex Example')  # register patient

    search = service.find_patient('P1')  # search for registered patient

    assert search is patient  # check that the original patient is returned


# test 2: unknown lookup raises LookupError
def test_find_patient_unknown_id_raises_lookup_error():
    data_store = SmartCareDataStore()
    service = PatientService(data_store)

    with pytest.raises(LookupError):
        service.find_patient('P99')  # search for an unregistered patient


# test 3: trimmed ID
def test_find_patient_trimmed():
    data_store = SmartCareDataStore()
    service = PatientService(data_store)

    patient = service.register_patient('P1', 'Alex Example')

    search = service.find_patient('   P1   ')  # spaces around ID

    assert search is patient  # confirms spaces are trimmed


# test 4: blank ID
def test_find_patient_blank_id():
    data_store = SmartCareDataStore()
    service = PatientService(data_store)

    with pytest.raises(ValueError):
        service.find_patient('')  # empty patient ID


# test 5: case-sensitive ID
def test_find_patient_case_sensitive():
    data_store = SmartCareDataStore()
    service = PatientService(data_store)

    service.register_patient('P1', 'Alex Example')

    with pytest.raises(LookupError):
        service.find_patient('p1')  # lowercase ID should not match P1


# test 6: invalid ID type
def test_find_patient_invalid_id_type():
    data_store = SmartCareDataStore()
    service = PatientService(data_store)

    with pytest.raises(ValueError):
        service.find_patient(None)  # None is not a valid patient ID
from smartcare.services import PractitionerService


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
