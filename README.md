# 💹 PyEconomy: Persistent Banking & Corporate Simulator

![Version](https://img.shields.io/badge/version-1.1.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)

A terminal-based economic engine designed to simulate complex financial relationships. This project transitions from simple scripting to **System Engineering**, featuring persistent data, secure accounts, and a multi-entity marketplace.

---

## 📖 Table of Contents
* [Core Features](#-core-features)
* [The Time-Jump Engine](#-the-time-jump-engine)
* [System Architecture](#-system-architecture)
* [Installation](#-installation)
* [Project Goals](#-project-goals)

---

## ✨ Core Features

* **🔐 Secure Authentication:** Multi-user login system. Passwords are protected using `hashlib` to ensure data privacy.
* **💾 JSON Persistence:** The entire state of the world (users, balances, companies) is saved to a local database file.
* **🏦 Banking & Debt:** Users can deposit into interest-bearing savings accounts or take out loans with compounding interest.
* **🏢 Corporate Management:** Users can found companies, set salary structures, and hire other users to work for them.
* **📊 Transaction Integrity:** Advanced validation prevents "double-spending," overdrafts, and negative transfers.

---

## ⏳ The Time-Jump Engine (Admin Feature)

The simulation includes a powerful **Temporal Controller**. Administrators can "fast-forward" the entire economy by a set number of days. This isn't just a number change; it triggers a **Cascading Update Logic**:

1.  **Compound Interest:** Accrues interest for all savings and debt across the entire user base.
2.  **Payroll Cycles:** Automatically transfers salary budgets from Companies to Employees.
3.  **Entity Checks:** If a company lacks funds for payroll on "Day 4" of a 30-day jump, the engine halts their operations and flags them as bankrupt.



---

## 🏗 System Architecture

The project is built using a **Modular Design** to ensure that data management and user interaction remain separate.

* **`auth.py`**: Manages registration, logins, and password hashing.
* **`economy_logic.py`**: Contains the math for interest, tax, and the Time-Jump engine.
* **`data_manager.py`**: Handles the reading and writing of the `database.json` file.
* **`main.py`**: The primary Command Line Interface (CLI) for users.



---

## 🛠 Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/py-economy.git](https://github.com/yourusername/py-economy.git)
    cd py-economy
    ```
2.  **Initialize the Database:**
    ```bash
    python init_db.py
    ```
3.  **Run the Simulation:**
    ```bash
    python main.py
    ```

---

## 🎯 Project Goals

This project represents an **order of magnitude** increase in complexity from basic logic scripts:

* **State Management:** Moving from temporary variables to a persistent global state.
* **Relational Logic:** Understanding how a change in one entity (Company) affects another (User Wallet).
* **Algorithmic Thinking:** Implementing the Time-Jump engine requires applying mathematical formulas across a large dataset in a loop.

---

## 💻 Technical Example

```python
# Example of the Time-Jump Logic flow
def fast_forward(days):
    for day in range(days):
        apply_interest_rates()
        process_corporate_payroll()
        check_for_bankruptcies()
    save_database()
