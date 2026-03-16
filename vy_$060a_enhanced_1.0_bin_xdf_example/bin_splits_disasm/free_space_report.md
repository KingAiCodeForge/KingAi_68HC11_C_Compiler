# VY V6 $060A Enhanced — Free Space Analysis Report
**Generated:** 2026-02-16 21:30  
**Free byte:** `0x00`  
**Minimum region size:** 32 bytes  
**Source files:**
- Bank 1 (Base): `Enhanced_v1.0a_bank1.bin` (65,536 bytes)
- Bank 2 (Engine overlay): `Enhanced_v1.0a_bank2.bin` (32,768 bytes)
- Bank 3 (Trans/diag overlay): `Enhanced_v1.0a_bank3.bin` (32,768 bytes)

---

## Memory Map Reference

```
128KB Flash (M29W800DB / Am29F010), 68HC11 expanded mode:

Full binary:  0x00000-0x1FFFF  (131,072 bytes)

Bank 1 (64KB): File 0x00000-0x0FFFF  ->  CPU $0000-$FFFF
  $0000-$03FF  RAM (1,024 bytes — HC11F has 1KB)
  $1000-$105F  I/O registers (96 bytes — HC11F extended)
  $2000-$3FFF  Pseudo-vector jump table + subroutines
  $4000-$7FFF  Calibration tables (spark, fuel, trans, etc.)
  $8000-$C467  Executable code (main loop, ISRs, subroutines)
  $C468-$FFBF  FREE SPACE (THE1 zero-filled padding)
  $FFC0-$FFFF  Interrupt vector table (21 vectors)

Bank 2 (32KB): File 0x10000-0x17FFF  ->  CPU $8000-$FFFF  (engine overlay)
Bank 3 (32KB): File 0x18000-0x1FFFF  ->  CPU $8000-$FFFF  (trans/diag overlay)

Banks 2 and 3 share the same CPU address range ($8000-$FFFF).
PORTG ($1002) bit selects which bank is active — only one is visible at a time.
Free space in bank 2 does NOT mean the same address is free in bank 3.
```

---

## Bank 1 (Base)

> Full 64KB — RAM ($0000-$03FF), I/O regs ($1000-$105F), calibration ($4000-$7FFF), code ($8000-$FFBF), vectors ($FFC0-$FFFF)

**File size:** 65,536 bytes  
**Total free space:** 17,998 bytes (27.5%)  
**Free regions found:** 26

| # | File Offset | CPU Address | Size | Region |
|---|-------------|-------------|------|--------|
| 1 | `0x02030`-`0x0207F` | `$2030`-`$207F` | 80 B | Pseudo-vector jump table + code [caution] |
| 2 | `0x02A21`-`0x02A40` | `$2A21`-`$2A40` | 32 B | Pseudo-vector jump table + code [caution] |
| 3 | `0x03E87`-`0x03FE1` | `$3E87`-`$3FE1` | 347 B | Pseudo-vector jump table + code [caution] |
| 4 | `0x0435B`-`0x0438D` | `$435B`-`$438D` | 51 B | Calibration tables [caution] |
| 5 | `0x04632`-`0x04655` | `$4632`-`$4655` | 36 B | Calibration tables [caution] |
| 6 | `0x04850`-`0x04871` | `$4850`-`$4871` | 34 B | Calibration tables [caution] |
| 7 | `0x04BCD`-`0x04BF5` | `$4BCD`-`$4BF5` | 41 B | Calibration tables [caution] |
| 8 | `0x04C00`-`0x04C23` | `$4C00`-`$4C23` | 36 B | Calibration tables [caution] |
| 9 | `0x05117`-`0x05248` | `$5117`-`$5248` | 306 B | Calibration tables [caution] |
| 10 | `0x05BF8`-`0x05C2C` | `$5BF8`-`$5C2C` | 53 B | Calibration tables [caution] |
| 11 | `0x05C31`-`0x05CB8` | `$5C31`-`$5CB8` | 136 B | Calibration tables [caution] |
| 12 | `0x05CBA`-`0x05CDF` | `$5CBA`-`$5CDF` | 38 B | Calibration tables [caution] |
| 13 | `0x05CE1`-`0x05D01` | `$5CE1`-`$5D01` | 33 B | Calibration tables [caution] |
| 14 | `0x05D05`-`0x05EFC` | `$5D05`-`$5EFC` | 504 B | Calibration tables [caution] |
| 15 | `0x05F27`-`0x05F89` | `$5F27`-`$5F89` | 99 B | Calibration tables [caution] |
| 16 | `0x06394`-`0x063BE` | `$6394`-`$63BE` | 43 B | Calibration tables [caution] |
| 17 | `0x06559`-`0x066D7` | `$6559`-`$66D7` | 383 B | Calibration tables [caution] |
| 18 | `0x06852`-`0x06876` | `$6852`-`$6876` | 37 B | Calibration tables [caution] |
| 19 | `0x06AA3`-`0x06ACA` | `$6AA3`-`$6ACA` | 40 B | Calibration tables [caution] |
| 20 | `0x06F41`-`0x06F7B` | `$6F41`-`$6F7B` | 59 B | Calibration tables [caution] |
| 21 | `0x07151`-`0x07232` | `$7151`-`$7232` | 226 B | Calibration tables [caution] |
| 22 | `0x07677`-`0x07697` | `$7677`-`$7697` | 33 B | Calibration tables [caution] |
| 23 | `0x07A64`-`0x07A85` | `$7A64`-`$7A85` | 34 B | Calibration tables [caution] |
| 24 | `0x07E54`-`0x07EA9` | `$7E54`-`$7EA9` | 86 B | Calibration tables [caution] |
| 25 | `0x07FCF`-`0x07FF5` | `$7FCF`-`$7FF5` | 39 B | Calibration tables [caution] |
| 26 | `0x0C468`-`0x0FFBF` | `$C468`-`$FFBF` | 15,192 B | Verified free space (THE1 zero-filled padding) [free_verified] |

---

## Bank 2 (Engine overlay)

> 32KB engine code overlay — mapped to CPU $8000-$FFFF when PORTG selects bank 2

**File size:** 32,768 bytes  
**Total free space:** 313 bytes (1.0%)  
**Free regions found:** 1

| # | File Offset | CPU Address | Size | Region |
|---|-------------|-------------|------|--------|
| 1 | `0x17E87`-`0x17FBF` | `$FE87`-`$FFBF` | 313 B | Upper overlay code/free region [Bank 2 (Engine overlay)] |

---

## Bank 3 (Trans/diag overlay)

> 32KB trans/diagnostic overlay — mapped to CPU $8000-$FFFF when PORTG selects bank 3

**File size:** 32,768 bytes  
**Total free space:** 22,472 bytes (68.6%)  
**Free regions found:** 3

| # | File Offset | CPU Address | Size | Region |
|---|-------------|-------------|------|--------|
| 1 | `0x19B0B`-`0x1BFFF` | `$9B0B`-`$BFFF` | 9,461 B | Overlay code region [Bank 3 (Trans/diag overlay)] |
| 2 | `0x1CA57`-`0x1CBB6` | `$CA57`-`$CBB6` | 352 B | Overlay code region [Bank 3 (Trans/diag overlay)] |
| 3 | `0x1CE3F`-`0x1FFB1` | `$CE3F`-`$FFB1` | 12,659 B | Overlay code region [Bank 3 (Trans/diag overlay)] |

---

## Bank 2 vs Bank 3 — Crossover Analysis

Banks 2 and 3 both map to CPU `$8000`-`$FFFF`. This section compares
them byte-by-byte to show where space is truly free in both overlays
vs occupied in one or both.

### Summary

| State | Bytes | % of 32KB | Meaning |
|-------|-------|-----------|---------|
| Both free | 722 | 2.2% | Address unused in **both** overlays — safest for injection |
| Both used | 8,968 | 27.4% | Address has code/data in **both** overlays — DO NOT touch |
| Bank 2 free, Bank 3 used | 207 | 0.6% | Free only when engine overlay is active |
| Bank 2 used, Bank 3 free | 22,871 | 69.8% | Free only when trans/diag overlay is active |

### Detail (regions >= minimum size)

| CPU Address | Size | Bank 2 | Bank 3 | Verdict | bank 
|-------------|------|--------|--------|---------|
| `$8033`-`$8076` | 68 B | USED | USED | OCCUPIED — do not modify |
| `$8084`-`$80A3` | 32 B | USED | USED | OCCUPIED — do not modify |
| `$80A6`-`$80CF` | 42 B | USED | USED | OCCUPIED — do not modify |
| `$816F`-`$81C0` | 82 B | USED | USED | OCCUPIED — do not modify |
| `$822B`-`$826E` | 68 B | USED | USED | OCCUPIED — do not modify |
| `$82E5`-`$8347` | 99 B | USED | USED | OCCUPIED — do not modify |
| `$83EE`-`$846C` | 127 B | USED | USED | OCCUPIED — do not modify |
| `$847D`-`$84B0` | 52 B | USED | USED | OCCUPIED — do not modify |
| `$84BA`-`$8503` | 74 B | USED | USED | OCCUPIED — do not modify |
| `$8569`-`$8592` | 42 B | USED | USED | OCCUPIED — do not modify |
| `$85A2`-`$85CD` | 44 B | USED | USED | OCCUPIED — do not modify |
| `$85CF`-`$8609` | 59 B | USED | USED | OCCUPIED — do not modify |
| `$8631`-`$8676` | 70 B | USED | USED | OCCUPIED — do not modify |
| `$872A`-`$8770` | 71 B | USED | USED | OCCUPIED — do not modify |
| `$877E`-`$87E2` | 101 B | USED | USED | OCCUPIED — do not modify |
| `$87ED`-`$8830` | 68 B | USED | USED | OCCUPIED — do not modify |
| `$8832`-`$8854` | 35 B | USED | USED | OCCUPIED — do not modify |
| `$886A`-`$88B6` | 77 B | USED | USED | OCCUPIED — do not modify |
| `$8911`-`$8935` | 37 B | USED | USED | OCCUPIED — do not modify |
| `$8957`-`$8985` | 47 B | USED | USED | OCCUPIED — do not modify |
| `$89F5`-`$8A15` | 33 B | USED | USED | OCCUPIED — do not modify |
| `$8A22`-`$8A76` | 85 B | USED | USED | OCCUPIED — do not modify |
| `$8AD1`-`$8B05` | 53 B | USED | USED | OCCUPIED — do not modify |
| `$8B07`-`$8B98` | 146 B | USED | USED | OCCUPIED — do not modify |
| `$8BB9`-`$8BE1` | 41 B | USED | USED | OCCUPIED — do not modify |
| `$8EC8`-`$8EF1` | 42 B | USED | USED | OCCUPIED — do not modify |
| `$8EF3`-`$8F40` | 78 B | USED | USED | OCCUPIED — do not modify |
| `$8F98`-`$8FCA` | 51 B | USED | USED | OCCUPIED — do not modify |
| `$8FD9`-`$9042` | 106 B | USED | USED | OCCUPIED — do not modify |
| `$9227`-`$926B` | 69 B | USED | USED | OCCUPIED — do not modify |
| `$9275`-`$9295` | 33 B | USED | USED | OCCUPIED — do not modify |
| `$9297`-`$92BD` | 39 B | USED | USED | OCCUPIED — do not modify |
| `$92BF`-`$92E0` | 34 B | USED | USED | OCCUPIED — do not modify |
| `$92E8`-`$9315` | 46 B | USED | USED | OCCUPIED — do not modify |
| `$9365`-`$938D` | 41 B | USED | USED | OCCUPIED — do not modify |
| `$93E5`-`$9437` | 83 B | USED | USED | OCCUPIED — do not modify |
| `$944A`-`$947F` | 54 B | USED | USED | OCCUPIED — do not modify |
| `$9481`-`$94A1` | 33 B | USED | USED | OCCUPIED — do not modify |
| `$94A3`-`$94C7` | 37 B | USED | USED | OCCUPIED — do not modify |
| `$94FC`-`$951E` | 35 B | USED | USED | OCCUPIED — do not modify |
| `$9592`-`$95B6` | 37 B | USED | USED | OCCUPIED — do not modify |
| `$95DE`-`$9611` | 52 B | USED | USED | OCCUPIED — do not modify |
| `$9614`-`$963B` | 40 B | USED | USED | OCCUPIED — do not modify |
| `$96A0`-`$96C5` | 38 B | USED | USED | OCCUPIED — do not modify |
| `$96C7`-`$975A` | 148 B | USED | USED | OCCUPIED — do not modify |
| `$9778`-`$979F` | 40 B | USED | USED | OCCUPIED — do not modify |
| `$97A1`-`$97CE` | 46 B | USED | USED | OCCUPIED — do not modify |
| `$97F8`-`$9824` | 45 B | USED | USED | OCCUPIED — do not modify |
| `$98E7`-`$9916` | 48 B | USED | USED | OCCUPIED — do not modify |
| `$993B`-`$9967` | 45 B | USED | USED | OCCUPIED — do not modify |
| `$99D5`-`$99F6` | 34 B | USED | USED | OCCUPIED — do not modify |
| `$99F8`-`$9A32` | 59 B | USED | USED | OCCUPIED — do not modify |
| `$9A3C`-`$9A5D` | 34 B | USED | USED | OCCUPIED — do not modify |
| `$9ACB`-`$9AED` | 35 B | USED | USED | OCCUPIED — do not modify |
| `$9B38`-`$9B7E` | 71 B | USED | FREE | Free only in trans/diag overlay |
| `$9BA2`-`$9C21` | 128 B | USED | FREE | Free only in trans/diag overlay |
| `$9C23`-`$9C43` | 33 B | USED | FREE | Free only in trans/diag overlay |
| `$9C79`-`$9E01` | 393 B | USED | FREE | Free only in trans/diag overlay |
| `$9E17`-`$9E9F` | 137 B | USED | FREE | Free only in trans/diag overlay |
| `$9EA1`-`$9FDF` | 319 B | USED | FREE | Free only in trans/diag overlay |
| `$9FE1`-`$A0B1` | 209 B | USED | FREE | Free only in trans/diag overlay |
| `$A0B4`-`$A0D3` | 32 B | USED | FREE | Free only in trans/diag overlay |
| `$A0D5`-`$A0FC` | 40 B | USED | FREE | Free only in trans/diag overlay |
| `$A0FF`-`$A13B` | 61 B | USED | FREE | Free only in trans/diag overlay |
| `$A173`-`$A243` | 209 B | USED | FREE | Free only in trans/diag overlay |
| `$A24B`-`$A305` | 187 B | USED | FREE | Free only in trans/diag overlay |
| `$A308`-`$A345` | 62 B | USED | FREE | Free only in trans/diag overlay |
| `$A348`-`$A40D` | 198 B | USED | FREE | Free only in trans/diag overlay |
| `$A41F`-`$A450` | 50 B | USED | FREE | Free only in trans/diag overlay |
| `$A452`-`$A4A5` | 84 B | USED | FREE | Free only in trans/diag overlay |
| `$A4A8`-`$A4D0` | 41 B | USED | FREE | Free only in trans/diag overlay |
| `$A4FD`-`$A5BC` | 192 B | USED | FREE | Free only in trans/diag overlay |
| `$A5E1`-`$A67C` | 156 B | USED | FREE | Free only in trans/diag overlay |
| `$A67E`-`$A6BA` | 61 B | USED | FREE | Free only in trans/diag overlay |
| `$A6BC`-`$A71A` | 95 B | USED | FREE | Free only in trans/diag overlay |
| `$A721`-`$A7E9` | 201 B | USED | FREE | Free only in trans/diag overlay |
| `$A82B`-`$A84E` | 36 B | USED | FREE | Free only in trans/diag overlay |
| `$A869`-`$A893` | 43 B | USED | FREE | Free only in trans/diag overlay |
| `$A895`-`$A928` | 148 B | USED | FREE | Free only in trans/diag overlay |
| `$A92F`-`$A968` | 58 B | USED | FREE | Free only in trans/diag overlay |
| `$A992`-`$A9E5` | 84 B | USED | FREE | Free only in trans/diag overlay |
| `$A9E7`-`$AA1E` | 56 B | USED | FREE | Free only in trans/diag overlay |
| `$AA20`-`$AA45` | 38 B | USED | FREE | Free only in trans/diag overlay |
| `$AA89`-`$AB75` | 237 B | USED | FREE | Free only in trans/diag overlay |
| `$AB77`-`$ABBA` | 68 B | USED | FREE | Free only in trans/diag overlay |
| `$ABBC`-`$AE68` | 685 B | USED | FREE | Free only in trans/diag overlay |
| `$AE6A`-`$AEA9` | 64 B | USED | FREE | Free only in trans/diag overlay |
| `$AEAC`-`$B0F0` | 581 B | USED | FREE | Free only in trans/diag overlay |
| `$B270`-`$B2A6` | 55 B | USED | FREE | Free only in trans/diag overlay |
| `$B2A8`-`$B325` | 126 B | USED | FREE | Free only in trans/diag overlay |
| `$B332`-`$B3AA` | 121 B | USED | FREE | Free only in trans/diag overlay |
| `$B3AC`-`$B539` | 398 B | USED | FREE | Free only in trans/diag overlay |
| `$B53B`-`$B5C4` | 138 B | USED | FREE | Free only in trans/diag overlay |
| `$B5C6`-`$B624` | 95 B | USED | FREE | Free only in trans/diag overlay |
| `$B632`-`$B673` | 66 B | USED | FREE | Free only in trans/diag overlay |
| `$B675`-`$B6E0` | 108 B | USED | FREE | Free only in trans/diag overlay |
| `$B6E2`-`$B75C` | 123 B | USED | FREE | Free only in trans/diag overlay |
| `$B75F`-`$B88F` | 305 B | USED | FREE | Free only in trans/diag overlay |
| `$B891`-`$B8B4` | 36 B | USED | FREE | Free only in trans/diag overlay |
| `$B92B`-`$B94B` | 33 B | USED | FREE | Free only in trans/diag overlay |
| `$B94D`-`$B987` | 59 B | USED | FREE | Free only in trans/diag overlay |
| `$B989`-`$B9AE` | 38 B | USED | FREE | Free only in trans/diag overlay |
| `$B9E0`-`$BA04` | 37 B | USED | FREE | Free only in trans/diag overlay |
| `$BA26`-`$BA94` | 111 B | USED | FREE | Free only in trans/diag overlay |
| `$BB30`-`$BB5D` | 46 B | USED | FREE | Free only in trans/diag overlay |
| `$BB7F`-`$BBD1` | 83 B | USED | FREE | Free only in trans/diag overlay |
| `$BC22`-`$BC90` | 111 B | USED | FREE | Free only in trans/diag overlay |
| `$BC92`-`$BCC5` | 52 B | USED | FREE | Free only in trans/diag overlay |
| `$BD07`-`$BD48` | 66 B | USED | FREE | Free only in trans/diag overlay |
| `$BD61`-`$BDA4` | 68 B | USED | FREE | Free only in trans/diag overlay |
| `$BDBF`-`$BDE1` | 35 B | USED | FREE | Free only in trans/diag overlay |
| `$BDE3`-`$BE09` | 39 B | USED | FREE | Free only in trans/diag overlay |
| `$BE10`-`$BE3D` | 46 B | USED | FREE | Free only in trans/diag overlay |
| `$BE77`-`$BEBA` | 68 B | USED | FREE | Free only in trans/diag overlay |
| `$BED5`-`$BEF7` | 35 B | USED | FREE | Free only in trans/diag overlay |
| `$BEF9`-`$BF1F` | 39 B | USED | FREE | Free only in trans/diag overlay |
| `$BF26`-`$BF53` | 46 B | USED | FREE | Free only in trans/diag overlay |
| `$BF86`-`$BFBC` | 55 B | USED | FREE | Free only in trans/diag overlay |
| `$C0AC`-`$C0D0` | 37 B | USED | USED | OCCUPIED — do not modify |
| `$C1A5`-`$C1D9` | 53 B | USED | USED | OCCUPIED — do not modify |
| `$C1DB`-`$C1FF` | 37 B | USED | USED | OCCUPIED — do not modify |
| `$C2E3`-`$C303` | 33 B | USED | USED | OCCUPIED — do not modify |
| `$C385`-`$C3A6` | 34 B | USED | USED | OCCUPIED — do not modify |
| `$CA57`-`$CA84` | 46 B | USED | FREE | Free only in trans/diag overlay |
| `$CA86`-`$CAF0` | 107 B | USED | FREE | Free only in trans/diag overlay |
| `$CAF2`-`$CB15` | 36 B | USED | FREE | Free only in trans/diag overlay |
| `$CB17`-`$CB4F` | 57 B | USED | FREE | Free only in trans/diag overlay |
| `$CB51`-`$CBB6` | 102 B | USED | FREE | Free only in trans/diag overlay |
| `$CDBC`-`$CE0E` | 83 B | USED | USED | OCCUPIED — do not modify |
| `$CE52`-`$D015` | 452 B | USED | FREE | Free only in trans/diag overlay |
| `$D017`-`$D4D7` | 1,217 B | USED | FREE | Free only in trans/diag overlay |
| `$D4F8`-`$D52D` | 54 B | USED | FREE | Free only in trans/diag overlay |
| `$D52F`-`$D6AB` | 381 B | USED | FREE | Free only in trans/diag overlay |
| `$D6CC`-`$D70F` | 68 B | USED | FREE | Free only in trans/diag overlay |
| `$D711`-`$D979` | 617 B | USED | FREE | Free only in trans/diag overlay |
| `$D97B`-`$D9AC` | 50 B | USED | FREE | Free only in trans/diag overlay |
| `$D9AE`-`$DA8E` | 225 B | USED | FREE | Free only in trans/diag overlay |
| `$DA90`-`$DACC` | 61 B | USED | FREE | Free only in trans/diag overlay |
| `$DAE0`-`$DD24` | 581 B | USED | FREE | Free only in trans/diag overlay |
| `$DD4C`-`$DEAF` | 356 B | USED | FREE | Free only in trans/diag overlay |
| `$DED2`-`$DF12` | 65 B | USED | FREE | Free only in trans/diag overlay |
| `$DF17`-`$DF89` | 115 B | USED | FREE | Free only in trans/diag overlay |
| `$DFC0`-`$E002` | 67 B | USED | FREE | Free only in trans/diag overlay |
| `$E004`-`$E048` | 69 B | USED | FREE | Free only in trans/diag overlay |
| `$E059`-`$E0A4` | 76 B | USED | FREE | Free only in trans/diag overlay |
| `$E0A7`-`$E0D9` | 51 B | USED | FREE | Free only in trans/diag overlay |
| `$E0E3`-`$E105` | 35 B | USED | FREE | Free only in trans/diag overlay |
| `$E119`-`$E166` | 78 B | USED | FREE | Free only in trans/diag overlay |
| `$E168`-`$E2A5` | 318 B | USED | FREE | Free only in trans/diag overlay |
| `$E2A7`-`$E2D8` | 50 B | USED | FREE | Free only in trans/diag overlay |
| `$E2DA`-`$E335` | 92 B | USED | FREE | Free only in trans/diag overlay |
| `$E352`-`$E373` | 34 B | USED | FREE | Free only in trans/diag overlay |
| `$E37D`-`$E42D` | 177 B | USED | FREE | Free only in trans/diag overlay |
| `$E42F`-`$E532` | 260 B | USED | FREE | Free only in trans/diag overlay |
| `$E54D`-`$E5E1` | 149 B | USED | FREE | Free only in trans/diag overlay |
| `$E5E4`-`$E662` | 127 B | USED | FREE | Free only in trans/diag overlay |
| `$E680`-`$E6A3` | 36 B | USED | FREE | Free only in trans/diag overlay |
| `$E6C0`-`$E6EB` | 44 B | USED | FREE | Free only in trans/diag overlay |
| `$E756`-`$E7D2` | 125 B | USED | FREE | Free only in trans/diag overlay |
| `$E7D4`-`$E87C` | 169 B | USED | FREE | Free only in trans/diag overlay |
| `$E87E`-`$E8B3` | 54 B | USED | FREE | Free only in trans/diag overlay |
| `$E8C1`-`$EACD` | 525 B | USED | FREE | Free only in trans/diag overlay |
| `$EACF`-`$EB22` | 84 B | USED | FREE | Free only in trans/diag overlay |
| `$EB31`-`$EBA5` | 117 B | USED | FREE | Free only in trans/diag overlay |
| `$EBCD`-`$EC0A` | 62 B | USED | FREE | Free only in trans/diag overlay |
| `$EC32`-`$EC77` | 70 B | USED | FREE | Free only in trans/diag overlay |
| `$EC86`-`$ECBE` | 57 B | USED | FREE | Free only in trans/diag overlay |
| `$ECCC`-`$EDD0` | 261 B | USED | FREE | Free only in trans/diag overlay |
| `$EDD2`-`$EEB3` | 226 B | USED | FREE | Free only in trans/diag overlay |
| `$EEE0`-`$EF1F` | 64 B | USED | FREE | Free only in trans/diag overlay |
| `$EF21`-`$EF64` | 68 B | USED | FREE | Free only in trans/diag overlay |
| `$EF66`-`$EF8E` | 41 B | USED | FREE | Free only in trans/diag overlay |
| `$EF90`-`$F03A` | 171 B | USED | FREE | Free only in trans/diag overlay |
| `$F05E`-`$F144` | 231 B | USED | FREE | Free only in trans/diag overlay |
| `$F1C4`-`$F1E3` | 32 B | USED | FREE | Free only in trans/diag overlay |
| `$F1E6`-`$F234` | 79 B | USED | FREE | Free only in trans/diag overlay |
| `$F23E`-`$F26D` | 48 B | USED | FREE | Free only in trans/diag overlay |
| `$F277`-`$F481` | 523 B | USED | FREE | Free only in trans/diag overlay |
| `$F483`-`$F4E6` | 100 B | USED | FREE | Free only in trans/diag overlay |
| `$F4E8`-`$F509` | 34 B | USED | FREE | Free only in trans/diag overlay |
| `$F50B`-`$F555` | 75 B | USED | FREE | Free only in trans/diag overlay |
| `$F557`-`$F59B` | 69 B | USED | FREE | Free only in trans/diag overlay |
| `$F5C3`-`$F605` | 67 B | USED | FREE | Free only in trans/diag overlay |
| `$F607`-`$F62F` | 41 B | USED | FREE | Free only in trans/diag overlay |
| `$F63E`-`$F6B4` | 119 B | USED | FREE | Free only in trans/diag overlay |
| `$F6CA`-`$F6F0` | 39 B | USED | FREE | Free only in trans/diag overlay |
| `$F6FE`-`$F72D` | 48 B | USED | FREE | Free only in trans/diag overlay |
| `$F76E`-`$F8C2` | 341 B | USED | FREE | Free only in trans/diag overlay |
| `$F8C4`-`$F97D` | 186 B | USED | FREE | Free only in trans/diag overlay |
| `$F97F`-`$F99F` | 33 B | USED | FREE | Free only in trans/diag overlay |
| `$F9A9`-`$FA01` | 89 B | USED | FREE | Free only in trans/diag overlay |
| `$FA0F`-`$FA67` | 89 B | USED | FREE | Free only in trans/diag overlay |
| `$FA6F`-`$FAAB` | 61 B | USED | FREE | Free only in trans/diag overlay |
| `$FAAD`-`$FAF3` | 71 B | USED | FREE | Free only in trans/diag overlay |
| `$FAF5`-`$FB20` | 44 B | USED | FREE | Free only in trans/diag overlay |
| `$FB76`-`$FB9E` | 41 B | USED | FREE | Free only in trans/diag overlay |
| `$FBA0`-`$FC3D` | 158 B | USED | FREE | Free only in trans/diag overlay |
| `$FC45`-`$FC83` | 63 B | USED | FREE | Free only in trans/diag overlay |
| `$FC93`-`$FE86` | 500 B | USED | FREE | Free only in trans/diag overlay |
| `$FE87`-`$FFB1` | 299 B | FREE | FREE | SAFE — inject in either overlay |

---

## Recommendations for Code Injection

### Safest targets (verified free, no crossover conflict):

1. **Bank 1 main free space:** `$C468`+ (15,192 bytes)
   - Always accessible regardless of bank switching
   - Recommended `ORG` for compiled C patches
   - THE1's zero-filled padding area — confirmed unused

2. **Overlay both-free region:** `$FE87`+ (299 bytes)
   - Free in both bank 2 AND bank 3
   - Safe to use from either overlay context

### Regions to avoid:

- `$FFC0`-`$FFFF` — Interrupt vector table (all banks)
- `$0000`-`$01FF` — RAM (bank 1)
- `$1000`-`$103F` — I/O registers (bank 1)
- `$4000`-`$7FFF` — Calibration tables (bank 1) — unless intentionally modifying tuning data
- Any address marked 'USED' in both overlays

### Workflow:

```
1. Write C code targeting a free region    -> examples/*.c
2. Compile to HC11 assembly                -> hc11cc.py
3. Assemble to binary                      -> hc11kit.py
4. Validate disassembly of output           -> 68hc11_disassembler_tool_for_vy_v6/
5. Flash to ECU                            -> OSE Flash Tool / ALDL kernel
```
### what could potenially be suppression of the dtc suppresion, dtf masked or turned off. and then removed?
maf sensor remove, use baro and tps and rpm with a rewrite of a enhanced bin.
other things


### Disassembly file comparison (all in bin_splits_disasm/)

Compare each bank across Custom, GNU, and udis disassembler outputs:
- `Enhanced_v1.0a_bank{1,2,3}.asm` (custom)
- `Enhanced_v1.0a_bank{1,2,3}_gnu.asm` (GNU objdump)
- `Enhanced_v1.0a_bank{1,2,3}_udis.asm` (udis)

---
---

# Cross-Referenced Research (from workspace docs)

> Gathered 2026-02-20 from all workspace repos. All addresses verified against the v1.0a binary.
>
> **Source repos:**
> - VY_V6_Assembly_Modding (primary research)
> - kingai_c_compiler_v0.1 (compiler & tooling)
> - kingai_commie_flasher (flash tool)
>
> **Key reference files:**
> - `VY_V6_Assembly_Modding\HARDWARE_SPECS.md`
> - `VY_V6_Assembly_Modding\MEMORY_MAP_VERIFIED.md`
> - `VY_V6_Assembly_Modding\BANK_SWITCHING_AND_ISR_ANALYSIS.md`
> - `VY_V6_Assembly_Modding\Rev_Limiter_Analysis_Validated.md`
> - `VY_V6_Assembly_Modding\TIC3_ISR_ANALYSIS.md`
> - `VY_V6_Assembly_Modding\ENHANCED_V1.0A_RAM_MAP_COMPLETE.md`
> - `VY_V6_Assembly_Modding\VY_V6_SPARK_CUT_IMPLEMENTATION_GUIDE.md`
> - `VY_V6_Assembly_Modding\ENHANCED_v204c_SPARK_CUT_ANALYSIS.md`
> - `VY_V6_Assembly_Modding\68HC11_Reference\M68HC11RM.md` (Motorola Reference Manual)
> - `VY_V6_Assembly_Modding\68HC11_Reference\M68HC11ERG.md` (E-series Reference Guide)
> - `VY_V6_Assembly_Modding\68HC11_Reference\DARC_vtsc_disasm_frompcmhacking\` (Antus VT SC disasm)
> - `VY_V6_Assembly_Modding\68HC11_Reference\JBug11_F1\` (F1 eval board config)
> - `VY_V6_Assembly_Modding\xdf_exports\OSE_11P_V104.md` ($11P MEMCAL XDF)
> - `VY_V6_Assembly_Modding\xdf_exports\VY_V6_060A.md` ($060A XDF)
> - `VY_V6_Assembly_Modding\xdfs_and_adx_and_bins_related_to_project\VX VY_V6_$060A_Enhanced_v2.04c\` (v2.04c spark cut bin+XDF)
> - `VY_V6_Assembly_Modding\techedge_decompiled\TECHEDGE_TOOLS_DECOMPILATION_REFERENCE.md`

---

## 1. HC11 Variant Identification — What We Know vs What We Assume

### The Question

Is the CPU in the VY V6 $060A PCM an HC11F0, F1, F3, FC0, or something else? Are they all the same silicon with different mask options? What about the VT SC?

### Evidence Summary

| Source | Says | For Which ECU | Authority |
|--------|------|:-------------:|-----------|
| DARC DARClow.asm line 7 | `68HC11FC0 [RAM=1024 ROM=0 EPROM=0 EEPROM=0]` | **VT V6 SC (L67)** | IDA Pro config chosen by Antus |
| DARC memory.x linker | `page0: ORIGIN=0x0000, LENGTH=0x03FF` (1KB RAM) | VT V6 SC | GNU ld script |
| PCMHacking topic_3007 | "motorola processor 68hc11f1 - e87j" | **VT ECU** (physical chip reading, Brazil) | Physical inspection |
| PCMHacking topic_1573 (sabercatpuck) | "ive just used 68HC11F1 config" | VT/VX/VY ECUs | IDA Pro config choice |
| PCMHacking topic_982 (VL400) | Crystal = 13.631488 MHz | VX/VY Flash PCMs | Timing measurement |
| PCMHacking topic_4539 (Antus, oscilloscope) | "3.41MHz on the VX/VY (Flash PCMs)" | VX/VY | Scope measurement |
| PCMHacking topic_655 | "same 8bit HC11 derivative" | All VN-VY | General statement |
| HARDWARE_SPECS.md (corrected Feb 2026) | "68HC11F-family derivative (68HC11FC0 per DARC/IDA Pro)" | VY V6 $060A | Project analysis |
| M68HC11RM.md (Motorola Reference Manual) | "MC68HC11F1 is available only in a 68-pin PLCC package" | F1 spec | Official Motorola |
| JBug11 F1 config | RAM=0000..03FF, Regs=1000-105F, EEPROM=0E00..0FFF | HC11F1 eval board | Dev board config |

### HC11F Sub-Variants (from Motorola Reference Manual)

| Feature | HC11E9 | HC11F1 | HC11FC0 (DARC) |
|---------|:------:|:------:|:---------------:|
| RAM | 512 bytes ($0000-$01FF) | **1,024 bytes** ($0000-$03FF) | **1,024 bytes** |
| ROM | 12 KB | 0 | 0 |
| EPROM | 0 | 0 | 0 |
| EEPROM | 512 bytes ($B600-$B7FF) | 512 bytes ($0E00-$0FFF) | **0 bytes** |
| Package | 52-pin PLCC | **68-pin PLCC** | 68-pin PLCC |
| I/O regs | 64 bytes ($1000-$103F) | **96 bytes** ($1000-$105F) | 96 bytes |
| Bus | Multiplexed (Port B/C) | **Non-multiplexed** | Non-multiplexed |
| Port G | No | **Yes** | Yes |
| Port F | No | **Yes** | Yes |
| Chip Selects | No | **Yes** (CSCTL, CSSTRH, etc.) | Yes |
| DDRA | No ($01 reserved) | **Yes** ($1001) | Yes |

### What "FC0" Means

The "FC0" designation in DARC appears to be a **custom GM mask set** of the F1 die:
- **F** = F-series (non-multiplexed bus, 1KB RAM, chip selects)
- **C** = Custom? (GM-specific mask options)
- **0** = Zero EEPROM, Zero ROM (pure external-memory device)

This makes sense for an ECU — you don't need on-chip ROM (you have external flash) and you don't need EEPROM (VY uses flash for cal storage). The underlying **silicon is the same as F1** — same instruction set, same register map, same timer system.

### CONFIRMED for VY V6 $060A

- CPU is **MC68HC11 F-family** (not E-series) — proven by:
  - 1KB RAM usage confirmed in binary analysis ($0000-$03FF)
  - Register block extends to $105F (96 bytes, not E-series 64 bytes)
  - PORTG/PORTF register definitions present in disassembler tools
  - Non-multiplexed bus (required for 128KB external flash banking)
- **E-clock = 3.408 MHz** (crystal 13.631488 MHz ÷ 4) — scope-confirmed by Antus
- **Same instruction set** as all other HC11 variants (100% opcode compatible)

### ASSUMED (High Confidence)

- The VY V6 $060A uses the **same silicon** as the VT V6 SC — both labeled HC11FC0 / F1
- "FC0" is a mask set, not a different chip — same die, different options
- **No one has physically photographed the chip** in a VY V6 $060A PCM (09356445)

### STILL UNKNOWN

- Exact package (68-pin PLCC assumed, but could be BGA/QFP on IPCM-6 board)
- Whether GM sourced a true F1 or a custom derivative (common in automotive)
- Whether any F0 / F3 variants exist (not documented in Motorola Reference Manual)
- VT SC ECU (Delco 808) vs VY V6 PCM (IPCM-6) — same chip, different board?

### VT SC vs VY V6 — ECU Platform Comparison

| Aspect | VT V6 SC (L67) | VY V6 N/A (L36) |
|--------|:--------------:|:----------------:|
| CPU | MC68HC11 F-family | MC68HC11 F-family |
| ECU Platform | **Delco 808**, MEMCAL | **IPCM-6**, Flash |
| Part Number | — | 09356445 |
| Mask/OSID | **$07** | **$060A / $060B** |
| Binary Size | 32KB (single bank) | **128KB** (bank-switched) |
| ROM Type | MEMCAL PROM chip | **External NOR flash** (M29W800DB) |
| Bank Switching | None (32KB fits in $8000-$FFFF) | **Yes** — PORTC bit 3 → A16 |
| DARC Source | ✅ DARClow.asm + DARChigh.asm | ❌ No complete disassembly |
| Crystal | 13.631488 MHz (same) | 13.631488 MHz (same) |
| E-Clock | 3.408 MHz (same) | 3.408 MHz (same) |

**Key insight:** The VT SC uses a **single 32KB MEMCAL** (no banking), while the VY V6 has **128KB flash with bank switching**. The CPU is the same silicon — the banking is done with external address decoding via PORTC bit 3.

### Answer to "Are F0/F1/F3 All The Same?"

There is **no F0 or F3** documented in the Motorola M68HC11 Reference Manual. The F-series variants documented are:

| Variant | Notes |
|---------|-------|
| **MC68HC11F1** | The standard F-series part. 68-pin PLCC, 1KB RAM, 512B EEPROM, chip selects |
| **MC68HC711F1** | OTP (one-time programmable) version of F1 |
| **MC68HC11FC0** | Custom mask — appears to be F1 with 0 EEPROM/ROM (per DARC IDA config) |

If you've seen "F0" referenced, it's likely a confusion with "FC0" (the mask set designation). All F-family parts share:
- Same 68HC11 CPU core (identical instruction set)
- Same timer system (IC1-3, OC1-5, pulse accumulator)
- Same SCI and SPI peripherals
- Same register map ($1000-$105F)
- 1KB internal RAM

The **only differences** between F-family mask sets are:
- Whether internal EEPROM is present (F1: yes, FC0: no)
- Whether internal ROM/OTP is present
- Potentially different CONFIG register defaults

---

## 2. Processor & Hardware (Corrected)

| Spec | Value |
|------|-------|
| CPU | Motorola 68HC11F-family (68HC11FC0 mask per DARC) |
| Architecture | 8-bit, Big Endian |
| E-Clock | **3.408 MHz** (13.631488 MHz crystal ÷ 4) |
| RAM | **1,024 bytes** ($0000-$03FF) |
| Flash | M29W800DB / Am29F010 / SST39SF010, **128 KB** |
| PCM Part # | 09356445 (VX/VY V6) |
| Mask ID | $060A / $060B |
| Ignition | Wasted Spark DFI — 3 coil packs (pairs: 1&4, 2&5, 3&6) |
| Crank Sensor | **24X** (NOT 3X) — 15° per pulse |
| Baud Rate | 8192 baud half-duplex serial (ALDL) |

**Previous errors corrected:**
- Was identified as HC11E9 with 2 MHz E-clock → corrected to HC11FC0, 3.408 MHz
- Was identified as 3X crank → corrected to 24X crank via TIC3 ISR disassembly

---

## 3. Complete CPU Address Space (HC11F Expanded Mode)

```
$0000-$00FF   Internal RAM    — Direct page (256 bytes, fast 8-bit addressing)
$0100-$03FF   Internal RAM    — Extended (768 bytes, HC11F has 1KB total)
$1000-$105F   I/O Registers   — HC11F memory-mapped (96 bytes: PORTA thru CONFIG)
$2000-$3FFF   ALWAYS VISIBLE  — Pseudo-vector jump table + common subroutines
$4000-$4007   ALWAYS VISIBLE  — Checksum bytes (SKIPPED in checksum calculation)
$4008-$7FFF   ALWAYS VISIBLE  — Calibration tables (all XDF data lives here)
$8000-$FFBF   BANK-SWITCHED   — Engine OR Trans/Diag overlay (PORTC bit 3 selects)
$FFC0-$FFFF   BANK-SWITCHED   — Interrupt vector table (21 vectors)
```

---

## 4. Bank Switching Mechanism

**Hardware:** PORTG ($1002) controls bank selection (HC11F-series)

On the HC11F, $1002 = PORTG (data register) and $1003 = DDRG (direction register).
The code manipulates PORTG bits to control which overlay bank is visible at $8000-$FFFF.

| PORTG State | Bank at $8000-$FFFF | File Offsets |
|:-----------:|:-------------------:|:------------:|
| Low bit(s) cleared | Engine (Bank 2) | 0x10000-0x17FFF |
| Low bit(s) set | Trans/Diag (Bank 3) | 0x18000-0x1FFFF |

**Binary proof:**
- PORTG ($1002) is read/written 20+ times across banks 1-3 for bank switching and ADC MUX control
- `STAB $1003` at CPU $C76A (bank2, file 0x1476A) writes `$F7` to DDRG — this sets Port G **data direction**, not data
- Pattern: `LDAA $1002; ANDA #$F8; ORAA #imm; STAA $1002` appears at $98BB, $CB1A, $AEC4, etc. — controls Port G low bits for ADC MUX channel selection; higher bits control bank switching

**CORRECTION 2026-02-20:** Previous versions said "PORTC ($1003) bit 3 controls A16".
This was wrong — $1003 is DDRG (Port G DDR) on F-series, not PORTC. The actual
bank switching register is PORTG at $1002. The "BSET $03,#$CC at 0x0B0B9" reference
was also wrong — that address is in the middle of a `STAA $1C03` instruction, not a BSET.

### Address Conversion

```python
# Common area: CPU address = file offset
if 0x2000 <= cpu_addr <= 0x7FFF:
    file_offset = cpu_addr

# Bank-switched: AMBIGUOUS — must know active bank
if 0x8000 <= cpu_addr <= 0xFFFF:
    bank1_file = cpu_addr                # 0x08000-0x0FFFF
    bank2_file = cpu_addr + 0x8000       # 0x10000-0x17FFF
    bank3_file = cpu_addr + 0x10000      # 0x18000-0x1FFFF
```

### Cross-Bank Constraint

A `JSR` in the $8000-$FFFF range executes whatever is in the **currently visible bank** at that address. To call Bank1 from Bank2, you need a trampoline through COMMON ($2000-$7FFF).

$D000-$EFFF is **identical** between LOW and HIGH halves (shared lookup tables). Only 3 vectors differ: COP, CMF, RESET.

---

## 5. Interrupt Vectors & Pseudo-Vector Table

### Pseudo-Vector Table at $2000-$202F (COMMON, always visible)

| CPU Addr | Target | Purpose | HW Vector |
|:--------:|:------:|---------|:---------:|
| `$2000` | $2BAF | Default ISR (RTI) | SPI/PAIE/PAO/TOF/TOC5/TOC2/RTI |
| `$2003` | $29D3 | SCI (serial/ALDL) | $FFD6 |
| `$2006` | $35DE | TOC4 ISR | $FFE2 |
| `$2009` | $35BD | **TOC3 ISR (EST spark output)** | $FFE4 |
| `$200C` | $37A6 | TOC1 ISR | $FFE8 |
| `$200F` | $35FF | **TIC3 ISR (24X crank input)** | $FFEA |
| `$2012` | $358A | TIC2 ISR (CAM/sync) | $FFEC |
| `$2015` | $301F | TIC1 ISR | $FFEE |
| `$2018` | $30BA | IRQ handler | $FFF2 |
| `$201B` | $2BAC | XIRQ handler | $FFF4 |
| `$201E` | $2BA0 | SWI handler | $FFF6 |
| `$2021` | $2BA6 | ILLOP handler | $FFF8 |
| `$2024` | ∞ loop | COP (engine bank) | $FFFA |
| `$2027` | ∞ loop | CMF (engine bank) | $FFFC |
| `$202A` | ∞ loop | RESET (engine bank) | $FFFE |

### Vectors Differing Between Banks

| Vector | Engine (LOW) | Trans (HIGH) |
|--------|:------------:|:------------:|
| COP | $2024 (∞ loop) | $C015 |
| CMF | $2027 (∞ loop) | $C019 |
| RESET | $202A (∞ loop) | $C011 (boot) |

---

## 6. TIC3 ISR (24X Crank Handler) at $35FF

```asm
$35FF:  LDAA  #$01        ; IC3F flag bit mask
$3601:  STAA  $1023       ; Acknowledge interrupt (TFLG1)
$3604:  INC   $1B8C       ; Increment 24X pulse counter
$3607:  INC   $18E5       ; Increment secondary counter
$360A:  BRCLR $46,#$01,$361C  ; Test bit 0 of $0046
$360E:  BRSET $48,#$01,$3616  ; Test bit 0 of $0048
$3612:  BRCLR $44,#$10,$361C  ; Test bit 4 of $0044
$3616:  BCLR  $48,#$01    ; Clear bit 0 of $0048
$3619:  JMP   $3719       ; Jump to RTI (early exit — engine not synced)
$361C:  FDIV               ; (data/alignment byte, not real instruction)
$361D:  FDIV               ; (data/alignment byte)
$361E:  LDAB  $016D       ; Load cylinder index
$3621:  LDX   #$6852      ; Cylinder timing table base
...
$3631:  JSR   $371A       ; Call Dwell_Calc
$3634:  STAA  $017D       ; Store dwell result
$3637:  LDAA  $15CA       ; Load calibration constant
$363A:  NOP                ; (padding — double-read pattern)
$363B:  LDD   $15CA       ; Re-load as 16-bit word
$363E:  STD   $0178       ; Store TIC3 capture value
...
$3713:  LDD   $0178       ; Reload capture value
$3716:  STD   $1B7A       ; Store previous period
$3719:  RTI                ; Return from interrupt
```

**CORRECTION 2026-02-20:** Previous version claimed "STD $194C at $3618 (cold-start init only)".
This was WRONG. Address $3618 is the last byte of the BCLR $48,#$01 instruction at $3616
(3-byte instruction: 15 48 01). There is NO `STD $194C` anywhere in the TIC3 ISR at $35FF.

The actual `STD $194C` instructions are in **bank2** at completely different addresses:
- $B30A: `STD $194C` — CCP/canister purge logic (not crank period init)
- $B618: `STD $194C` — secondary period calculation
- $B35D: `STAA $194C` — additional reference

`$194C` is used for canister purge/CCP timing in bank2, with 5 references total (2 STD, 1 STAA, 1 LDAA, 1 LDX).
It is NOT a "cold-start only" variable and it is NOT in the TIC3 ISR.

Also previously listed `$361C: PULB` — this was wrong. Byte `$03` = FDIV, not PULB (`$33`).

### TOC3 ISR (EST Spark Output) at $35BD

```asm
$35C9:  ORAA  #$10       ; Set bit 4 (EST high = coil charge)
$35CB:  ANDA  #$F7       ; Clear bit 3
$35CD:  STAA  $1000      ; Write PORTA → controls EST
$35D0:  JSR   $88B0      ; Call timing routine (Bank2)
```

---

## 7. I/O Register Map ($1000-$105F)

### HC11E-Series Registers ($1000-$103F) — All present on F-series too

| Address | Name | Description |
|:-------:|:----:|-------------|
| `$1000` | PORTA | Port A (timer/PA pins PA0-PA7) |
| `$1001` | DDRA | Port A DDR (**F-series only**, reserved on E) |
| `$1002` | PIOC | Parallel I/O Control (E) / **PORTG** (F) |
| `$1003` | PORTC | Port C — **multiplexed data bus in expanded mode** |
| `$1004` | PORTB | Port B — address bus high byte in expanded mode |
| `$1005` | PORTCL | Port C Latched (E) / **PORTF** (F) |
| `$1008` | PORTD | Port D (SCI + SPI: TxD, RxD, SDO, SDI, SCK, SS) |
| `$100A` | PORTE | Port E (A/D inputs AN0-AN7) |
| `$100C` | OC1M | Output Compare 1 Mask |
| `$100D` | OC1D | Output Compare 1 Data |
| `$100E` | TCNT | Timer Counter (16-bit, free-running) |
| `$1010` | TIC1 | Input Capture 1 |
| `$1012` | TIC2 | Input Capture 2 |
| `$1014` | TIC3 | Input Capture 3 (24X crank) |
| `$1016` | TOC1 | Output Compare 1 |
| `$1018` | TOC2 | Output Compare 2 |
| `$101A` | TOC3 | Output Compare 3 (EST spark) |
| `$101C` | TOC4 | Output Compare 4 |
| `$101E` | TI4/O5 | Input Capture 4 / Output Compare 5 |
| `$1020` | TCTL1 | Timer Control 1 (OC edge/level) |
| `$1021` | TCTL2 | Timer Control 2 (IC edge config) |
| `$1022` | TMSK1 | Timer Interrupt Mask 1 |
| `$1023` | TFLG1 | Timer Flag 1 (OC/IC flags) |
| `$1024` | TMSK2 | Timer Interrupt Mask 2 |
| `$1025` | TFLG2 | Timer Flag 2 |
| `$1026` | PACTL | Pulse Accumulator Control |
| `$1027` | PACNT | Pulse Accumulator Counter |
| `$1028` | SPCR | SPI Control |
| `$1029` | SPSR | SPI Status |
| `$102A` | SPDR | SPI Data |
| `$102B` | BAUD | SCI Baud Rate |
| `$102C` | SCCR1 | SCI Control 1 |
| `$102D` | SCCR2 | SCI Control 2 |
| `$102E` | SCSR | SCI Status |
| `$102F` | SCDR | SCI Data |
| `$1030` | ADCTL | A/D Control/Status |
| `$1031-$1034` | ADR1-4 | A/D Result Registers |
| `$1035` | BPROT | EEPROM Block Protect |
| `$1039` | OPTION | System Config (ADPU, CSEL, IRQE, DLY, CME, CR) |
| `$103B` | PPROG | EEPROM Programming Control |
| `$103C` | HPRIO | Highest Priority I-bit Interrupt |
| `$103D` | INIT | RAM/Register Mapping (write ONCE in first 64 cycles) |
| `$103F` | CONFIG | Configuration (NOSEC, NOCOP, ROMON, EEON) |

### F-Series Extended Registers ($1040-$105F)

| Address | Name | Description |
|:-------:|:----:|-------------|
| `$1040-$105F` | CSSTRH, CSGADR, CSGSIZ, CSCTL, etc. | Chip Select control registers |

**Critical E vs F difference at $1002/$1005:**
- **E-series:** $1002 = PIOC (parallel I/O control), $1005 = PORTCL (Port C latched)
- **F-series:** $1002 = PORTG (extra I/O port), $1005 = PORTF (extra I/O port)

The VY V6 binary accesses $1002 and $1005 — whether it treats them as PIOC/PORTCL (E) or PORTG/PORTF (F) affects interpretation. On an F-series chip in expanded mode, PORTC ($1003) is the data bus and PORTG/PORTF are the extra I/O.

---

## 8. RAM Map (Verified Variables)

### High-Confidence Engine Variables

| Address | Size | Purpose | Refs | Notes |
|:-------:|:----:|---------|:----:|-------|
| `$00A2` | 1B | **Engine RPM** (×25) | 83 | 0xC0=4800, 0xEC=5900, 0xF0=6000, 0xFF=6375 |
| `$009D` | 2B | **16-bit RPM** (used by The1's v2.04c) | — | `LDD $009D` then `CPD` in spark cut code |
| `$00A4` | 1B | TPS or calculated load | 79 | Capped at #$C0 |
| `$0083` | 1B | MAF/Airflow (ADC1 at $1031) | 50 | |
| `$00F3` | 1B | Coolant temp (ECT) | 56 | |
| `$00A6` | 1B | IAT or secondary temp | 20 | |
| `$0153` | 2B | Injector pulse width | 2 | |
| `$016B` | 2B | Secondary fuel variable | 5 | |
| `$016D` | 1B | Cylinder index | — | |
| **`$017B`** | **2B** | **Dwell intermediate** (hook target) | **2** | **NOT crank period** |
| `$0199` | 2B | Dwell time storage | 4 | |
| `$194C` | 2B | 24X crank period (TIC3) | 5 | Bank2 only — CCP/purge logic at $B30A, $B332, $B35D, $B5C0, $B618 |
| `$149E` | 1B | EST control flag (The1's code clears bit 0) | — | Application RAM |
| `$16FA` | 1B | Timing flag (ORAB #$FF = force-activate) | — | |

### Free RAM

| Address | Notes |
|:-------:|-------|
| `$01A0` | 0 references — confirmed unused |
| `$0046` bit 7 | 0 refs — **recommended limiter flag** |
| `$0046` bit 6 | 0 refs — free |
| `$0046` bit 3 | 0 refs — free |

---

## 9. RPM Scaling & Rev Limiter

### RPM = $00A2 × 25

| Hex | Decimal | RPM |
|:---:|:-------:|----:|
| $80 | 128 | 3,200 |
| $A0 | 160 | 4,000 |
| $C0 | 192 | 4,800 |
| $E0 | 224 | 5,600 |
| $EB | 235 | 5,875 |
| $EC | 236 | 5,900 |
| $F0 | 240 | 6,000 |
| $FF | 255 | 6,375 |

**8-bit hard cap:** Max representable = 255 × 25 = 6,375 RPM. Exceeding this requires code mod.

### Stock Fuel-Cut Rev Limiter at file 0x77DE

```
0x77DE:  EC EB EC EB EC EB FE FD FE FD FF FF
         5900 5875 5900 5875 5900 5875 6350 6325 6350 6325 6375 6375
```

- Fuel cut ON: 0xEC (236) = **5,900 RPM**
- Fuel cut OFF: 0xEB (235) = **5,875 RPM** (25 RPM hysteresis)
- Enhanced v1.0a: ALL = 0xFF (6,375 — limiters effectively disabled)

### Rev Limiter Comparison Across Platforms

| Platform | OSID | Start Cut (Drive) | Full Cut (Drive) | Spark Cut Available? | Address |
|----------|:----:|:-----------------:|:----------------:|:--------------------:|:-------:|
| **VS V6** | $51 | 5,600 RPM | 5,900 RPM | No | 0x77DE |
| **VT V6** | $A5G | 5,875 RPM | 5,900 RPM | No | 0x77DE |
| **VY V6** | $060A | 5,875 RPM | 5,900 RPM | No | 0x77DE |
| **OSE 11P** | $11P | 5,700 RPM | 5,800 RPM | **Yes (flag, disabled)** | 0x60B9/0x60C0 |
| **Enhanced v2.04c** | $060A | 5,875 RPM | 5,900 RPM | **Yes (added by The1)** | 0x77DE + 0x78B2 |

### OSE 11P Spark Cut (Reference Architecture)

The $11P MEMCAL firmware has spark cut as a **built-in but disabled feature**:
- Flag at `0x6004` bit 5: "Enable Spark Cut Rev Limit" — **Not Set** by default
- Flag at `0x6069` bit 5: Same for Power mode — **Not Set** by default
- Separate Econ/Power thresholds at `0x60B9` / `0x60C0` (5,800 RPM)
- Hysteresis: ON at 5,800, OFF at 5,700 (0x60B7 / 0x60BE)

This proves GM **designed** spark cut into the 11P codebase but **disabled it** in production calibration. The VY $060A firmware does NOT have this feature — it was added by The1 in v2.04c.

---

## 10. Spark Cut Implementation Comparison

### Stock VY V6 = Fuel Cut Only (No Spark Cut)

### The1's v2.04c (Enhanced v1.1a binary)

| Aspect | Detail |
|--------|--------|
| XDF Parameter | "Spark - RPM Cut" at **0x78B2** |
| Default Value | 3,000 RPM (0x0BB8) — 16-bit, direct RPM value |
| Binary Changes | 269 bytes changed from v1.0a → v1.1a |
| Hook | File 0x056F4: `00` → `60` |
| Code Location | File 0x17D84 (CPU $7D84 in banked area): `DC 9D 1A B3 78 B2...` |
| Method | Direct EST line control — triggers DTC 41/42, jumps over MALF routines |
| Status | **Shelved** — EST bypass causes diagnostic issues |

### Our v38 (Chr0m3-inspired dwell starvation)

| Aspect | Detail |
|--------|--------|
| Hook Point | File 0x101E1: `FD 01 7B` → `BD C5 00` |
| Patch Location | CPU $C500 (Bank1 free space, file 0x0C500) |
| Method | Fake dwell intermediate ($3E80) → coils starved → no spark |
| RPM Variable | $00A2 (8-bit, ×25 scale) |
| Threshold | 0xF0 = 6,000 RPM (hardcoded, not XDF-tunable yet) |
| Flag | $0046 bit 7 (verified free, 0 refs) |
| Code Size | 25 bytes |
| Status | **Untested** — needs bench validation |

### OSE 11P (VL400's proven production method)

| Aspect | Detail |
|--------|--------|
| Method | Dwell → 200µs (confirmed VL400 Post #164) |
| Soft Zone | Yes — 150 RPM, 5.98° retard before hard cut |
| DTC | Conditionally disables MALF 41/42 during cut |
| Platform | 1227424 (64KB, no bank switching) — direct TIO control |
| Status | **Production-tested (10+ years)** |

### Method Comparison

| Feature | OSE 11P (VL400) | Our v38 | The1's v2.04c |
|---------|:---------------:|:-------:|:-------------:|
| Method | Dwell starvation | Dwell starvation | EST line off |
| Proven? | ✅ 10+ years | ⬜ Untested | ⚠️ Shelved |
| Soft Zone | ✅ 150 RPM | ❌ Hard cut | ❌ Hard cut |
| DTC Safe | ✅ Conditional | ✅ No DTC trigger | ❌ Triggers MALF |
| XDF Tunable | ✅ All params | ❌ Hardcoded | ✅ 0x78B2 |
| Code Size | Large (production) | 25 bytes | ~120 bytes |

---

## 11. Spark Cut Verified Patch (v38 — Dwell Intermediate Method)

### Hook (3 bytes at file 0x101E1)

```
Before:  FD 01 7B         (STD $017B)
After:   BD C5 00         (JSR $C500)
```

### Patch (25 bytes at file 0x0C500)

```asm
        ORG $C500
SPARK_CUT_CHECK:
        PSHA                    ; $36
        LDAA   $00A2            ; $96 $A2     RPM/25
        CMPA   #$F0             ; $81 $F0     240 = 6000 RPM
        BCS    .normal          ; $25 $07     RPM < threshold
        BSET   $46,#$80         ; $1C $46 $80 Set limiter flag
        PULA                    ; $32
        LDD    #$3E80           ; $CC $3E $80 Fake dwell = 16000
        STD    $017B            ; $FD $01 $7B Override
        RTS                     ; $39
.normal:
        BCLR   $46,#$80         ; $1D $46 $80 Clear flag
        PULA                    ; $32
        STD    $017B            ; $FD $01 $7B Store real value
        RTS                     ; $39
```

### Hex Bytes

```
36 96 A2 81 F0 25 07 1C 46 80 32 CC 3E 80 FD 01 7B 39 1D 46 80 32 FD 01 7B 39
```

---

## 12. RPM Threshold References Found in Binary

Binary scan for `LDAA/LDAB $A2` + `CMPA/CMPB` against cal addresses with values ≥ 0xC0:

| Bank2 CPU | Cal Addr | Cal Value | ~RPM | Likely Purpose |
|:---------:|:--------:|:---------:|:----:|----------------|
| `$8F2B` | $7B0E | 0xC0 | 4,800 | Overrev / fuel cutoff enable |
| `$8F30` | $7B0F | 0xA0 | 4,000 | Overrev hysteresis OFF |
| `$A70F` | $6880 | 0xF0 | 6,000 | Spark advance threshold |
| `$D6EA` | $571D | 0xFF | 6,375 | Max RPM gate |
| `$F658` | $6976 | 0xE1 | 5,625 | Spark table boundary |
| `$FCF9` | $651B | 0xFF | 6,375 | RPM gate |

---

## 13. Checksum Details

- **Region 1:** 0x02000 → 0x03FFF
- **Region 2:** 0x04008 → 0x1FFFF
- **Skipped:** 0x04000-0x04007 (checksum storage)
- **Tools:** `hc11kit.py checksum`, KingAI Commie Flasher auto-fix

---

## 14. Calibration Table Locations (Spark & Fuel)

### Spark Tables

| Offset | XDF Title |
|:------:|-----------|
| 0x57AF | Main High-Octane Spark > 850-1650mg |
| 0x58C2 | Main Low-Octane Spark > 850-1650mg |
| 0x614E | Main High-Octane Spark < 4800 RPM |
| 0x6272 | Main Low-Octane Spark < 4800 RPM |
| 0x63C2 | Base ECT Spark Table |
| 0x646D | Cold Spark Offset Table |
| 0x6776 | Dwell Threshold (If Delta Cylair > This → Max Dwell) — stock $20 |
| 0x6783 | Spark Timing when Cranking Low RPM |
| 0x78B2 | **Spark - RPM Cut** (v2.04c only, NOT in v1.0a) — 3,000 RPM default |

### Fuel Tables

| Offset | XDF Title |
|:------:|-----------|
| 0x59D5 | Fuel Trim / Injector Multiplier vs RPM & Cylair |
| 0x6D1D | Maximum Airflow vs RPM (MAF limit) |
| 0x7502 | PE Commanded AFR Multiplier vs Time - RPM Limit |
| 0x77DE | **Rev limiter (fuel cut)** — 12-byte table |

### OSE 11P Table Locations (for comparison)

| $11P Offset | $060A Equivalent | XDF Title |
|:-----------:|:----------------:|-----------|
| 0x60B9 | 0x77DE | High RPM Fuel/Spark Cut threshold (Econ) |
| 0x60C0 | 0x77DE | High RPM Fuel/Spark Cut threshold (Power) |
| 0x6004 bit 5 | — (not present) | Enable Spark Cut Rev Limit flag |
| 0x6049 | ~0x6783 | EST Idle Spark Advance |
| 0x7534 | ~0x614E | Main Spark Advance table |
| 0x6E06 | ~0x59D5 | Main VE table |

---

## 15. Opcode Quick Reference

| Instruction | Hex | Notes |
|-------------|:---:|-------|
| `JMP $xxxx` | 7E xx xx | 3B |
| `JSR $xxxx` | BD xx xx | 3B |
| `RTS` | 39 | 1B |
| `RTI` | 3B | 1B |
| `NOP` | 01 | 1B |
| `LDAA #$xx` | 86 xx | 2B |
| `LDAA $xx` | 96 xx | 2B (direct page) |
| `LDAA $xxxx` | B6 xx xx | 3B (extended) |
| `LDD #$xxxx` | CC xx xx | 3B |
| `STD $xxxx` | FD xx xx | 3B |
| `CMPA #$xx` | 81 xx | 2B |
| `BCS $rel` | 25 xx | 2B (unsigned <) |
| `BCC $rel` | 24 xx | 2B (unsigned >=) |
| `BEQ $rel` | 27 xx | 2B |
| `BNE $rel` | 26 xx | 2B |
| `PSHA` | 36 | 1B |
| `PULA` | 32 | 1B |
| `BSET $xx,#$mm` | 1C xx mm | 3B |
| `BCLR $xx,#$mm` | 1D xx mm | 3B |
| `BRSET $xx,#$mm,$rel` | 12 xx mm rr | 4B |
| `BRCLR $xx,#$mm,$rel` | 13 xx mm rr | 4B |

---

## 16. Code Injection Patterns

### Hook + Patch (Antus: "patch, not rebuild")

```asm
; Replace 3-byte instruction with JSR to free space:
; Original:  BD 24 AA   (JSR $24AA)
; Patched:   BD C4 68   (JSR $C468)

ORG $C468
CUSTOM:
    ; ... your logic ...
    JSR $24AA       ; Call original subroutine
    RTS
```

### Cross-Bank Trampoline

```asm
; Bank2 ($FE87) → COMMON ($3E87) → Bank1 ($C468)
; In Bank2: JMP $3E87
; In COMMON: switch bank, JSR $C468, switch back, RTS
```

### Toolchain Pipeline

```bash
python hc11cc.py patch.c --target vy_v6           # C → HC11 ASM
python hc11kit.py asm spark_cut.asm -o out.bin     # ASM → binary
python hc11kit.py patch stock.bin patch.asm --at 0x5D05 --hook 0x101E1:3 --verify
python hc11kit.py free ECU.bin --min-size 64       # Find free space
python hc11kit.py checksum ECU.bin --fix           # Fix checksum
```

---

## 17. XDF Statistics

- **2,188 total definitions** — 334 tables, 1,546 constants, 548 flags
- All map to file offsets $04000-$07FFC (calibration area, COMMON)
- **No XDF definitions** for Bank2 or Bank3 code
- Enhanced v1.1a (v2.04c) adds "Spark - RPM Cut" at 0x78B2 (not in v1.0a)
- Enhanced v2.09b does NOT carry forward 0x78B2 — spark cut was dropped/refactored

---

## 18. Corrections Record

| Date | Was | Corrected To | Source |
|------|-----|-------------|--------|
| 2026-02-20 | §4: "PORTC ($1003) bit 3 controls A16" | PORTG ($1002) controls bank switching. $1003 = DDRG (direction register for PORTG on F-series) | Labeled v2 disasm: 20+ PORTG $1002 R/W in bank-switch code, single $1003 write = DDRG init |
| 2026-02-20 | §4: "BSET $03,#$CC at file 0x0B0B9" | Address 0x0B0B9 is middle of STAA $1C03 instruction, NOT a BSET | Labeled v2 disasm: $B0B8 = B7 1C 03 = STAA $1C03 |
| 2026-02-20 | §6: "STD $194C at $3618 in TIC3 ISR" | $3618 is last byte of BCLR $48,#01 at $3616. No STD $194C in TIC3 ISR. All $194C refs are in bank2 ($B30A, $B618, etc.) | Labeled v2 disasm verification |
| 2026-02-20 | §6: "$361B: BRA $3633" | $3619: JMP $3719 (to RTI). No instruction at $361B — it's inside JMP operand | Labeled v2 disasm |
| 2026-02-20 | §6: "$361C: PULB" | $361C: FDIV (opcode $03, not $33). Byte $03 = FDIV | Labeled v2 disasm |
| 2026-02-20 | §8: $194C has "1 ref, cold-start init only" | 5 refs in bank2 — CCP/canister purge logic, not cold-start only | Labeled v2 grep across all banks |
| 2026-02-20 | Top memory map: RAM = 512B ($0000-$01FF) | RAM = 1,024B ($0000-$03FF) — HC11F has 1KB | Consistent with §2/§3 in same document |
| 2026-02-20 | Top memory map: I/O regs = $1000-$103F | I/O regs = $1000-$105F (96 bytes) — HC11F extended | Consistent with §7 in same document |
| 2026-02-20 | Bank3 vectors $FFFA/$FFFC/$FFFE shown as `subb` | Corrected to `.word $C015/$C019/$C011` (direct address pointers, not BRA trampolines) | Binary analysis — bank3 last 3 vectors differ from banks 1&2 |
| 2026-02-20 | `_udis.asm` files end at correct address | **TRUNCATED** — bank1_udis ends at $FE2A, bank2_udis at $FE9B, bank3_udis at $FF06 | udis/6811.py NEGA/NEGB length bugs (see §21) |
| 2026-02-20 | udis/6811.py NEGA=3 bytes, NEGB=3 bytes | Fixed to 1 byte each (inherent mode). CLR indexedy opcode 0x187F fixed to 0x186F | udis opcode table audit |
| 2026-02-08 | HC11E9 / 2 MHz E-clock | HC11FC0 / 3.408 MHz | VL400 topic 982, Antus 4539 |
| 2026-01-31 | $017B = crank period | $017B = dwell intermediate | TIC3 ISR disasm |
| 2026-01-31 | 3X crank sensor | 24X crank (15° pulses) | TIC3 ISR disasm |
| 2026-02-07 | $194C hook viable | $3618 = cold-start init only | BNE at $360C |
| 2026-02-09 | 5+ hex digit CPU addrs | HC11 max = $FFFF | Architecture |
| 2026-01-15 | $18156 is free | 97.6% active code | Binary scan |
| 2026-02-12 | $5117-$5248 is free | 14 XDF torque tables | XDF overlap check |
| 2026-02-12 | "37KB total free" | Misleading — cross-bank sum | Bank architecture |

---

## 19. Open Research Questions

1. **Physical chip ID:** No one has photographed the actual die marking on a VY V6 $060A PCM. Is it labeled "68HC11F1" like the VT, or something different?
2. **Package type:** 68-pin PLCC (standard F1) or something else on the IPCM-6 board?
3. **PORTG/PORTF usage:** Binary accesses $1002/$1005 — are these PIOC/PORTCL (E-series) or PORTG/PORTF (F-series)? Runtime test would confirm.
4. **INIT register ($103D):** Reading this at runtime would confirm RAM/register mapping.
5. **External RAM:** Does the VY V6 have any external SRAM beyond the 1KB internal? References to $1B8C/$18E5/$194C suggest possible external RAM in the $1000+ region.
6. **Why was spark cut dropped from v2.09b?** The1's 0x78B2 parameter exists in v2.04c but not v2.09b — suggests the implementation had issues (EST bypass causing DTCs).
7. **The 0x056F4 hook:** What function does this byte control? Disassembly of $56E0-$5710 region needed.
8. **16-bit RPM at $009D:** The1's v2.04c uses `LDD $009D` for 16-bit RPM comparison. How does this relate to `$00A2` (8-bit RPM/25)?

---

## 20. Key Documents Index

| Document | Location | Contents |
|----------|----------|----------|
| HARDWARE_SPECS.md | VY_V6_Assembly_Modding\ | Processor, clock, RAM, corrected specs |
| MEMORY_MAP_VERIFIED.md | VY_V6_Assembly_Modding\ | Address space, bank layout |
| BANK_SWITCHING_AND_ISR_ANALYSIS.md | VY_V6_Assembly_Modding\ | PORTC bit 3, cross-bank rules |
| Rev_Limiter_Analysis_Validated.md | VY_V6_Assembly_Modding\ | 0x77DE fuel cut, RPM scaling |
| TIC3_ISR_ANALYSIS.md | VY_V6_Assembly_Modding\ | 24X crank handler disassembly |
| ENHANCED_V1.0A_RAM_MAP_COMPLETE.md | VY_V6_Assembly_Modding\ | All RAM variable references |
| VY_V6_SPARK_CUT_IMPLEMENTATION_GUIDE.md | VY_V6_Assembly_Modding\ | Dwell method, hook point |
| ENHANCED_v204c_SPARK_CUT_ANALYSIS.md | VY_V6_Assembly_Modding\ | v38 vs The1 comparison, binary diffs |
| FREE_SPACE_ANALYSIS_DEFINITIVE.md | VY_V6_Assembly_Modding\ | Tier 1-3 free space locations |
| M68HC11RM.md | 68HC11_Reference\ | Official Motorola reference manual |
| M68HC11ERG.md | 68HC11_Reference\ | E-series reference guide |
| DARClow.asm / DARChigh.asm | 68HC11_Reference\DARC_*\ | VT SC complete disassembly |
| OSE_11P_V104.md | xdf_exports\ | $11P MEMCAL XDF (spark cut flags) |
| Enhanced_v1.md | VX VY_..._v2.04c\ | v1.1a calibration export |
| TECHEDGE_TOOLS_DECOMPILATION_REFERENCE.md | techedge_decompiled\ | ASM tool chain reference |

---

## 21. Disassembly Tool Errata & Status (2026-02-20)

### Tool Comparison

| Tool | Files | End Address | Vectors? | Status |
|------|-------|:-----------:|:--------:|--------|
| Custom HC11 disassembler | bank{1,2,3}.asm, bank{1,2,3}_labeled.asm | $FFFE | Yes, labeled | **Working** (bank3 vector fix applied) |
| GNU objdump (m68hc11-elf) | bank{1,2,3}_gnu.asm | bank1: $AA40, bank2/3: $FFFE | bank2/3 only | Stops at 0x00-fill gaps; bank1 misses $C468-$FFFF |
| udis (Jeff Tranter) | bank{1,2,3}_udis.asm, bank{1,2,3}_udis_labeled.asm | **TRUNCATED** | No | **3 bugs fixed 2026-02-20** — needs re-disassembly |

### udis/6811.py Bugs Found & Fixed

Three bugs in `VY_V6_Assembly_Modding/68HC11_Reference/udis/6811.py` caused all `_udis.asm` files to be truncated:

| Bug | Was | Fixed To | Impact |
|-----|-----|----------|--------|
| **NEGA (0x40)** length | `[3, "nega", "inherent"]` | `[1, "nega", "inherent"]` | Every `0x40` byte in data consumed 2 extra bytes from file stream |
| **NEGB (0x50)** length | `[3, "negb", "inherent"]` | `[1, "negb", "inherent"]` | Same — 2 extra bytes consumed per occurrence |
| **CLR indexedy** opcode | `0x187f` (wrong) | `0x186f` (correct HC11 opcode) | CLR with Y-indexed addressing would decode wrong bytes |

**Root cause of truncation:** udis reads bytes sequentially from the binary file. When it encounters a `0x40` or `0x50` byte (common in data regions — calibration tables, lookup values), it reads 2 extra operand bytes that don't exist. After hundreds of occurrences across a 64KB file, the file position overshoots by ~470+ bytes, hitting EOF before the address counter reaches $FFFF. This is why:
- bank1_udis.asm ends at **$FE2A** (missing 470 bytes of address space)
- bank2_udis.asm ends at **$FE9B** (missing 357 bytes)
- bank3_udis.asm ends at **$FF06** (missing 250 bytes)

**Fix applied:** `udis/6811.py` corrected. The `_udis.asm` files need to be regenerated to reach $FFFE.

### udis Opcode Coverage vs Full Disassembler

| Metric | udis/6811.py | core/opcodes.py (full) |
|--------|:------------:|:----------------------:|
| Total opcode entries | 308 | 311 |
| Unique mnemonics | 139 | ~145 |
| Prebyte 0x18 entries | ~60 | 64 |
| Prebyte 0x1A entries | ~5 | 7 |
| Prebyte 0xCD entries | ~4 | 4 |
| Duplicate key aliases | 6 (BCC/BHS, BCS/BLO, ASL/LSL × 3, ASLD/LSLD) | Handled separately |

The 3-entry gap is due to Python dict silently overwriting duplicate keys (e.g., BCC and BHS share opcode `0x24` — only the last one wins). This doesn't affect disassembly correctness since the aliases decode identically.

### Bank 3 Vector Table Anomaly

Banks 1 and 2 use **BRA trampolines** (`0x20 xx`) for ALL 32 vector entries at $FFC0-$FFFE. These BRA instructions jump to the pseudo-vector table at $2000-$202F which then JMPs to the actual ISR handler.

Bank 3 uses the same BRA trampoline pattern for vectors $FFC0-$FFF8, but the **last 3 vectors differ**:

| Vector | Bank 1 & 2 | Bank 3 | Meaning |
|--------|:----------:|:------:|---------|
| $FFFA (COP) | `20 24` → BRA $2024 → ∞ loop | `C0 15` → **.word $C015** | Direct pointer to COP handler in bank 3 |
| $FFFC (CMF) | `20 27` → BRA $2027 → ∞ loop | `C0 19` → **.word $C019** | Direct pointer to CMF handler in bank 3 |
| $FFFE (RESET) | `20 2A` → BRA $202A → ∞ loop | `C0 11` → **.word $C011** | Direct pointer to RESET code in bank 3 |

This means bank 3 (trans/diag overlay) has its own **independent boot and watchdog handlers** at $C011/$C015/$C019, bypassing the pseudo-vector table. The disassembler wrongly decoded `C0` as `SUBB #imm` instruction — fixed to `.word` directives in the corrected asm files.

### GNU objdump Limitation (bank1_gnu.asm)

`m68hc11-elf-objdump -D` stops disassembling when it encounters the large 0x00-filled free space at $C468-$FFBF (15,192 bytes of zeros). It treats these as data rather than continuing to the vector table at $FFC0. This is a known limitation of using objdump on flat binary files and is **not fixable** without creating a proper ELF with section headers. The custom disassembler handles this correctly.

### 68HC11 Successor Status (Community Reference)

The 68HC11 is officially **legacy/end-of-life** status. Per community discussion:
- **68HCS12** is the architecturally closest successor (source-compatible, NOT binary-compatible)
- The HCS12 is also nearing obsolescence (many parts listed "not for new designs")
- **STM8** is the closest actively-manufactured architecture to the 6800 family
- For new designs: ARM MCU or FPGA with a soft 6801/6811 core
- The VY V6 PCM uses a **Delco-branded** HC11 die (no Motorola markings visible) per pcmhacking.net forum reports
- R/W signal confirmed present on **memcal header pin 36** (VL400/Antus discovery) — enables NVRAM board without PCB modification
- VX/VY flash PCMs use **Am29F010B** (or M29W800DB/SST39SF010) 128KB NOR flash