# How to Build the Switch

> **Translated from Russian**  
> **Original Document:** Как собрать переключатель.docx  
> Originally written by an unknown author from the Russian BMW tuning community.

The switch supports both 12V and 5V power supply. Choose how you will power it: The 5V is taken directly from the DME. If you are not going to power it from 12V, then you don't need to assemble the voltage converter circuit, i.e., don't solder the 2931 converter, diode, and capacitors.

After assembly, check by powering the switch - when toggling the switch, there should be a logic "1" (i.e., 5V) on the DME wire in one position and a logic "0" (i.e., ground/minus) in the other switch position. Accordingly, the display indication should change from 1 to 2.

> **Note:** The original VK (VKontakte) image links below may no longer work. Refer to the schematic images included in this folder (`Общая схема.png`, `Схема переключателя.jpg`, `Плата.JPG`) instead.

<!-- Original VK image links (likely expired) -->
<!-- ![Switch Image 1](https://pp.userapi.com/c824700/v824700201/eefff/SbHgIj0Sqkc.jpg) -->
<!-- ![Switch Image 2](https://pp.userapi.com/c824700/v824700201/ef007/v37cV4-ccnQ.jpg) -->
<!-- ![Switch Image 3](https://pp.userapi.com/c824700/v824700201/ef019/cX-WKD1WF4g.jpg) -->

## Components Required:
- **ATtiny 2313** microcontroller
- **LED** - any type
- **Resistors** - SMD 510 Ohm
- **Voltage stabilizer circuit** - see schematic images in this folder
- **7-segment display** - with common cathode (common minus)

<!-- Original VK image links (likely expired) -->
<!-- ![Component Image 1](https://pp.userapi.com/c846216/v846216613/25a2c/fQ7JDeW8L9Y.jpg) -->
<!-- ![Component Image 2](https://pp.userapi.com/c834203/v834203613/11088f/JK1ZVmRgcU4.jpg) -->
