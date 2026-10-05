#!/usr/bin/env python3
"""
cvss_calculator.py
------------------
Calculate CVSS v3.1 Base Score from metric values.

Accepts metric shortcuts (e.g., --av N --ac L --pr N --ui N --s U --c H --i H --a H)
or full names (--av N --ac L --pr N --ui N --s U --c H --i H --a H).

Prints the Base Score (rounded to 1 decimal) and the severity rating.
"""

import argparse
import math

# Numeric weights for each metric value
AV_VALUES = {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.20}
AC_VALUES = {"L": 0.77, "H": 0.44}
PR_VALUES = {"N": 0.85, "L": 0.62, "H": 0.27}
UI_VALUES = {"N": 0.85, "R": 0.62}
# Scope does not have a weight; it's a flag used in formulas.
S_VALUES = {"U": 0.0, "C": 1.0}  # we will treat as boolean later
C_VALUES = {"N": 0.00, "L": 0.22, "H": 0.56}
I_VALUES = {"N": 0.00, "L": 0.22, "H": 0.56}
A_VALUES = {"N": 0.00, "L": 0.22, "H": 0.56}

def parse_args():
    parser = argparse.ArgumentParser(description="CVSS v3.1 Base Score calculator")
    parser.add_argument("--av", required=True, choices=AV_VALUES.keys(), help="Attack Vector: N, A, L, P")
    parser.add_argument("--ac", required=True, choices=AC_VALUES.keys(), help="Attack Complexity: L, H")
    parser.add_argument("--pr", required=True, choices=PR_VALUES.keys(), help="Privileges Required: N, L, H")
    parser.add_argument("--ui", required=True, choices=UI_VALUES.keys(), help="User Interaction: N, R")
    parser.add_argument("--s",  required=True, choices=S_VALUES.keys(), help="Scope: U (Unchanged), C (Changed)")
    parser.add_argument("--c",  required=True, choices=C_VALUES.keys(), help="Confidentiality: N, L, H")
    parser.add_argument("--i",  required=True, choices=I_VALUES.keys(), help="Integrity: N, L, H")
    parser.add_argument("--a",  required=True, choices=A_VALUES.keys(), help="Availability: N, L, H")
    return parser.parse_args()

def calc_base_score(args):
    # Exploitability
    EXP = 8.22 * AV_VALUES[args.av] * AC_VALUES[args.ac] * PR_VALUES[args.pr] * UI_VALUES[args.ui]
    # Impact
    IMP = 1 - ((1 - C_VALUES[args.c]) * (1 - I_VALUES[args.i]) * (1 - A_VALUES[args.a]))
    if args.s == "U":
        IMP = 6.42 * IMP
    else:  # Scope changed
        IMP = 7.52 * (IMP - 0.029) - 3.25 * math.pow((IMP - 0.02), 15)
    # Base Score
    if IMP <= 0:
        base = 0.0
    else:
        if args.s == "U":
            base = min(IMP + EXP, 10.0)
        else:
            base = min(1.08 * (IMP + EXP), 10.0)
    # Round up to 1 decimal
    base_rounded = math.ceil(base * 10) / 10
    # Determine severity
    if base_rounded == 0.0:
        severity = "None"
    elif 0.1 <= base_rounded <= 3.9:
        severity = "Low"
    elif 4.0 <= base_rounded <= 6.9:
        severity = "Medium"
    elif 7.0 <= base_rounded <= 8.9:
        severity = "High"
    else:  # 9.0 - 10.0
        severity = "Critical"
    return base_rounded, severity

def main():
    args = parse_args()
    base, severity = calc_base_score(args)
    print(f"CVSS v3.1 Base Score: {base:.1f}")
    print(f"Severity: {severity}")
    # Also output the vector string for reference
    vector = f"CVSS:3.1/AV:{args.av}/AC:{args.ac}/PR:{args.pr}/UI:{args.ui}/S:{args.s}/C:{args.c}/I:{args.i}/A:{args.a}"
    print(f"Vector String: {vector}")

if __name__ == "__main__":
    main()