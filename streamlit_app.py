import streamlit as st
from datetime import date
from src.agent import agent
from data.hospital_data import DEPARTMENTS, DOCTORS, AVAILABLE_SLOTS, BOOKINGS
from src.tools import confirm_demo_booking

st.set_page_config(page_title="Hospital Appointment Assistant", page_icon="🏥", layout="wide")

st.title("🏥 Hospital Appointment Assistant")
st.caption("LangChain + OpenAI • Streamlit classroom demo • Simulated data only")
st.warning("Educational demo only. Not connected to a real hospital. Do not enter sensitive medical information. Not for diagnosis, treatment, or emergencies.")

with st.sidebar:
    st.header("Hospital directory")
    st.subheader("Departments")
    for dept in DEPARTMENTS:
        st.write(f"• {dept}")
    st.divider()
    st.subheader("Doctors")
    for doctor in DOCTORS:
        st.markdown(f"**{doctor['name']}**  \n{doctor['department']} · {doctor['experience']}")
    st.caption("Available slots in the supplied demo data are currently dated 2026-10-15.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I can list departments, find doctors, check demo slots, and help with appointment requests. Try: “What slots are available with Dr. Ananya Rao on 2026-10-15?”"}
    ]
if "pending_booking" not in st.session_state:
    st.session_state.pending_booking = None

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask about departments, doctors, slots, or demo bookings…")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Checking the demo system…"):
            try:
                result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
                msgs = result.get("messages", [])
                # Show final assistant response. Tool messages are also scanned for a booking approval request.
                response = ""
                for item in reversed(msgs):
                    role = getattr(item, "type", None) or getattr(item, "role", None)
                    content = getattr(item, "content", "")
                    if role in ("ai", "assistant") and content:
                        if isinstance(content, str):
                            response = content
                        elif isinstance(content, list):
                            response = "\\n".join(
                                x.get("text", "") if isinstance(x, dict) else str(x)
                                for x in content
                            )
                        break
                if not response:
                    response = "I couldn't produce a response. Please try rephrasing."
                for item in msgs:
                    content = getattr(item, "content", "")
                    if isinstance(content, str) and "APPROVAL_REQUIRED |" in content:
                        try:
                            fields = {}
                            tail = content.split("APPROVAL_REQUIRED |", 1)[1]
                            for part in tail.split("|"):
                                if "=" in part:
                                    k, v = part.strip().split("=", 1)
                                    fields[k.strip()] = v.strip().split(". This is", 1)[0]
                            required = {"patient_name", "department", "doctor_name", "date", "time"}
                            if required.issubset(fields):
                                st.session_state.pending_booking = fields
                        except Exception:
                            pass
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as exc:
                error = f"Application error: {exc}\n\nCheck your API key, model access, internet connection, and installed requirements."
                st.error(error)
                st.session_state.messages.append({"role": "assistant", "content": error})

if st.session_state.pending_booking:
    b = st.session_state.pending_booking
    st.divider()
    st.subheader("Confirm demo appointment")
    st.info(
        f"**Patient:** {b['patient_name']}  \n"
        f"**Department:** {b['department']}  \n"
        f"**Doctor:** {b['doctor_name']}  \n"
        f"**Date:** {b['date']}  \n"
        f"**Time:** {b['time']}\n\n"
        "No booking is saved until you explicitly approve below."
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Approve demo booking", type="primary", use_container_width=True):
            try:
                booking = confirm_demo_booking(**b)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Demo appointment confirmed. Booking ID: **{booking['booking_id']}**"
                })
                st.session_state.pending_booking = None
                st.rerun()
            except Exception as exc:
                st.error(str(exc))
    with c2:
        if st.button("Reject / clear request", use_container_width=True):
            st.session_state.pending_booking = None
            st.session_state.messages.append({"role": "assistant", "content": "Booking request rejected. No appointment was saved."})
            st.rerun()

with st.expander("Book directly using the demo form"):
    with st.form("direct_booking_form"):
        patient = st.text_input("Patient name")
        department = st.selectbox("Department", DEPARTMENTS)
        doctors_for_dept = [d for d in DOCTORS if d["department"] == department]
        doctor_name = st.selectbox("Doctor", [d["name"] for d in doctors_for_dept])
        available_dates = sorted({d for doc, d in AVAILABLE_SLOTS if doc == doctor_name})
        if available_dates:
            chosen_date = st.selectbox("Date", available_dates)
            slots = AVAILABLE_SLOTS.get((doctor_name, chosen_date), [])
        else:
            chosen_date, slots = "", []
        chosen_time = st.selectbox("Available time", slots if slots else ["No slots available"])
        submitted = st.form_submit_button("Request appointment")
    if submitted:
        if not patient.strip():
            st.error("Enter a patient name.")
        elif not slots:
            st.error("No demo slots are available for this doctor.")
        else:
            st.session_state.pending_booking = {
                "patient_name": patient.strip(),
                "department": department,
                "doctor_name": doctor_name,
                "date": chosen_date,
                "time": chosen_time,
            }
            st.rerun()

with st.expander("Demo bookings currently saved"):
    if BOOKINGS:
        st.dataframe(BOOKINGS, use_container_width=True, hide_index=True)
    else:
        st.write("No demo bookings yet.")
