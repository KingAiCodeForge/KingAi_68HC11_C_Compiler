# How to Create a Dual-Mode Firmware File

> **Translated from Russian**  
> **Original Document:** Как создать файл двухрежимной прошивки.docx  
> Originally written by an unknown author from the Russian BMW tuning community.

So, how to create a dual-mode firmware - it's quite simple.

## Option 1: Combining Two Different Full Dumps

Combine two different full dumps (your stock and tuned version). For this, use the ALMI program (link will be at the bottom), or manually in a HEX editor add one firmware to the end of the other and save. The size of the combined firmware should be exactly twice as large.

**Note:** With this option, switching while driving may not always work correctly - the engine may stall because the base software is different.

**Also**, with this option, if there is EWS (Electronic Immobilizer), you will need to write the original ISN into the tuned dump, since the base software is different and the ISN is stored in the base software. The exception is MS41 where the ISN is in the calibrations, but there it can be disabled either programmatically or manually by entering FF in the ISN area.

## Option 2: Calibration Swap (Recommended)

Take your original full dump, remove the calibrations from it, and insert the tuned calibrations in their place, then save the resulting firmware. Don't forget to verify the checksum using a checksum correction tool appropriate for your ECU platform.

Essentially, we manually did what MPPS, KESS, etc. do through the OBD port. Now, just like in option 1, combine the resulting firmware with the stock using the program or manually.

**With this option**, switching while driving is possible without problems because the base software is the same — only the calibrations are different.

**Also**, the ISN remains intact since we're not changing the base software.
