# Stage 6 Domain Test file

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import (AppointmentStatus, Appointment, Patient)
from smartcare.services import (AppointmentService, PatientService, PractitionerService)

def test_patient_valid_construction():
    patient = Patient('P1', 'Alex Example')

    assert patient.patient_id == 'P1'
    assert patient.name == 'Alex Example'


def test_blank_patient_id_rejected():
    with pytest.raises(ValueError):
        Patient('', 'Alex Example')


def test_whitespace_patient_id_rejected():
    with pytest.raises(ValueError):
        Patient('  ', 'Alex Example')


def test_blank_patient_name_rejected():
    with pytest.raises(ValueError):
        Patient('P1', '')


def test_whitespace_patient_name_rejected():
    with pytest.raises(ValueError):
        Patient('P1', '  ')