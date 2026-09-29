# Problem Statement & System Architecture

## Problem Statement
Students at Vellore Institute of Technology (VIT) often struggle to keep track of their attendance margins and target marks required in the Final Assessment Test (FAT) to achieve their desired grades. 

Specifically:
1. **Attendance Margin Risk:** Computing how many classes can be safely skipped (or attended to recover from <75%) requires manual formula application.
2. **Grade Target Ambiguity:** Calculating the exact FAT score out of 100 required to attain target letter grades ($S, A, B, C, D$) based on weighted internal marks ($CAT-1$, $CAT-2$, $DA/Quizzes$) is prone to manual arithmetic errors.

## Solution
`vtop-attendance-grade-predictor` provides a modular Python engine that:
- Automatically calculates attendance thresholds and margin recovery.
- Maps current internal performance against final grade thresholds.
- Persists course-level data using structured JSON storage.

## Mathematical Formulation

### Attendance Engine
Let $A$ be attended classes and $T$ be total classes. Current percentage $P = \frac{A}{T} \times 100$.

- **Safe Bunks ($B$)** when $P \ge P_{target}$:
  $$B = \left\lfloor \frac{100 \cdot A}{P_{target}} \right\rfloor - T$$

- **Required Classes ($R$)** when $P < P_{target}$:
  $$R = \left\lceil \frac{P_{target} \cdot T - 100 \cdot A}{100 - P_{target}} \right\rceil$$

### Grade Engine
Internal score out of 60 ($I_{60}$):
$$I_{60} = \left(\frac{CAT1}{50} \times 15\right) + \left(\frac{CAT2}{50} \times 15\right) + DA_{quiz}$$

Required FAT mark out of 100 ($F_{100}$) for target cutoff $G$:
$$F_{100} = \frac{G - I_{60}}{0.40}$$