import pytest

from smartcare.data_store import SmartCareDataStore
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