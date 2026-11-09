
"""Stage 9 tests for SmartCare console workflows."""

from unittest.mock import patch

import pytest

from smartcare.console import run_menu


def run_console(monkeypatch, capsys, inputs):
    """Run a complete menu session with simulated user inputs."""
    answers = iter(inputs)

    def fake_input(prompt=''):
        return next(answers)

    monkeypatch.setattr('builtins.input', fake_input)
    run_menu()
    return capsys.readouterr().out


def test_patient_registration_and_lookup(monkeypatch, capsys):
    """A registered patient can be found in the same session."""
    output = run_console(monkeypatch, capsys, [
        '1', 'P1', 'Alex Example',
        '2', 'P1',
        '0',
    ])

    assert 'Patient P1 registered successfully.' in output
    assert 'Patient found: P1 - Alex Example' in output


def test_practitioner_registration_and_lookup(monkeypatch, capsys):
    """A registered practitioner can be found in the same session."""
    output = run_console(monkeypatch, capsys, [
        '3', 'DR1', 'Taylor Example', 'General Practice',
        '4', 'DR1',
        '0',
    ])

    assert 'Practitioner DR1 registered successfully.' in output
    assert 'Practitioner found: DR1' in output
    assert 'Taylor Example' in output


def test_booking_and_appointment_lookup(monkeypatch, capsys):
    """A valid appointment can be booked and retrieved."""
    output = run_console(monkeypatch, capsys, [
        '1', 'P1', 'Alex Example',
        '3', 'DR1', 'Taylor Example', 'General Practice',
        '5', 'A1', 'P1', 'DR1', '2026-12-01 09:00',
        '7', 'A1',
        '0',
    ])

    assert 'Appointment booked successfully.' in output
    assert 'Appointment found:' in output
    assert 'A1: P1 with DR1' in output


def test_practitioner_conflict_is_rejected(monkeypatch, capsys):
    """Two appointments cannot use the same practitioner and time."""
    output = run_console(monkeypatch, capsys, [
        '1', 'P1', 'Alex Example',
        '3', 'DR1', 'Taylor Example', 'General Practice',
        '5', 'A1', 'P1', 'DR1', '2026-12-01 09:00',
        '5', 'A2', 'P1', 'DR1', '2026-12-01 09:00',
        '7', 'A1',
        '7', 'A2',
        '0',
    ])

    assert output.count('Appointment booked successfully.') == 1
    assert 'Practitioner already has a SCHEDULED appointment' in output
    assert 'Appointment found:' in output
    assert 'Error: Appointment not found' in output


def test_cancelled_appointment_remains_available(monkeypatch, capsys):
    """Cancellation retains history and frees the time slot."""
    output = run_console(monkeypatch, capsys, [
        '1', 'P1', 'Alex Example',
        '3', 'DR1', 'Taylor Example', 'General Practice',
        '5', 'A1', 'P1', 'DR1', '2026-12-01 09:00',
        '6', 'A1',
        '7', 'A1',
        '5', 'A2', 'P1', 'DR1', '2026-12-01 09:00',
        '7', 'A2',
        '0',
    ])

    assert 'Appointment cancelled successfully.' in output
    assert 'A1: P1 with DR1, 2026-12-01 09:00, cancelled' in output
    assert 'Appointment booked successfully.' in output
    assert 'A2: P1 with DR1, 2026-12-01 09:00, scheduled' in output


def test_duplicate_patient_does_not_replace_original(monkeypatch, capsys):
    """Rejected registration must preserve the original patient."""
    output = run_console(monkeypatch, capsys, [
        '1', 'P1', 'Alex Example',
        '1', 'P1', 'Different Name',
        '2', 'P1',
        '0',
    ])

    assert 'Error:' in output
    assert 'Patient found: P1 - Alex Example' in output
    assert 'Patient found: P1 - Different Name' not in output


@pytest.mark.parametrize('bad_date', [
    '01/12/2026 09:00',
    '2026-02-30 09:00',
    'invalid',
])
def test_invalid_dates_do_not_create_appointments(
    monkeypatch, capsys, bad_date
):
    """Invalid dates are rejected without creating an appointment."""
    output = run_console(monkeypatch, capsys, [
        '1', 'P1', 'Alex Example',
        '3', 'DR1', 'Taylor Example', 'General Practice',
        '5', 'A1', 'P1', 'DR1', bad_date,
        '7', 'A1',
        '5', 'A1', 'P1', 'DR1', '2026-12-01 09:00',
        '0',
    ])

    assert 'Error:' in output
    assert 'Error: Appointment not found' in output
    assert 'Appointment booked successfully.' in output


def test_unknown_menu_choice_recovers(monkeypatch, capsys):
    """An unknown choice does not stop the menu."""
    output = run_console(monkeypatch, capsys, [
        '99',
        '1', 'P1', 'Alex Example',
        '0',
    ])

    assert 'Invalid menu choice.' in output
    assert 'Patient P1 registered successfully.' in output


def test_repeated_cancellation_is_rejected(monkeypatch, capsys):
    """A cancelled appointment cannot be cancelled twice."""
    output = run_console(monkeypatch, capsys, [
        '1', 'P1', 'Alex Example',
        '3', 'DR1', 'Taylor Example', 'General Practice',
        '5', 'A1', 'P1', 'DR1', '2026-12-01 09:00',
        '6', 'A1',
        '6', 'A1',
        '7', 'A1',
        '0',
    ])

    assert output.count('Appointment cancelled successfully.') == 1
    assert 'Error:' in output
    assert 'A1: P1 with DR1, 2026-12-01 09:00, cancelled' in output


def test_unknown_patient_recovers(monkeypatch, capsys):
    """Unknown lookup is handled and a valid action still works."""
    output = run_console(monkeypatch, capsys, [
        '2', 'P999',
        '1', 'P1', 'Alex Example',
        '2', 'P1',
        '0',
    ])

    assert 'Error: Patient not found' in output
    assert 'Patient found: P1 - Alex Example' in output
