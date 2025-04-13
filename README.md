# Assignment Task 1: Linear Feedback Shift Register (LFSR)

This project implements a Linear Feedback Shift Register (LFSR) in Python, as specified in Assignment Task 1. LFSRs are used in stream ciphers to generate pseudo-random bit sequences. The task involves creating two classes:

1. **`BasicLFSR`**: A fixed 4-bit LFSR with a specific configuration.
2. **`GeneralLFSR`**: A customizable LFSR that allows setting the register size, state, and tap sequence.

The implementations follow the specifications provided in the assignment and include a demonstration program to verify their correctness.

## Table of Contents

- [Introduction to LFSRs](#introduction-to-lfsrs)
- [BasicLFSR Class](#basiclfsr-class)
- [GeneralLFSR Class](#generallfsr-class)
- [Usage Examples](#usage-examples)
- [Verification](#verification)
- [Running the Demonstration Program](#running-the-demonstration-program)

## Introduction to LFSRs

A Linear Feedback Shift Register (LFSR) is a shift register whose input bit is a linear function of its previous state. The most common linear function used is the XOR of specific bits, known as "taps." LFSRs are widely used in digital systems for generating pseudo-random sequences, such as in stream ciphers for encryption.

In this project:
- The LFSR shifts its bits to the right.
- The least significant bit (LSB) is output as the stream bit.
- The feedback bit is computed by XORing the bits at the tap positions and is inserted as the new most significant bit (MSB).

## BasicLFSR Class

The `BasicLFSR` class implements a 4-bit LFSR with a fixed configuration:
- **Initial state**: `0110` (where the state is represented as `[R3, R2, R1, R0]`).
- **Taps**: Positions 0 and 3 (corresponding to `R3` and `R0` in the state list).

### Feedback Function
The feedback bit is computed as the XOR of `R0` and `R3`. This configuration ensures a maximal period of 15 states before repeating, as shown in the assignment table.

### Methods
- **`__init__()`**: Initializes the LFSR with the state `[0, 1, 1, 0]`.
- **`set_state(state)`**: Sets the state to a 4-bit list of 0s and 1s.
- **`get_state()`**: Returns the current state.
- **`next_stream_bit()`**: Generates the next stream bit (LSB), computes the feedback bit, shifts the state right, and inserts the feedback bit as the new MSB.

## GeneralLFSR Class

The `GeneralLFSR` class provides a flexible LFSR implementation that can be customized for different register sizes and tap sequences.

### Features
- Allows setting the register size.
- Supports any tap sequence (list of indices for XOR feedback).
- Can be reset to an all-zero state.

### Methods
- **`__init__(size, taps, initial_state=None)`**: Initializes the LFSR with the given size, taps, and optional initial state (defaults to all zeros).
- **`set_size(size)`**: Sets the register size and resets the state to all zeros.
- **`get_size()`**: Returns the current register size.
- **`set_state(state)`**: Sets the state to a list matching the register size.
- **`get_state()`**: Returns the current state.
- **`set_taps(taps)`**: Sets the tap sequence.
- **`reset()`**: Resets the state to all zeros.
- **`next_stream_bit()`**: Generates the next stream bit (LSB), computes the feedback bit by XORing the tap positions, shifts the state right, and inserts the feedback bit as the new MSB.

## Usage Examples

### BasicLFSR Usage

```python
from lfsr import BasicLFSR

# Initialize BasicLFSR
lfsr = BasicLFSR()

# Print initial state
print("Initial state:", lfsr.get_state())

# Generate and print the next stream bit and updated state
for _ in range(5):
    stream_bit = lfsr.next_stream_bit()
    print(f"Stream bit: {stream_bit}, New state: {lfsr.get_state()}")
```

### GeneralLFSR Usage

```python
from lfsr import GeneralLFSR

# Initialize GeneralLFSR with size 4, taps at positions 0 and 3, and initial state [0, 1, 1, 0]
lfsr = GeneralLFSR(size=4, taps=[0, 3], initial_state=[0, 1, 1, 0])

# Print initial state
print("Initial state:", lfsr.get_state())

# Generate and print the next stream bit and updated state
for _ in range(5):
    stream_bit = lfsr.next_stream_bit()
    print(f"Stream bit: {stream_bit}, New state: {lfsr.get_state()}")

# Reset the LFSR
lfsr.reset()
print("State after reset:", lfsr.get_state())
```

## Verification

The correctness of both implementations was verified by:
1. Running the `BasicLFSR` for 20 iterations and checking that the state sequence matches the expected 15-state cycle from the assignment table, repeating after every 15 steps.
2. Configuring the `GeneralLFSR` to match the `BasicLFSR` (size=4, taps=[0, 3], initial_state=[0, 1, 1, 0]) and confirming that it produces the same sequence.

The output for both classes matches the expected state transitions, as shown in the assignment document.

## Running the Demonstration Program

The main program demonstrates both classes:
- It initializes a `BasicLFSR` and prints the state and stream bit for 20 iterations.
- It then initializes a `GeneralLFSR` with the same configuration and repeats the process, verifying that both produce identical output.

To run the demonstration:
1. Ensure you have Python installed.
2. Run the following command in your terminal:

```bash
python lfsr.py
```

---
---
---

# Assignment Task 2: Stock Warehouse API

This project is a Django-based API designed to manage a stock warehouse system. It handles items, purchases, and sales while providing a reporting feature to track stock changes over time. The system follows best practices for modularity, scalability, and maintainability, ensuring it can be easily extended or integrated into larger systems.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [How It Works](#how-it-works)
  - [Items](#items)
  - [Purchases](#purchases)
  - [Sales](#sales)
  - [Stock Management](#stock-management)
  - [Reporting](#reporting)
- [Soft Delete Mechanism](#soft-delete-mechanism)
- [Error Handling](#error-handling)
- [Example Usage](#example-usage)

## Overview
The Stock Warehouse API allows users to manage inventory in a warehouse setting. It supports creating and managing items, recording purchases to replenish stock, and logging sales to deplete stock. Additionally, it provides a reporting feature to generate stock change reports over specified date ranges, helping with audit and inventory tracking.

## Features
- **Item Management**: Create, read, update, and soft delete items.
- **Purchase Management**: Record purchases to increase stock and update balance.
- **Sale Management**: Record sales to decrease stock and update balance using a FIFO (First In, First Out) approach.
- **Stock Reporting**: Generate detailed stock reports for specific items over a given date range.
- **Soft Delete**: All deletions are soft deletes, preserving data for audit purposes.
- **RESTful API**: Follows REST conventions for easy integration and usage.

## Tech Stack
- **Django 5.1.3**: Web framework for building the API.
- **Django REST Framework 3.15.2**: Toolkit for building Web APIs.
- **SQLite**: Default database (can be swapped for other databases supported by Django).

## Project Structure
```
Assignment 2/
├── README.md
├── manage.py
├── warehouse/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── api/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations/
    ├── models.py
    ├── serializers.py
    ├── urls.py
    └── views.py
```

- **`api/models.py`**: Defines database models for items, purchases, sales, and allocations.
- **`api/serializers.py`**: Serializers for converting model instances to JSON.
- **`api/views.py`**: API views handling requests and responses.
- **`api/urls.py`**: URL routing for API endpoints.
- **`warehouse/settings.py`**: Django project settings.
- **`warehouse/urls.py`**: Root URL configuration.

## Setup Instructions
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Assignment\ 2
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install django==5.1.3 djangorestframework==3.15.2
   ```

4. **Apply database migrations**:
   ```bash
   python manage.py makemigrations api
   python manage.py migrate
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the API** at `http://127.0.0.1:8000/`.

## API Endpoints
- **Items**:
  - `GET /items/`: List all items.
  - `GET /items/{code}/`: Retrieve a specific item.
  - `POST /items/`: Create a new item.
  - `PUT /items/{code}/`: Update an existing item.
  - `DELETE /items/{code}/`: Soft delete an item.
- **Purchases**:
  - `GET /purchase/`: List all purchase headers.
  - `GET /purchase/{code}/`: Retrieve a specific purchase header.
  - `POST /purchase/`: Create a new purchase header.
  - `PUT /purchase/{code}/`: Update a purchase header.
  - `DELETE /purchase/{code}/`: Soft delete a purchase header and its details.
  - `GET /purchase/{header_code}/details/`: List details for a specific purchase.
  - `POST /purchase/{header_code}/details/`: Add a detail to a specific purchase.
- **Sales**:
  - `GET /sell/`: List all sale headers.
  - `GET /sell/{code}/`: Retrieve a specific sale header.
  - `POST /sell/`: Create a new sale header.
  - `PUT /sell/{code}/`: Update a sale header.
  - `DELETE /sell/{code}/`: Soft delete a sale header and its details.
  - `GET /sell/{header_code}/details/`: List details for a specific sale.
  - `POST /sell/{header_code}/details/`: Add a detail to a specific sale.
- **Report**:
  - `GET /report/{item_code}/?start_date=yyyy-mm-dd&end_date=yyyy-mm-dd`: Generate a stock report for an item over a date range.

## How It Works

### Items
- Items represent the goods stored in the warehouse.
- Each item has a unique `code`, `name`, `unit`, `description`, `stock` (current quantity), and `balance` (current value).
- Stock and balance are automatically updated when purchases or sales are made.

### Purchases
- Purchases are used to replenish stock.
- A purchase consists of a header (metadata like `code`, `date`, and `description`) and details (specific items bought).
- When a purchase detail is created, it increases the item's `stock` by the purchased quantity and the `balance` by `quantity * unit_price`.

### Sales
- Sales are used to deplete stock.
- A sale consists of a header (metadata) and details (specific items sold).
- Sales deplete stock using a **FIFO (First In, First Out)** approach:
  - The system tracks which purchase batches are depleted by each sale.
  - It decreases the item's `stock` by the sold quantity and the `balance` by the total cost of the depleted batches.

### Stock Management
- **Purchases**: Increase stock and balance.
- **Sales**: Decrease stock and balance based on the cost of the oldest available stock (FIFO).
- The system ensures that sales cannot be made if there is insufficient stock.

### Reporting
- The reporting feature generates a detailed stock report for a specific item over a given date range.
- The report includes:
  - A list of transactions (purchases and sales) within the date range.
  - For each transaction, it shows the date, description, code, incoming/outgoing quantities, prices, and totals.
  - A summary of total incoming, outgoing, and remaining stock.
- The report accounts for stock from purchases before the start date and correctly handles FIFO depletion for sales.

## Soft Delete Mechanism
- All deletions are **soft deletes**, meaning records are marked as deleted (`is_deleted=True`) but not removed from the database.
- This preserves data for audit purposes and allows for potential recovery.
- Soft-deleted records are excluded from API responses and stock calculations.

## Error Handling
- The API includes validation to prevent invalid operations, such as:
  - Selling more stock than available.
  - Using invalid date formats in report requests.
  - Attempting to access non-existent or deleted records.
- Appropriate error messages are returned in such cases.

## Example Usage
1. **Create an Item**:
   ```bash
   curl -X POST http://127.0.0.1:8000/items/ \
   -H "Content-Type: application/json" \
   -d '{"code": "I-001", "name": "History Book", "unit": "Pcs", "description": "Books that tell the history of the ancient"}'
   ```

2. **Create a Purchase**:
   - First, create a purchase header:
     ```bash
     curl -X POST http://127.0.0.1:8000/purchase/ \
     -H "Content-Type: application/json" \
     -d '{"code": "P-001", "date": "2025-01-01", "description": "Buy history books"}'
     ```
   - Then, add a purchase detail:
     ```bash
     curl -X POST http://127.0.0.1:8000/purchase/P-001/details/ \
     -H "Content-Type: application/json" \
     -d '{"item_code": "I-001", "quantity": 10, "unit_price": 60000}'
     ```

3. **Create a Sale**:
   - First, create a sale header:
     ```bash
     curl -X POST http://127.0.0.1:8000/sell/ \
     -H "Content-Type: application/json" \
     -d '{"code": "S-001", "date": "2025-03-01", "description": "Sell history books to library"}'
     ```
   - Then, add a sale detail:
     ```bash
     curl -X POST http://127.0.0.1:8000/sell/S-001/details/ \
     -H "Content-Type: application/json" \
     -d '{"item_code": "I-001", "quantity": 5}'
     ```

4. **Generate a Report**:
   ```bash
   curl -X GET "http://127.0.0.1:8000/report/I-001/?start_date=2025-01-01&end_date=2025-03-31"
   ```
   - This will return a JSON report detailing stock changes, including purchases and sales, with a summary of total stock movements.
