; =============================================================================
; MINIMAL WATCHDOG KERNEL - Milestone 1
; =============================================================================
; Target: Delco 09356445 (VY V6 L36) - HC11F1
; Purpose: Proves custom code is RUNNING on the PCM
;
; Success criteria: PCM doesn't reset after upload. It "hangs" but stays alive.
;                   That means your code is executing.
;
; Credit: Protocol from OSE Flash Tool (VL400, pcmhacking.net)
;
; Size: ~30 bytes
; Load address: $0300 (RAM - this is where OSE uploads to)
;
; HC11F1 register map:
;   $103A = COPRST  (COP watchdog reset register)
;   $1000 = PORTA   (Port A - indicator)
;
; To feed COP watchdog on HC11:
;   Write $55 to COPRST, then write $AA to COPRST
;   Must be done within COP timeout period or CPU resets
; =============================================================================

        ORG     $0300           ; RAM load address (OSE uploads kernel here)

; =============================================================================
; Entry point - jumped to by Mode 6 upload executor
; =============================================================================
START:
        ; --- Feed the COP watchdog ---
        LDAA    #$55
        STAA    $103A           ; COPRST <- $55
        LDAA    #$AA
        STAA    $103A           ; COPRST <- $AA

        ; --- Toggle Port A bit 0 as a sign of life (optional) ---
        ; LDAA    $1000         ; Read PORTA
        ; EORA    #$01          ; Toggle bit 0
        ; STAA    $1000         ; Write PORTA

        ; --- Small delay loop ---
        LDX     #$FFFF          ; 65535 iterations
DELAY:  DEX
        BNE     DELAY

        ; --- Loop forever ---
        BRA     START

; =============================================================================
; Expected assembled bytes (hand-assembled):
;
; $0300: 86 55       LDAA #$55
; $0302: B7 10 3A    STAA $103A
; $0305: 86 AA       LDAA #$AA
; $0307: B7 10 3A    STAA $103A
; $030A: CE FF FF    LDX  #$FFFF
; $030D: 09          DEX
; $030E: 26 FD       BNE  DELAY ($030D)
; $0310: 20 EE       BRA  START ($0300)
;
; Total: 18 bytes ($0300-$0311)
;
; Raw bytes: 86 55 B7 10 3A 86 AA B7 10 3A CE FF FF 09 26 FD 20 EE
; =============================================================================
