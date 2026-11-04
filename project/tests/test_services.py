import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.services import PatientService


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
