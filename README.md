# API Documentation

This document outlines the API endpoints and their functionalities.

## Endpoint: `/upload-csv` (POST)

**Summary:** Upload CSV file to insert into a MySQL database.

**Description:**
This endpoint allows users to upload CSV files, which are then processed and inserted into the MySQL database.

### Request:
- **Method:** POST
- **Request Headers:**
  - Content-Type: `multipart/form-data`
  - Custom Headers:
    - `table`: Must contain one of these table names - `departments`, `jobs`, `hiredemployees`
- **Request Body:**
  - Parameter: `file` (CSV file)

### Responses:
- **200 OK:** File uploaded successfully.
  - Content: `table`

- **400 Bad Request:** Invalid request.

---

## Endpoint: `/analytics/employees-hired` (GET)

**Summary:** Get number of employees hired by department and job in 2021.

**Description:**
Retrieves the count of employees hired for each job and department in 2021, segmented by quarter.

### Request:
- **Method:** GET

### Responses:
- **200 OK:** Successful operation.
  - Content: HTML table with the data.

---

## Endpoint: `/analytics/list-id-employees` (GET)

**Summary:** Get list of IDs, names, and number of employees hired for high-hiring departments.

**Description:**
Fetches the IDs, names, and employee count for departments that hired more employees than the mean of all departments in 2021.

### Request:
- **Method:** GET

### Responses:
- **200 OK:** Successful operation.
  - Content: HTML table with the data.
