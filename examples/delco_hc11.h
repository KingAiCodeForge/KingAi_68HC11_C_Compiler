/**
 * delco_hc11.h — Delco 68HC11 PCM Register Definitions
 * ═══════════════════════════════════════════════════════
 *
 * Register map for 68HC11F1/E9 variants used in Delco automotive ECUs.
 * Compatible with: 09356445 (VY V6), and similar.
 *
 * Reference: Motorola MC68HC11F1 Technical Data (MC68HC11F1/D)
 *
 * Usage with hc11cc:
 *   The compiler's preprocessor resolves #define macros, so these
 *   register addresses can be used directly in expressions:
 *     PORTA |= 0x01;
 *     *(volatile unsigned char *)0x1000 = 0x55;
 *
 * KingAI — 68HC11 C Compiler for Delco PCMs
 */

#ifndef DELCO_HC11_H
#define DELCO_HC11_H

/* ── Register Base ─────────────────────────── */
#define REG_BASE    0x1000

/* ── I/O Ports ─────────────────────────────── */
#define PORTA       0x1000      /* Port A Data Register          */
#define DDRA        0x1001      /* Port A Data Direction          */
#define PIOC        0x1002      /* Parallel I/O Control           */
#define PORTC       0x1003      /* Port C Data (active on F1)     */
#define PORTB       0x1004      /* Port B Data Register           */
#define PORTCL      0x1005      /* Port C Latched                 */
#define DDRC        0x1007      /* Port C Data Direction          */
#define PORTD       0x1008      /* Port D Data Register           */
#define DDRD        0x1009      /* Port D Data Direction          */
#define PORTE       0x100A      /* Port E Data (ADC inputs)       */

/* ── Timer System ──────────────────────────── */
#define TCNT_H      0x100E      /* Free-Running Counter (high)    */
#define TCNT_L      0x100F      /* Free-Running Counter (low)     */
#define TIC1_H      0x1010      /* Input Capture 1 (high)         */
#define TIC1_L      0x1011      /* Input Capture 1 (low)          */
#define TIC2_H      0x1012      /* Input Capture 2 (high)         */
#define TIC2_L      0x1013      /* Input Capture 2 (low)          */
#define TIC3_H      0x1014      /* Input Capture 3 (high)         */
#define TIC3_L      0x1015      /* Input Capture 3 (low)          */
#define TOC1_H      0x1016      /* Output Compare 1 (high)        */
#define TOC1_L      0x1017      /* Output Compare 1 (low)         */
#define TOC2_H      0x1018      /* Output Compare 2 (high)        */
#define TOC2_L      0x1019      /* Output Compare 2 (low)         */
#define TOC3_H      0x101A      /* Output Compare 3 (high)        */
#define TOC3_L      0x101B      /* Output Compare 3 (low)         */
#define TOC4_H      0x101C      /* Output Compare 4 (high)        */
#define TOC4_L      0x101D      /* Output Compare 4 (low)         */
#define TIC4_H      0x101E      /* IC4/OC5 (high)                 */
#define TIC4_L      0x101F      /* IC4/OC5 (low)                  */
#define TCTL1       0x1020      /* Timer Control 1                */
#define TCTL2       0x1021      /* Timer Control 2                */
#define TMSK1       0x1022      /* Timer Interrupt Mask 1         */
#define TFLG1       0x1023      /* Timer Interrupt Flag 1         */
#define TMSK2       0x1024      /* Timer Interrupt Mask 2         */
#define TFLG2       0x1025      /* Timer Interrupt Flag 2         */
#define PACTL       0x1026      /* Pulse Accumulator Control      */
#define PACNT       0x1027      /* Pulse Accumulator Count        */

/* ── SPI System ────────────────────────────── */
#define SPCR        0x1028      /* SPI Control Register           */
#define SPSR        0x1029      /* SPI Status Register            */
#define SPDR        0x102A      /* SPI Data Register              */

/* ── SCI (Serial) System ──────────────────── */
#define BAUD        0x102B      /* Baud Rate Register             */
#define SCCR1       0x102C      /* SCI Control 1                  */
#define SCCR2       0x102D      /* SCI Control 2                  */
#define SCSR        0x102E      /* SCI Status Register            */
#define SCDR        0x102F      /* SCI Data Register              */

/* ── ADC System ────────────────────────────── */
#define ADCTL       0x1030      /* A/D Control Register           */
#define ADR1        0x1031      /* A/D Result 1                   */
#define ADR2        0x1032      /* A/D Result 2                   */
#define ADR3        0x1033      /* A/D Result 3                   */
#define ADR4        0x1034      /* A/D Result 4                   */

/* ── System Configuration ──────────────────── */
#define OPTION      0x1039      /* System Configuration Options   */
#define COPRST      0x103A      /* COP Reset Register             */
#define PPROG       0x103B      /* EEPROM Programming Register    */
#define HPRIO       0x103C      /* Highest Priority I-Bit Int     */
#define INIT        0x103D      /* RAM/IO Mapping Register        */
#define TEST1       0x103E      /* Factory Test Register          */
#define CONFIG      0x103F      /* Configuration Register         */

/* ── HC11F1 Extended Registers ─────────────── */
#define CSSTRH      0x105C      /* Chip Select Clock Stretch      */
#define CSCTL       0x105D      /* Chip Select Control            */
#define CSGADR      0x105E      /* General CS Address Register    */
#define CSGSIZ      0x105F      /* General CS Size Register       */

/* ── Bit Masks ─────────────────────────────── */

/* ADCTL bits */
#define ADCTL_CCF   0x80        /* Conversion Complete Flag        */
#define ADCTL_SCAN  0x20        /* Continuous Scan                 */
#define ADCTL_MULT  0x10        /* Multiple Channel                */
#define ADCTL_CD    0x08        /* Channel Select D                */
#define ADCTL_CC    0x04        /* Channel Select C                */
#define ADCTL_CB    0x02        /* Channel Select B                */
#define ADCTL_CA    0x01        /* Channel Select A                */

/* TFLG1 bits (timer interrupt flags) */
#define TFLG1_OC1F  0x80       /* OC1 Flag                        */
#define TFLG1_OC2F  0x40       /* OC2 Flag                        */
#define TFLG1_OC3F  0x20       /* OC3 Flag                        */
#define TFLG1_OC4F  0x10       /* OC4 Flag                        */
#define TFLG1_IC4F  0x08       /* IC4/OC5 Flag                    */
#define TFLG1_IC1F  0x04       /* IC1 Flag                        */
#define TFLG1_IC2F  0x02       /* IC2 Flag                        */
#define TFLG1_IC3F  0x01       /* IC3 Flag                        */

/* TMSK1 bits (timer interrupt enables) */
#define TMSK1_OC1I  0x80       /* OC1 Interrupt Enable            */
#define TMSK1_OC2I  0x40       /* OC2 Interrupt Enable            */
#define TMSK1_OC3I  0x20       /* OC3 Interrupt Enable            */
#define TMSK1_OC4I  0x10       /* OC4 Interrupt Enable            */
#define TMSK1_IC4I  0x08       /* IC4/OC5 Interrupt Enable        */
#define TMSK1_IC1I  0x04       /* IC1 Interrupt Enable            */
#define TMSK1_IC2I  0x02       /* IC2 Interrupt Enable            */
#define TMSK1_IC3I  0x01       /* IC3 Interrupt Enable            */

/* ── VY V6 PCM Specifics (09356445) ────────── */
/* Bank switching: PORTC bit 3 controls A16 address line
 * VY_BANK_PORT is the direct-page offset of PORTC ($1003).
 * Value 0x03 works because HC11 BSET/BCLR use direct-page
 * addressing and the I/O registers start at $1000 (INIT=$10).
 * Full address: $1003. Direct-page offset: $03. */
#define VY_BANK_PORT    0x03   /* PORTC direct-page offset ($1003)*/
#define VY_BANK_PORT_EXT 0x1003 /* PORTC full extended address     */
#define VY_BANK_BIT     0x08   /* Bit 3 mask (A16 address line)   */
/* BCLR VY_BANK_PORT,#VY_BANK_BIT  = select Bank 2 (engine code)  */
/* BSET VY_BANK_PORT,#VY_BANK_BIT  = select Bank 3 (trans/diag)   */

/* Known VY V6 RAM locations (verified against XDF v2.09b defs) */
#define VY_RPM          0x00A2  /* Engine RPM (x25 scaling, 8-bit) */
#define VY_DWELL_CALC   0x017B  /* Dwell intermediate calculation  */
#define VY_MODE_BYTE    0x0046  /* Mode byte (bits 3,6,7 free)    */

/* WARNING: VY_CRANK_PERIOD was previously listed as 0x194C but that
 * is a FILE OFFSET in bank 3 (0x18000+0x194C-0x8000), NOT a RAM address.
 * The actual RAM address for the 24X crank period captured by the TIC3
 * ISR needs verification on-hardware. Commenting out until confirmed.
 * #define VY_CRANK_PERIOD 0x???  -- needs hardware verification */
/* Ref: 3X_PERIOD_ANALYSIS_COMPLETE.md, VY_V6_Assembly_Modding docs */

/* ── Common Delco PCM Models ──────────────── */
/* 1227165: 1986-89 V8 TPI, 27C128 (16KB) at $C000-$FFFF */
/* 1227730: 1990-92 V8 TPI / V6 PFI, 27C256 (32KB) at $8000-$FFFF */
/* 16197427: 1994-95 trucks, 27C512 (64KB) bank-switched */
/* 09356445: VY Commodore V6 3.8L Ecotec, AM29F010 (128KB) bank-switched */

#endif /* DELCO_HC11_H */
