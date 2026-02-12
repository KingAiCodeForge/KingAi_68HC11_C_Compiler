"""
Peephole Optimizer for the KingAI 68HC11 C Compiler.

Performs pattern-matching replacements on assembly text lines
to eliminate common redundancies in the generated code.

Rules are applied iteratively until no more matches are found.
Each rule is a (pattern, replacement) where pattern is a list
of lambda predicates on stripped instruction text, and replacement
is a function that returns new lines (or empty list to delete).
"""

from __future__ import annotations
import re
from typing import List, Optional, Tuple, Callable


def _strip(line: str) -> str:
    """Strip whitespace from an instruction line."""
    return line.strip()


def _is_instr(line: str, mnemonic: str) -> bool:
    """Check if a line is a specific instruction (case-insensitive)."""
    s = _strip(line)
    return s.upper().startswith(mnemonic.upper())


def _get_operand(line: str) -> str:
    """Extract the operand from an instruction line ('LDAA #$05' → '#$05')."""
    s = _strip(line)
    # Remove trailing comments
    if ";" in s:
        s = s[:s.index(";")].strip()
    parts = s.split(None, 1)
    return parts[1] if len(parts) > 1 else ""


def _is_label(line: str) -> bool:
    """Check if a line is a label (not indented, ends with ':')."""
    return not line.startswith(" ") and not line.startswith("\t") and ":" in line


def optimize(lines: List[str], max_passes: int = 10) -> List[str]:
    """Apply peephole optimization rules iteratively.

    Returns a new list of assembly lines with redundancies removed.
    """
    changed = True
    pass_count = 0
    result = list(lines)

    while changed and pass_count < max_passes:
        changed = False
        pass_count += 1
        new_lines = []
        i = 0
        while i < len(result):
            matched = False

            # ── Rule 1: Remove redundant TSX pairs ──
            # TSX immediately followed by TSX → keep only one
            if (i + 1 < len(result)
                    and _is_instr(result[i], "TSX")
                    and _is_instr(result[i + 1], "TSX")):
                new_lines.append(result[i])
                i += 2
                changed = True
                matched = True

            # ── Rule 2: Remove PSHA immediately followed by PULA ──
            # (with nothing between them — the push/pop is a no-op)
            if not matched and (i + 1 < len(result)
                    and _is_instr(result[i], "PSHA")
                    and _is_instr(result[i + 1], "PULA")):
                i += 2
                changed = True
                matched = True

            # ── Rule 3: Remove PSHB+PSHA immediately followed by PULA+PULB ──
            # (16-bit push/pop no-op)
            if not matched and (i + 3 < len(result)
                    and _is_instr(result[i], "PSHB")
                    and _is_instr(result[i + 1], "PSHA")
                    and _is_instr(result[i + 2], "PULA")
                    and _is_instr(result[i + 3], "PULB")):
                i += 4
                changed = True
                matched = True

            # ── Rule 4: LDAA #imm followed by TSTA → remove TSTA ──
            # LDAA already sets condition codes (N, Z flags)
            if not matched and (i + 1 < len(result)
                    and _is_instr(result[i], "LDAA")
                    and _is_instr(result[i + 1], "TSTA")):
                new_lines.append(result[i])
                i += 2
                changed = True
                matched = True

            # ── Rule 5: LDD #imm followed by SUBD #$0000 → remove SUBD ──
            # LDD already sets Z flag, no need to test D
            if not matched and (i + 1 < len(result)
                    and _is_instr(result[i], "LDD")
                    and _strip(result[i + 1]).startswith("SUBD")
                    and "#$0000" in result[i + 1]):
                new_lines.append(result[i])
                i += 2
                changed = True
                matched = True

            # ── Rule 6: LDAA addr; STAA addr (same addr) → keep only LDAA ──
            # The store is redundant if storing to same place we just loaded
            if not matched and (i + 1 < len(result)
                    and _is_instr(result[i], "LDAA")
                    and _is_instr(result[i + 1], "STAA")):
                op_load = _get_operand(result[i])
                op_store = _get_operand(result[i + 1])
                if op_load and op_load == op_store and not op_load.startswith("#"):
                    new_lines.append(result[i])
                    i += 2
                    changed = True
                    matched = True

            # ── Rule 7: LDD addr; STD addr (same addr) → keep only LDD ──
            if not matched and (i + 1 < len(result)
                    and _is_instr(result[i], "LDD")
                    and _is_instr(result[i + 1], "STD")):
                op_load = _get_operand(result[i])
                op_store = _get_operand(result[i + 1])
                if op_load and op_load == op_store and not op_load.startswith("#"):
                    new_lines.append(result[i])
                    i += 2
                    changed = True
                    matched = True

            # ── Rule 8: TAB followed by TBA → remove both (A unchanged) ──
            if not matched and (i + 1 < len(result)
                    and _is_instr(result[i], "TAB")
                    and _is_instr(result[i + 1], "TBA")):
                i += 2
                changed = True
                matched = True

            # ── Rule 9: TBA followed by TAB → remove both (B unchanged) ──
            if not matched and (i + 1 < len(result)
                    and _is_instr(result[i], "TBA")
                    and _is_instr(result[i + 1], "TAB")):
                i += 2
                changed = True
                matched = True

            # ── Rule 10: CLRA followed by CLRA → remove duplicate ──
            if not matched and (i + 1 < len(result)
                    and _is_instr(result[i], "CLRA")
                    and _is_instr(result[i + 1], "CLRA")):
                new_lines.append(result[i])
                i += 2
                changed = True
                matched = True

            # ── Rule 11: CLRB followed by CLRB → remove duplicate ──
            if not matched and (i + 1 < len(result)
                    and _is_instr(result[i], "CLRB")
                    and _is_instr(result[i + 1], "CLRB")):
                new_lines.append(result[i])
                i += 2
                changed = True
                matched = True

            # ── Rule 12: while(1) pattern — nonzero constant before BEQ ──
            # LDAA #$01; TSTA; BEQ lbl → remove all three (always true)
            if not matched and (i + 2 < len(result)
                    and _is_instr(result[i], "LDAA")
                    and "#$01" in result[i]
                    and _is_instr(result[i + 1], "TSTA")
                    and _is_instr(result[i + 2], "BEQ")):
                i += 3
                changed = True
                matched = True

            # ── Rule 12b: Same but after Rule 4 already removed TSTA ──
            # LDAA #$01; BEQ lbl → remove both (BEQ never fires on nonzero)
            if not matched and (i + 1 < len(result)
                    and _is_instr(result[i], "LDAA")
                    and "#$01" in result[i]
                    and _is_instr(result[i + 1], "BEQ")):
                i += 2
                changed = True
                matched = True

            # ── Rule 13: INS repeated N times → aggregate comment ──
            # (Keep the INS instructions but this rule is a placeholder for
            #  future LEAS optimization if targeting HC12)

            if not matched:
                new_lines.append(result[i])
                i += 1

        result = new_lines

    return result
