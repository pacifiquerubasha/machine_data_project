# MACHINE_DATA_PROJECT

This repository contains a Python-based application that processes and analyzes simulated machine data and exposes a basic REST API to interact with the data.

---

## Project Structure

The project is organized into the following directories:

```plaintext
MACHINE_DATA_PROJECT/
├── analytics/
│   ├── data_analytics.py
│   └── __init__.py
├── data/
│   └── machine_data.json
├── data_process/
│   ├── data_generator.py
│   ├── data_processor.py
│   ├── __init__.py
│   └── main.py
├── flask_api/
│   ├── app.py
│   ├── controllers.py
│   ├── routes.py
│   ├── lib/
│   │   └── __init__.py
│   └── requirements.txt
└── README.md

### Folder Structure Explanation

- **analytics/**: Contains the data analytics functionality.
- **data/**: Stores the simulated machine data.
- **data_process/**: Handles the data ingestion and processing.
- **flask_api/**: Implements the Flask-based REST API.
- **controllers/**: Contains API controllers for handling logic.
- **routes/**: Defines API routes.
- **lib/**: Contains shared utility modules and libraries.
- **requirements.txt**: Lists the project's dependencies.
- **README.md**: This documentation file.


## Tasks Completed

### Data Ingestion and Processing
- The `data_process/main.py` script:
  - Reads a continuous stream of simulated machine data (temperature, speed, and status) from a JSON file every 10 seconds.
  - Transforms the data to calculate a moving average for each parameter over the last 5 readings.
  - Outputs the transformed data in JSON format.

### Basic REST API Development
- The `flask_api/app.py` script sets up a simple Flask-based REST API with two endpoints:
  - **GET `/data`**: Returns the processed machine data as JSON.
  - **POST `/status`**: Allows updating the machine's job status (e.g., "STARTED", "COMPLETED").
    - Includes input validation to ensure only allowed statuses are accepted.
    - Stores the machine status updates in memory.

### Simple Data Analytics
- The `analytics/data_analytics.py` script:
  - Implements a Python function that reads a list of timestamps and values (e.g., machine speed) and calculates:
    - The average value over the entire period.
    - The maximum and minimum values.
  - Includes a bonus feature to detect anomalies (i.e., if any value deviates by more than 20% from the average).
```

## How to Run

### Data Ingestion and Processing

1. Navigate to the `data_process` directory.
2. Run the following command:
   ```bash
   python3 main.py
   ```

### Basic REST API

1. Navigate to the `flask_api` directory.
2. Run the following command to start the Flask API:
   ```bash
   PYTHONPATH=.. python3 app.py
   ```
3. The API will be available at http://localhost:5000.

### Data Analytics

1. Navigate to the project's root directory.
2. Run the following command to execute the data analytics script:
   ```bash
   python3 analytics/data_analytics.py
   ```

## Dependencies

The project's dependencies are listed in the flask_api/requirements.txt file. You can install them using the following command:

```bash
pip install -r flask_api/requirements.txt
```

## App Tests README

This project includes unit tests to ensure the correctness of the app's core functionalities. The tests are implemented using the `unittest` framework.

### Test Files

1. **test_data_generation**:  
   This file contains tests related to the generation of machine data. It verifies the correct structure, data types, and behavior of functions that simulate machine data generation and its saving to a JSON file.

2. **test_data_analytics**:  
   This file contains tests related to the analysis and processing of the generated data. It checks whether the app correctly analyzes the data, performs required calculations, and handles edge cases.

### Running the Tests

To run the tests, use the following command:

```bash
python -m unittest discover -s tests
```
