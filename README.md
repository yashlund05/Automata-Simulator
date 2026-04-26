# Automata Simulator Tool — TOC Project

A complete **Theory of Computation (TOC)** project that allows users to design, simulate, and analyze **DFA/NFA automata** with step-by-step transitions.

This project includes:

* Automata definitions
* Transition tables
* Formal 5-tuple representation
* Step-by-step simulation
* Test cases (accepted & rejected)
* JFLAP construction guidance
* Interactive UI built with Streamlit

---

## 🚀 Features

* ✅ Supports multiple automata problems:

  * Strings ending with `01`
  * Strings containing `aba`
  * Binary numbers divisible by 3
  * Even number of `a`’s and `b`’s

* ✅ Step-by-step simulation:

  ```
  q0 --a--> q1
  q1 --b--> q2
  ```

* ✅ Displays:

  * Current state
  * Input symbol
  * Next state
  * Final result (Accepted / Rejected)

* ✅ Academic Requirements Covered:

  * State Diagram (via JFLAP steps)
  * Transition Table
  * Formal Definition (Q, Σ, δ, q₀, F)
  * Test Cases
  * Implementation Code

---

## 🖥️ Tech Stack

* Python 3.x
* Streamlit (UI)
* CLI-based simulation logic

---

## 📂 Project Structure

```
automata-project/
│── automata.py      # Backend logic
│── app.py           # Streamlit UI
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```
git clone https://github.com/your-username/automata-project.git
cd automata-project
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run the application

```
python -m streamlit run app.py
```

---

## 🎮 Usage

1. Select a problem from dropdown
2. View:

   * Formal definition
   * Transition table
   * JFLAP steps
3. Enter input string
4. Click **Run Simulation**
5. View step-by-step transitions and result

---

## 🧠 Viva Preparation

This project helps with:

* State explanation
* Transition justification
* DFA/NFA understanding
* NFA to DFA conversion
* Code walkthrough

---

## 📌 Example

Input:

```
101
```

Output:

```
q0 --1--> q0
q0 --0--> q1
q1 --1--> q2

Accepted ✅
```

---

## 📚 Future Improvements

* Graphical state diagram rendering
* File export (PDF report)
* More automata problems

---

## 👨‍💻 Author

* Yash Lund

---

## ⭐ If you like this project

Give it a star on GitHub!

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)