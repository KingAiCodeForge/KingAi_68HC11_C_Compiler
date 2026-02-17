# Dual-Mode Switch / Двурежимный переключатель

> **Translated from Russian** — This documentation was originally written by an unknown author from the Russian BMW tuning community. English translations provided for accessibility.

This folder contains documentation and files for building a dual-mode firmware switch for BMW ECUs.

## Document Translations / Перевод документов

| Original (Russian) | English Translation |
|-------------------|---------------------|
| Как собрать переключатель.md | How to Build the Switch (English).md |
| Как создать файл двухрежимной прошивки.md | How to Create a Dual-Mode Firmware File (English).md |
| Мануал двухрежимки BMW для всех ЭБУ.md | Dual-Mode BMW Manual for All ECUs (English).md |
| Прошивки/Разное.txt | Прошивки/Miscellaneous Notes (English).md |

## Folder Name Translations / Названия папок

| Russian | English |
|---------|---------|
| Двурежимная прошивка | Dual-Mode Firmware |
| Прошивки | Firmwares |
| Версия на 2 переключателя (ДВС и КПП) | 2-Switch Version (Engine and Transmission) |
| Файлы для создания переключателя | Files for Building the Switch |

## Main Files / Основные файлы

| Russian | English | Description |
|---------|---------|-------------|
| Общая схема.png | General Schematic | Overall wiring diagram |
| Плата.JPG | PCB Board | Photo of assembled PCB |
| Схема переключателя.jpg | Switch Schematic | Switch circuit diagram |

## Subfolders / Подпапки

### Версия на 2 переключателя (ДВС и КПП) / 2-Switch Version (Engine and Transmission)

| File | English Name | Description |
|------|--------------|-------------|
| 575033967.jpg | Reference Photo | Reference image |
| tuning switch rev2.hex | Tuning Switch Rev 2 | ATtiny microcontroller firmware (revision 2) |
| version2.lay | PCB Layout V2 | Sprint Layout PCB file |

### Файлы для создания переключателя / Files for Building the Switch

| File | English Name | Description |
|------|--------------|-------------|
| Прошивка платы (Аттини).hex | ATtiny Firmware | Microcontroller firmware |
| Чертеж платы.lay | PCB Layout Drawing | Sprint Layout PCB file |

### Прошивки / Firmwares

See `Прошивки/Firmwares Index (English).md` for complete firmware index.

## Summary

This system allows you to switch between two different ECU calibrations (stock and tuned) using a physical toggle switch. The switch connects to the address line of a doubled-capacity flash memory chip, effectively selecting which half of the memory (which firmware) the ECU reads from.

## ECU Support

- **Bosch M1.1, M1.3, M3.1** - M20, M30, M50 engines
- **Bosch M1.7, M3.3** - M40, M42, M43, M50TU, M60 engines  
- **Siemens MS42** - M52TU engines
- **Siemens MS43** - M54 engines
- **Bosch ME7.2** - M62 V8 engines
