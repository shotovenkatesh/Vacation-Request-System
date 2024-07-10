from flask import Flask, request, jsonify
from transformers import pipeline
from database import get_employee, update_vacation_days
from datetime import datetime, timedelta

app = Flask(__name__)

# Initializing the NLP pipeline
qa_pipeline = pipeline('question-answering', model='distilbert-base-uncased')

# Initializing a dictionary to hold conversation states
conversations = {}

# rules
PROBATION_PERIOD = timedelta(days=90)
NOTICE_PERIOD = timedelta(days=30)
PAID_LEAVE_ENTITLEMENT = 20
PART_TIME_PAID_LEAVE_ENTITLEMENT = 10  # Example value
BLACKOUT_PERIODS = [(datetime(2024, 12, 15), datetime(2025, 1, 15))]  # Example blackout period


#  helper function to process the message
def process_message(employee_name, message):
    if employee_name not in conversations:
        conversations[employee_name] = {'state': 'initial'}

    state = conversations[employee_name]['state']
    employee = get_employee(employee_name)

    if not employee:
        return "Employee not found."

    if state == 'initial':
        if 'leave' in message.lower():
            conversations[employee_name]['state'] = 'request_type'
            return "Are you requesting a paid, unpaid, or emergency leave?"

    elif state == 'request_type':
        if 'paid' in message.lower():
            conversations[employee_name]['leave_type'] = 'paid'
        elif 'unpaid' in message.lower():
            conversations[employee_name]['leave_type'] = 'unpaid'
        elif 'emergency' in message.lower():
            conversations[employee_name]['leave_type'] = 'emergency'
        else:
            return "Please specify if you are requesting paid, unpaid, or emergency leave."

        conversations[employee_name]['state'] = 'dates'
        return "Please provide the start and end dates for your leave in the format 'YYYY-MM-DD to YYYY-MM-DD'."

    elif state == 'dates':
        try:
            start_date, end_date = message.split(' to ')
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            conversations[employee_name]['start_date'] = start_date
            conversations[employee_name]['end_date'] = end_date

            # Convert employee.start_date to datetime for comparison
            probation_end_date = datetime.combine(employee.start_date, datetime.min.time()) + PROBATION_PERIOD

            # Check probationary period for paid leave
            if conversations[employee_name]['leave_type'] == 'paid':
                if start_date < probation_end_date:
                    return "You are in the probation period, you cannot take paid leave. Would you like to request unpaid leave instead?"

            # Check blackout periods
            for blackout_start, blackout_end in BLACKOUT_PERIODS:
                if (start_date <= blackout_end and end_date >= blackout_start):
                    return "Your requested dates fall within a blackout period. Please choose different dates."

            # Check notice period
            if (start_date - datetime.now()).days < NOTICE_PERIOD.days:
                return "Leave requests must be submitted at least 30 days in advance for planned leave."

            # Check leave entitlement
            leave_days = (end_date - start_date).days + 1
            if conversations[employee_name]['leave_type'] == 'paid':
                if employee.vacation_days < leave_days:
                    return f"You do not have enough paid leave days available. You have {employee.vacation_days} days remaining."

            # Special case: emergency leave
            if conversations[employee_name]['leave_type'] == 'emergency':
                return "Your emergency leave request has been noted. Please follow up with HR for further processing."

            # Update vacation days in the database for paid leave
            if conversations[employee_name]['leave_type'] == 'paid':
                update_vacation_days(employee_name, leave_days)

            return "Your vacation request has been approved."
        except ValueError:
            return "The date format is incorrect. Please provide the dates in the format 'YYYY-MM-DD to YYYY-MM-DD'."

    return "I didn't understand that. Could you please repeat?"


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    employee_name = data['name']
    message = data['message']

    response = process_message(employee_name, message)

    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)
