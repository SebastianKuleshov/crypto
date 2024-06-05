# Crypto

## Introduction
This project is a basic web application that includes:
- User login and registration
- Currency rates parsing from Binance
- A simulated "storage" within the platform containing tokens (e.g., 1000 BTC, 30000 USDT, 15 ETH)
- User and superuser interactions for token transactions

## Features
### User Authentication:
- Basic login and registration functionality.

### Currency Parsing:
- Fetch and display the latest currency rates from Binance.

### Token Storage:
- A central storage managed by the superuser, which holds various tokens.
- Initial tokens: 1000 BTC, 12000 USDT, 5 ETH.

### Superuser Capabilities:
- Ability to adjust the number and types of tokens in the storage via an interface (not through Django admin).
- View balances of all users and details of all transactions in tables.

### User Requests and Transactions:
- Users can request tokens from the storage (e.g., 1 BTC).
- Superuser can approve or deny requests.
- Upon approval, the requested amount is deducted from the storage and added to the user's balance.

### Currency Conversion:
- Users can convert their tokens based on the rates fetched from Binance.
- Example: Convert 1 BTC to 70000 USDT and update the user's balance accordingly.

## Installation
To run this project locally:

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Set up a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

7. Access the application:
    Open your web browser and go to http://127.0.0.1:8000/.

## Usage
### Superuser Setup:
- Log in with superuser credentials.
- Adjust token quantities in the storage as needed through the provided interface.

### User Interaction:
- Register and log in as a user.
- Request tokens from the storage.
- Convert tokens using the conversion feature based on the latest Binance rates.

### Handling Requests:
- Superuser reviews and approves or denies user requests.
- Approved transactions update both the storage and the user's balance.