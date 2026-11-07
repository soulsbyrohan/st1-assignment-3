## Stage 7: FR-07 / AC-05.2 cancelled appointment history integration tests.


from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import AppointmentService, PatientService, PractitionerService

## create a datetime 
# Use the same appointment date and time in all our tests.
WHEN = datetime(2026, 10, 1, 9)

##Create independent participants in one shared store for each test.
# This sets up a new, empty system for each test.
# It saves from repeating the same patient and practitioner setup.
def make_registered_services():
    
    store = SmartCareDataStore()

    # Register a patient and practitioner who can make an appointment.
    patient = PatientService(store).register_patient('P1', 'Alex Example')
    practitioner = PractitionerService(store).register_practitioner(
        'D1', 'Taylor Example', 'General'
    )

    # Return everything the tests need to use the same data store.
    return store, patient, practitioner, AppointmentService(store)

##TEST-FR07-01: cancelling preserves the same stored appointment
def test_fr07_cancelled_history_is_found_by_id_and_in_list():
    # Create the patient, practitioner and appointment service
    store, _, _, service = make_registered_services()

    # Book an appointment that is scheduled for 9 am
    original = service.book_appointment('A1', 'P1', 'D1', WHEN)

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
    original = service.book_appointment('A1', 'P1', 'D1', WHEN)

    # Cancel it so the time slot is available again.
    service.cancel_appointment('A1')

    # Book a new appointment at the same time, but with a new ID.
    replacement = service.book_appointment('A2', 'P1', 'D1', WHEN)

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
    original = service.book_appointment('A1', 'P1', 'D1', WHEN)
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
    original = Appointment('A1', patient, practitioner, WHEN, AppointmentStatus.COMPLETED)
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
    original = service.book_appointment('A1', 'P1', 'D1', WHEN)
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
    original = service.book_appointment('A1', 'P1', 'D1', WHEN)
    service.cancel_appointment('A1')

    # Try an invalid ID. SmartCare should raise ValueError.
    with pytest.raises(ValueError):
        service.cancel_appointment(invalid_id)

    # Check the real appointment is still stored and remains CANCELLED.
    assert store.list_appointments() == [original]
    assert service.find_appointment('A1') is original
    assert original.status is AppointmentStatus.CANCELLED
