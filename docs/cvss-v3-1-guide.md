# CVSS v3.1 – Quick Guide for Scoring Vulnerabilities

CVSS (Common Vulnerability Scoring System) v3.1 provides a standardized way to convey the severity of software vulnerabilities. The **Base Score** ranges from 0.0 to 10.0, where higher values indicate greater severity.

## 1. Metric Groups
The Base Score is derived from three groups of metrics:

| Group | Metrics (choose one value each) |
|-------|---------------------------------|
| **Exploitability** | Attack Vector (AV), Attack Complexity (AC), Privileges Required (PR), User Interaction (UI) |
| **Impact** | Confidentiality (C), Integrity (I), Availability (A) |
| **Scope** | Scope (S) – changed vs. unchanged |

## 2. Metric Values & Numeric Weights

| Metric | Abbrev | Values | Weight (used in formula) |
|--------|--------|--------|--------------------------|
| Attack Vector | AV | N (Network) = 0.85<br>A (Adjacent) = 0.62<br>L (Local) = 0.55<br>P (Physical) = 0.20 | — |
| Attack Complexity | AC | L (Low) = 0.77<br>H (High) = 0.44 | — |
| Privileges Required | PR | N (None) = 0.85<br>L (Low) = 0.62<br>H (High) = 0.27 | *Note: PR weight depends on Scope* |
| User Interaction | UI | N (None) = 0.85<br>R (Required) = 0.62 | — |
| Scope | S | U (Unchanged) = 1.00<br>C (Changed) = 1.08 | — |
| Confidentiality | C | H (High) = 0.56<br>L (Low) = 0.22<br>N (None) = 0.00 | — |
| Integrity | I | H (High) = 0.56<br>L (Low) = 0.22<br>N (None) = 0.00 | — |
| Availability | A | H (High) = 0.56<br>L (Low) = 0.22<br>N (None) = 0.00 | — |

## 3. Formulas (Simplified)

**Exploitability Sub‑score**  
`EXP = 8.22 * AV * AC * PR * UI`

**Impact Sub‑score**  
`IMP = 1 - [(1 - C) * (1 - I) * (1 - A)]`  
If Scope = U: `IMP = 6.42 * IMP`  
If Scope = C: `IMP = 7.52 * (IMP - 0.029) - 3.25 * (IMP - 0.02)^15`

**Base Score**  
If IMP ≤ 0: `BaseScore = 0`  
Else if Scope = U:  
`BaseScore = roundup(min(IMP+EXP, 10))`  
Else (Scope = C):  
`BaseScore = roundup(min(1.08*(IMP+EXP), 10))`

*Roundup* rounds up to the nearest 0.1.

## 4. Severity Ratings
| Base Score Range | Severity |
|------------------|----------|
| 0.0              | None |
| 0.1 – 3.9        | Low |
| 4.0 – 6.9        | Medium |
| 7.0 – 8.9        | High |
| 9.0 – 10.0       | Critical |

## 5. Example Calculations

### Example 1 – Remote Code Execution (RCE) with no auth
- AV = N (0.85)
- AC = L (0.77)
- PR = N (0.85)
- UI = N (0.85)
- S = U
- C = H (0.56)
- I = H (0.56)
- A = H (0.56)

```
EXP = 8.22 * 0.85 * 0.77 * 0.85 * 0.85 ≈ 3.23
IMP = 1 - (1-0.56)^3 = 1 - 0.44^3 = 1 - 0.085 = 0.915
IMP = 6.42 * 0.915 ≈ 5.88
BaseScore = min(5.88+3.23,10) = 9.1 → roundup → 9.1 (Critical)
```

### Example 2 – Stored XSS requiring user interaction
- AV = N (0.85)
- AC = L (0.77)
- PR = L (0.62)   # low privilege needed to post comment
- UI = R (0.62)   # victim must view the page
- S = U
- C = L (0.22)   # could steal data
- I = L (0.22)   # could alter page
- A = N (0.00)

```
EXP = 8.22 * 0.85 * 0.77 * 0.62 * 0.62 ≈ 1.73
IMP = 1 - (1-0.22)*(1-0.22)*(1-0) = 1 - 0.78*0.78 = 1 - 0.6084 = 0.3916
IMP = 6.42 * 0.3916 ≈ 2.51
BaseScore = min(2.51+1.73,10) = 4.24 → roundup → 4.3 (Medium)
```

## 6. Using the Helper Script
The repository includes `scripts/cvss_calculator.py` which accepts metric shortcuts:

```
python scripts/cvss_calculator.py --av N --ac L --pr N --ui N --s U --c H --i H --a H
```

You can also use the full names:
```
python scripts/cvss_calculator.py --av N --ac L --pr N --ui N --s U --c H --i H --a H
```

The script prints the Base Score and severity.

## 7. References
- FIRST.Org CVSS v3.1 Specification: https://www.first.org/cvss/specification-document
- CVSS v3.1 Calculator (online): https://www.first.org/cvss/calculator/3.1
- NIST CVSS Documentation: https://nvd.nist.gov/vuln-metrics/cvss
