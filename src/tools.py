from typing import List

from langchain.tools import tool

from data.hospital_data import (
    AVAILABLE_SLOTS,
    BOOKINGS,
    DEPARTMENTS,
    DOCTORS,
)


@tool
def list_departments() -> List[str]:
    """List hospital departments available in the demo system."""
    return DEPARTMENTS


@tool
def find_doctors(department: str) -> List[dict]:
    """Find doctors belonging to a hospital department."""
    department_clean = department.strip().lower()
    results = [
        doctor
        for doctor in DOCTORS
        if doctor["department"].lower() == department_clean
    ]
    return results


@tool
def check_available_slots(doctor_name: str, date: str) -> List[str]:
    """Return available appointment times for a doctor on YYYY-MM-DD."""
    return AVAILABLE_SLOTS.get((doctor_name, date), [])


@tool
def book_appointment(
    patient_name: str,
    department: str,
    doctor_name: str,
    date: str,
    time: str,
) -> str:
    """Book a demo appointment only after explicit human confirmation."""
    valid_slots = AVAILABLE_SLOTS.get((doctor_name, date), [])

    if time not in valid_slots:
        return (
            f"Booking failed: {time} is not available for {doctor_name} "
            f"on {date}. Available slots: {valid_slots}"
        )

    existing = [
        b for b in BOOKINGS
        if b["doctor_name"] == doctor_name
        and b["date"] == date
        and b["time"] == time
    ]

    if existing:
        return "Booking failed: that slot has already been booked."

    print("\n--- HUMAN APPROVAL REQUIRED ---")
    print(f"Patient   : {patient_name}")
    print(f"Department: {department}")
    print(f"Doctor    : {doctor_name}")
    print(f"Date      : {date}")
    print(f"Time      : {time}")
    print("This is a DEMO booking. No real hospital system is connected.")

    approval = input("Type APPROVE to confirm, or anything else to cancel: ").strip()

    if approval.upper() != "APPROVE":
        return "Booking cancelled by human approval gate."

    booking = {
        "booking_id": f"DEMO-{len(BOOKINGS) + 1:04d}",
        "patient_name": patient_name,
        "department": department,
        "doctor_name": doctor_name,
        "date": date,
        "time": time,
    }
    BOOKINGS.append(booking)

    return (
        "Appointment booked successfully in the demo system. "
        f"Booking ID: {booking['booking_id']}"
    )


@tool
def cancel_appointment(booking_id: str) -> str:
    """Cancel an existing demo appointment by booking ID."""
    for booking in BOOKINGS:
        if booking["booking_id"] == booking_id:
            BOOKINGS.remove(booking)
            return f"Demo appointment {booking_id} cancelled."

    return f"No demo appointment found with booking ID {booking_id}."
