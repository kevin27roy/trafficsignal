# Smart Traffic Light Control using Reinforcement Learning

## Problem Statement
Traditional traffic lights use fixed timing and cannot adapt to changing traffic conditions. This project uses Reinforcement Learning to dynamically optimize traffic signals and reduce congestion.

---

## SDG Mapping
This project supports SDG 11 – Sustainable Cities and Communities by reducing traffic congestion, waiting time, fuel wastage, and urban pollution.

---

## Features
- Traffic signal simulator
- Q-Learning agent
- Adaptive traffic control
- Fixed timer baseline comparison
- Reward tracking
- Queue monitoring
- Experiment logging
- Policy saving

---

## Technologies Used
- Python
- NumPy
- Pandas
- Matplotlib
- Git/GitHub

---

## RL Methodology

### State
Queue lengths in all four directions + current traffic phase.

### Action
- 0 → North-South Green
- 1 → East-West Green

### Reward
Negative of total queue length / waiting time.

### Exploration Strategy
Epsilon-greedy exploration.

---

## Project Structure

```text
sim/
agents/
experiments/
plots/
policies/
```

---

## How to Run

```bash
pip install -r requirements.txt

python train.py

python baseline.py

python evaluate.py
```

---

## Results

The RL-based controller achieved lower average waiting time than the traditional fixed-timer system.

| Metric | Fixed Timer | RL Policy |
|---|---|---|
| Avg Waiting Time | 26.39 s | 18.7 s |

---

## Monitoring Plan

If deployed in real-world traffic systems, the model would monitor:
- average waiting time
- queue lengths
- throughput
- safety constraints

---

## Future Improvements

- Deep Q Networks (DQN)
- Multi-intersection control
- Emergency vehicle prioritization
- Real-time visualization

---

## Authors

Kevin Roy
Lakshmish R K
Monish P G
Monish Reddy B
