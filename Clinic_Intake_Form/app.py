from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

EXCEL_FILE = 'clinic_intake_form.xlsx'

# Load or initialize Excel file
def load_excel():
    if not os.path.exists(EXCEL_FILE):
        event_df = pd.DataFrame(columns=[
            "Date of Clinic", "Type of Clinic", "Attorney Volunteers Present",
            "Non-Attorney Volunteers Present", "Staff Present", "PBI Office Reporting",
            "Clinic Feedback and Comments", "Service Type", "Clinic Location"
        ])
        participant_df = pd.DataFrame(columns=[
            "Event ID", "Service Agreement Accepted", "Name", "Date of Birth",
            "Provide Demographic Info", "Race/Ethnicity", "Gender", "Zip Code",
            "Email Address", "Phone Number", "Safe to Contact", "Employed",
            "Dependents", "Monthly Income", "Referral Source", "Legal Issue Types",
            "Family Law Issue"
        ])
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
            event_df.to_excel(writer, sheet_name='Event Information', index=False)
            participant_df.to_excel(writer, sheet_name='Participant Submissions', index=False)

@app.route('/', methods=['GET', 'POST'])
def event_form():
    if request.method == 'POST':
        session['event'] = request.form.to_dict()
        session['event_id'] = datetime.now().strftime('%Y%m%d%H%M%S')
        return redirect(url_for('participant_form'))
    return render_template('form.html', step='event')

@app.route('/participant', methods=['GET', 'POST'])
def participant_form():
    if request.method == 'POST':
        if request.form.get('add_participant') == 'no':
            try:
                save_event_and_participants()
                session.clear()
                return redirect(url_for('event_form'))
            except PermissionError:
                flash("Error: Unable to save data. Please close the Excel file and try again.")
                return redirect(url_for('participant_form'))

        participant = request.form.to_dict()
        if 'participants' not in session:
            session['participants'] = []
        session['participants'].append(participant)
        return redirect(url_for('participant_form'))

    return render_template('form.html', step='participant')

def save_event_and_participants():
    event_data = session.get('event', {})
    event_id = session.get('event_id')
    participants = session.get('participants', [])

    event_df = pd.read_excel(EXCEL_FILE, sheet_name='Event Information', engine='openpyxl')
    participant_df = pd.read_excel(EXCEL_FILE, sheet_name='Participant Submissions', engine='openpyxl')

    event_data_row = {**event_data}
    event_df = pd.concat([event_df, pd.DataFrame([event_data_row])], ignore_index=True)

    for p in participants:
        p['Event ID'] = event_id
        participant_df = pd.concat([participant_df, pd.DataFrame([p])], ignore_index=True)

    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='w') as writer:
        event_df.to_excel(writer, sheet_name='Event Information', index=False)
        participant_df.to_excel(writer, sheet_name='Participant Submissions', index=False)

if __name__ == '__main__':
    load_excel()
    app.run(debug=True)

