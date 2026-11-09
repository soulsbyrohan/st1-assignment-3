

# Stage 9 Query Tests


from datetime import datetime
import pytest
from smartcare.domain import Patient, Practitioner, Appointment, AppointmentStatus
from smartcare.queries import appointment_sort_key, select_appointments




# Create sample appointments for query testing
def make_appointments():
    patient = Patient("P1", "Alex Example")
    practitioner_one = Practitioner("D1", "Taylor Example", "General")
    practitioner_two = Practitioner("D2", "Sam Example", "General")


    # Create appointments directly without using services
    a1 = Appointment(
        "A1", patient, practitioner_one,
        datetime(2026, 10, 1, 9), AppointmentStatus.CANCELLED
    )
    a2 = Appointment(
        "A2", patient, practitioner_one,
        datetime(2026, 10, 1, 11), AppointmentStatus.SCHEDULED
    )
    a3 = Appointment(
        "A3", patient, practitioner_two,
        datetime(2026, 10, 1, 10), AppointmentStatus.SCHEDULED
    )


    return a1, a2, a3




# QRY-01: Only select the requested practitioner
def test_only_select_requested_practitioner():
    a1, a2, a3 = make_appointments()


    appointments = [a1, a2, a3]
    result = select_appointments(appointments, "D1")


    assert result == [a1, a2]
    assert a3 not in result




# QRY-02: Filter by appointment status
def test_qry02_status_filter():
    a1, a2, a3 = make_appointments()


    appointments = [a1, a2, a3]


    all_results = select_appointments(appointments, "D1")
    scheduled = select_appointments(
        appointments, "D1", AppointmentStatus.SCHEDULED
    )
    cancelled = select_appointments(
        appointments, "D1", AppointmentStatus.CANCELLED
    )
    completed = select_appointments(
        appointments, "D1", AppointmentStatus.COMPLETED
    )


    assert all_results == [a1, a2]
    assert scheduled == [a2]
    assert cancelled == [a1]
    assert completed == []




# QRY-03: Sort by date/time and then appointment ID
def test_qry03_sorting():
    a1, a2, a3 = make_appointments()


    # Add another appointment at the same time as A1
    a4 = Appointment(
        "A4", a1.patient, a1.practitioner,
        datetime(2026, 10, 1, 9), AppointmentStatus.COMPLETED
    )


    appointments = [a2, a4, a1]
    original = appointments.copy()


    result = select_appointments(appointments, "D1")


    assert result == [a1, a4, a2]
    assert appointments == original




# FP-01: Repeated queries return the same results without changes
def test_fp01_query_is_repeatable():
    a1, a2, a3 = make_appointments()


    appointments = [a3, a2, a1]
    original_order = appointments.copy()
    original_values = [
        (a.appointment_id, a.status, a.date_time)
        for a in appointments
    ]


    first = select_appointments(appointments, "D1")
    second = select_appointments(appointments, "D1")


    assert first == second


    # Check the original list order and values are unchanged
    assert all(a is b for a, b in zip(appointments, original_order))
    assert [
        (a.appointment_id, a.status, a.date_time)
        for a in appointments
    ] == original_values




# FP-02: Return a new list containing the original appointment objects
def test_fp02_new_list():
    a1, a2, a3 = make_appointments()


    appointments = [a1, a2]
    result = select_appointments(appointments, "D1")


    assert result is not appointments
    assert result[0] is a1
    assert result[1] is a2




# FP-02: Empty input must also return a new empty list
def test_fp02_empty_list():
    appointments = []


    result = select_appointments(appointments, "D1")


    assert result == []
    assert result is not appointments




# FP-02: Already sorted input must still return a new list
def test_fp02_already_sorted():
    a1, a2, a3 = make_appointments()


    appointments = [a1, a2]
    result = select_appointments(appointments, "D1")


    assert result == [a1, a2]
    assert result is not appointments




# FP-03: Check the named appointment sorting key
def test_fp03_appointment_key_sort():
    a1, a2, a3 = make_appointments()


    result = appointment_sort_key(a1)


    assert result == (a1.date_time, a1.appointment_id)