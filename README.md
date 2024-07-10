# Vacation Request System

This is a Flask-based AI system to manage and process vacation requests for employees based on company Standard Operating Procedures (SOPs). The AI system uses a pre-trained NLP model to understand and process the requests and ensure they comply with the company's SOPs.


## Project Description

The Vacation Request System is designed to handle and automate the process of requesting and approving vacation leaves for employees. It ensures that the requests comply with the company's SOPs, including probation periods, notice periods, blackout periods, and leave entitlements.

The system consists of:
- A Flask web application
- A database to store employee information
- An NLP model to process and understand natural language requests

## SOP Rules

1. **Scope**: Applicable to all employees within the company. Covers all types of leave: paid, unpaid, and emergency leave.
2. **Eligibility**:
   - Employees must complete a probationary period (typically 3-6 months) before becoming eligible for paid leave.
   - Unpaid leave can be requested during the probation period but is subject to managerial approval.
3. **Leave Entitlement**:
   - Full-time employees are entitled to a specific number of paid leave days per year (e.g., 20 days).
   - Part-time and temporary employees have prorated leave entitlements.
4. **Request Procedure**:
   - Notice Period: Leave requests must be submitted at least 30 days in advance for planned leave. Emergency leave must be reported as soon as possible.
   - Submission: Employees must submit leave requests via the designated system (e.g., HR software, email).
   - Approval Workflow: Leave requests are reviewed by the immediate supervisor, then forwarded to HR for final approval.
5. **Blackout Periods**: Certain times of the year may be designated as blackout periods during which leave requests are not granted (e.g., peak business seasons).
6. **Leave Balances and Carryover**:
   - Employees can check their leave balances through the HR system.
   - Unused leave days may be carried over to the next year, subject to a maximum limit.
7. **Special Circumstances**:
   - Medical Leave: Separate procedures for medical leave, requiring a doctor’s note.
   - Maternity/Paternity Leave: Specific entitlements and procedures for parental leave.
8. **Responsibilities**:
   - Employees: Ensure accurate and timely submission of leave requests.
   - Supervisors: Review and approve/deny leave requests based on operational needs.
   - HR Department: Maintain leave records, update balances, and ensure compliance with the SOP.
9. **Non-Compliance**: Disciplinary actions for non-compliance with the SOP, such as taking leave without approval.

## Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/shotovenkatesh/vacation-request-system.git
   cd vacation-request-system
2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`
3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt

4. Initialize the database with example data:

   ```bash
   python database.py

### Running The Application

1. Start the Flask app:

  ```bash
  python app.py
 ```

2. The app will be running at http://127.0.0.1:5000.

## Usage

You can interact with the AI system using curl commands or Postman:

Using curl
Initial Greeting:
  ```bash

curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"name": "Jane Smith", "message": "Hi, I need to take a leave."}'
 ```
Specify Leave Type:
```bash
curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"name": "Jane Smith", "message": "Paid leave."}'

 ```

Provide Leave Dates:
```bash
curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"name": "Jane Smith", "message": "2024-04-15 to 2024-04-18"}'

 ```
## Test Cases
**Test Case 1**: Employee in Probation Period Requests Paid Leave

**Request 1**: Initial Greeting
```bash
curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"name": "Jane Smith", "message": "Hi, I need to take a leave."}'

```
**Response:**
```json
{
  "response": "Are you requesting a paid, unpaid, or emergency leave?"
}
```
**Request 2**: Specify Leave Type

```bash
curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"name": "Jane Smith", "message": "Paid leave."}'


```
**Response:**
```json
{
  "response": "Please provide the start and end dates for your leave in the format 'YYYY-MM-DD to YYYY-MM-DD'."
}
```
**Request 3**: Providing Leave Dates Within Probation Period

```bash
curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"name": "Jane Smith", "message": "2024-04-15 to 2024-04-18"}'
```
**Response:**

```json
{
  "response": "You are in the probation period, you cannot take paid leave. Would you like to request unpaid leave instead?"
}
```
### Test Case 2: Employee Requests Leave Within Blackout Period

**Request 1**: Initial Greeting

```bash
curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"name": "John Doe", "message": "Hi, I need to take a leave."}'
```


### Test Case 2: Employee Requests Leave Within Blackout Period

**Request 1**: Initial Greeting

```bash
curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"name": "John Doe", "message": "Hi, I need to take a leave."}'
```
Response:

json
```json
{
  "response": "Are you requesting a paid, unpaid, or emergency leave?"
}
```
## Request 2: Specify Leave Type

```bash
curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"name": "John Doe", "message": "Paid leave."}'
```
Response:

```json
{
  "response": "Please provide the start and end dates for your leave in the format 'YYYY-MM-DD to YYYY-MM-DD'."
}
```
## Request 3: Provide Leave Dates Within Blackout Period

```bash
curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"name": "John Doe", "message": "2024-12-20 to 2024-12-25"}'
```
Response:

```json
{
  "response": "Your requested dates fall within a blackout period. Please choose different dates."
}
```

## Test Case 3: Employee Requests Leave Without Adequate Notice
Request 1: Initial Greeting

```bash
curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"name": "Jane Smith", "message": "Hi, I need to take a leave."}'
```
Response:

```json
{
  "response": "Are you requesting a paid, unpaid, or emergency leave?"
}
```
Request 2: Specify Leave Type

```bash
curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"name": "Jane Smith", "message": "Paid leave."}'
```
Response:

```json
{
  "response": "Please provide the start and end dates for your leave in the format 'YYYY-MM-DD to YYYY-MM-DD'."
}
```
Request 3: Provide Leave Dates Without Adequate Notice

```bash
curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"name": "Jane Smith", "message": "2024-04-10 to 2024-04-15"}'
```
Response:

```json
{
  "response": "Leave requests must be submitted at least 30 days in advance for planned leave."
}
```

# Code Explanation
## app.py
This file contains the Flask application that handles the vacation requests.

**Initialization**: The app initializes a Flask application and sets up an NLP pipeline using Hugging Face's transformers library.
**State Management**: A dictionary named conversations is used to keep track of the state of each conversation.
**Message Processing**: The process_message function handles incoming messages and processes them according to the current state of the conversation.
**Routes**: The /chat route handles POST requests to process chat messages.

## database.py
This file sets up the database schema and provides functions to interact with the database.

**Database Setup**: Uses SQLAlchemy to create a SQLite database and define the Employee model.
**Data Initialization**: Example data is inserted into the database if it doesn't already exist.
**Functions**: Functions to get an employee by name and update vacation days.

## requirements.txt
This file lists the dependencies required to run the project.
```bash
Flask==2.0.2
transformers==4.11.3
torch==1.10.0
SQLAlchemy==1.4.27
```
## NLP Model
The NLP model used in this project is a pre-trained model from the Hugging Face transformers library. Specifically, the DistilBERT model is utilized for its efficiency and performance in understanding and processing natural language.

**Applications in the Project
Understanding Requests**: 
The NLP model is used to understand and parse natural language requests from employees. For example, when an employee requests a leave, the model helps in determining the type of leave, the start and end dates, and any other relevant information.

**Ensuring Compliance**: The NLP model aids in ensuring that the leave requests comply with the company's SOPs. It helps in checking conditions such as probation periods, notice periods, and blackout periods.

**Conversation Management**: The model assists in managing the state of conversations. Depending on the context of the conversation, it prompts users for additional information or provides appropriate responses.

**Example Usage**
When an employee sends a message like "I need to take a paid leave from 2024-04-15 to 2024-04-18," the NLP model processes this message to extract the leave type and dates. It then checks if the employee is eligible for paid leave and if the requested dates comply with the SOP rules.
