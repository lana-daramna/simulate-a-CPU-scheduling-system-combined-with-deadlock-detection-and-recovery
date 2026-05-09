# CPU Scheduling + Deadlock Detection Simulator

## Overview

This project simulates a complete CPU scheduling system combined with:

* **Priority Scheduling**
* **Round Robin Scheduling**
* **I/O Waiting**
* **Resource Allocation**
* **Deadlock Detection and Recovery**
* **Gantt Chart Visualization**

The simulator models how an operating system manages processes, CPU bursts, I/O operations, and shared resources.

It also detects deadlocks using a **Resource Allocation Graph** and resolves them by terminating one of the involved processes.

---

# Features

## 1. Priority Scheduling

Processes are scheduled based on their priority value.

* Lower priority number = higher priority
* Ready queue is always sorted by:

  1. Priority
  2. Arrival time

---

## 2. Round Robin Scheduling

If multiple processes have the same priority:

* The scheduler switches to **Round Robin**
* Uses a configurable **time quantum**
* Prevents starvation
* Ensures fairness among equal-priority processes

Default Time Quantum:

```python
time_quantum = 5
```

---

## 3. I/O Burst Handling

Processes may contain:

* CPU bursts
* I/O bursts

When a process requests I/O:

* It moves to the waiting queue
* Returns to ready queue after I/O completion

---

## 4. Resource Allocation

The system supports up to:

```python
20 resources
```

Resources are represented as:

```text
R[1], R[2], ..., R[20]
```

Processes can:

* Request resources → `R[x]`
* Release resources → `F[x]`

---

## 5. Deadlock Detection

The simulator detects deadlocks using:

* Resource Allocation Graph
* Cycle Detection Algorithm

If a deadlock is detected:

* The process causing the deadlock is terminated
* All its resources are released

---

## 6. Gantt Chart Visualization

At the end of execution:

* A Gantt chart is generated using Matplotlib
* Displays CPU execution timeline for all processes

---

# Project Structure

```text
project/
│
├── main.py
├── input.txt
├── README.md
│
├── test_cases/
│   ├── priority.txt
│   ├── round_robin.txt
│   ├── io.txt
│   ├── resource_deadlock.txt
│   ├── full.txt
│   └── mixed.txt
```

---

# Process Input Format

Each line in the input file represents one process.

Format:

```text
PID ARRIVAL_TIME PRIORITY BURSTS
```

Example:

```text
1 0 1 CPU {5,R[1],3,F[1]} IO {4} CPU {6}
```

---

# Burst Syntax

## CPU Burst

```text
CPU {execution_time}
```

Example:

```text
CPU {5}
```

---

## CPU Burst with Resource Request

```text
CPU {R[1],5,F[1]}
```

Meaning:

1. Request resource R[1]
2. Execute for 5 units
3. Release R[1]

---

## I/O Burst

```text
IO {4}
```

Meaning:

* Process waits for 4 time units

---

# Scheduling Logic

## Ready Queue

Contains processes ready for execution.

Sorted by:

1. Priority
2. Arrival Time

---

## Waiting Queue

Contains processes waiting for:

* I/O completion
* Resource availability

---

# Deadlock Example

Suppose:

* Process P1 holds R1 and requests R2
* Process P2 holds R2 and requests R1

A cycle occurs:

```text
P1 → R2 → P2 → R1 → P1
```

The simulator detects this cycle and terminates one process.

---

# Test Cases Included

The project includes 6 test cases:

## 1. Priority Scheduling

Tests:

* Priority-based execution
* Queue ordering

File:

```text
priority.txt
```

---

## 2. Round Robin

Tests:

* Equal priority processes
* Time quantum switching

File:

```text
round_robin.txt
```

---

## 3. I/O Scheduling

Tests:

* I/O waiting
* Returning to ready queue

File:

```text
io.txt
```

---

## 4. Resource Allocation

Tests:

* Resource requests/releases

File:

```text
resource_deadlock.txt
```

---

## 5. Deadlock Detection

Tests:

* Circular wait
* Deadlock recovery

File:

```text
resource_deadlock.txt
```

---

## 6. Full System Test

Tests all features together:

* Priority
* Round Robin
* I/O
* Resources
* Deadlock handling

File:

```text
full.txt
```

---

# How to Run

## Requirements

Install Python packages:

```bash
pip install matplotlib
```

---

## Run Program

```bash
python main.py
```

---

# Output

The simulator prints:

* Process execution details
* Resource allocation/release
* Waiting queue updates
* Deadlock detection messages
* Average waiting time
* Average turnaround time

Example:

```text
Resource R[1] allocated to Process 1.
Process 2 added to waiting queue for Resource R[1].
Deadlock detected with Process 3 requesting Resource R[2].
```

---

# Performance Metrics

## Waiting Time

```text
Total time spent in ready queue
```

---

## Turnaround Time

```text
Completion Time - Arrival Time
```

---

# Main Classes

## Process

Represents a process in the system.

Stores:

* PID
* Priority
* Bursts
* Waiting time
* Resources
* Execution state

---

## ResourceManager

Handles:

* Resource allocation
* Resource release
* Deadlock detection

---

# Algorithms Used

## Scheduling Algorithms

* Priority Scheduling
* Round Robin

## Deadlock Handling

* Resource Allocation Graph
* Cycle Detection (DFS)

---

# Visualization

The simulator automatically generates a Gantt chart using:

```python
matplotlib
```

This helps visualize:

* CPU utilization
* Process switching
* Scheduling behavior

---

# Notes

* Lower priority number means higher priority.
* Only one instance exists for each resource.
* The scheduler supports preemption using Round Robin.
* Deadlocks are resolved by process termination.
