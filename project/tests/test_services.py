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



def test_cancel_blank_appointment_id():
    # testing blank appointment ID
    data_store = SmartCareDataStore()
    service = AppointmentService(data_store)

    with pytest.raises(ValueError):
        service.cancel_appointment('')


def test_cancel_invalid_appointment_id_type():
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

    when = datetime( 2026, 10, 1, 9)

    original = appointment_service.book_appointment('A1', 'P1', 'D1', when)

    appointment_service.cancel_appointment('A1')

    replacement = appointment_service.book_appointment('A2', 'P1', 'D1', when)

    assert original.status is AppointmentStatus.CANCELLED
    assert replacement.status is AppointmentStatus.SCHEDULED
    assert appointment_service.find_appointment('A1') is original
    assert appointment_service.find_appointment('A2') is replacement