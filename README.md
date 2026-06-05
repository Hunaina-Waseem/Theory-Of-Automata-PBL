# 🌸 Escape the Magical Palace (DFA Simulator) 🌸

Welcome to the **Escape the Magical Palace** repository! This is an interactive, graphical text-adventure game built using Python and Tkinter. The entire game loop and movement mechanics are strictly driven by a mathematical **Deterministic Finite Automaton (DFA)**.

This project was developed as part of a Project-Based Learning (PBL) assignment for the **Theory of Automata and Formal Languages** course.

---

## 🔮 Project Overview
Instead of traditional game logic, player movements (`NORTH`, `SOUTH`, `EAST`, `WEST`) are processed as input string tokens by a state machine. The game tracks your current location as an internal state and maintains a live, scrollable **History Log** of all transitions. 
* Reaching the final state successfully triggers an **INPUT ACCEPTED** notification.
* Entering an incorrect sequence or hitting a wall drops the player into a dead **TRAP STATE**, triggering an **INPUT REJECTED** notification.

---

## 🧮 The Mathematical Model
The underlying automaton is formally defined as a 5-tuple: 

$$M = (Q, \Sigma, \delta, q_0, F)$$

### 1. States ($Q$)
* `q0`: The Dressing Room (Initial State)
* `q1`: The Grand Ballroom
* `q2`: The Royal Courtyard
* `q_win`: Freedom! (Accept State)
* `q_lose`: Caught by Guards (Trap / Dead State)

### 2. Alphabet ($\Sigma$)
* `{"north", "south", "east", "west"}`

### 3. Transition Function ($\delta$)
| Current State | Input Token | Next State | Path Type |
| :--- | :--- | :--- | :--- |
| **q0** | `north` | **q1** | Valid Path |
| **q0** | `south`, `east`, `west` | **q_lose** | Trap State |
| **q1** | `east` | **q2** | Valid Path |
| **q1** | `south` | **q0** | Closure Loop |
| **q1** | `north`, `west` | **q_lose** | Trap State |
| **q2** | `north` | **q_win** | **Accept State** |
| **q2** | `south`, `east`, `west` | **q_lose** | Trap State |

---

## 🎯 Complexity Features
The machine handles a non-trivial **Kleene Star loop closure** between states `q0` and `q1`. A player can move back and forth infinitely (`north` $\rightarrow$ `south` $\rightarrow$ `north`) before deciding to progress to the exit, proving the system effectively handles language iteration and recursion.

The regular expression for a minimal winning sequence is: 
$$\text{north} \cdot (\text{south} \cdot \text{north})^* \cdot \text{east} \cdot \text{north}$$

---

## 🚀 How to Run the App

1. Make sure you have **Python 3.x** installed.
2. Clone this repository or download the `game.py` file.
3. Open your terminal/command prompt in the file directory and run:
   ```bash
   python game.py
