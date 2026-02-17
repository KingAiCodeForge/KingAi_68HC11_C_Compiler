# Examples — HC11 C Compiler Test Programs

Example C source files for the KingAI 68HC11 C Compiler. These demonstrate the compiler's capabilities and serve as test inputs for the `hc11cc` → `hc11kit` pipeline.

> **Status:** Templates and toolchain tests — not validated on real hardware.
> If a foundational issue exists in the compiler, it will affect all examples.

## Files

| File | Description |
|------|-------------|
| `delco_hc11.h` | HC11F1 register definitions + VY V6 RAM addresses (shared header) |
| `blink.c` | Toggle an I/O port pin in a loop — simplest hardware test |
| `adc_read.c` | Read ADC channel and store result |
| `sci_serial.c` | SCI serial TX — send bytes over ALDL |
| `timer_delay.c` | Timer-based delay using output compare |
| `isr_example.c` | Interrupt service routine with `__attribute__((interrupt))` |
| `rpm_limiter.c` | RPM threshold check — spark cut logic |
| `test_rpm.c` | RPM comparison test case |
| `fan_control.c` | Thermo fan relay control via PORTB |
| `eeprom_write.c` | Internal EEPROM write sequence |
| `pulse_counter.c` | Count input capture events |
| `spi_transfer.c` | SPI byte transfer |
| `mode4_responder.c` | ALDL Mode 4 command handler |
| `aldl_hello.c` | Send "HELLO" over ALDL SCI |
| `aldl_hello_world.asm` | Hand-written ASM version of the hello world test |
| `aldl_chatter_disable.c` | Disable BCM/PCM chatter on ALDL bus |
| `aldl_flash_erase_sector.c` | Flash sector erase command |
| `aldl_flash_read_sector.c` | Flash sector read |
| `aldl_flash_unlock.c` | Security unlock sequence |
| `aldl_flash_write_block.c` | Flash block write command |
| `aldl_report_rpm.c` | Read and report RPM over ALDL |

## Usage

```bash
# Compile a single example to assembly
python hc11cc.py examples/blink.c --target vy_v6

# Compile to binary
python hc11kit.py compile examples/rpm_limiter.c -o rpm_limiter.bin --target vy_v6

# Run all examples through the compiler (test script)
pytest tests/ -v -k examples
```

## Notes

- All examples use `delco_hc11.h` for register and RAM address definitions
- The ALDL-prefixed examples target the serial communication subsystem
- Examples are designed to be small, single-purpose routines suitable for code injection into free ROM space