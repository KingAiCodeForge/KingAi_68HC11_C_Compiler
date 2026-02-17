# BMW Dual-Mode Switch - Downloads Inventory

**Archive Path:** `FULL_ARCHIVE_V2/downloads/BMW/Dualmode_Switch/`  
**Source Path:** `Dualmode Switch/Двурежимная прошивка/`  
**Inventory Date:** January 22, 2026  
**Origin:** Unknown — sourced from Russian-speaking BMW tuning community (VK / forums)

---

## 📁 Directory Structure for Archive Integration

```
downloads/BMW/Dualmode_Switch/
│
├── README.md                           # This inventory file
│
├── hardware/
│   ├── firmware/
│   │   ├── attiny_firmware_v1.hex      # From: Прошивка платы (Аттини).hex
│   │   └── attiny_firmware_v2.hex      # From: tuning switch rev2.hex
│   │
│   ├── pcb_layouts/
│   │   ├── pcb_layout_v1.lay           # From: Чертеж платы.lay
│   │   └── pcb_layout_v2.lay           # From: version2.lay
│   │
│   └── schematics/
│       ├── general_schematic.png       # From: Общая схема.png
│       ├── switch_schematic.jpg        # From: Схема переключателя.jpg
│       └── pcb_photo.jpg               # From: Плата.JPG
│
├── documentation/
│   ├── BMW_Dual_Mode_Manual.pdf        # From: Мануал двухрежимки BMW для всех ЭБУ.pdf
│   ├── How_to_Build_Switch.docx        # From: Как собрать переключатель.docx
│   └── How_to_Create_Firmware.docx     # From: Как создать файл двухрежимной прошивки.docx
│
├── tools/
│   ├── MiniPro.exe                     # EPROM programmer software
│   └── MiniProHelp.chm                 # Help file
│
└── firmwares/
    ├── Bosch_M60_V8/
    ├── Bosch_Motronic_1.3/
    ├── Siemens_MS42/
    ├── Siemens_MS43/
    └── Bosch_ME7.2/
```

---

## 📦 Complete File Inventory

### Hardware Files

| Original Path (Russian) | Archive Path (English) | Size | Type |
|-------------------------|------------------------|------|------|
| `Файлы для создания переключателя/Прошивка платы (Аттини).hex` | `hardware/firmware/attiny_firmware_v1.hex` | 390 B | Intel HEX |
| `Версия на 2 переключателя (ДВС и КПП)/tuning switch rev2.hex` | `hardware/firmware/attiny_firmware_v2.hex` | 504 B | Intel HEX |
| `Файлы для создания переключателя/Чертеж платы.lay` | `hardware/pcb_layouts/pcb_layout_v1.lay` | 7,833 B | Sprint Layout |
| `Версия на 2 переключателя (ДВС и КПП)/version2.lay` | `hardware/pcb_layouts/pcb_layout_v2.lay` | 68,003 B | Sprint Layout |
| `Общая схема.png` | `hardware/schematics/general_schematic.png` | 372,788 B | PNG |
| `Схема переключателя.jpg` | `hardware/schematics/switch_schematic.jpg` | 288,905 B | JPEG |
| `Плата.JPG` | `hardware/schematics/pcb_photo.jpg` | 727,538 B | JPEG |

### Documentation Files

| Original Path (Russian) | Archive Path (English) | Size |
|-------------------------|------------------------|------|
| `Мануал двухрежимки BMW для всех ЭБУ.pdf` | `documentation/BMW_Dual_Mode_Manual.pdf` | 971,947 B |
| `Как собрать переключатель.docx` | `documentation/How_to_Build_Switch.docx` | 415,935 B |
| `Как создать файл двухрежимной прошивки.docx` | `documentation/How_to_Create_Firmware.docx` | 12,415 B |

### Tool Files

| Original Path | Archive Path | Size |
|---------------|--------------|------|
| `Прошивки/MiniPro/MiniPro.exe` | `tools/MiniPro.exe` | 1,019,904 B |
| `Прошивки/MiniPro/MiniProHelp.chm` | `tools/MiniProHelp.chm` | 428,027 B |

---

## 🔧 Firmware Files - Bosch M60 V8

**Archive Path:** `firmwares/Bosch_M60_V8/`

| Original Filename (Russian) | English Translation | Size | Engine | Trans |
|-----------------------------|---------------------|------|--------|-------|
| `1429180_540МКПП_безлямбдовая_1995г..bin` | `1429180_540_manual_no_lambda_1995.bin` | 65,536 B | M60B40 | Manual |
| `M60B30 АКПП.BIN` | `M60B30_auto.bin` | 65,536 B | M60B30 | Auto |
| `m60b30 для V8POWER.bin` | `M60B30_V8POWER_tune.bin` | 65,536 B | M60B30 | - |
| `M60b30 МКПП lambda.bin` | `M60B30_manual_lambda.bin` | 65,536 B | M60B30 | Manual |
| `M60B30 МКПП безлямбда.bin` | `M60B30_manual_no_lambda.bin` | 65,536 B | M60B30 | Manual |
| `M60B30 МКПП безлямбда2.bin` | `M60B30_manual_no_lambda_v2.bin` | 65,536 B | M60B30 | Manual |
| `M60B30 МКПП безлямбда3 возможно тюн.bin` | `M60B30_manual_no_lambda_v3_maybe_tuned.bin` | 65,536 B | M60B30 | Manual |
| `m60b30 МКППstock.bin` | `M60B30_manual_stock.bin` | 65,536 B | M60B30 | Manual |
| `m60b30stock мкпп.bin` | `M60B30_stock_manual.bin` | 65,536 B | M60B30 | Manual |
| `m60b30akppnolambda1429331.bin` | `M60B30_auto_no_lambda_1429331.bin` | 65,536 B | M60B30 | Auto |
| `М60В30МКППno.lambd1429190.bin` | `M60B30_manual_no_lambda_1429190.bin` | 65,536 B | M60B30 | Manual |
| `m60b40 автомат без лямбда тюнинг.bin` | `M60B40_auto_no_lambda_tuned.bin` | 65,536 B | M60B40 | Auto |
| `M60B40akppnolambd1429009superchips.bin` | `M60B40_auto_no_lambda_superchips.bin` | 65,536 B | M60B40 | Auto |
| `Без лямбды мех M60.bin` | `M60_manual_no_lambda.bin` | 65,536 B | M60 | Manual |
| `безкатовая для е38 м60в30 мкпп 1429218/1429218.bin` | `E38_M60B30_manual_catless_1429218.bin` | 65,536 B | M60B30 | Manual |
| `bmw 7tkach.BIN` | `bmw_7tkach.bin` | 32,768 B | - | - |
| `TMS27C512-STOK.bin` | `TMS27C512_stock.bin` | 65,536 B | - | - |

### Bosch M60 Archives

| Archive | Contents | Size |
|---------|----------|------|
| `484_e38_без ews_.rar` | E38 without EWS | 33,096 B |
| `Без лямбды мех M60.rar` | M60 Manual No-Lambda | 29,990 B |
| `bocsh 404 no lamda mkkp.rar` | Bosch 404 Manual No-Lambda | 29,977 B |
| `безкатовая для е38 м60в30 мкпп 1429218.zip` | E38 M60B30 Catless | 34,082 B |
| `eproms_m60.zip` | M60 EPROMs collection | 61,847 B |
| `m60b30mkppnolambd1744050.zip` | M60B30 Manual No-Lambda | 62,192 B |
| `M60B30_tun.zip` | M60B30 Tuned | 30,893 B |
| `M60B40404_superchipNOLZ.zip` | M60B40 Superchips No-Lambda | 31,402 B |

---

## 🔧 Firmware Files - Bosch Motronic 1.3

**Archive Path:** `firmwares/Bosch_Motronic_1.3/`

### M20 Engine (E30)

| Subfolder | Filename | Description |
|-----------|----------|-------------|
| `enzo-m20b20/` | `Enzo.bin` (32,768 B) | M20B20 tune |
| `enzo-m20b25/` | `Enzo.bin` (32,768 B) | M20B25 tune |
| `320=325/` | `Jcchip.bin` (32,768 B) | 320i→325i conversion |
| `325+15ps/` | `325jcchip.bin` (32,768 B) | 325i +15hp tune |

### M30 Engine (E34)

| Subfolder | Filename | Description |
|-----------|----------|-------------|
| `m30 535 m1.3/` | `1726685_.bin` (32,768 B) | 535i stock |
| `m30 b35 m1.3/` | `1730697.bin` (32,768 B) | M30B35 stock |
| `m30 b35 m1.3/` | `М30-0261200179 РАЛЛИ@7000рпм.BIN` (32,768 B) | Rally 7000 RPM tune |

### M30B35 Firmware Pack (Пак прошивок)

**Organized by features:**

| Folder (Russian) | Translation | Contents |
|------------------|-------------|----------|
| `c EML, c ASC+T/` | With EML + ASC+T | 4 files (АКПП/МКПП × лямбда/безлямбда) |
| `c EML, без ASC+T/` | With EML, No ASC+T | 4 files |
| `без EML, без ASC+T/` | No EML, No ASC+T | 4 files |

**File naming pattern:**
`M30B35 Motronic M1.3 179 [TRANS] [LAMBDA] 1730697_[CODE].bin`

| Code | Transmission | Lambda | EML | ASC+T |
|------|--------------|--------|-----|-------|
| 6358 | Auto | No | Yes | Yes |
| C358 | Auto | Yes | Yes | Yes |
| 6058 | Manual | No | Yes | Yes |
| C058 | Manual | Yes | Yes | Yes |
| 635A | Auto | No | Yes | No |
| C35A | Auto | Yes | Yes | No |
| 605A | Manual | No | Yes | No |
| C05A | Manual | Yes | Yes | No |
| 635E | Auto | No | No | No |
| C35E | Auto | Yes | No | No |
| 605E | Manual | No | No | No |
| C05E | Manual | Yes | No | No |

---

## 🔧 Firmware Files - Siemens MS42

**Archive Path:** `firmwares/Siemens_MS42/`

### Organized by Model

```
Siemens_MS42/
├── E39/
│   ├── 520i/
│   ├── 523i/
│   └── 528i/
└── E46/
    ├── 320i/
    └── 328i/
```

### E39 520i (M52TUB20 2.0L)

| Calibration Folder | Files | Description |
|--------------------|-------|-------------|
| `84ad420g_Ca0110AD/` | 4 files | MOD2 + Stock |
| `84ad620f_Ca0110AD/` | 4 files | MOD2 + Stock |
| `84c3420g_Ca0110C6/` | 4 files | MOD2 + Stock |
| `84c3420g_Ca0110C6_2.0L/` | 4 files | 2.0L specific |
| `91c6120r_ca0110C6/` | 4 files | MOD2 + Stock |
| `93c9420r_Ca0110CA_2.0L/` | 4 files | Latest cal |

### E39 523i (M52TUB25 2.3/2.5L)

| Calibration Folder | Files | Description |
|--------------------|-------|-------------|
| `81ab220o_Сa0110AB/` | 4 files | MOD3 + Stock |
| `84c3520g_Ca0110C6/` | 4 files | MOD2 + Stock |
| `91c6522g_Ca0110C6_2.3L/` | 4 files | 2.3L specific |
| `93c95204_Ca0110CA_2.3L/` | 4 files | Latest cal |

### E39 528i (M52TUB28 2.8L)

| Calibration Folder | Files | Description |
|--------------------|-------|-------------|
| `7225320f_Ca011025_2.8L/` | 4 files | Early cal |
| `72253b0f_Ca011025_2.8L/` | 4 files | Early cal |
| `84ad320m_Ca0110AD/` | 4 files | Standard cal |
| `84ads20f_Ca0110AD_2.8L/` | 4 files | 2.8L specific |
| `84c33204_Ca0110C6_2.8L/` | 4 files | Later cal |
| `93c9620g_Ca0110CA_2.8L/` | 4 files | Latest cal |

### E46 320i/328i

| Model | Calibration Folders | Total Files |
|-------|---------------------|-------------|
| 320i | `84c3120g_Ca0110C6_2.0L/` | 4 files |
| 328i | Multiple (Ca0110AB, Ca0110AD) | 28+ files |

---

## 🔧 Firmware Files - Siemens MS43

**Archive Path:** `firmwares/Siemens_MS43/`

### Organized by Model

```
Siemens_MS43/
├── E39/
│   ├── 525i/
│   └── 530i/
├── E46/
│   ├── 325i/
│   └── 330i/
└── E53/
    └── X5_3.0i/
```

### File Pattern

Each calibration folder contains 4 files:
- `*_MOD4.bin` - Tuned version
- `*_MOD4_E0.bin` - Tuned + EWS delete
- `*_MOD4_E2.bin` - Tuned + EWS delete (alt)
- `*_Stok.bin` - Stock firmware

### E39 525i Calibrations

| Folder | Cal ID | Notes |
|--------|--------|-------|
| `b137b56g_Сa430037/` | Ca430037 | Standard |
| `b137b57g_Сa430037/` | Ca430037 | Variant |
| `b137c56g_Ca430037/` | Ca430037 | 65KB files |
| `C256b50f_Ca430056/` | Ca430056 | Later |
| `c256b52d_Ca430056/` | Ca430056 | Variant |
| `C256C528_Ca430056/` | Ca430056 | Variant |
| `c256z50h_Ca430056/` | Ca430056 | Variant |

### E39 530i Calibrations

| Folder | Cal ID | Notes |
|--------|--------|-------|
| `b137c56d_430037/` | Ca430037 | Standard |
| `b137j54g_Ca430037/` | Ca430037 | 512KB |
| `C256J508_Ca430056/` | Ca430056 | Later |
| `c6668528_Ca430066/` | Ca430066 | Latest |

### E46 330i Calibrations (Many variants)

Total: 12+ calibration folders with MOD4 variants

### E53 X5 3.0i Calibrations

| Folder | Cal ID | Notes |
|--------|--------|-------|
| `b137b56g_Сa430037/` | Ca430037 | Cross-ref E39 |
| `c256454k_Ca430056/` | Ca430056 | X5 specific |
| `C356450h_Ca430056/` | Ca430056 | Variant |
| `c356750c_Ca430056/` | Ca430056 | Variant |
| `c356750f_Ca430056/` | Ca430056 | 512KB |
| `c464x53j_Ca430064/` | Ca430064 | Later |
| `c566450f_Ca430066/` | Ca430066 | Latest |
| `c566450k_Ca430066/` | Ca430066 | Variant |
| `C769X54J_Ca430069/` | Ca430069 | X5 specific |

---

## 🔧 Firmware Files - Bosch ME7.2 (M62 V8)

**Archive Path:** `firmwares/Bosch_ME7.2/`

### File Inventory

| Folder | Description | Files |
|--------|-------------|-------|
| `0261204620_350411/` | ME7.2 E38/E39 | MOD3 + Stock |
| `0261204620_350476/` | ME7.2 variant | MOD3 + Stock |
| `0261204620_350516/` | ME7.2 variant | MOD3 + Stock |
| `0261204620_356367/` | ME7.2 + EEPROM | MOD3 + Stock + 95P08.bin |
| `0261204620_368125/` | ME7.2 E53 | MOD3 + Stock |
| `0261207106_368125/` | ME7.2 X5 4.4 | MOD3 + Stock + 5P08.bin |

### Special File

| Filename | Description | Size |
|----------|-------------|------|
| `X5 E53 4.4 2002г.в. Bosch ME7.20261207106_368125_TUN.bin` | X5 4.4 V8 2002 Tuned | 524,288 B |

---

## 📊 Statistics Summary

| Category | File Count | Total Size |
|----------|------------|------------|
| Hardware (HEX/LAY) | 4 | ~77 KB |
| Schematics (Images) | 3 | ~1.4 MB |
| Documentation | 3 | ~1.4 MB |
| Tools | 2 | ~1.4 MB |
| Bosch M60 Firmwares | 30+ | ~2 MB |
| Motronic 1.3 Firmwares | 20+ | ~700 KB |
| MS42 Firmwares | 100+ | ~30 MB |
| MS43 Firmwares | 150+ | ~80 MB |
| ME7.2 Firmwares | 15+ | ~8 MB |
| **TOTAL** | **~330 files** | **~125 MB** |

---

## 🔄 Copy Commands for Archive Integration

```powershell
# Create directory structure
$destBase = "A:\repos\PCM_SCRAPING_TOOLS\FULL_ARCHIVE_V2\downloads\BMW\Dualmode_Switch"
New-Item -Path "$destBase\hardware\firmware" -ItemType Directory -Force
New-Item -Path "$destBase\hardware\pcb_layouts" -ItemType Directory -Force
New-Item -Path "$destBase\hardware\schematics" -ItemType Directory -Force
New-Item -Path "$destBase\documentation" -ItemType Directory -Force
New-Item -Path "$destBase\tools" -ItemType Directory -Force
New-Item -Path "$destBase\firmwares\Bosch_M60_V8" -ItemType Directory -Force
New-Item -Path "$destBase\firmwares\Bosch_Motronic_1.3" -ItemType Directory -Force
New-Item -Path "$destBase\firmwares\Siemens_MS42" -ItemType Directory -Force
New-Item -Path "$destBase\firmwares\Siemens_MS43" -ItemType Directory -Force
New-Item -Path "$destBase\firmwares\Bosch_ME7.2" -ItemType Directory -Force

# Copy would be done manually or via script due to Cyrillic paths
```

---

**Generated:** January 22, 2026
