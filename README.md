# Blood Pressure Reporting Service

A RESTful API service for recording and reporting blood pressure measurements.
Built with FastAPI, this service allows users to record their blood pressure records and generate monthly statistical reports.

## Features

- **Record Blood Pressure Measurements**: Add systolic and diastolic records with timestamps for any user
- **Monthly Reports**: Generate comprehensive monthly reports with statistical analysis including:
  - Average systolic and diastolic values
  - Standard deviations
  - Average pulse pressure
  - Count of high records (>140/90 mmHg)
  - Count of low records (<100/60 mmHg)
- **Data Validation**: Automatic validation of blood pressure values and timestamps
- **Logging**: Comprehensive logging to both console and file
- **In-Memory Storage**: Fast, lightweight storage solution (data persists during server runtime)

## API Endpoints

### Health Check
```
GET /
```
Returns a simple health check message.

### Add Blood Pressure Reading
```
POST /users/{user_id}/blood-pressure
```
Adds a new blood pressure reading for a user.

**Path Parameters:**
- `user_id` (integer): The ID of the user (must be positive)

**Request Body:**
```json
{
  "systolic": 120,
  "diastolic": 80,
  "timestamp": "2024-01-15T10:00:00"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Blood pressure record added successfully"
}
```

**Validation Rules:**
- Systolic: 1-300 mmHg
- Diastolic: 1-200 mmHg
- Systolic must be greater than diastolic

### Get Monthly Report
```
GET /reports/monthly?year={year}&month={month}
```
Retrieves a monthly report for all users.

**Query Parameters:**
- `year` (integer): Year (1900-2100)
- `month` (integer): Month (1-12)

**Response:**
```json
[
  {
    "user_id": 1,
    "measurements_count": 5,
    "average_systolic": 120.5,
    "average_diastolic": 80.2,
    "systolic_std": 5.3,
    "diastolic_std": 3.1,
    "pulse_pressure_avg": 40.3,
    "high_records_count": 1,
    "low_records_count": 0
  }
]
```

## Input Validation Assumptions

This section documents all assumptions made for input validation and checks:

- **User ID**: Must be a positive integer (greater than 0)
- **Systolic Pressure**: Must be between 1-300 mmHg
- **Diastolic Pressure**: Must be between 1-200 mmHg
- **Systolic vs Diastolic**: Systolic value must be greater than diastolic value
- **Timestamp Format**: ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
- **Year Range**: Valid years are between 1900-2100
- **Month Range**: Valid months are 1-12 (January to December)
- **Future Dates**: Reports cannot be requested for future dates
- **Required Fields**: All fields (systolic, diastolic, timestamp) are required when adding a reading

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   git clone https://github.com/NogaHaimovich/blood-pressure.git
   cd blood-pressure
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Start the Development Server

```bash
uvicorn main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive API Documentation**: http://localhost:8000/docs
- **Alternative API Documentation**: http://localhost:8000/redoc

### Running with Custom Port

```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```


## Testing

Run the test suite using pytest:

```bash
pytest
```

1. **API Layer** (`main.py`): FastAPI routes and request handling
2. **Controller Layer** (`controller.py`): Request validation and error handling
3. **Service Layer** (`bp_service.py`): Business logic and statistics calculations
4. **Storage Layer** (`storage.py`): Data persistence (currently in-memory)
5. **Models/Schemas**: Data structures and validation rules

## Notes

- **Data Persistence**: Currently uses in-memory storage.
- **Date Validation**: The service prevents requesting reports for future dates.

## License

This project is provided as-is for educational and development purposes.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

