; =============================================================================
; flash_erase_write_kernel.asm — M29W800DB Flash Erase/Write Kernel
; =============================================================================
; Target: Delco 09356445 (VY V6 L36) - HC11F1 + M29W800DB flash
; Load:   $0300 (PCM RAM, uploaded via Mode 6)
; Purpose: Erase a flash sector and write new data, communicating
;          status back over ALDL (SCI TX).
;
; Flash: STMicroelectronics M29W800DB (8Mbit, bottom boot, TSOP48)
;        Organized as: 1x16KB + 2x8KB + 1x32KB + 7x64KB
;        VY V6 uses 128KB (0x0000-0x1FFFF) across 3 banks
;
; M29W800DB Command Sequences (from datasheet):
;   CHIP ERASE:
;     Write 0xAA to 0x555, Write 0x55 to 0x2AA, Write 0x80 to 0x555
;     Write 0xAA to 0x555, Write 0x55 to 0x2AA, Write 0x10 to 0x555
;
;   SECTOR ERASE:
;     Write 0xAA to 0x555, Write 0x55 to 0x2AA, Write 0x80 to 0x555
;     Write 0xAA to 0x555, Write 0x55 to 0x2AA, Write 0x30 to sector_addr
;
;   BYTE PROGRAM:
;     Write 0xAA to 0x555, Write 0x55 to 0x2AA, Write 0xA0 to 0x555
;     Write data to target_address
;     Poll DQ7 for completion (toggle polling)
;
;   DQ7 POLLING:
;     Read address — if DQ7 matches data DQ7, operation complete
;     If DQ5 = 1 (timeout), read again — if still wrong, error
;
; Communication Protocol (kernel ↔ host tool):
;   Kernel sends status bytes over ALDL SCI:
;     0xAA = Ready / OK
;     0x55 = Error
;     0x01 = Erase started
;     0x02 = Erase complete
;     0x03 = Write started
;     0x04 = Write complete (per block)
;     0x05 = Verify started
;     0x06 = Verify complete / all done
;     0xFE = Waiting for data
;     0xFF = Checksum error
;
;   Host sends commands to kernel:
;     [CMD] [ADDR_HI] [ADDR_LO] [LEN] [DATA...] [CHECKSUM]
;     CMD 0x01 = Erase sector at ADDR
;     CMD 0x02 = Write LEN bytes at ADDR from DATA
;     CMD 0x03 = Verify LEN bytes at ADDR
;     CMD 0xFF = Reset/exit kernel
;
; Credits: OSE Flash Tool protocol, pcmhacking.net community
; Author:  KingAustraliaGG
; Date:    2026-02-15
;
; SIZE: ~200 bytes estimated
; =============================================================================

; -- Register Equates (HC11F1) --
PORTA   EQU     $1000           ; Port A
PORTB   EQU     $1004           ; Port B (relay outputs)
SCCR2   EQU     $102D           ; SCI control register 2
SCSR    EQU     $102E           ; SCI status register
SCDR    EQU     $102F           ; SCI data register
COPRST  EQU     $103A           ; COP watchdog reset

; SCI bits
TDRE    EQU     $80             ; TX Data Register Empty
RDRF    EQU     $20             ; RX Data Register Full
TE      EQU     $08             ; TX Enable
RE      EQU     $04             ; RX Enable

; Flash command addresses (relative to flash base)
; For M29W800DB in Word mode (which most HC11 designs use)
FLASH_CMD1  EQU $0555           ; Command address 1
FLASH_CMD2  EQU $02AA           ; Command address 2

; Status codes (sent back to host over ALDL)
STS_READY       EQU $AA
STS_ERROR       EQU $55
STS_ERASE_START EQU $01
STS_ERASE_DONE  EQU $02
STS_WRITE_START EQU $03
STS_WRITE_DONE  EQU $04
STS_VERIFY_START EQU $05
STS_ALL_DONE    EQU $06
STS_WAIT_DATA   EQU $FE
STS_CK_ERROR    EQU $FF

; Host commands
CMD_ERASE       EQU $01
CMD_WRITE       EQU $02
CMD_VERIFY      EQU $03
CMD_EXIT        EQU $FF

; COP feed values
COP_55  EQU     $55
COP_AA  EQU     $AA

        ORG     $0300           ; RAM load address

; =============================================================================
; Entry Point — send READY, then wait for commands
; =============================================================================
KERNEL_START:
        ; Enable SCI TX + RX
        LDAA    #(TE|RE)        ; Enable both TX and RX
        STAA    SCCR2

        ; Send READY status
        LDAA    #STS_READY
        BSR     SCI_TX

; =============================================================================
; Main Command Loop
; =============================================================================
CMD_LOOP:
        ; Feed COP watchdog (MUST do this or CPU resets!)
        LDAA    #COP_55
        STAA    COPRST
        LDAA    #COP_AA
        STAA    COPRST

        ; Wait for command byte from host
        BSR     SCI_RX          ; Returns byte in A
        TAB                     ; Save command in B

        ; Dispatch command
        CMPB    #CMD_ERASE
        BEQ     DO_ERASE

        CMPB    #CMD_WRITE
        BEQ     DO_WRITE

        CMPB    #CMD_VERIFY
        BEQ     DO_VERIFY

        CMPB    #CMD_EXIT
        BEQ     DO_EXIT

        ; Unknown command — send error, loop
        LDAA    #STS_ERROR
        BSR     SCI_TX
        BRA     CMD_LOOP

; =============================================================================
; ERASE SECTOR — CMD_ERASE [ADDR_HI] [ADDR_LO]
; Erases the flash sector containing the given address.
; =============================================================================
DO_ERASE:
        ; Receive target address
        BSR     SCI_RX          ; ADDR_HI → A
        TAB                     ; Save in B
        BSR     SCI_RX          ; ADDR_LO → A
        XGDX                   ; D → X (address now in X)

        ; Send erase started status
        LDAA    #STS_ERASE_START
        BSR     SCI_TX

        ; --- M29W800DB Sector Erase Sequence ---
        LDAA    #$AA
        STAA    FLASH_CMD1      ; Write $AA to $0555
        LDAA    #$55
        STAA    FLASH_CMD2      ; Write $55 to $02AA
        LDAA    #$80
        STAA    FLASH_CMD1      ; Write $80 to $0555
        LDAA    #$AA
        STAA    FLASH_CMD1      ; Write $AA to $0555
        LDAA    #$55
        STAA    FLASH_CMD2      ; Write $55 to $02AA
        LDAA    #$30
        STAA    0,X             ; Write $30 to sector address → ERASE!

        ; --- Poll for erase completion (DQ7 polling) ---
        ; During erase, DQ7 outputs complement of final data
        ; When done, DQ7 = 1 (erased byte = $FF, DQ7 of $FF = 1)
ERASE_POLL:
        ; Feed COP while waiting
        PSHA
        LDAA    #COP_55
        STAA    COPRST
        LDAA    #COP_AA
        STAA    COPRST
        PULA

        LDAA    0,X             ; Read flash status
        BITA    #$80            ; Test DQ7
        BNE     ERASE_OK        ; DQ7=1 means erase complete
        BITA    #$20            ; Test DQ5 (timeout flag)
        BEQ     ERASE_POLL      ; DQ5=0, keep polling
        ; DQ5=1, check DQ7 one more time
        LDAA    0,X
        BITA    #$80
        BNE     ERASE_OK
        ; Erase failed!
        LDAA    #STS_ERROR
        BSR     SCI_TX
        BRA     CMD_LOOP

ERASE_OK:
        LDAA    #STS_ERASE_DONE
        BSR     SCI_TX
        BRA     CMD_LOOP

; =============================================================================
; WRITE DATA — CMD_WRITE [ADDR_HI] [ADDR_LO] [LEN] [DATA...] [CHECKSUM]
; Programs LEN bytes starting at ADDR.
; =============================================================================
DO_WRITE:
        ; Receive address
        BSR     SCI_RX          ; ADDR_HI
        TAB
        BSR     SCI_RX          ; ADDR_LO
        XGDX                   ; Address in X

        ; Receive byte count
        BSR     SCI_RX          ; LEN → A
        STAA    $00F0           ; Store count in RAM temp

        ; Send write started
        PSHA
        LDAA    #STS_WRITE_START
        BSR     SCI_TX
        PULA

        ; Receive and program each byte
WRITE_LOOP:
        ; Feed COP
        PSHA
        LDAA    #COP_55
        STAA    COPRST
        LDAA    #COP_AA
        STAA    COPRST
        PULA

        BSR     SCI_RX          ; Get data byte → A
        TAB                     ; Save data in B

        ; --- M29W800DB Byte Program Sequence ---
        LDAA    #$AA
        STAA    FLASH_CMD1      ; $AA → $0555
        LDAA    #$55
        STAA    FLASH_CMD2      ; $55 → $02AA
        LDAA    #$A0
        STAA    FLASH_CMD1      ; $A0 → $0555 (program command)
        TBA                     ; Restore data byte
        STAA    0,X             ; Write data to target address

        ; Poll DQ7 for program completion
PROG_POLL:
        LDAA    0,X             ; Read status
        EORA    0,X             ; Toggle detection (two reads)
        BITA    #$40            ; Test DQ6 toggle
        BNE     PROG_POLL       ; Still toggling = not done
        ; Programming complete for this byte

        INX                     ; Next address
        DEC     $00F0           ; Decrement count
        BNE     WRITE_LOOP      ; More bytes to write

        ; All bytes written
        LDAA    #STS_WRITE_DONE
        BSR     SCI_TX
        BRA     CMD_LOOP

; =============================================================================
; VERIFY DATA — CMD_VERIFY [ADDR_HI] [ADDR_LO] [LEN]
; Reads LEN bytes from ADDR and sends them back over ALDL for host to verify.
; =============================================================================
DO_VERIFY:
        BSR     SCI_RX          ; ADDR_HI
        TAB
        BSR     SCI_RX          ; ADDR_LO
        XGDX                   ; Address in X

        BSR     SCI_RX          ; LEN → A
        STAA    $00F0           ; Store count

        LDAA    #STS_VERIFY_START
        BSR     SCI_TX

VERIFY_LOOP:
        LDAA    0,X             ; Read flash byte
        BSR     SCI_TX          ; Send to host
        INX                     ; Next address
        DEC     $00F0
        BNE     VERIFY_LOOP

        LDAA    #STS_ALL_DONE
        BSR     SCI_TX
        BRA     CMD_LOOP

; =============================================================================
; EXIT — Return control to stock OS (or just loop forever)
; =============================================================================
DO_EXIT:
        LDAA    #STS_READY
        BSR     SCI_TX
        ; Could JMP to reset vector, but safer to just loop
HANG:
        LDAA    #COP_55
        STAA    COPRST
        LDAA    #COP_AA
        STAA    COPRST
        BRA     HANG

; =============================================================================
; SCI Subroutines — Blocking TX/RX
; =============================================================================

; SCI_TX: Transmit byte in A over ALDL
;   Waits for TDRE, then writes to SCDR
SCI_TX:
        PSHB                    ; Preserve B
        TAB                     ; Save byte in B
SCI_TX_WAIT:
        LDAA    SCSR            ; Read status
        BITA    #TDRE           ; TX buffer empty?
        BEQ     SCI_TX_WAIT
        TBA                     ; Restore byte
        STAA    SCDR            ; Transmit
        PULB                    ; Restore B
        RTS

; SCI_RX: Receive byte from ALDL into A
;   Waits for RDRF, then reads SCDR
;   Also feeds COP watchdog while waiting
SCI_RX:
SCI_RX_WAIT:
        ; Feed COP to prevent reset during long waits
        PSHA
        LDAA    #COP_55
        STAA    COPRST
        LDAA    #COP_AA
        STAA    COPRST
        PULA

        LDAA    SCSR            ; Read status
        BITA    #RDRF           ; RX data ready?
        BEQ     SCI_RX_WAIT
        LDAA    SCDR            ; Read received byte
        RTS

; =============================================================================
; End of kernel
; =============================================================================

; Hand-assembled size estimate: ~200-250 bytes
; Well within the 1KB RAM available on HC11F1
; Load address $0300 leaves $0000-$02FF for stack and variables
