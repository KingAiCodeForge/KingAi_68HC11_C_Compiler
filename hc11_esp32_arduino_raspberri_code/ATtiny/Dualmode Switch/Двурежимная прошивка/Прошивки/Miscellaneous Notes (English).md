# Miscellaneous Notes

> **Translated from Russian**  
> **Original Document:** Разное.txt  
> Technical notes from the original Russian archive.

## CO Adjustment in M60B30 Firmwares
**Address:** 0xFE8C

## CO Trim Values Location
Look starting from address **0x7E88** through **0x7EB8** for the last filled cell (value not equal to 0xFF).

### Value Interpretation:
- **0x80** = 0 (neutral/stock)
- Range: **0x00 to 0xFE** corresponds to **-127 to +127** on DIS diagnostic tool

### Example:
| Hex Value | DIS Reading |
|-----------|-------------|
| 0x00 | -127 (lean) |
| 0x80 | 0 (stock) |
| 0xFE | +127 (rich) |
