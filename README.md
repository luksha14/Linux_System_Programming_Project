# Linux System Programming Project (Python)

This project was developed as part of the **Operating Systems** course at the **University of Rijeka, Faculty of Informatics and Digital Technologies**.  
The entire project was implemented and tested on the **Ubuntu Linux** platform, using only built-in Python modules — without any external dependencies.

---

## 🧩 Overview

The program is a console-based interactive system that demonstrates **process control**, **signal handling**, and **multithreaded synchronization** in Linux.  
It presents a main menu that allows the user to select between four functional tasks, each illustrating a core operating system concept.

---

## ⚙️ Functionalities

### 1️⃣ Process Management
- Allows the user to input a number `n` (1–20).
- Creates a **child process** using the `fork()` system call.
- The child process switches to the user’s home directory and displays information for itself, its parent, and grandparent process in a **tabular format**:
  - PID (Process ID)
  - PPID (Parent Process ID)
  - UID (User ID)
  - Priority
- The child runs for `n` seconds before returning control to the main process.
- Properly avoids **zombie processes**.

### 2️⃣ Signal Handling
- The user inputs a **signal name** (e.g., `INT`, `SIGTERM`, `SIGHUP`).
- The program validates the input and sends the corresponding signal to its own interpreter.
- If the signal is **SIGHUP** or **SIGABRT**, the current **stack trace** is written to a file `stacking.txt` on the **Desktop**.
- Signals `10`, `12`, and `18` are ignored, while others behave as per default Linux handling.
- Custom signal handlers are implemented using the `signal` module.

### 3️⃣ Multithreading and Synchronization
- The user enters a positive integer `m > 3,000,000`.
- The program launches **three threads**, each computing a portion of the sum of square roots in the interval `[1, m]`:
  \\( \sqrt{1} + \sqrt{2} + ... + \sqrt{m} \\)
- The computation is synchronized using **semaphores** to ensure safe shared data access.
- The partial results are written step-by-step into the file `step_by_step.txt` located in the user’s home directory.

### 4️⃣ Threaded Divisor Analysis
- The user inputs a number `k` (1300 ≤ k ≤ 130000).
- Two threads compute all **divisors** for numbers in their respective halves of the range `[1, k]`.
- Once both finish, a third thread extracts all **odd numbers** from the combined results and displays them on screen.
- The third thread also measures and prints its **execution time**.
- Thread synchronization is implemented using **Locks** and **Events** to manage execution order.

---

## 📘 Getting Started
### 🧩 Prerequisites

This project requires:

Python 3.9 or higher

A Linux-based operating system (e.g., Ubuntu, Debian, Fedora etc. on Windows, or macOS) to properly support system-level operations like os.fork, signal handling, and process priority management.

### ⚙️ Installation and Execution
1️⃣ Clone the Repository

Navigate to your desired directory and clone the project:

git clone [YOUR_REPOSITORY_LINK]
cd [YOUR_REPOSITORY_NAME]

2️⃣ Run the Main Program

Execute the main Python file from the terminal:

python3 os_work.py

3️⃣ Use the Menu

Once started, the program displays a main menu with options (1–4).
To exit, type stop or zaustavi.

### ⚠️ Important Notes for Functionalities 2 & 3

Functionality 2 automatically creates a file named stacking.txt on your Desktop (e.g., ~/Desktop/stacking.txt).
It contains the current stack trace when specific signals (e.g., SIGHUP, SIGABRT) are triggered.

Functionality 3 generates a file named step_by_step.txt inside your Home directory (e.g., ~/step_by_step.txt).
It contains incremental calculations of the sum of square roots for the selected range

---

## 🧠 Technologies Used
- **Python 3**
- **Ubuntu Linux**
- Modules: `os`, `signal`, `threading`, `math`, `time`, `traceback`, `platform`

---

## 🧾 Author
**Luka Mikulić**  
University of Rijeka — Faculty of Informatics and Digital Technologies
