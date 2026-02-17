# Dual-Mode BMW Manual for All ECUs

> **Translated from Russian**  
> **Original Document:** Мануал двухрежимки BMW для всех ЭБУ.pdf  
> Originally written by an unknown author from the Russian BMW tuning community.

## Connection to DME BOSCH M1.1, M1.3, M3.1
**Engines: M20, M30, M50**

These ECUs use the 27C256 memory chip. To flash the dual-mode firmware, simply replace it with a chip of twice the capacity - W27C512. The chips are completely identical in the number of pins and pinout.

## General Manual for ECU Connection

The principle is replacing the flash with one of twice the capacity. Switching works on all ECUs that use external flash for firmware storage - whether transmission or engine ECUs, and not only on BMW but on any car. If your ECU is not in this manual, take a photo of the board - if there's a flash chip, this system can be implemented without problems.

## Important Notes:

- **Pin soldering:** The pin to which we solder the DME wire from the switch should remain in the air (not soldered to the board). The chip leg breaks off easily - I killed several flash chips this way during experiments. Be careful!

- **For 28 and 29 series flash chips:** It's advisable to buy or make an adapter as shown in the photo, since they are soldered in. Constant desoldering and soldering while you're perfecting the firmware will be destructive to the ECU board. With frequent desoldering/soldering, the pads for soldering the legs fall off, and constant heating with a hot air gun deforms and damages the board.

- **Flash compatibility:** A 28 series flash can be replaced with a 29 series, but NOT vice versa.

- **EWS/ISN considerations:** On ECUs with EWS, you will need to correct the ISN if you're building firmware with different base software versions. If you're keeping your own base software and only changing calibrations, you don't need to edit the ISN - it's not stored in the calibrations, except for MS41, but there EWS can be disabled via software.

**Mode switch wire connects to pin A15 (pin 1).**

---

## Connection to DME BOSCH M1.7, M3.3
**Engines: M40, M42, M43, M50TU, M60**

These DMEs use the W27C512 chip. This chip is replaced with one of twice the memory - W27C010. This chip has 4 more pins than the original, so we install it with an offset - the first four pins of the chip don't go into the socket and hang in the air. You need to connect the VCC power pin of the chip to the NC pin that falls into the socket at the VCC pin position.

**Mode switch wire connects to pin A16 (pin 2).**
