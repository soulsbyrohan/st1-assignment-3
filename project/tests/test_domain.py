
import pytest
from smartcare.domain import Practitioner


# Test 1: Create a practitioner with valid information
def test_create_practitioner_with_valid_details():
    doctor = Practitioner("DOC001", "John Smith", "Cardiology")

    assert doctor.practitioner_id == "DOC001"
    assert doctor.name == "John Smith"
    assert doctor.specialty == "Cardiology"


# Test 2: Check that an empty practitioner ID is rejected
def test_practitioner_empty_id():
    doctor_id = ""
    doctor_name = "John Smith"
    doctor_specialty = "Cardiology"

    with pytest.raises(ValueError):
        Practitioner(doctor_id, doctor_name, doctor_specialty)


# Test 3: Check that an empty name is rejected
def test_practitioner_empty_name():
    doctor_id = "DOC002"
    doctor_name = ""
    doctor_specialty = "Cardiology"

    with pytest.raises(ValueError):
        Practitioner(doctor_id, doctor_name, doctor_specialty)


# Test 4: Check that an empty specialty is rejected
def test_practitioner_empty_specialty():
    doctor_id = "DOC003"
    doctor_name = "Sarah Wilson"
    doctor_specialty = ""

    with pytest.raises(ValueError):
        Practitioner(doctor_id, doctor_name, doctor_specialty)


# Test 5: Check that a practitioner ID cannot contain only spaces
def test_practitioner_id_with_only_spaces():
    doctor_id = "   "
    doctor_name = "John Smith"
    doctor_specialty = "Cardiology"

    with pytest.raises(ValueError):
        Practitioner(doctor_id, doctor_name, doctor_specialty)


# Test 6: Check that a practitioner name cannot contain only spaces
def test_practitioner_name_with_only_spaces():
    doctor_id = "DOC004"
    doctor_name = "   "
    doctor_specialty = "Cardiology"

    with pytest.raises(ValueError):
        Practitioner(doctor_id, doctor_name, doctor_specialty)


# Test 7: Check that a specialty cannot contain only spaces
def test_practitioner_specialty_with_only_spaces():
    doctor_id = "DOC005"
    doctor_name = "Sarah Wilson"
    doctor_specialty = "   "

    with pytest.raises(ValueError):
        Practitioner(doctor_id, doctor_name, doctor_specialty)


# Test 8: Check that extra spaces are removed from valid information
def test_practitioner_removes_extra_spaces():
    doctor = Practitioner(
        " DOC006 ",
        " Sarah Wilson ",
        " Dermatology "
    )

    assert doctor.practitioner_id == "DOC006"
    assert doctor.name == "Sarah Wilson"
    assert doctor.specialty == "Dermatology"
