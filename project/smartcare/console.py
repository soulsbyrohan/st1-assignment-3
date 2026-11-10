
"""Console helpers and interactive menu for SmartCare."""

import re
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def parse_date_time(text: str) -> datetime:
    """Parse YYYY-MM-DD HH:MM and reject invalid dates."""
    if (
        not isinstance(text, str)
        or re.fullmatch(
            r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}',
            text,
        ) is None
    ):
        raise ValueError('Use date/time format YYYY-MM-DD HH:MM')

    try:
        return datetime.strptime(text, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValueError(
            'Invalid calendar date/time; use YYYY-MM-DD HH:MM'
        ) from None


def format_appointment(appointment: Appointment) -> str:
    """Return readable appointment details without changing state."""
    return (
        f'{appointment.appointment_id}: '
        f'{appointment.patient.patient_id} with '
        f'{appointment.practitioner.practitioner_id}, '
        f'{appointment.date_time:%Y-%m-%d %H:%M}, '
        f'{appointment.status.value}'
    )


def run_demo() -> None:
    """Demonstrate registration and booking with synthetic records."""
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)

    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner(
        'DR1',
        'Taylor Example',
        'General practice',
    )

    try:
        appointments.book_appointment(
            'A1',
            'P1',
            'DR1',
            parse_date_time('2026-10-01 09:00'),
        )
        print(format_appointment(appointments.find_appointment('A1')))
    except (ValueError, LookupError) as error:
        print(f'Error: {error}')

    print('Session-only data: records are lost on exit.')


def run_menu() -> None:
    """Run the interactive SmartCare menu using one shared store."""
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)

    while True:
        print('\n===== SmartCare Menu =====')
        print('1. Register patient')
        print('2. Find patient')
        print('3. Register practitioner')
        print('4. Find practitioner')
        print('5. Book appointment')
        print('6. Cancel appointment')
        print('7. Find appointment')
        print('8. List practitioner appointments')
        print('0. Exit')

        try:
            choice = input('Enter your choice: ').strip()

            if choice == '0':
                print('Exiting SmartCare.')
                print('Session data will be lost.')
                break

            elif choice == '1':
                patient_id = input('Enter patient ID: ').strip()
                name = input('Enter patient name: ').strip()

                patient = patients.register_patient(patient_id, name)
                print(
                    f'Patient {patient.patient_id} registered successfully.'
                )

            elif choice == '2':
                patient_id = input('Enter patient ID: ').strip()

                patient = patients.find_patient(patient_id)
                print(
                    f'Patient found: {patient.patient_id} - {patient.name}'
                )

            elif choice == '3':
                practitioner_id = input(
                    'Enter practitioner ID: '
                ).strip()
                name = input('Enter practitioner name: ').strip()
                specialty = input('Enter specialty: ').strip()

                practitioner = practitioners.register_practitioner(
                    practitioner_id,
                    name,
                    specialty,
                )
                print(
                    f'Practitioner {practitioner.practitioner_id} '
                    'registered successfully.'
                )

            elif choice == '4':
                practitioner_id = input(
                    'Enter practitioner ID: '
                ).strip()

                practitioner = practitioners.find_practitioner(
                    practitioner_id
                )
                print(
                    f'Practitioner found: {practitioner.practitioner_id} '
                    f'- {practitioner.name} ({practitioner.specialty})'
                )

            elif choice == '5':
                appointment_id = input(
                    'Enter appointment ID: '
                ).strip()
                patient_id = input('Enter patient ID: ').strip()
                practitioner_id = input(
                    'Enter practitioner ID: '
                ).strip()
                date_text = input(
                    'Enter date/time (YYYY-MM-DD HH:MM): '
                ).strip()

                date_time = parse_date_time(date_text)

                appointment = appointments.book_appointment(
                    appointment_id,
                    patient_id,
                    practitioner_id,
                    date_time,
                )

                print('Appointment booked successfully.')
                print(format_appointment(appointment))

            elif choice == '6':
                appointment_id = input(
                    'Enter appointment ID to cancel: '
                ).strip()

                appointment = appointments.cancel_appointment(
                    appointment_id
                )

                print('Appointment cancelled successfully.')
                print(format_appointment(appointment))

            elif choice == '7':
                appointment_id = input(
                    'Enter appointment ID: '
                ).strip()

                appointment = appointments.find_appointment(
                    appointment_id
                )

                print('Appointment found:')
                print(format_appointment(appointment))

            elif choice == '8':
                practitioner_id = input(
                    'Enter practitioner ID: '
                ).strip()
                status_text = input(
                    'Enter status (scheduled/cancelled/completed) '
                    'or leave blank for all: '
                ).strip().lower()

                if status_text == '':
                    status = None
                else:
                    try:
                        status = AppointmentStatus(status_text)
                    except ValueError:
                        raise ValueError(
                            'Invalid status. Use scheduled, '
                            'cancelled or completed.'
                        ) from None

                results = appointments.list_practitioner_appointments(
                    practitioner_id,
                    status,
                )

                if not results:
                    print('No matching appointments found.')
                else:
                    print('Appointments:')
                    for appointment in results:
                        print(format_appointment(appointment))

            else:
                print('Invalid menu choice. Please try again.')

        except (ValueError, LookupError) as error:
            print(f'Error: {error}')

        except (EOFError, KeyboardInterrupt):
            print('\nExiting SmartCare.')
            print('Session data will be lost.')
            break


def handle_book_appointment(service: AppointmentService) -> None:
    """Handle a booking using the existing appointment service."""
    try:
        # Ask the user to enter the details needed for a booking
        appointment_id = input('Appointment ID: ')
        patient_id = input('Patient ID: ')
        practitioner_id = input('Practitioner ID: ')
        date_text = input('Date (YYYY-MM-DD): ')
        time_text = input('Time (HH:MM): ')

        # Convert the entered date and time into a datetime object
        when = parse_date_time(f'{date_text} {time_text}')

        # Use the existing appointment service to create the booking
        appointment = service.book_appointment(
            appointment_id, patient_id, practitioner_id, when
        )

        # Display a confirmation with the booked appointment details
        print(f'Appointment booked: {format_appointment(appointment)}')

    # Handle invalid inputs or unknown records without crashing
    except (ValueError, LookupError) as error:
        print(f'Error: {error}')


def handle_cancel_appointment(service: AppointmentService) -> None:
    """Handle cancellation using the existing appointment service."""
    try:
        # Ask the user which appointment they want to cancel
        appointment_id = input('Appointment ID to cancel: ')

        # Use the existing service to cancel the appointment
        appointment = service.cancel_appointment(appointment_id)

        # Display the cancelled appointment details
        print(f'Appointment cancelled: {format_appointment(appointment)}')

    # Handle invalid IDs, unknown appointments or repeated cancellation
    except (ValueError, LookupError) as error:
        print(f'Error: {error}')
    