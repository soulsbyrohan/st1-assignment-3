from datetime import datetime
import pytest
from smartcare.domain import (Appointment, Practitioner, Patient, AppointmentStatus)

# Test 1: cancel a scheduled appointment
def test_domain_cancel_scheduled_appointment() -> None:
    # Create paitent and practitioner
    patient = Patient("P1", "Alex Example")
    practitioner = Practitioner("D1", "Taylor Example", "General")

    # Create scheduled appointment
    appointment = Appointment( "A1", patient, practitioner, datetime(2026, 10, 1, 9))

    # Cancel Appointment
    appointment.cancel()

    # Check appointment status
    assert appointment.status is AppointmentStatus.CANCELLED


# Test 2: reject repeated cancelled appointment
def test_domain_cancel_already_cancelled() -> None:
    # Create paitent and practitioner
    patient = Patient("P1", "Alex Example")
    practitioner = Practitioner("D1", "Taylor Example", "General")

    # Create scheduled appointment
    appointment = Appointment( "A1", patient, practitioner, datetime(2026, 10, 1, 9))

    # Cancel Appointment
    appointment.cancel()

    # Attempt to cancel appointment again
    with pytest.raises(ValueError):
        appointment.cancel()

    # Check that the status is unchanged
    assert appointment.status is AppointmentStatus.CANCELLED


# Reject cancellation of a already completed appointment
def test_domain_cancel_completed_appointment() -> None:
    # Create paitent and practitioner
    patient = Patient("P1", "Alex Example")
    practitioner = Practitioner("D1", "Taylor Example", "General")

    # Create appointment with COMPLETED status
    appointment = Appointment( "A1", patient, practitioner, datetime(2026, 10, 1, 9), AppointmentStatus.COMPLETED)
    
    # Attempt to cancel the completed appointment
    with pytest.raises(ValueError):
        appointment.cancel()

    # Check that the status is unchanged
    assert appointment.status is AppointmentStatus.COMPLETED