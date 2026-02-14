; ============================================
; aldl_hello_world.asm — POC: Transmit "HELLO" over ALDL (SCI serial)
; ============================================
;
; PURPOSE:
;   Proof-of-concept that custom code can run on the HC11 and produce
;   observable output via the ALDL diagnostic port. This is the simplest
;   possible "does my code actually execute?" test.
;
; WHAT IT DOES:
;   1. Configures the SCI (Serial Communication Interface) for TX
;   2. Sends ASCII "HELLO\r\n" out the ALDL pin at 8192 baud
;   3. Loops forever (can be extended to repeat or wait for input)
;
; HOW TO USE:
;   1. Assemble:  python hc11kit.py asm examples/aldl_hello_world.asm -o hello.bin
;   2. Patch:     python hc11kit.py patch stock.bin hello.bin --at <free_space_addr>
;   3. Connect:   ALDL cable (USB-serial + level shifter) to OBD port pin 9
;   4. Terminal:  8192 baud, 8N1 — should see "HELLO" appear
;
; HARDWARE:
;   VY V6 Delco PCM (09356445) — HC11F1, 8 MHz crystal, 2 MHz E-clock
;   ALDL pin = SCI TX ($102F) at CMOS 12V levels
;   ALDL cable: USB-to-serial + MAX232 or FTDI 3.3V→12V level shifter
;
; SCI REGISTERS:
;   $102B = BAUD  — baud rate (SCP1:SCP0 prescaler, SCR2:1:0 divider)
;   $102C = SCCR1 — control 1 (word length, wake mode) — leave default
;   $102D = SCCR2 — control 2 (TE=bit3, RE=bit2 enable TX/RX)
;   $102E = SCSR  — status (TDRE=bit7 = TX buffer empty)
;   $102F = SCDR  — data register (write = transmit, read = receive)
;
; BAUD RATE:
;   8192 baud is the standard ALDL rate for all VN-VZ Holden Delco PCMs.
;   The Delco PCM may use a custom crystal frequency to hit 8192 exactly.
;   On a standard 8 MHz crystal (2 MHz E-clock):
;     2,000,000 / (16 * prescaler * divider) = 8192
;     → No exact match with standard HC11 BAUD register values.
;   The stock OS initialises BAUD during startup — if this code runs as
;   a patch (JSR hook), BAUD is already configured. If running standalone
;   in RAM, you may need to set it manually.
;
;   Common BAUD values to try:
;     $30 = prescaler ÷1, divider ÷16   → 7812.5 baud (close but ~5% off)
;     $31 = prescaler ÷1, divider ÷32   → 3906.25 baud
;     $32 = prescaler ÷1, divider ÷64   → 1953.13 baud
;     $33 = prescaler ÷1, divider ÷128  → 976.56 baud
;     The exact setting depends on the actual crystal. If the stock OS
;     already set BAUD, skip the BAUD init and use whatever is configured.
;
; SIZE: ~30 bytes code + 8 bytes string = ~38 bytes total
;
; NOTE ON SAFETY:
;   This code does NOT touch engine control — no spark, fuel, timing.
;   It only writes to the SCI transmit register. Safe to run on a bench
;   PCM with key-on engine-off (KOEO). Does not affect normal operation
;   if patched as a one-shot call during init.
;
; ============================================

; -- SCI Register Equates --
BAUD    EQU     $102B           ; Baud rate register
SCCR1   EQU     $102C           ; SCI control register 1
SCCR2   EQU     $102D           ; SCI control register 2
SCSR    EQU     $102E           ; SCI status register
SCDR    EQU     $102F           ; SCI data register

; Bit masks
TDRE    EQU     $80             ; Transmit Data Register Empty (SCSR bit 7)
TE      EQU     $08             ; Transmitter Enable (SCCR2 bit 3)
RE      EQU     $04             ; Receiver Enable (SCCR2 bit 2)

        ORG     $5D00           ; Place in known free space (adjust per binary)

; ============================================
; ENTRY: Called via JSR from hook point
; ============================================
HELLO_WORLD:
        ; -- Enable SCI transmitter --
        ; If running as a patch, the stock OS already has SCI configured
        ; for ALDL receive. We just need to make sure TX is enabled too.
        LDAA    SCCR2           ; Read current SCCR2
        ORAA    #TE             ; Set TE bit (enable transmitter)
        STAA    SCCR2           ; Write back

        ; -- Send the string --
        LDX     #MSG            ; X = pointer to message string

TX_LOOP:
        LDAA    0,X             ; Load next character
        BEQ     TX_DONE         ; If null terminator, we're done

TX_WAIT:
        LDAB    SCSR            ; Read SCI status
        ANDB    #TDRE           ; Check TDRE (bit 7)
        BEQ     TX_WAIT         ; Spin until TX buffer is empty

        STAA    SCDR            ; Transmit the character
        INX                     ; Advance to next character
        BRA     TX_LOOP         ; Loop

TX_DONE:
        RTS                     ; Return to caller (stock OS continues)

; -- Message Data --
MSG:    FCC     "HELLO"
        FCB     $0D,$0A         ; Carriage return + line feed
        FCB     $00             ; Null terminator

        END
