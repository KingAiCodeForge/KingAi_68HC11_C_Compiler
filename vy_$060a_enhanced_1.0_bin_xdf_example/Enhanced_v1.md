# ECU Calibration Export

## Metadata

| Property | Value |
|----------|-------|
| Source File | `VX-VY_V6_$060A_Enhanced_v1.0a.bin` |
| Definition | `VY_V6_$060A_Enhanced` |
| Binary Size | 131,072 bytes |
| MD5 Checksum | `b5fe9212095f52b9e5e84301803f4f95` |
| Export Date | 2026-02-20 09:56:28 |
| Exporter | KingAI TunerPro Exporter v3.3.0 |
| Author | kingaustraliagg (Jason King) |
| GitHub | [KingAiCodeForge](https://github.com/KingAiCodeForge) |

## Summary

- **Scalars:** 1310
- **Flags:** 548
- **Tables:** 330

## Table of Contents

1. [Scalar Values](#scalar-values)
2. [Flags](#flags)
3. [Tables](#tables)

---

## Scalar Values

| Parameter | Value | Unit | Category |
|-----------|-------|------|----------|
| C/L Upper o2 Threshold, o2 A/D Units | 0.70 | VOLTS | Engine/Transmission Diagnostics |
| C/L Lower o2 Threshold, o2 A/D Units | 0.25 | VOLTS | Engine/Transmission Diagnostics |
| C/L Timer,  Warm Temperature Threshold | 90.00 | DEG/C | Engine/Transmission Diagnostics |
| Warm C/L Timer Value, Sec | 5.00 | Sec | Engine/Transmission Diagnostics |
| Cold C/L Timer Value, Sec | 60.00 | Sec | Engine/Transmission Diagnostics |
| Temperature Threshold For C/L Determination | 44.00 | DEG/C | Engine/Transmission Diagnostics |
| Temperature Threshold For O/L Determination | 38.00 | DEG/C | Engine/Transmission Diagnostics |
| o2 Sensor Not Ready Timer Limit, Sec  For Both Left & Right Sensor | 6.00 | SEC | Engine/Transmission Diagnostics |
| IF RPM < This Remain in O/L | 0.00 | RPM | Engine/Transmission Diagnostics |
| If RPM >= CAL For KRPMCLTM Time Go C/L | 1.00 | - | Engine/Transmission Diagnostics |
| Closed Loop - Air Fuel Ratio | 14.76 | :1 | Engine/Transmission Diagnostics |
| C/L Lean-Out F/A Ratio By 1 CNT Every CAL Time | 0.21 | SEC | Engine/Transmission Diagnostics |
| C/L Richen F/A Ratio By 1 CNT Every CAL Time | 0.80 | SEC | Engine/Transmission Diagnostics |
| o2 Slow Trim INTGRT Delay Factor (R) | 1.99 | MULT | Engine/Transmission Diagnostics |
| o2 Slow Trim Intergrator Delay Factor When In Idle Cell (Right Side) | 1.99 | MULT | Engine/Transmission Diagnostics |
| o2 Slow Trim INTGRT Delay Factor (L) | 1.99 | MULT | Engine/Transmission Diagnostics |
| o2 Slow Trim Intergrator Delay Factor When In Idle Cell (Left Side) | 1.99 | MULT | Engine/Transmission Diagnostics |
| Run Time To Use Cold EOS Thresholds After This Time Use Hot EOS Thresholds | 150.00 | SEC | Engine/Transmission Diagnostics |
| Run Time After Which EOS Threshold Determination To Be Flow Based | 150.00 | SEC | Engine/Transmission Diagnostics |
| If Airflow > KO2HIFL1 For Time > CAL, Use Hot EOS Thresholds (High Flow Condition Timer) | 150.00 | SEC | Engine/Transmission Diagnostics |
| If Airflow > KO2HIFL2 For Time > CAL, Use Hot EOS Thresholds (Moderate Flow Condition Timer) | 300.00 | SEC | Engine/Transmission Diagnostics |
| If Airflow > CAL, And Timer > KO2HITM1, Then Use Hot EOS Thresholds (High Flow Condition Threshold) | 36.14 | GM/S | Engine/Transmission Diagnostics |
| If Airflow > CAL, Decrement EOSHOTTM | 0.08 | GM/S | Engine/Transmission Diagnostics |
| CAL Rate To Decrement EOSHOTTM When Airflow < KO2LOFLO | 0.00 | SEC | Engine/Transmission Diagnostics |
| o2 Cold Rich Threshold, o2 A/D Units | 0.65 | VOLTS | Engine/Transmission Diagnostics |
| o2 Cold Lean Threshold, o2 A/D Units | 0.40 | VOLTS | Engine/Transmission Diagnostics |
| o2 Idle Rich Threshold, o2 A/D Unit | 0.60 | VOLTS | Engine/Transmission Diagnostics |
| o2 Idle Lean Threshold, o2 A/D Unit | 0.40 | VOLTS | Engine/Transmission Diagnostics |
| If CYL_AIR <= Cal Skip Updating | 62.50 | MG/CYL | Engine/Transmission Diagnostics |
| If Coolant <= Cal Skip Learning (BLM) | 20.00 | DEG/C | Engine/Transmission Diagnostics |
| If CYL_AIR <= Cal Skip Learning (BLM) | 66.41 | MG/Cyl | Engine/Transmission Diagnostics |
| EPROM ID | 1918.00 | HEX | Calibration Option Parameters |
| Minimum TCC Duty Cycle | 0.00 | % | Transmission Diagnostics |
| Cold Engine Coolant Temp Threshold (TCC Off) | 50.00 | DEG/C | Transmission Diagnostics |
| Cold Engine Coolant Temp Threshold (TCC On) | -0.25 | DEG/C | Transmission Diagnostics |
| Cold Engine Coolant Temp Threshold (TCC On) | -3.25 | DEG/C | Transmission Diagnostics |
| Cold Transmission Temp Threshold (TCC On) | -3.25 | DEG/C | Transmission Diagnostics |
| High Temperature Calculated Apply Point Threshold | 2.00 | MPH | Transmission Diagnostics |
| High Temperature Point Low Vehicle Speed Threshold | 0.00 | MPH | Transmission Diagnostics |
| Trans Temp Threshold For Min Apply Speed (Off) | 149.00 | DEG/C | Transmission Diagnostics |
| Trans Temp Threshold For Min Apply Speed (On) | 146.00 | DEG/C | Transmission Diagnostics |
| Hot Transmission Temp Entry Point | 128.00 | DEG/C | Transmission Diagnostics |
| Hot Transmission Temp Exit Point | 121.25 | DEG/C | Transmission Diagnostics |
| Vehicle Speed Limit, 2nd, A/C On, TCC On | 93.50 | MPH | Transmission Diagnostics |
| Vehicle Speed Limit, 3rd, A/C On,TCC On | 93.50 | MPH | Transmission Diagnostics |
| Vehicle Speed Limit, 4th, A/C On, TCC On | 93.50 | MPH | Transmission Diagnostics |
| Vehicle Speed Limit, 5th, A/C On, TCC On | 93.50 | MPH | Transmission Diagnostics |
| Vehicle Speed Limit, 2nd, A/C On, TCC Off | 93.50 | MPH | Transmission Diagnostics |
| Vehicle Speed Limit, 3rd, A/C On, TCC Off | 93.50 | MPH | Transmission Diagnostics |
| Vehicle Speed Limit, 4th, A/C On, TCC Off | 93.50 | MPH | Transmission Diagnostics |
| Vehicle Speed Limit, 5th, A/C On, TCC Off | 93.50 | MPH | Transmission Diagnostics |
| Cope TCC Trans Temperature Low Threshold | 150.50 | DEG/C | Transmission Diagnostics |
| Cope TCC Trans Temperature High Threshold | 149.75 | DEG/C | Transmission Diagnostics |
| If Slip < CAL Then Off Mode | 7992.00 | RPM | Transmission Diagnostics |
| If Off Mode, Stay Off Until Slip > CAL | 0.00 | RPM | Transmission Diagnostics |
| High Vehicle Speed Threshold For Throttle Thresholds | 47.00 | MPH | Transmission Diagnostics |
| Low Vehicle Speed Threshold For Throttle Thresholds | 45.00 | MPH | Transmission Diagnostics |
| Low Vehicle Speed Throttle Threshold | 1.18 | % | Transmission Diagnostics |
| Cruise Mode Low Vehicle Speed Throttle Threshold | 1.18 | % | Transmission Diagnostics |
| Performance Mode Low Vehicle Speed Throttle Threshold | 1.18 | % | Transmission Diagnostics |
| Low Vehicle Speed Throttle Threshold | 1.96 | % | Transmission Diagnostics |
| Cruise Mode Low Vehicle Speed Throttle Threshold | 1.96 | % | Transmission Diagnostics |
| Performance Mode Low Vehicle Speed Throttle Threshold | 1.96 | % | Transmission Diagnostics |
| High Vehicle Speed Throttle Threshold | 1.18 | % | Transmission Diagnostics |
| High Vehicle Speed Throttle Threshold Cruise Mode | 1.18 | % | Transmission Diagnostics |
| High Vehicle Speed Throttle Threshold Performance Mode | 1.18 | % | Transmission Diagnostics |
| High Vehicle Speed Throttle Threshold | 1.96 | % | Transmission Diagnostics |
| High Vehicle Speed Throttle Threshold Cruise Mode | 1.96 | % | Transmission Diagnostics |
| High Vehicle Speed Throttle Threshold Performance Mode | 1.96 | % | Transmission Diagnostics |
| Delta Throttle Threshold | 3890.20 | %/S | Transmission Diagnostics |
| KNDTTIME | 0.50 | SEC | Transmission Diagnostics |
| Delta Throttle Threshold | 784.31 | %/S | Transmission Diagnostics |
| Stay In Release CAL Time If KPDELTHR Release | 1.00 | SEC | Transmission Diagnostics |
| Duration Of Apply | 3.00 | SEC | Transmission Diagnostics |
| Downshift Off Time 2-1 | 18.70 | SEC | Transmission Diagnostics |
| Downshift Off Time 3-2 | 18.70 | SEC | Transmission Diagnostics |
| Downshift Off Time 4-3 | 18.70 | SEC | Transmission Diagnostics |
| Upshift Off Time 1-2 | 18.70 | SEC | Transmission Diagnostics |
| Upshift Off Time 2-3 | 18.70 | SEC | Transmission Diagnostics |
| Upshift Off Time 3-4 | 18.70 | SEC | Transmission Diagnostics |
| Upper Slip Threshold, First Lock | 8191.88 | RPM | Transmission Diagnostics |
| Lower Slip Threshold, First Lock | 0.00 | RPM | Transmission Diagnostics |
| Time Needed Below KLOCKL For First Lock | 6.38 | SEC | Transmission Diagnostics |
| Change TCC DC By CAL If DTPS > KPDELTHR | 4000.00 | %/S | Transmission Diagnostics |
| Ignore Slip Less Than This While Releasing | 50.00 | RPM | Transmission Diagnostics |
| Minimum Value Of Delay Time LKDLYTIM | 0.30 | SEC | Transmission Diagnostics |
| Time Between Min Throttle For Busyness | 20.00 | SEC | Transmission Diagnostics |
| Time Delay For Reapplying If TCC Busy | 4.00 | SEC | Transmission Diagnostics |
| Reapply Delay Time Is Set Equal To If One Scheduled Throttle Release Occurs Before The Busyness Determination Timer Expires | 2.00 | SEC | Transmission Diagnostics |
| The Additional Delay Time Added To Reapply If Two Or More Scheduled Throttle Releases Occure Before The Busyness Determination Timer | 4.00 | SEC | Transmission Diagnostics |
| The Busyness Determination Timer Is Set Equal To If Minimum Throttle Release Or A Scheduled Throttle Release Occurs | 20.00 | SEC | Transmission Diagnostics |
| Vehicle Speed At Which TCC DC Is Set To Max | 26.00 | MPH | Transmission Diagnostics |
| Vehicle Speed At Which TCC DC Is Set To Min | 24.00 | MPH | Transmission Diagnostics |
| Enable On Delay | 0.00 | SEC | Transmission Diagnostics |
| Apply Ramp Delay | 0.03 | SEC | Transmission Diagnostics |
| Enable Off Delay | 0.25 | SEC | Transmission Diagnostics |
| Failsafe Delay | 0.00 | SEC | Transmission Diagnostics |
| 3rd Gear Apply Detent Threshold | 127.50 | MPH | Transmission Diagnostics |
| 4th Gear Apply Detent Threshold | 127.50 | MPH | Transmission Diagnostics |
| 2nd Gear Hot Apply Detent Threshold | 127.50 | MPH | Transmission Diagnostics |
| 3rd Gear Hot Apply Detent Threshold | 34.00 | MPH | Transmission Diagnostics |
| 4th Gear Hot Apply Detent Threshold | 127.50 | MPH | Transmission Diagnostics |
| 2nd Gear Release Detent Threshold | 127.00 | MPH | Transmission Diagnostics |
| 3rd Gear Release Detent Threshold | 30.00 | MPH | Transmission Diagnostics |
| 4th Gear Release Detent Threshold | 127.00 | MPH | Transmission Diagnostics |
| 3rd Gear Release Detent Threshold | 127.00 | MPH | Transmission Diagnostics |
| 4th Gear Release Detent Threshold | 127.00 | MPH | Transmission Diagnostics |
| BCC ID | 808665392.00 | HEX | Calibration Option Parameters |
| DOUBLE BYTE SEQUENCE NUMBER | 16688.00 | - | Calibration Option Parameters |
| CRC CHECKSUM | 36463.00 | - | Calibration Option Parameters |
| SOFTWARE ID         (XDF) | 43530.00 | HEX | Calibration Option Parameters |
| UPDATE EEPROM IF KMS FROM KEY ON > CAL AT KEY OFF | 10.00 | - | Calibration Option Parameters |
| TRANSMISSION ID | 32705.00 | - | Calibration Option Parameters |
| APPLICATION ID | 305.00 | - | Calibration Option Parameters |
| PROGRAM ID           (PCM BOX CODE) | 16269238.00 | - | Calibration Option Parameters |
| CALIBRATION ID | 92118883.00 | - | Calibration Option Parameters |
| If Output Speed > This Enable M24 | 0.88 | RPM | Transmission Calibration |
| Successive Power Ups With No Malfs | 50.00 | CYCLES | Transmission Calibration |
| If Output Speed < This Enable M24 | 250.00 | RPM | Transmission Calibration |
| Throttle Minimum Value (Idle) | 64.00 | COUNTS | Engine/Transmission Diagnostics |
| Throttle Offset Filter Time Constant | 0.02 | SEC | Engine/Transmission Diagnostics |
| TPS - Throttle Gain % | 0.59 | %/CNT | Engine/Transmission Diagnostics |
| TPS - Filter Coefficient Increasing | 56.25 | Coeff | Engine/Transmission Diagnostics |
| TPS - Transmission Filter Coefficient | 99.61 | Coeff | Engine/Transmission Diagnostics |
| TPS Offset Increase For Each Decal | 2.00 | % | Engine/Transmission Diagnostics |
| Vehicle Speed Change To Define Decel | 5.00 | MPH | Engine/Transmission Diagnostics |
| TPS Threshold For Non-Brake Switch Auto-Zero | 70.00 | ADCNTS | Engine/Transmission Diagnostics |
| Upper Limit For Closed Throttle Determination | 5.00 | ADCNTS | Engine/Transmission Diagnostics |
| Lower Limit For Closed Throttle Determination | 3.00 | ADCNTS | Engine/Transmission Diagnostics |
| Base Injector Rate | 361.33 | MSEC/ GRAM | Engine/Transmission Diagnostics |
| Min Injector Off Time | 0.45 | Msec | Engine/Transmission Diagnostics |
| Min Base Pulse Width | 1.01 | Msec | Engine/Transmission Diagnostics |
| Default Pulse width for low calculated pw | 1.02 | Msec | Engine/Transmission Diagnostics |
| EOI Target Param Fuel Boundry Located Cal Deg After 3x REF Which Occurs Just Prior To Intake Valve Closure | 9.84 | - | Engine/Transmission Diagnostics |
| Time Delay from Closed to Open Loop Idle When in P/N | 10.00 | Sec | Engine/Transmission Diagnostics |
| Default Time Delay for Closed to Open Loop Idle | 35.00 | Sec | Engine/Transmission Diagnostics |
| If Powerdown Coolant Temp > CAL - Then Key On Prime Pulse Allowed Even If Last Prime Wasn't Burned | 9.75 | DEG/C | Engine/Transmission Diagnostics |
| Coolant Temp Below Which Prime Pulse Disabled If Prime Disabled ASYNC Pulse Delivered On F63B 3X | 151.25 | DEG/C | Engine/Transmission Diagnostics |
| CLR FLD Entered TPS > CAL - Exit When <= CAL | 79.69 | TPS% | Engine/Transmission Diagnostics |
| RPM Above Which Clear Flood Mode Terminated | 800.00 | RPM | Engine/Transmission Diagnostics |
| RPLSCNTR = This When In Clear Flood | 8.00 | COUNTS | Engine/Transmission Diagnostics |
| RPLSCNTR = This When Run/NoRun Trans | 0.00 | COUNTS | Engine/Transmission Diagnostics |
| Step Crank/Run Fuel Every KRAMPCTR Refs | 1.00 | COUNTS | Engine/Transmission Diagnostics |
| If Coolant Temp < CAL - Wait To Deliver Crank Fuel | 151.25 | DEG/C | Engine/Transmission Diagnostics |
| Wait CAL Refs To Deliver Crank Fuel When Cold | 0.00 | REFS | Engine/Transmission Diagnostics |
| Crank Table Scalar For Max Crank Pulse Width | 8520.00 | Msec | Engine/Transmission Diagnostics |
| Coolant Temp Must Be < CAL - To Use Short Run Crank Fuelling | 80.00 | DEG/C | Engine/Transmission Diagnostics |
| Last Powerdown Temperature - Current Temperature Must Be > CAL - To Use Short Run F64SRMUL | 0.75 | DEG/C | Engine/Transmission Diagnostics |
| If KPH > CAL Use Drive CALS For RPM Fuel Cutoff | 16.09 | KPH | Engine/Transmission Diagnostics |
| If RPM < CAL, Disable High KPH Fuel Shutoff | 2000.00 | RPM | Engine/Transmission Diagnostics |
| If FILTKPH >= CAL, Shut Off Fuel - 4th Gear | 408.77 | KPH | Engine/Transmission Diagnostics |
| If FILTKPH >= CAL, Don't Turn Fuel Back On 4th | 407.16 | KPH | Engine/Transmission Diagnostics |
| If FILTKPH >= CAL, Shut Off Fuel - 3rd Gear | 408.77 | KPH | Engine/Transmission Diagnostics |
| If FILTKPH >= CAL,  Don't Turn Fuel Back On 3rd | 407.16 | KPH | Engine/Transmission Diagnostics |
| If In 3rd And  FILTKPH >= CAL, Freak Out Fuel | 410.38 | KPH | Engine/Transmission Diagnostics |
| If In 4th And FILTKPH > CAL, Freak Out Fuel | 410.38 | KPH | Engine/Transmission Diagnostics |
| Fuel Freak Out Factor | 1.05 | GAIN | Engine/Transmission Diagnostics |
| Degrees Retard / KPH Over KVSSLMT | 2.81 | DEG | Engine/Transmission Diagnostics |
| Time to Remain At KFCORATO After F.C.O. Ends | 0.10 | SEC | Engine/Transmission Diagnostics |
| Fuel Cutoff A/F Ratio in Drive | 16.06 | RATIO | Engine/Transmission Diagnostics |
| Fuel Cutoff A/Fl Ratio in P/N And Reverse | 16.06 | RATIO | Engine/Transmission Diagnostics |
| Scaler for Torque Management | 190.00 | SCALER | Engine/Transmission Diagnostics |
| Torque Multiplier When Speed Ratio >= 1 | 1.00 | MULT | Engine/Transmission Diagnostics |
| Do Not Use Torque Multiplier Until Run Time > This | 0.00 | SEC | Engine/Transmission Diagnostics |
| Default Torque Value for Engine Perf | 168.00 | TORQUE | Engine/Transmission Diagnostics |
| Sea Level Torque Value used for Altitude Compensation of F31 Functions | 184.00 | TORQUE | Engine/Transmission Diagnostics |
| Default Torque Value for Engine Perf50 | 176.00 | TORQUE | Engine/Transmission Diagnostics |
| ENGPERF Counts Per TPS% | 1.05 | COUNTS/% | Engine/Transmission Diagnostics |
| TPS Deadband For ENGPERF 100 Learn Window | 1.17 | TPS% | Engine/Transmission Diagnostics |
| Filter Coefficient For Learning ENGPERF | 0.02 | COEFF | Engine/Transmission Diagnostics |
| Don't Learn Engine Perf50 if RPM <= This | 1600.00 | RPM | Engine/Transmission Diagnostics |
| Don't Learn Engine Perf50 if RPM >= This | 1800.00 | RPM | Engine/Transmission Diagnostics |
| Don't Learn Engine Perf50 if TPS < This | 25.78 | TPS% | Engine/Transmission Diagnostics |
| Don't Learn Engine Perf50 if TPS >= This | 26.95 | TPS% | Engine/Transmission Diagnostics |
| Filter Coefficient For Learning ENGPERF50 | 0.02 | COEFF | Engine/Transmission Diagnostics |
| Torque If ENGPERF >= This - Set ENGPERF MIL = 0 | 160.00 | TORQUE | Engine/Transmission Diagnostics |
| Torque If ENGPERF50 <= This - Set ENGPERF50 MIL = 0 | 168.00 | TORQUE | Engine/Transmission Diagnostics |
| Miles If ENGPMIL >= This - Set ENGPERF = ENGPERF | 0.00 | MILES | Engine/Transmission Diagnostics |
| Sec Time Counts Down After Exiting TCS, During This Time The Down Shifts Are Inhibited | 0.06 | SEC | Engine/Transmission Diagnostics |
| Sec Delay Timer From The Commencement Of TCS Or The Last Upshift With TCS, Until The Next Upshift Occures | 0.06 | SEC | Engine/Transmission Diagnostics |
| TRQREQ Command Upshift If KUPTMR Expired And TRQRDMOD > KUPMODE | 1.56 | TRQREQ | Engine/Transmission Diagnostics |
| KPH If During TCS Vehicle Speed Droop > KDWNKPH Then Do Not Inhibit Downshifts | 20.00 | KPH | Engine/Transmission Diagnostics |
| RPM Stall Saver Threshold For Traction Control | 2000.00 | RPM | Engine/Transmission Diagnostics |
| Stall Saver Maximum Mode | 350.00 | RPM | Engine/Transmission Diagnostics |
| Timer Before Incrementing TCS Mode When | 0.11 | SEC | Engine/Transmission Diagnostics |
| Coefficient Q Value To Filter Torque Multiplier | 0.99 | COEFF | Engine/Transmission Diagnostics |
| Multiplier For DFPWX When Cylinder Is Re-Activated After Changing Mode | 1.50 | - | Engine/Transmission Diagnostics |
| If RPM < This - Disable TCS Torque Reduction | 850.00 | RPM | Engine/Transmission Diagnostics |
| If RPM < This - Keep TCS Torque Reduction Disabled | 1000.00 | RPM | Engine/Transmission Diagnostics |
| If TPS > This - Disable TCS Torque Reduction | 99.61 | TPS% | Engine/Transmission Diagnostics |
| Hysteresis For DCTRQREQ (Requested Torque) | 0.00 | DC% | Engine/Transmission Diagnostics |
| TRQRATIO Hysteresis When TRQRATIO Increasing | 1.17 | TRQRAT | Engine/Transmission Diagnostics |
| TRQRATIO Hysteresis When TRQRATIO Decreasing | 0.78 | TRQRAT | Engine/Transmission Diagnostics |
| TCMAXTRQ Filter Coefficient | 0.31 | COEFF | Engine/Transmission Diagnostics |
| Coolant Default for TCS Enable Look-up | -40.00 | DEG/C | Engine/Transmission Diagnostics |
| F/A Ratio Per CAL Time To Ramp From TCS F/A | 0.00 | 1/RATIO | Engine/Transmission Diagnostics |
| Time To Delay Between F/A Ramp Increments | 0.00 | SEC | Engine/Transmission Diagnostics |
| ABS Speed Must Be >= To CAL To Command A 1-2 Upshift | 45.00 | KPH | Engine/Transmission Diagnostics |
| ABS Speed Must Be >= To CAL To Command A 2-3 Upshift | 65.00 | KPH | Engine/Transmission Diagnostics |
| Engine Speed Must Be >= To CAL To Command A 1-2 Upshift | 3400.00 | RPM | Engine/Transmission Diagnostics |
| Engine Speed Must Be >= To CAL To Command A 2-3 Upshift | 3000.00 | RPM | Engine/Transmission Diagnostics |
| CAL Delay Time Must Elapse To Allow 2-1 Downshift | 2.50 | SEC | Engine/Transmission Diagnostics |
| CAL Delay Time Must Elapse To Allow 3-2 Downshift | 2.00 | SEC | Engine/Transmission Diagnostics |
| If TRQRDMOD = 0 And TPS <= CAL Then The Previous Downshift Delays Will Be Cleared | 39.84 | TPS% | Engine/Transmission Diagnostics |
| TRQRDMOD Must Be > CAL For Upshift | 2.00 | MODE | Engine/Transmission Diagnostics |
| 12.5MS Loops To Delay Between Decs Of TCSCATTM | 3.00 | LOOPS | Engine/Transmission Diagnostics |
| If TRQRDMOD > CAL Don't Inc TSCATTM | 5.00 | MODE | Engine/Transmission Diagnostics |
| If TCSATTM >= CAL Ramp Boost Off | 3.00 | CNTS | Engine/Transmission Diagnostics |
| If TCSATTM >= CAL Ramp Power Back On | 11.00 | CNTS | Engine/Transmission Diagnostics |
| If TCSATTM >= CAL Reset TCSATTM To Zero | 39.00 | CNTS | Engine/Transmission Diagnostics |
| If TCS Active For CAL Time Ramp Out Cruise | 6.00 | SEC | Engine/Transmission Diagnostics |
| Maximum Engine Torque Reduction Mode | 24.00 | - | Engine/Transmission Diagnostics |
| Maximum Engine Torque | 12.80 | - | Engine/Transmission Diagnostics |
| Final Drive Ratio | 3227648.00 | RATIO | Engine/Transmission Diagnostics |
| Final Drive Efficiency Factor (0 to 1) | 241.00 | RATIO | Engine/Transmission Diagnostics |
| Time To Keep TC/PM A/F Ratio After Leaving TC/PM | 0.00 | SEC | Engine/Transmission Diagnostics |
| If NTSRPM < TCSROM - KTCSRPM Disable TCS | 3000.00 | RPM | Engine/Transmission Diagnostics |
| ACTGEAR ACTRATIO Default Update Timer | 2.00 | SEC | Engine/Transmission Diagnostics |
| 3rd Gear To 4th Gear Update Timer | 11.00 | SEC | Engine/Transmission Diagnostics |
| 4th Gear To 3rd Gear Update Timer | 3.00 | SEC | Engine/Transmission Diagnostics |
| Initialisation of Cylair50 at crank. this CAL is multiplied by F6CRNKPF before being applied | 500.00 | GM/CYL | Engine/Transmission Diagnostics |
| Initialisation of Chargair at crank. this CAL is multiplied by F6CRNKPF before being applied | 0.50 | GM | Engine/Transmission Diagnostics |
| Filter Coeff for Increasing Airflow | 12.50 | % | Engine/Transmission Diagnostics |
| Filter Coeff for Decreasing Airflow | 8.59 | % | Engine/Transmission Diagnostics |
| Filter coeff for Inc Flow for DSPFLOEL | 18.75 | % | Engine/Transmission Diagnostics |
| Filter Coeff for Dec Flow for DSPFLOEL | 75.00 | % | Engine/Transmission Diagnostics |
| RPM at which to enter thru-put savings mode when thru-put savings mode is disabled | 4500.00 | RPM | Engine/Transmission Diagnostics |
| RPM at which to exit thru-put savings mode when thru-put savings mode is enabled | 4000.00 | RPM | Engine/Transmission Diagnostics |
| Minimum Frequency Of High Frequency MAF | 1890.00 | HERTZ | Engine/Transmission Diagnostics |
| Mass Air Rate Offset 1 | 767.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Scaling Factor 1 | 6.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Offset 2 | 2048.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Scaling Factor 2 | 10.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Offset 3 | 4360.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Scaling Factor 3 | 15.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Offset 4 | 8169.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Scaling Factor 4 | 22.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Offset 5 | 13717.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Scaling Factor 5 | 32.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Offset 6 | 21805.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Scaling Factor 6 | 42.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Offset 7 | 32471.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Scaling Factor 7 | 53.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Offset 8 | 45902.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Scaling Factor 8 | 67.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Offset 9 | 62898.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Scaling Factor 9 | 56.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Offset 10 | 65535.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Scaling Factor 10 | 92.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Offset 11 | 65535.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Scaling Factor 11 | 139.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Offset 12 | 65535.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Scaling Factor 12 | 179.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Offset 13 | 65535.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Scaling Factor 13 | 225.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Offset 14 | 65535.00 | - | Engine/Transmission Diagnostics |
| Mass Air Rate Scaling Factor 14 | 255.00 | - | Engine/Transmission Diagnostics |
| TPS Filter Value For 3X Filtered TPS | 0.08 | - | Engine/Transmission Diagnostics |
| % Filter Coefficient For Increase Chargeair Airflow | 0.12 | COEFF | Engine/Transmission Diagnostics |
| % Filter Coefficient For Decrease Chargeair Airflow | 0.12 | COEFF | Engine/Transmission Diagnostics |
| Filter Coefficient For Filtered Reference Period Calculation | 0.12 | COEFF | Engine/Transmission Diagnostics |
| In/Out CNTR Delta MAF Hysteresis | 0.20 | GPS | Engine/Transmission Diagnostics |
| In/Out CNTR TPS Hysteresis | 0.39 | TPS% | Engine/Transmission Diagnostics |
| If Delta MAF > CAL - Must Do Transient Fuel Calcs | 0.30 | GPS | Engine/Transmission Diagnostics |
| If RPM < CAL - Do Transient Fuel | 3200.00 | RPM | Engine/Transmission Diagnostics |
| ECT Above Which Spark Option BIT 1 is Enabled | 96.00 | DEG/C | Engine/Transmission Diagnostics |
| High Resolution Idle RPM Filter Coefficient | 2560.00 | COEFF | Engine/Transmission Diagnostics |
| IAC Spark Correction Lower Coolant Threshold | -40.00 | DEG/C | Engine/Transmission Diagnostics |
| High RPM Spark Correction Multiplier | 0.04 | DEG% | Engine/Transmission Diagnostics |
| Low RPM Spark Correction Multiplier | 0.04 | DEG% | Engine/Transmission Diagnostics |
| RPM Error Limit For Spark Advance Correction | 512.00 | RPM | Engine/Transmission Diagnostics |
| Idle Spark Correction Limit | 5.27 | DEG | Engine/Transmission Diagnostics |
| Load Threshold For Closed Throttle Spark | 250.00 | MG/CYL | Engine/Transmission Diagnostics |
| Minimum Closed Throttle Time For Closed Throttle Spark | 0.30 | SEC | Engine/Transmission Diagnostics |
| Closed Throttle Spark Ramp Rate | 21.09 | DEG/SEC | Engine/Transmission Diagnostics |
| Load Threshold For Clutch Switch Spark | 250.00 | MG/CYL | Engine/Transmission Diagnostics |
| If Closed Throttle Detected, And Shift Flare Also Detected, Then Use This SAMAIN Hold Time, Else Use KCTTIME | 0.00 | SEC | Engine/Transmission Diagnostics |
| Rate To Ramp Spark Down To Idle When Shift Flare Detected, Else Use KCTSPRMP | 7199.89 | DEG/SE | Engine/Transmission Diagnostics |
| If RPM Increase In Last 100 Msec Is >= CAL (Referenced To RPM DFCO Filtered RPM), And All Other Closed Throttle Spark Conditions Met, Then Gear Shift Has Occured, So Use KCTTIMEF And KCTSRMPF | 75.00 | RPM | Engine/Transmission Diagnostics |
| Rate To Ramp To Retarded Idle When All Conditions Are Met | 0.99 | DEG/S | Engine/Transmission Diagnostics |
| # Of 3X Refs To Delay PE (Or Rich A/F) Spark | 0.00 | REFS | Engine/Transmission Diagnostics |
| If Delta Cylair > This - Then Max Dwell | 125.00 | MG/CYL | Engine/Transmission Diagnostics |
| Burst Knock Min Coolant Temp | 151.25 | Deg C | Engine/Transmission Diagnostics |
| Burst Knock Max RPM | 6375.00 | RPM | Engine/Transmission Diagnostics |
| Burst Knock Delta TPS | 4.69 | TPS % | Engine/Transmission Diagnostics |
| Burst Knock - Stage1 Duration | 1.00 | REFPLS | Engine/Transmission Diagnostics |
| Burst Knock - Stage2 Duration | 5.00 | REFPLS | Engine/Transmission Diagnostics |
| Burst Knock Retard | 12.13 | DEG | Engine/Transmission Diagnostics |
| Burst Knock - Stage 1 Decay Delta | 1.05 | DEG | Engine/Transmission Diagnostics |
| Burst Knock - Stage 2 Decay Delta | 0.35 | DEG | Engine/Transmission Diagnostics |
| Burst Knock - TPS Offset % | 2.34 | TPS% | Engine/Transmission Diagnostics |
| Knock Maximum Retard | 11.95 | DEG | Engine/Transmission Diagnostics |
| High Resolution RPM Filter Coefficient | 0.50 | COEFF | Engine/Transmission Diagnostics |
| Spark Advance RDSC Lower Limit | 0.70 | DEG | Engine/Transmission Diagnostics |
| Increasing/Decreasing TPS Threshold | 1.17 | TPS% | Engine/Transmission Diagnostics |
| A/D TPS Rate For RDSC & Bump | 2.00 | COUNT | Engine/Transmission Diagnostics |
| Low/High TPS Threshold For RDSC | 1.56 | % | Engine/Transmission Diagnostics |
| Disable RDSC if TPS > This | 99.61 | % | Engine/Transmission Diagnostics |
| Disable RDSC if Coolant < This | 8.00 | DEG/C | Engine/Transmission Diagnostics |
| Disable RDSC if KPH <= This | 0.00 | KPH | Engine/Transmission Diagnostics |
| Disable RDSC if RPM >= This | 6000.00 | RPM | Engine/Transmission Diagnostics |
| Disable RDSC if RPM < This | 500.00 | RPM | Engine/Transmission Diagnostics |
| Selects RPM Ring Buffer Location For 1st Gear | 2.00 | INDEX | Engine/Transmission Diagnostics |
| Selects RPM Ring Buffer Location For 2nd Gear | 4.00 | INDEX | Engine/Transmission Diagnostics |
| Selects RPM Ring Buffer Location For 3rd Gear | 6.00 | INDEX | Engine/Transmission Diagnostics |
| Selects RPM Ring Buffer Location For 4th Gear | 8.00 | INDEX | Engine/Transmission Diagnostics |
| Selects RPM Ring Buffer Location For 5th Gear | 9.00 | INDEX | Engine/Transmission Diagnostics |
| Selects RPM Ring Buffer Location For Neutral | 7.00 | INDEX | Engine/Transmission Diagnostics |
| Tip-in Gain Amount For 1st Gear | 0.00 | DEG/RP | Engine/Transmission Diagnostics |
| Tip-in Gain Amount For 2nd Gear | 0.00 | DEG/RP | Engine/Transmission Diagnostics |
| Tip-in Gain Amount For 3rd Gear | 0.00 | DEG/RP | Engine/Transmission Diagnostics |
| Tip-in Gain Amount For 4th Gear | 0.00 | DEG/RP | Engine/Transmission Diagnostics |
| Tip-in Gain Amount For 5th Gear | 0.00 | DEG/RP | Engine/Transmission Diagnostics |
| Tip-in Gain Amount For Neutral | 0.00 | DEG/RP | Engine/Transmission Diagnostics |
| Spark RDSC Negative Change Limit | 0.00 | DEG | Engine/Transmission Diagnostics |
| Spark RDSC Positive Change Limit | 0.00 | DEG | Engine/Transmission Diagnostics |
| Time RDSC Enabled When Increasing TPS | 1.00 | SEC | Engine/Transmission Diagnostics |
| Tip-out Gain Amount For 1st Gear | 0.00 | DEG/RP | Engine/Transmission Diagnostics |
| Tip-out Gain Amount For 2nd Gear | 0.00 | DEG/RP | Engine/Transmission Diagnostics |
| Tip-out Gain Amount For 3rd Gear | 0.00 | DEG/RP | Engine/Transmission Diagnostics |
| Tip-out Gain Amount For 4th Gear | 0.00 | DEG/RP | Engine/Transmission Diagnostics |
| Tip-out Gain Amount For 5th Gear | 0.00 | DEG/RP | Engine/Transmission Diagnostics |
| Tip-out Gain Amount For Neutral | 0.00 | DEG/RP | Engine/Transmission Diagnostics |
| Time RDSC is Active When Decreasing TPS | 0.00 | SEC | Engine/Transmission Diagnostics |
| Spark RDSC Negative Change Limit (Tip-out) | 0.00 | DEG | Engine/Transmission Diagnostics |
| Spark RDSC Positive Change Limit (Tip-out) | 0.00 | DEG | Engine/Transmission Diagnostics |
| Minimum Vehicle Speed to Enable Bump Spark | 0.00 | KPH | Engine/Transmission Diagnostics |
| Time Bump Spark is Active | 0.25 | SEC | Engine/Transmission Diagnostics |
| Time Bump Spark is held steady before decay | 0.01 | SEC | Engine/Transmission Diagnostics |
| Time Bump Spark Not Allowed After Gear Change | 0.03 | SEC | Engine/Transmission Diagnostics |
| Upper Bump Spark Limit | 74.88 | DEG | Engine/Transmission Diagnostics |
| (For 1st,2nd & 3rd Gears Only) Idle Drive Gain Amount (0-16) | 0.00 | FACTOR | Engine/Transmission Diagnostics |
| Idle Drive Negative Change Limit (Tip-in) | 0.00 | DEG | Engine/Transmission Diagnostics |
| Idle Drive Positive Change Limit (Tip-in) | 0.00 | DEG | Engine/Transmission Diagnostics |
| Idle RDSC Enable RPM Threshold | 1150.00 | RPM | Engine/Transmission Diagnostics |
| EC' DSNEF Intergration C | 200.12 | MICROS | Engine/Transmission Diagnostics |
| Knock Retard Limit Not in PE Mode | 15.00 | DEG | Engine/Transmission Diagnostics |
| Knock Retard Limit When in PE Mode | 15.00 | DEG | Engine/Transmission Diagnostics |
| High Cylair Shift If Downshift & Cylair > This | 199.22 | MG/CYL | Engine/Transmission Diagnostics |
| Clear High Cylair Shift If Shift Occured > This Time Ago | 3.10 | SEC | Engine/Transmission Diagnostics |
| Adaptive Spark Cell - RPM Limit | 2000.00 | RPM | Engine/Transmission Diagnostics |
| Adaptive Spark Cell RPM Hysteresis | 100.00 | RPM | Engine/Transmission Diagnostics |
| Adaptive Spark Cell Load Limit 1 | 343.75 | MG/CYL | Engine/Transmission Diagnostics |
| Adaptive Spark Cell Load Limit 2 | 437.50 | MG/CYL | Engine/Transmission Diagnostics |
| Adaptive Spark Cell Load Hysteresis | 15.62 | MG/CYL | Engine/Transmission Diagnostics |
| Spark Knock Must Be > This - To Use Light Knock Retard Rate | 1.05 | DEG | Engine/Transmission Diagnostics |
| Spark Knock Must Be > This - To Use Heavy Knock Retard Rate | 5.98 | DEG | Engine/Transmission Diagnostics |
| Adaptive Spark - Hi/Lo Main Spark Table Difference Must be > This - To Move Toward Retard | 2.11 | DEG | Engine/Transmission Diagnostics |
| Time Between Retard Updates For Light Knock | 1.11 | SEC | Engine/Transmission Diagnostics |
| Time Between Retard Updates For Heavy Knock | 1.05 | SEC | Engine/Transmission Diagnostics |
| Rate At Which Multiplier Moves Toward Retard Table | 0.14 | %/SEC | Engine/Transmission Diagnostics |
| Time Between Retard Updates Of Multiplier If Cell Has Recently Changed | 4.19 | SEC | Engine/Transmission Diagnostics |
| Use Spark Retard Delay For This Amount Of Time If Cell Has Recently Changed | 4.00 | SEC | Engine/Transmission Diagnostics |
| Adaptive Spark - Hi/Lo Main Spark Table Difference Must Be > This To Move Toward Advance | 2.11 | Deg | Engine/Transmission Diagnostics |
| Adaptive Spark Min RPM | 1000.00 | RPM | Engine/Transmission Diagnostics |
| Adaptive Spark Max RPM | 5625.00 | RPM | Engine/Transmission Diagnostics |
| Time Between Advance Update of Multiplier | 1.99 | SEC | Engine/Transmission Diagnostics |
| % Sec Rate at which Multiplier moves toward advance table | 0.14 | %/SEC | Engine/Transmission Diagnostics |
| % Adaptive Spark Retent Multiplier Applied to Adaptive Spark At S.D. | 80.08 | % | Engine/Transmission Diagnostics |
| Adaptive Spark Multiplier If Option Flag 3 (FIXADP=1) | 0.50 | MULT | Engine/Transmission Diagnostics |
| Minimum Run Time For Applying The Adaptive Spark Multiplier Correction On Next Power Up | 500.00 | S | Engine/Transmission Diagnostics |
| Attack Rate = Zero If Runtime < CAL | 5.00 | SEC | Engine/Transmission Diagnostics |
| Attack Rate = Zero If Coolant < CAL | 20.00 | DEG/C | Engine/Transmission Diagnostics |
| USE HI CYLAIR RECOVERY RATE IF CYLAIR IS > THIS | 199.22 | MG/CYL | Engine/Transmission Diagnostics |
| Recovery Update Interval | 0.70 | S | Engine/Transmission Diagnostics |
| ESC DELAY CAL 12.5MS LOOPS PER RECOVERY UPDATE | 0.10 | S | Engine/Transmission Diagnostics |
| Max MAD | 0.20 | V | Engine/Transmission Diagnostics |
| Min MAD | 0.15 | V | Engine/Transmission Diagnostics |
| Integrator Output Filter Coefficient Modified Applied When Knock Is Present | 1.00 | MULT | Engine/Transmission Diagnostics |
| MAD Filter Coefficient | 0.00 | - | Engine/Transmission Diagnostics |
| If RPM lower than this value disable knock control | 500.00 | RPM | Engine/Transmission Diagnostics |
| Change Limit Of Cylair50 In 12.5ms Interval | 37.50 | MG/CYL | Engine/Transmission Diagnostics |
| Transient Mode Delay Time | 0.50 | S | Engine/Transmission Diagnostics |
| Positive Delta RPM Threshold To Select KESCQINC | 100.00 | RPM/12.5 Msec | Engine/Transmission Diagnostics |
| Negative Delta RPM Threshold To Select KESCQDEC | 100.00 | RPM/12.5 Msec | Engine/Transmission Diagnostics |
| Positive Delta TPS Threshold To Select KESCQINC | 1.17 | TPS%/12.5 Msec | Engine/Transmission Diagnostics |
| Negative Delta TPS Threshold To Select KESCQDEC | 1.17 | TPS%/12.5 Msec | Engine/Transmission Diagnostics |
| Filter Coefficient For Instantaneous A/D Knock Signal When RPM Or TPS Increases | 0.20 | COEFF | Engine/Transmission Diagnostics |
| Filter Coefficient For Instantaneous A/D Knock Signal When RPM Or TPS Decreases | 0.10 | COEFF | Engine/Transmission Diagnostics |
| Filter Coefficient For Instantaneous A/D Knock Signal During Steady State | 0.10 | COEFF | Engine/Transmission Diagnostics |
| If Average < This - Then Gain = Gain + ESCGADJ | 0.80 | V | Engine/Transmission Diagnostics |
| If Average > This - Then Gain = Gain ESCGADJ | 1.46 | V | Engine/Transmission Diagnostics |
| DSNEF ESC Minimum Gain | 0.00 | DB | Engine/Transmission Diagnostics |
| DSNEF ESC Maximum Gain | 26.00 | DB | Engine/Transmission Diagnostics |
| Cylinder Knock Average Initialisation | 4.98 | V | Engine/Transmission Diagnostics |
| Cylinder Knock Average Minimum | 0.51 | V | Engine/Transmission Diagnostics |
| MAD Filtering Low RPM Threshold | 1200.00 | RPM | Engine/Transmission Diagnostics |
| Minimum Load For Which MAD Filtering Is Enabled | 300.00 | MG/CYL | Engine/Transmission Diagnostics |
| Minimum RPM For Which MALF 93 Is Enabled | 1000.00 | RPM | Engine/Transmission Diagnostics |
| Raw Sensor Reading Limit | 3.50 | V | Engine/Transmission Diagnostics |
| Minimum Raw Sensor Reading Delta | 1.50 | V | Engine/Transmission Diagnostics |
| Maximum Number Of Faults | 80.00 | - | Engine/Transmission Diagnostics |
| Number Of Tests After Which The M93 Fault Counters Are Reset | 100.00 | - | Engine/Transmission Diagnostics |
| Retard Degree When ESC MALF Present | 4.92 | DEG | Engine/Transmission Diagnostics |
| The Minimum RPM For Which MALF 61/62 Is Enabled | 1000.00 | RPM | Engine/Transmission Diagnostics |
| The Minimum Airflow For Which MALF 61/62 Is Enabled | 362.50 | MG/CYL | Engine/Transmission Diagnostics |
| The Minimum Coolant Temperature For Which MALF 61/62 Is Enabled | 35.00 | DEG/C | Engine/Transmission Diagnostics |
| Raw Sensor Reading Lower Limit | 0.16 | V | Engine/Transmission Diagnostics |
| Maximum Number Of Faults | 80.00 | - | Engine/Transmission Diagnostics |
| Number Of Tests After Which The M61/62 Fault Counters Are Reset | 100.00 | - | Engine/Transmission Diagnostics |
| Throttle Follower - Hi Gain in Drive When Underspeed | 0.20 | Steps | Engine/Transmission Diagnostics |
| Throttle Follower - Hi Gain in P/N When Underspeed | 0.05 | Steps | Engine/Transmission Diagnostics |
| Throttle Follower - Gain in Drive When Underspeed | 0.10 | Steps | Engine/Transmission Diagnostics |
| Throttle Follower - Gain in P/N When Underspeed | 0.03 | Steps | Engine/Transmission Diagnostics |
| Throttle Follower - Hi Gain in Drive When Overspeed | 0.07 | Steps | Engine/Transmission Diagnostics |
| Throttle Follower - Hi Gain in P/N Drive When Overspeed | 0.05 | Steps | Engine/Transmission Diagnostics |
| Throttle Follower - Gain in Drive When Overspeed | 0.04 | Steps | Engine/Transmission Diagnostics |
| Throttle Follower - Gain in P/N Drive When Overspeed | 0.03 | Steps | Engine/Transmission Diagnostics |
| Throttle Follower - TPS > This Skip all shift Anticipates | 1.57 | TPS% | Engine/Transmission Diagnostics |
| Throttle Follower - P/N to Drive RPM Drop Shift Set | 10.00 | RPM | Engine/Transmission Diagnostics |
| Throttle Follower - Drive to P/N Rise Shift Set | 50.00 | RPM | Engine/Transmission Diagnostics |
| Throttle Follower - Delay for adding Anticipate Steps after Shift | 0.30 | Sec | Engine/Transmission Diagnostics |
| Throttle Follower - Must be in P/N This long before steps can be added | 1.00 | Sec | Engine/Transmission Diagnostics |
| Throttle Follower - Delay for Removing Anticipate Steps after Shift | 0.00 | Sec | Engine/Transmission Diagnostics |
| Throttle Follower - Must be in P/N This long before steps can be Removed | 1.00 | Sec | Engine/Transmission Diagnostics |
| Throttle Follower - Min Time in Gear to Enable Gear to Neutral Step Removal | 0.00 | Sec | Engine/Transmission Diagnostics |
| Throttle Follower - IAC Steps to Remove for Gear to Neutral Transition | 0.00 | Steps | Engine/Transmission Diagnostics |
| Throttle Follower - Min time in Reverse to Enable Rev to Drive Steps | 1.00 | Sec | Engine/Transmission Diagnostics |
| Throttle Follower - Delay time before adding steps after rev to drive shift | 0.60 | Sec | Engine/Transmission Diagnostics |
| Throttle Follower - IAC Steps to add after transition from rev to drive | 22.00 | Steps | Engine/Transmission Diagnostics |
| Throttle Follower - Delay time before adding steps after drive to reverse shift | 0.00 | Sec | Engine/Transmission Diagnostics |
| Throttle Follower - Must be in Drive > This to add Drive to Reverse Steps | 1.00 | Sec | Engine/Transmission Diagnostics |
| Throttle Follower - IAC Steps to Add After Drive to Rev Shift | 22.00 | Steps | Engine/Transmission Diagnostics |
| Max Motor Position | 220.00 | STEPS | Engine/Transmission Diagnostics |
| If Eruntime > This Enable Motor Reset | 0.00 | SEC | Engine/Transmission Diagnostics |
| If Coolant > CAL, RPLCNTR=0, Enable Reset | -0.25 | DEG/C | Engine/Transmission Diagnostics |
| ISSPMP = KISPKSP1 After NONVRAM Failure | 110.00 | STEPS | Engine/Transmission Diagnostics |
| If RPM <= CAL Disable Crank Airflow Check | 50.00 | RPM | Engine/Transmission Diagnostics |
| If REF Pulses <= CAL Disable Airflow Check | 6.00 | REFPLS | Engine/Transmission Diagnostics |
| If Airflow < CALThen Open Up IAC Motor | 3.20 | GM/SEC | Engine/Transmission Diagnostics |
| Load Selector ENG Perf50, 0= ENG Perf50, 1= ENG Perf, 2= Use NBARO Axis | 1.00 | - | Engine/Transmission Diagnostics |
| ENG Perf50 1= ENG Perf, 2= Use NBARO Axis, 3= Super ENG Perf | 1.00 | - | Engine/Transmission Diagnostics |
| Raise Idle SPD By CAL When CCP Needs It | 0.00 | RPM | Engine/Transmission Diagnostics |
| If KPH >= This Disable Hot Offset | 5.00 | KPH | Engine/Transmission Diagnostics |
| RPM Added To CMD Speed When PS Cramped | 25.00 | RPM | Engine/Transmission Diagnostics |
| Time CMD Speed Adjusted For After PS CRMP | 1.00 | SEC | Engine/Transmission Diagnostics |
| Delay Time Before ISESD Decrease Limit CHEK | 0.10 | SEC | Engine/Transmission Diagnostics |
| ENGPRF Below Which Hi ALT Idle Offset Added | 17.00 | FTLB | Engine/Transmission Diagnostics |
| RPM Added To CMD Speed When At Altitude | 0.00 | RPM | Engine/Transmission Diagnostics |
| RPM Added To CMD Speed When In Retarded Idle | 12.50 | RPM | Engine/Transmission Diagnostics |
| Timer For Ramping LBIDLEOFF Into Or Out Of Command Speed | 3.00 | SEC | Engine/Transmission Diagnostics |
| Every KLBSTPTM Sec, INC LBIDLEOFF By This Amount When Low Battery Idle Up Is Present | 12.90 | RPM | Engine/Transmission Diagnostics |
| Battery Voltage Idle Up Low Threshold | 12.00 | V | Engine/Transmission Diagnostics |
| Battery Voltage Idle Up Upper Threshold | 12.50 | V | Engine/Transmission Diagnostics |
| If Battery Voltage Is Below KLOWBATT For A Time > CAL The Low Battery Idle Up Will Be Enabled | 30.00 | SEC | Engine/Transmission Diagnostics |
| If Battery Voltage Is Above KHIBATT For A Time > CAL The Low Battery Idle Up Will Be Disabled | 30.00 | SEC | Engine/Transmission Diagnostics |
| Do Not Use Low Battery RPM Offset In The Engine Runtime < CAL | 48.00 | SEC | Engine/Transmission Diagnostics |
| KPH Threshold below which PID Enabled | 1.51 | KPH | Engine/Transmission Diagnostics |
| ISC TPS Threshold < This PID Enabled | 1.17 | TPS% | Engine/Transmission Diagnostics |
| Vehicle Speed Threshold For The PID Enable | 4.53 | KPH | Engine/Transmission Diagnostics |
| Vehicle Speed Threshold For The PID Disable | 5.03 | KPH | Engine/Transmission Diagnostics |
| Airflow >= CMDFLOW+CAL Do Not Enable PID | 1.50 | KPH | Engine/Transmission Diagnostics |
| If Conditions Met > CAL Time Enable PID | 0.12 | Sec | Engine/Transmission Diagnostics |
| RPM Above Which High RPM In P/N FLAG Set | 2000.00 | RPM | Engine/Transmission Diagnostics |
| Enable PID If Cond Met > Hi RPM In P/N Time | 0.80 | Sec | Engine/Transmission Diagnostics |
| Delay Between Decrements Of Command Air In P/N | 0.30 | SEC | Engine/Transmission Diagnostics |
| Delay Between Decrements Of Command Air In Drive | 0.40 | SEC | Engine/Transmission Diagnostics |
| If ISES < (ISESDD + This), Enable PID | 250.00 | RPM | Engine/Transmission Diagnostics |
| Max Airflow Offset To CMDAIR When Idle Sagging | 0.62 | MPS | Engine/Transmission Diagnostics |
| P/N, Throt: If ISES<ISESDD-CAL Then Incstep At 6.25Ms. | 3187.50 | RPM | Engine/Transmission Diagnostics |
| Drive Throt: If ISES <ISESDD-CAL Then Incst At 6.25Ms | 3187.50 | RPM | Engine/Transmission Diagnostics |
| P/N, Throt: If ISES<ISESDD -CAL Then INCSTEP At 12.5Ms | 3187.50 | RPM | Engine/Transmission Diagnostics |
| Drive, Throt: If ISES < ISESDD-CAL Then INCST At 12.5Ms | 200.00 | RPM | Engine/Transmission Diagnostics |
| P/N, Air: If ISES <ISESDD-CAL Then INCSTEP At 6.25Ms | 3187.50 | RPM | Engine/Transmission Diagnostics |
| Drive, Air: If ISES<ISESDD-CAL Then INCST At 6.25Ms | 3187.50 | RPM | Engine/Transmission Diagnostics |
| P/N, Air: If ISES<ISESDD-CAL Then INCSTEP At 12.5Ms | 3187.50 | RPM | Engine/Transmission Diagnostics |
| Drive, Air: If ISES<ISESDD-CAL Then INCSTEP At 12.5Ms | 200.00 | RPM | Engine/Transmission Diagnostics |
| P/N, PID: If ISES<ISESDD-CAL Then INCSTEP At 6.25Ms | 3187.50 | RPM | Engine/Transmission Diagnostics |
| Drive, PID: If ISES<ISESDD-CAL Then INCSTEP At 6.25Ms | 3187.50 | RPM | Engine/Transmission Diagnostics |
| P/N, PID: If ISES<ISESDD-CAL Then INCSTEP At 12.5Ms | 3187.50 | RPM | Engine/Transmission Diagnostics |
| Drive, PID: If ISES<ISESDD-CAL Then INCSTEP At 12.5MS | 250.00 | RPM | Engine/Transmission Diagnostics |
| If In PID Or Airflow Control Then Cease 6.25 & 12.5 Msec IAC INCSTEP If Airflow > LRNAIR + CAL | 2.00 | GM/SEC | Engine/Transmission Diagnostics |
| RPM Rate (NDOT) To Disable INT In Drive | 16.00 | DRPM/RF | Engine/Transmission Diagnostics |
| RPM Rate (NDOT) To Disable INT In Neutral | 16.00 | DRPM/RF | Engine/Transmission Diagnostics |
| If RPM Error > This Use High INT Gain (Drive) | 50.00 | RPM | Engine/Transmission Diagnostics |
| If RPM Error > This Use High INT Gain (P/N) | 50.00 | RPM | Engine/Transmission Diagnostics |
| If RPM Error < This Skip Integral (Underspeed) | 0.00 | RPM | Engine/Transmission Diagnostics |
| High INT Gain (Drive) When Underspeed | 0.20 | STEPS | Engine/Transmission Diagnostics |
| High INT Gain (P/N) When Underspeed | 0.05 | STEPS | Engine/Transmission Diagnostics |
| INT Gain (Drive) When Underspeed | 0.10 | STEPS | Engine/Transmission Diagnostics |
| INT Gain (P/N) When Underspeed | 0.03 | STEPS | Engine/Transmission Diagnostics |
| High INT Gain (Drive) When Overspeed | 0.07 | STEPS | Engine/Transmission Diagnostics |
| High INT Gain (P/N) When Overspeed | 0.05 | STEPS | Engine/Transmission Diagnostics |
| INT Gain (Drive) When Overspeed | 0.04 | STEPS | Engine/Transmission Diagnostics |
| Integrator Gain (P/N) When Overspeed | 0.03 | STEPS | Engine/Transmission Diagnostics |
| Low TPS Throttle Follower Gain | 2.52 | STEPS/TPS | Engine/Transmission Diagnostics |
| TPS Threshold For Use PF KLOTPSG | 12.50 | %TPS | Engine/Transmission Diagnostics |
| If Airflow < CMDFLOW + CAL Clear T/F | 0.50 | GM/SEC | Engine/Transmission Diagnostics |
| If ENG Run Time <= This Keep A/C Off | 0.00 | SEC | Speedometer |
| Do Not Engage A/C Clutch If RPM > CAL | 4800.00 | RPM | Speedometer |
| Do Not Check A/C Reengage Delay If RPM <= CAL | 4000.00 | RPM | Speedometer |
| Delay A/C Reengage For CAL Time If RPM > KACRPMH2 | 10.00 | SEC | Speedometer |
| If TPS >= CAL Turn Off A/C | 89.84 | %TPS | Speedometer |
| If TPS >= CAL Keep A/C Off | 85.94 | %TPS | Speedometer |
| A/C Kept Off For CAL Time At 'WOT' | 20.00 | SEC | Speedometer |
| If A/C On And Coolant > Then Turn A/C Off | 119.00 | DEG/C | Speedometer |
| If A/C Off And Coolant > This Keep A/C Off | 115.25 | DEG/C | Speedometer |
| After This Time Do Not Check For RPM Flare | 120.00 | SEC | Speedometer |
| If RPM > Command By More Than CAL Then Don't Add IAC Steps When A/C Engaged At Startup | 900.00 | RPM | Speedometer |
| Delay Time Before A/C Clutch Engages | 0.15 | SEC | Speedometer |
| Delay Time Before A/C Clutch Goes Off In P/N | 0.05 | SEC | Speedometer |
| Delay Time Til A/C Goes Off In DR And MPH<KACMPH | 0.05 | SEC | Speedometer |
| Delay Time Til A/C Goes Off In DR And MPH>KACMPH | 0.00 | SEC | Speedometer |
| If FILTMPH < CAL, Use KACOFDLS, Else Use KACOFDHS | 16.00 | MPH | Speedometer |
| If TPS > CAL + KISTATH Then Sub All A/C Steps | 1.17 | %TPS | Speedometer |
| Delay A/C Request For CAL Time After Fan Turned On | 2.00 | SEC | Speedometer |
| Hold Initial ACIAC For CAL Time | 0.40 | SEC | Speedometer |
| Time To Elapse Before Removing Next Step From (F41A) Anticipate Steps | 0.20 | SEC | Speedometer |
| CCI Not Allowed Above This Speed | 14.00 | MPH | Speedometer |
| CCI Allowed Below This Speed | 10.00 | MPH | Speedometer |
| CCI Allowed Below This Air Temp | 35.00 | DEG/C | Speedometer |
| CCI Allowed For This Time Period | 15.00 | SEC | Speedometer |
| Delay Time Before A/C Clutch Engages | 3.19 | SEC | Speedometer |
| Extra STPS For Multiple Stal Saver Recovery | 0.00 | STEPS | Speedometer |
| Speed Below Which Stall Saver Cycles Counted | 10.00 | MPH | Speedometer |
| If ATS <= This Then Exit Slugging Logic | 151.25 | DEG/C | Speedometer |
| If ATS Last Key Off <= CAL Exit Slug Logic | 151.25 | DEG/C | Speedometer |
| If Coolant >= This Then Exit Slugging Logic | -40.00 | DEG/C | Speedometer |
| If RPM <= KSLGRPM Exit Slugging Logic | 100.00 | RPM | Speedometer |
| Slugging Logic Keeps A/C On CAL REF PULS | 10.00 | REF PLS | Speedometer |
| Extra Steps For 1st Normal REQST After SLG P/N | 5.00 | STEPS | Speedometer |
| Extra Steps For 1st Normal REQST After SLG DRV | 5.00 | STEPS | Speedometer |
| Fan 1 Switch On Time Delay After Request | 0.20 | SEC | Engine/Transmission Diagnostics |
| Fan 2 Switch On Time Delay After Request | 0.20 | SEC | Engine/Transmission Diagnostics |
| IAC Anticipate Steps For Fan 1 | 4.00 | STEPS | Engine/Transmission Diagnostics |
| IAC Anticipate Steps For Fan 2 | 4.00 | STEPS | Engine/Transmission Diagnostics |
| Time To Hold IAC Anticipate Steps, Fan 1 Before Commencing To Decay Out | 0.20 | SEC | Engine/Transmission Diagnostics |
| Time To Hold IAC Anticipate Steps, Fan 1 Before Commencing To Decay Out | 0.20 | SEC | Engine/Transmission Diagnostics |
| Controls Decay Rate For Removing Fan 1 Anticipate Steps | 0.50 | SEC | Engine/Transmission Diagnostics |
| Controls Decay Rate For Removing Fan 2 Anticipate Steps | 0.50 | SEC | Engine/Transmission Diagnostics |
| Steady State IAC Offset For Fan 1 | 1.00 | STEPS | Engine/Transmission Diagnostics |
| Steady State IAC Offset For Fan 2 | 1.00 | STEPS | Engine/Transmission Diagnostics |
| If TPS > CAL Skip All Shift Anticipates | 1.56 | %TPS | Engine/Transmission Diagnostics |
| P/N To Drive Drop At Which RPM Drop (Shift) Set | 10.00 | RPM | Engine/Transmission Diagnostics |
| Drive To P/N Rise At Which RPM Rise (Shift) Set | 50.00 | RPM | Engine/Transmission Diagnostics |
| Delay For Adding Anticipate Steps After Shift | 0.30 | SEC | Engine/Transmission Diagnostics |
| Must Be In PN This Long Before Steps Can Be Added | 1.00 | SEC | Engine/Transmission Diagnostics |
| Delay For Remove Anticipate Steps After Shift | 0.00 | SEC | Engine/Transmission Diagnostics |
| Must Be In DRV This Long Before Steps Can Be Removed | 1.00 | SEC | Engine/Transmission Diagnostics |
| Min Time In Gear To Enable Gear To Neutral Step Removal | 0.00 | SEC | Engine/Transmission Diagnostics |
| # Of IAC Steps To Remove For Gear To Neutral Transition | 0.00 | STEPS | Engine/Transmission Diagnostics |
| Min Time In Reverse To Enable Reverse To Drive Steps | 1.00 | SEC | Engine/Transmission Diagnostics |
| Delay Time Before Adding Steps After A Reverse To Drive Shift | 0.60 | SEC | Engine/Transmission Diagnostics |
| IAC Steps To Add After Transition From Reverse To Drive | 2.00 | STEPS | Engine/Transmission Diagnostics |
| Delay Time Before Adding Steps After A Drive To Reverse Shift | 0.00 | SEC | Engine/Transmission Diagnostics |
| Must Be In Drive > CAL Time Before Shift, To Add Drive To Reverse Steps | 1.00 | SEC | Engine/Transmission Diagnostics |
| IAC Steps To Add After Drive To Reverse Shift | 2.00 | STEPS | Engine/Transmission Diagnostics |
| PS Cramp When RPM Below CMD SPD By CAL | 75.00 | RPM | Engine/Transmission Diagnostics |
| Time Enable Conditions Met For PS Cramp | 0.50 | SEC | Engine/Transmission Diagnostics |
| Table Not Used When RPM Flare > CAL | 0.00 | RPM | Engine/Transmission Diagnostics |
| Load Selector | 1.00 | - | Engine/Transmission Diagnostics |
| Load Selector | 0.00 | - | Engine/Transmission Diagnostics |
| Drive To Neutral Shift To PID- Enable Delay Time | 400.00 | MSEC | Engine/Transmission Diagnostics |
| Neutral To Drive Shift To PID Enable Delay Time | 400.00 | MSEC | Engine/Transmission Diagnostics |
| Min Coolant Value For Learning Airflow | 96.75 | Deg C | Engine/Transmission Diagnostics |
| Initial Value For Learned Airflow W/AC | 5.90 | G/S | Engine/Transmission Diagnostics |
| Initial Value for Learned Airflow WO/AC | 4.90 | G/S | Engine/Transmission Diagnostics |
| In Deadband Counter to Enable Airflow Learning | 250.00 | MSEC | Engine/Transmission Diagnostics |
| IF Learn Counter > This Then Learn Airflow | 250.00 | Msec | Engine/Transmission Diagnostics |
| Filter Time Constant For Airflow | 0.03 | COEFF | Engine/Transmission Diagnostics |
| Limit Learned Airflow To CAL Value (MAX) | 9.00 | G/S | Engine/Transmission Diagnostics |
| Limit Learned Airflow To CAL Value (MIN) | 4.00 | G/S | Engine/Transmission Diagnostics |
| IF RPM > Desired Idle RPM + This Dont Learn Airflow | 62.50 | RPM | Engine/Transmission Diagnostics |
| IF RPM <= Desired Idle RPM - This Dont Learn Airflow | 12.50 | RPM | Engine/Transmission Diagnostics |
| Run Time Must Be > This to Enable Learning | 65.00 | Sec | Engine/Transmission Diagnostics |
| Increase Learn Airflow Due to Table 4ADE | 0.30 | G/S | Engine/Transmission Diagnostics |
| Learn Air Offset Due To Fan1 Load Increase | 0.10 | GM/SEC | Engine/Transmission Diagnostics |
| Learn Air Offset Due To Fan2 Load Increase | 0.10 | GM/SEC | Engine/Transmission Diagnostics |
| Learn Air Offset Due To Low Battery Idle | -26.60 | GM/SEC | Engine/Transmission Diagnostics |
| Learn Air Offset Due To Open Loop A/F Operation | -27.00 | GM/SEC | Engine/Transmission Diagnostics |
| Learn Air Offset Applied During Retarded Idle | -27.00 | GM/SEC | Engine/Transmission Diagnostics |
| If RPM Above ISESDD By CAL Then DEC Learn Air | 3187.50 | RPM | Engine/Transmission Diagnostics |
| Air Decrease When PID Transition RPM > CAL | 0.00 | GM/SEC | Engine/Transmission Diagnostics |
| If Integrator > CAL, Subtract & Take Step | 4096.00 | STEPS | Engine/Transmission Diagnostics |
| Threshold For Underflow During Drive | 1.00 | GM/SEC | Engine/Transmission Diagnostics |
| If Airflow < Command Flow CAL Enable Air Control INT | 0.00 | GM/SEC | Engine/Transmission Diagnostics |
| Threshold For Underflow During P/N | 0.50 | GM/SEC | Engine/Transmission Diagnostics |
| Threshold For Overflow During Drive | 0.50 | GM/SEC | Engine/Transmission Diagnostics |
| If Airflow > Command Flow + CAL Enable Air Control INT | 0.00 | GM/SEC | Engine/Transmission Diagnostics |
| Threshold For Overflow During P/N | 0.50 | GM/SEC | Engine/Transmission Diagnostics |
| INT U Flow Hi Gain Steps/GM-SEC Error Drive | 100.00 | STEPS | Engine/Transmission Diagnostics |
| INT U Flow Lo Gain Steps/GM-SEC Error Drive | 50.00 | STEPS | Engine/Transmission Diagnostics |
| INT U Flow Hi Gain Steps/GM-SEC Error P/N | 100.00 | STEPS | Engine/Transmission Diagnostics |
| INT U Flow Lo Gain Steps/GM-SEC Error P/N | 50.00 | STEPS | Engine/Transmission Diagnostics |
| INT O Flow Hi Gain Steps/GM-SEC Error Drive | 60.00 | STEPS | Engine/Transmission Diagnostics |
| INT O Flow Lo Gain Steps/GM-SEC Error Drive | 30.00 | STEPS | Engine/Transmission Diagnostics |
| INT O Flow Hi Gain Steps/GM-SEC Error P/N | 60.00 | STEPS | Engine/Transmission Diagnostics |
| INT O Flow Lo Gain Steps/GM-SEC Error P/N | 30.00 | STEPS | Engine/Transmission Diagnostics |
| Airflow Offset For CAT Protection Open Loop | 0.00 | GM/SEC | Engine/Transmission Diagnostics |
| PE TPS Hysteresis | 3.12 | TPS% | Engine/Transmission Diagnostics |
| PE Cylair Hysteresis | 31.25 | MG/CYL | Engine/Transmission Diagnostics |
| PE If MT Gear >= This - Use High Gear PE Logic | 6.00 | GEAR | Engine/Transmission Diagnostics |
| PE If MT Gear Condition Met & Initial RPM <= CAL, Use High Gear PE Delay Logic (KF47) | 25.00 | RPM | Engine/Transmission Diagnostics |
| Time To Delay PE If High Gear Conditions Met | 0.00 | SEC | Engine/Transmission Diagnostics |
| PE Max TPS% - TPS Above Which F67 Multiplier Must Be >=1 | 1.17 | - | Engine/Transmission Diagnostics |
| PE Max RPM - RPM Above Which F67 Multiplier Must Be >=1 | 4000.00 | - | Engine/Transmission Diagnostics |
| PE Time Delay To Enter PE When All Enable Conditions Met | 0.00 | SEC | Engine/Transmission Diagnostics |
| Time To Delay Between Decrement Of PE Timer - No PE | 1.00 | SEC | Engine/Transmission Diagnostics |
| Delay CAL Time Between Decrements Of PE Time | 0.50 | SEC | Engine/Transmission Diagnostics |
| P/N O/L A/F Ratio If Non Zero | 0.00 | RATIO | Engine/Transmission Diagnostics |
| Limit Leanout Of A/F If Leaner Than CAL | 0.00 | RATIO | Engine/Transmission Diagnostics |
| O/L Lean-Out F/A Ratio By 1 CNT Every CAL Time | 10.00 | SEC | Engine/Transmission Diagnostics |
| Time Delay For Transaction From C/L To O/L Idle When Vehicle In Park/Neutral | 10.00 | SEC | Engine/Transmission Diagnostics |
| Default Time Delay For Transaction From C/L To O/L Idle | 35.00 | SEC | Engine/Transmission Diagnostics |
| Coolant Must Be < CAL To Use F51 A/F Shortrun Mode | 80.00 | DEG/C | Engine/Transmission Diagnostics |
| TPS Filter Constant for Synch Delta TPS AE | 0.06 | COEFFICIENT | Engine/Transmission Diagnostics |
| If Delta TPS > This - Enable Synch TPS AE | 1.56 | % TPS | Engine/Transmission Diagnostics |
| If Negative Delta TPS > This - Skip Synch TPS AE | 3.12 | % TPS | Engine/Transmission Diagnostics |
| If Refs in TPS AE < This - Skip Synch TPS AE | 0.00 | REFPLS | Engine/Transmission Diagnostics |
| If Refs in TPS AE > This - Skip Synch TPS AE | 64.00 | REFPLS | Engine/Transmission Diagnostics |
| CORRCL can't decrease for CAL Ref Pulses | 50.00 | REFPLS | Engine/Transmission Diagnostics |
| AETPERF | 1.00 | - | Engine/Transmission Diagnostics |
| TPS Filter Const For Synch Delta TPS DE | 0.02 | COEFF | Engine/Transmission Diagnostics |
| If Neg DELTATPS > CAL Enable SYNCH TPS DE | 3.12 | % TPS | Engine/Transmission Diagnostics |
| % + Delta TPS To Disable DE | 1.17 | %TPS | Engine/Transmission Diagnostics |
| If #REF Pulses > CAL Enable Synch TPS DE | 1.00 | REFPLS | Engine/Transmission Diagnostics |
| If #REF Pulses > CAL Disable Synch TPS DE | 254.00 | REFPLS | Engine/Transmission Diagnostics |
| CORRCL Can't Increase For CAL REF Pulses | 64.00 | REFPLS | Engine/Transmission Diagnostics |
| Minimum Coolant Temp For Lean Cruise | 80.00 | DEG/C | Engine/Transmission Diagnostics |
| Min Vehicle Speed For Lean Cruise | 52.30 | KPH | Engine/Transmission Diagnostics |
| Minimum Vehicle Speed For Lean Cruise To Check Hysterisis | 44.26 | KPH | Engine/Transmission Diagnostics |
| Time Delay Before Lean Cruise A/R Ratio Step | 0.10 | SEC | Engine/Transmission Diagnostics |
| 0..2 Exit Lean Cruise If FATC (F56F) > KLCFATC | 132.00 | RATIO | Engine/Transmission Diagnostics |
| Lean Cruise/KCLRATIO Multiplier Step Timer For Ramping In/Out Of BLM Maintenance Mode | 3.00 | TIME | Engine/Transmission Diagnostics |
| If Odometer < This - Use Vap Reduced Crank BPW & Reduced FATI Mode | 50.00 | - | Engine/Transmission Diagnostics |
| If Vap Mode Is Active, Multiply F64SRMUL By CAL (1=Full Shortrun Enleanment, 0= No Enleanment | 1.00 | MULT | Engine/Transmission Diagnostics |
| If SFROFTIM < KLODOFML & KLOWODO < ODOMETER, Then Limit FSROFTIM To KLODFML | 1.00 | MULT | Engine/Transmission Diagnostics |
| Altitude Compensation for Lean Cruise Spark Vs Load Selector | 1.00 | - | Engine/Transmission Diagnostics |
| If Fan 2 Off & Coolant > This - Turn On | 107.00 | DEG/C | Speedometer |
| If Fan 2 On & Coolant <= This - Turn Off | 103.25 | DEG/C | Speedometer |
| 1470 KPA Fan 1 High End of Hysteresis | 36.72 | - | Speedometer |
| 1170 KPA Fan 1 Low End of Hysteresis | 28.52 | - | Speedometer |
| 1770 KPA Fan 2 High End of Hysteresis | 48.83 | - | Speedometer |
| 1370 KPA Fan 2 Low End of Hysteresis | 36.72 | - | Speedometer |
| If Fan 1 Off & KPH > This - Keep Fan 1 Off | 28.97 | KPH | Speedometer |
| If Fan 1 On & KPH > This - Turn Fan 1 Off | 49.89 | KPH | Speedometer |
| If Fan 1 Off & KPH > This - Keep Off | 28.97 | KPH | Speedometer |
| If Fan 1 On & KPH > This - Turn Fan 1 Off | 49.89 | KPH | Speedometer |
| If Fan 1 Off & KPH > This - Keep Fan 1 Off | 16.09 | KPH | Speedometer |
| If Fan 1 On & KPH > This - Turn Fan 1 Off | 33.80 | KPH | Speedometer |
| If Fan 1 Off & Coolant > This - Turn On | 104.00 | DEG/C | Speedometer |
| If Fan 1 On & Coolant <= This - Turn Off | 99.50 | DEG/C | Speedometer |
| Fan 1 Off ATS > This - Check A/C else Fan 1 Off | 40.25 | DEG/C | Speedometer |
| Fan 1 On ATS > This - Check A/C else Fan 1 Off | 38.00 | DEG/C | Speedometer |
| If A/C Shuts Off - Keep Fan 1 On for this long | 0.00 | SEC | Speedometer |
| Don't Turn Fan 2 On until Fan 1 On > This Time | 6.00 | SEC | Speedometer |
| If Coolant <= This - Don't allow run-on | 116.75 | DEG/C | Speedometer |
| HIGH RES SPEED INPUT PPK ODOMETER- AUTO | 51318.76 | PPK | Theft |
| HIGH RES SPEED INPUT PPR ENGINE/ TRANS- AUTO | 43.69 | PPR | Theft |
| Road Speed Sensor Constant LOW RES SPEED INPUT PPK MANUAL | 1474.16 | PU/KM | Theft |
| MAGSPD Pulse Devider For VSS Pulse Selectable Between 9-11 | 10.00 | CONST | Theft |
| Ratio Of RPM To MPH For Gear 1 | 360.00 | RPM/MPH | Theft |
| Ratio Of RPM To MPH For Gear 2 | 217.50 | RPM/MPH | Theft |
| Ratio Of RPM To MPH For Gear 3 | 137.50 | RPM/MPH | Theft |
| Ratio Of RPM To MPH For Gear 4 | 107.50 | RPM/MPH | Theft |
| Ratio Of RPM To MPH For Gear 5 | 77.50 | RPM/MPH | Theft |
| Error Deadband For Gear 1 | 242.50 | RPM/MPH | Theft |
| Error Deadband For Gear 2 | 140.00 | RPM/MPH | Theft |
| Error Deadband For Gear 3 | 90.00 | RPM/MPH | Theft |
| Error Deadband For Gear 4 | 70.00 | RPM/MPH | Theft |
| Error Deadband For Gear 5 | 50.00 | RPM/MPH | Theft |
| 1-2 Shift Starting Derivative | 16368.75 | RPMDER | Transmission Diagnostics |
| 2-3 Shift Starting Derivative | 16368.75 | RPMDER | Transmission Diagnostics |
| 3-4 Shift Starting Derivative | 16368.75 | RPMDER | Transmission Diagnostics |
| 1-2 Shift Stopping Derivative | 16368.75 | RPMDER | Transmission Diagnostics |
| 2-3 Shift Stopping Derivative | 16354.00 | RPMDER | Transmission Diagnostics |
| 3-4 Shift Stopping Derivative | 16350.00 | RPMDER | Transmission Diagnostics |
| Duration Downs. 2-1 Modifier Is Applied | 2.00 | SEC | Transmission Diagnostics |
| Duration Downs. 3-2 Modifier Is Applied | 1.50 | SEC | Transmission Diagnostics |
| Duration Downs. 4-3 Modifier Is Applied | 1.00 | SEC | Transmission Diagnostics |
| Minimum Time Before Adaptable Ratio Change | 0.10 | SEC | Transmission Diagnostics |
| Cold Trans Temp Threshold | 62.00 | DEG/C | Transmission Diagnostics |
| Hot Trans Temp Threshold | 110.00 | DEG/C | Transmission Diagnostics |
| Adaptive Throttle Position Low - 1st Gear | 25.10 | TPS% | Transmission Diagnostics |
| Adaptive Throttle Position Low - 2nd Gear | 30.98 | TPS% | Transmission Diagnostics |
| Adaptive Throttle Position Low - 3rd Gear | 100.00 | TPS% | Transmission Diagnostics |
| Adaptive Throttle Position High - 1st Gear | 81.18 | TPS% | Transmission Diagnostics |
| Adaptive Throttle Position High - 2nd Gear | 81.18 | TPS% | Transmission Diagnostics |
| Adaptive Throttle Position High - 3rd Gear | 0.00 | TPS% | Transmission Diagnostics |
| Adaptive Throttle Position Change Threshold | 5.10 | TPS% | Transmission Diagnostics |
| Min Time Between Shifts For 1-2 Adapt | 2.00 | SEC | Transmission Diagnostics |
| Min Time Between Shifts For 2-3 Adapt | 2.00 | SEC | Transmission Diagnostics |
| Min Time Between Shifts For 3-4 Adapt | 2.00 | SEC | Transmission Diagnostics |
| Delay After Range Change For 1-2 Adapt | 6.00 | SEC | Transmission Diagnostics |
| Delay After Range Change For 2-3 Adapt | 6.00 | SEC | Transmission Diagnostics |
| Delay After Range Change For 3-4 Adapt | 6.00 | SEC | Transmission Diagnostics |
| Maximum Speed Change for 1-2 Adapt | 64.37 | KPH | Transmission Diagnostics |
| Maximum Speed Change for 2-3 Adapt | 64.37 | KPH | Transmission Diagnostics |
| Maximum Speed Change for 3-4 Adapt | 64.37 | KPH | Transmission Diagnostics |
| Large 1-2 Shift Time Error Value | 6.10 | SEC | Transmission Diagnostics |
| Large 2-3 Shift Time Error Value | 6.10 | SEC | Transmission Diagnostics |
| Large 3-4 Shift Time Error Value | 6.10 | SEC | Transmission Diagnostics |
| Pressure Modifier For Large Negative 1-2 Shift Time Error | 40.00 | PSI | Transmission Diagnostics |
| Pressure Modifier For Large Negative 2-3 Shift Time Error | 40.00 | PSI | Transmission Diagnostics |
| Pressure Modifier For Large Negative 3-4 Shift Time Error | 40.00 | PSI | Transmission Diagnostics |
| Trans Temp Threshold - Adaptive | 59.75 | DEG/C | Transmission Diagnostics |
| Adaptive Throttle Position | 25.10 | % | Transmission Diagnostics |
| Large Delay Time Error For 1-2 Shift | 2.00 | SEC | Transmission Diagnostics |
| Large Delay Time Error For 2-3 Shift | 2.00 | SEC | Transmission Diagnostics |
| Large Delay Time Error For 3-4 Shift | 2.00 | SEC | Transmission Diagnostics |
| Pressure Modifier For Long Shift Delay 1-2 | -112.00 | PSI | Transmission Diagnostics |
| Pressure Modifier For Long Shift Delay 2-3 | -112.00 | PSI | Transmission Diagnostics |
| Pressure Modifier For Long Shift Delay 3-4 | -112.00 | PSI | Transmission Diagnostics |
| Pressure Modifier For Large Negative 1-2 Shift Time Error | -112.00 | PSI | Transmission Diagnostics |
| Pressure Modifier For Large Negative 2-3 Shift Time Error | -112.00 | PSI | Transmission Diagnostics |
| Pressure Modifier For Large Negative 3-4 Shift Time Error | -112.00 | PSI | Transmission Diagnostics |
| Adjustment To Adaptive Modifier | 0.10 | FACTOR | Transmission Diagnostics |
| Adjustment To Adaptive Modifier | 0.25 | FACTOR | Transmission Diagnostics |
| Adjustment To Adaptive Modifier | 1.00 | FACTOR | Transmission Diagnostics |
| Adjustment To Adaptive Modifier | 0.25 | FACTOR | Transmission Diagnostics |
| Adjustment To Adaptive Modifier | 0.10 | FACTOR | Transmission Diagnostics |
| Adaptive 1-2 Minimum Upshift Time Limit | 0.40 | - | Transmission Diagnostics |
| Adaptive 2-3 Minimum Upshift Time Limit | 0.40 | - | Transmission Diagnostics |
| Adaptive 3-4 Minimum Upshift Time Limit | 0.40 | - | Transmission Diagnostics |
| Adaptive 1-2 Maximum Upshift Time Limit | 1.20 | - | Transmission Diagnostics |
| Adaptive 2-3 Maximum Upshift Time Limit | 1.20 | - | Transmission Diagnostics |
| Adaptive 3-4 Maximum Upshift Time Limit | 0.00 | - | Transmission Diagnostics |
| Baro Threshold Below Which Throttle Desired Shift Time Use Low Tables | 0.00 | KPA | Transmission Diagnostics |
| Baro Threshold Above which Throttle Desired Shift Time Use High Tables | 0.00 | KPA | Transmission Diagnostics |
| 1-2 Upshift RPM Threshold | 6375.00 | RPM | Transmission Diagnostics |
| 2-3 Upshift RPM Threshold | 6375.00 | RPM | Transmission Diagnostics |
| 3-4 Upshift RPM Threshold | 6375.00 | RPM | Transmission Diagnostics |
| 1-2 Upshift TPS Threshold | 100.00 | TPS% | Transmission Diagnostics |
| 2-3 Upshift TPS Threshold | 100.00 | TPS% | Transmission Diagnostics |
| 3-4 Upshift TPS Threshold | 100.00 | TPS% | Transmission Diagnostics |
| Low Mode 1-2 Upshift Threshold | 67.59 | KPH | Transmission Diagnostics |
| Low Mode 2-3 Upshift Threshold | 205.19 | KPH | Transmission Diagnostics |
| Low Mode 2-1 Downshift Threshold | 57.94 | KPH | Transmission Diagnostics |
| Low Mode 3-2 Downshift Threshold | 150.47 | KPH | Transmission Diagnostics |
| 1-2 Maximum Upshift Speed (KPH) | 66.79 | KPH | Transmission Diagnostics |
| 2-3 Maximum Upshift Speed (KPH) | 123.11 | KPH | Transmission Diagnostics |
| 3-4 Maximum Upshift Speed (KPH) | 205.19 | KPH | Transmission Diagnostics |
| 2-1 Maximum Downshift Speed (KPH) | 45.87 | KPH | Transmission Diagnostics |
| 3-2 Maximum Downshift Speed (KPH) | 114.26 | KPH | Transmission Diagnostics |
| 4-3 Maximum Downshift Speed (KPH) | 204.39 | KPH | Transmission Diagnostics |
| Keep Purge Off Until This Engine Run Time Cold Engine (Light CCP Threshold) | 190.00 | SEC | Engine/Transmission Diagnostics |
| Keep Purge Off Until This Engine Run Time Warm Engine (Light CCP Thresholds) | 5.00 | SEC | Engine/Transmission Diagnostics |
| Startup Coolant Temperature Selects The Time Above (Light CCP Thresholds) | 80.00 | DEG/C | Engine/Transmission Diagnostics |
| If Coolant < This - Turn Off Purge | 30.00 | Deg C | Engine/Transmission Diagnostics |
| Filter Coefficient For Low ATS Value | 0.04 | COEFF | Engine/Transmission Diagnostics |
| If Air Temp < This - Turn Off Purge | 12.00 | Deg C | Engine/Transmission Diagnostics |
| Purge DC When ATS Cold And In Idle | 1.17 | %DC | Engine/Transmission Diagnostics |
| Q Value For Filtering CCP Duty Cycle | 3.91 | % | Engine/Transmission Diagnostics |
| If TPS >= This - Keep Off | 91.80 | % TPS | Engine/Transmission Diagnostics |
| If TPS >= This - Turn Off | 94.92 | % TPS | Engine/Transmission Diagnostics |
| Use Heavy Purge If Engine Run Time > CAL | 15.00 | SEC | Engine/Transmission Diagnostics |
| Use Heavy Purge If Air Temp > CAL | 40.25 | DEG/C | Engine/Transmission Diagnostics |
| Use Heavy Purge If Coolant > CAL | 111.50 | DEG/C | Engine/Transmission Diagnostics |
| Skip Clear Canister Check If DC < CAL | 99.61 | %DC | Engine/Transmission Diagnostics |
| Skip Clear Canister Check If VSS < CAL | 79.69 | MPH | Engine/Transmission Diagnostics |
| Canister Clear If BLM > CAL | 122.00 | CTS | Engine/Transmission Diagnostics |
| If Cylair > This, Don't Change Purge DC | 937.50 | MG/CYL | Engine/Transmission Diagnostics |
| Delay Between Purge DC Updates (Idle) | 1.00 | SEC | Engine/Transmission Diagnostics |
| Delay Between Purge DC Updates (Off Idle) | 0.20 | SEC | Engine/Transmission Diagnostics |
| If INT >= This, Increase Purge DC (Idle) | 120.00 | CTS | Engine/Transmission Diagnostics |
| If INT >= This, Increase Purge DC (Off Idle) | 120.00 | CTS | Engine/Transmission Diagnostics |
| If INT < This, Decrease Purge DC (Idle) | 115.00 | CTS | Engine/Transmission Diagnostics |
| If INT < This, Decrease Purge DC (Off Idle) | 115.00 | CTS | Engine/Transmission Diagnostics |
| Decrease Due To INT (Idle) | 0.78 | %DC | Engine/Transmission Diagnostics |
| If INT < KCCPINTL, Subtract This From Purge DC (Off Idle) | 7.81 | %DC | Engine/Transmission Diagnostics |
| Increase Due To INT (Idle) | 0.39 | %DC | Engine/Transmission Diagnostics |
| If INT >= KCCPINTH, Add This To Purge DC (Off Idle) | 1.95 | %DC | Engine/Transmission Diagnostics |
| If BPW < This, Decrease Purge DC | 2.51 | MSEC | Engine/Transmission Diagnostics |
| Max Allowable Purge DC If Fast Idle For CCP | 16.41 | %DC | Engine/Transmission Diagnostics |
| Maximum Allowable Purge DC At Idle | 17.97 | %DC | Engine/Transmission Diagnostics |
| Delay Between Increments Of MXCCPRMP | 0.10 | SEC | Engine/Transmission Diagnostics |
| INC Value For MXCCPRMP | 1.56 | %DC | Engine/Transmission Diagnostics |
| If Not In DFCO, RPM <= CAL,  Dont Enable DFCO | 1200.00 | RPM | Engine/Transmission Diagnostics |
| If In DFCO, RPM <= CAL, Disable DFCO | 1175.00 | RPM | Engine/Transmission Diagnostics |
| Cyl_Air Must Be <= CAL To Enable DFCO | 125.00 | G/S | Engine/Transmission Diagnostics |
| Cyl_Air Must Be > CAL To Disable DFCO | 148.44 | G/S | Engine/Transmission Diagnostics |
| MPH must be < This, To Enable DFCO | 31.88 | MPH | Engine/Transmission Diagnostics |
| MPH must be >= This, To Disable DFCO | 31.88 | MPH | Engine/Transmission Diagnostics |
| Forced Spark Advance When In DFCO Mode | 0.12 | DEG | Engine/Transmission Diagnostics |
| Rate - Spark Ramped Down To KDFCOADV For Gear 1 | 14.06 | DEG/SEC | Engine/Transmission Diagnostics |
| Rate - Spark Ramped Down To KDFCOADV For Gear 2 | 17.58 | DEG/SEC | Engine/Transmission Diagnostics |
| Rate - Spark Ramped Down To KDFCOADV For Gear 3 | 21.09 | DEG/SEC | Engine/Transmission Diagnostics |
| Rate - Spark Ramped Down To KDFCOADV For Gear 4 | 21.09 | DEG/SEC | Engine/Transmission Diagnostics |
| Rate - Spark Ramped Down To KDFCOADV For Gear 5 | 21.09 | DEG/SEC | Engine/Transmission Diagnostics |
| Rate - Spark Ramped Via Declutch | 112.50 | DEG/SEC | Engine/Transmission Diagnostics |
| High Resolution RPM Filter Coeff, Used For Declutch Detection | 32768.00 | COEFF | Engine/Transmission Diagnostics |
| If RPM Decrease Last 100 Msec >= CAL No DFCO | 100.00 | RPM | Engine/Transmission Diagnostics |
| If Conditions Met > CAL Time Enable DFCO | 0.19 | SEC | Engine/Transmission Diagnostics |
| If TPS > CAL  Disable Decel Fuel Cutoff | 1.17 | %TPS | Engine/Transmission Diagnostics |
| If Coolant Temp < CAL  Disable DFCO | 80.00 | DEG/C | Engine/Transmission Diagnostics |
| If MPH < CAL Disable Decel Fuel Cutoff | 25.00 | MPH | Engine/Transmission Diagnostics |
| A/F Ratio Per Loop To Ramp Into DFCO | 20.00 | 1/RATO | Engine/Transmission Diagnostics |
| A/F Ratio Per Loop To Ramp Out Of DFCO | 10.00 | 1/RATO | Engine/Transmission Diagnostics |
| Time Between Dec Of Ramp | 0.00 | SEC | Transmission Diagnostics |
| DC To Subtract From Ramp Every Ramp Rate | 0.00 | % | Transmission Diagnostics |
| Max Slip Before Tightening Up | 50.00 | RPM | Transmission Diagnostics |
| Add CAL To Ramp If Slipping | 20.39 | % | Transmission Diagnostics |
| Time After Bump Ramp Till Next Slip | 0.00 | SEC | Transmission Diagnostics |
| Time Check For Jump Shift After 1-2 | 1.00 | SEC | Transmission Diagnostics |
| Time Check For Jump Shift After 2-3 | 1.00 | SEC | Transmission Diagnostics |
| K13MOD Added For This Time | 1.00 | SEC | Transmission Diagnostics |
| Pressure Added For 1-3 Upshift | 5.00 | PSI | Transmission Diagnostics |
| K14MOD Added For This Time | 0.50 | SEC | Transmission Diagnostics |
| Pressure Added For 1-4 Upshift | 5.00 | PSI | Transmission Diagnostics |
| K24MOD Subtracted For The Time | 0.50 | SEC | Transmission Diagnostics |
| Pressure Added For 2-4 Upshift | 0.00 | PSI | Transmission Diagnostics |
| ESC Modifier For Pressure | 0.00 | PSI | Transmission Diagnostics |
| Drive Garage Shift Time Limit | 0.20 | SEC | Transmission Diagnostics |
| Cold Trans Temp Threshold If Trans Temp > This, Cold Mode Off | 1.25 | DEG/C | Transmission Diagnostics |
| Cold Trans Temp Threshold If Trans Temp < This, Cold Mode On | -4.00 | DEG/C | Transmission Diagnostics |
| Drive (Norm Garage Shift Press Off) | 10.00 | PSI | Transmission Diagnostics |
| Drive (Norm Garage Shift Press Off) | 10.00 | PSI | Transmission Diagnostics |
| Reverse Garage Shift Time Limit | 0.20 | SEC | Transmission Diagnostics |
| Reverse Garage Shift Pressure Offset | 0.00 | PSI | Transmission Diagnostics |
| Reverse Garage Shift Pressure Offset | 10.00 | PSI | Transmission Diagnostics |
| Garage Shift Speed Threshold (P/N) | 8.00 | MPH | Transmission Diagnostics |
| Garage Shift Speed Threshold (Drive/Reverse) | 8.00 | MPH | Transmission Diagnostics |
| Garage Shift Pressure Threshold (P/N) | 5.00 | PSI | Transmission Diagnostics |
| Garage Shift Pressure Threshold (Drive) | 5.00 | PSI | Transmission Diagnostics |
| Garage Shift Pressure Threshold (Reverse) | 5.00 | PSI | Transmission Diagnostics |
| High Speed Lube Limit Delay, 4th Gear | 0.00 | SEC | Transmission Diagnostics |
| High Speed Lube Limit Delay, 5th Gear | 0.00 | SEC | Transmission Diagnostics |
| Pressure Added For 1-2 Upshift | 3.00 | PSI | Transmission Diagnostics |
| Pressure Added For 2-3 Upshift | 3.00 | PSI | Transmission Diagnostics |
| Pressure Added For 3-4 Upshift | 3.00 | PSI | Transmission Diagnostics |
| 1-2 Shift Ratio Threshold | 0.00 | RATIO | Transmission Diagnostics |
| 2-3 Shift Ratio Threshold | 0.00 | RATIO | Transmission Diagnostics |
| 2-1 Shift Ratio Threshold | 0.00 | RATIO | Transmission Diagnostics |
| 3-2 Shift Ratio Threshold | 0.00 | RATIO | Transmission Diagnostics |
| Pressure Subtracted For A/C On, 1st Gear | 0.00 | PSI | Transmission Diagnostics |
| Pressure Subtracted For A/C On, 2nd Gear | 1.00 | PSI | Transmission Diagnostics |
| Pressure Subtracted For A/C On, 3rd Gear | 2.00 | PSI | Transmission Diagnostics |
| Pressure Subtracted For A/C On, 4th Gear | 2.00 | PSI | Transmission Diagnostics |
| Coastdown Shift Time | 2.00 | SEC | Transmission Diagnostics |
| If Slip < CAL, Allow Engine Brake Pressure | 8190.75 | RPM | Transmission Diagnostics |
| Breakpoint Number 1 For Temp. Mod. | 12.94 | % | Transmission Diagnostics |
| Breakpoint Number 2 For Temp. Mod. | 25.10 | % | Transmission Diagnostics |
| Breakpoint Number 3 For Temp. Mod. | 36.86 | % | Transmission Diagnostics |
| Breakpoint Number 4 For Temp. Mod. | 50.20 | % | Transmission Diagnostics |
| Maximum Force Motor Pressure | 90.00 | PSI | Transmission Diagnostics |
| 1-2 Upshift Pressure MOD Time Limit | 2.50 | SEC | Transmission Diagnostics |
| 2-3 Upshift Pressure MOD Time Limit | 4.00 | SEC | Transmission Diagnostics |
| 3-4 Upshift Pressure MOD Time Limit | 4.00 | SEC | Transmission Diagnostics |
| KALTPRS2 | 1.00 | FAC | Transmission Diagnostics |
| KALTPRS3 | 1.00 | FAC | Transmission Diagnostics |
| KALTPRS4 | 1.00 | FAC | Transmission Diagnostics |
| Barometric Pressure Filter Coefficient | 0.00 | COEFF | Transmission Diagnostics |
| Maximum Allowed Current | 1.10 | AMPS | Transmission Diagnostics |
| Deadband High Value Of Current Error | 0.00 | AMPS | Transmission Diagnostics |
| Deadband Low Value Of Current Error | 0.00 | AMPS | Transmission Diagnostics |
| Maximum Allowed Pressure Control Solenoid Duty Cycle | 90.00 | % | Transmission Diagnostics |
| Minimum Allowed Pressure Control Solenoid Duty Cycle | 0.00 | % | Transmission Diagnostics |
| Ignition Voltage Threshold At 152c | 11.40 | VOLTS | Transmission Diagnostics |
| Ignition Voltage Threshold At -40c | 7.30 | VOLTS | Transmission Diagnostics |
| Ignition Voltage Threshold At 152c | 11.90 | VOLTS | Transmission Diagnostics |
| Ignition Voltage Threshold At -40c | 7.80 | VOLTS | Transmission Diagnostics |
| Time That Voltage Is Below Fail Threshold | 0.50 | SEC | Transmission Diagnostics |
| Pressure Control Solenoid Frequency | 10 | HZ | Transmission Diagnostics |
| If Delta TPS >= KCPTPSMN Use F9CCPFMN | 0.39 | %TPS | Engine/Transmission Diagnostics |
| If Not Using F9CCPFMN Use This As Min Purge DC | 5.86 | %DC | Engine/Transmission Diagnostics |
| Minimum Purge Duty Cycle After Filtering Of CCPSLEW | 5.08 | %DC | Engine/Transmission Diagnostics |
| RPM Low Hyst > This IDLE Cell Disabled | 900.00 | RPM | Engine/Transmission Diagnostics |
| RPM Hi Hyst > This IDLE Cell Disabled | 1000.00 | RPM | Engine/Transmission Diagnostics |
| If Engine Speed < This Enable M24 | 3000.00 | RPM | Transmission Calibration |
| If Conditions Met > This Time Set M24 | 3.00 | SEC | Transmission Calibration |
| If M24CNT > This, Disable M24 Recovery | 255.00 | CNTS | Transmission Calibration |
| Reverse Ratio (For Coping With M24) | 1339.96 | RATIO | Transmission Calibration |
| If NMAPLD < This, Disable M24 Test | 0.00 | KPA | Transmission Calibration |
| If NMAPLD > This, Disable M24 Test | 255.00 | KPA | Transmission Calibration |
| If THROTMOD < This, Disable M24 Test | 10.16 | % | Transmission Calibration |
| If THROTMOD > This, Disable M24 Test | 99.61 | % | Transmission Calibration |
| First Ratio (For Coping With M24) | 1790.54 | RATIO | Transmission Calibration |
| Second Ratio (For Coping With M24) | 953.75 | RATIO | Transmission Calibration |
| Third Ratio (For Coping With M24) | 585.14 | RATIO | Transmission Calibration |
| Fourth Ratio (For Coping With M24) | 409.57 | RATIO | Transmission Calibration |
| Fifth Ratio (For Coping With M24) | 409.57 | RATIO | Transmission Calibration |
| If Conditions Met For > This CAL Set M28 | 6.00 | SEC | Transmission Calibration |
| If M28 CNT > This, Disable M28 Recovery | 255.00 | CNTS | Transmission Calibration |
| Barometric Sensor High Reading Limit | 0.00 | CNTS | Transmission Calibration |
| Throttle Position Threshold For High Barometric Pressure reading | 0.00 | % | Transmission Calibration |
| RPM Threshold For High Barometric Pressure Reading | 6375.00 | RPM | Transmission Calibration |
| High Barometric Pressure Time Limit | 0.00 | SEC | Transmission Calibration |
| Barometric Sensor Low Reading Limit | 0.00 | CNTS | Transmission Calibration |
| Throttle Position Threshold For Low Barometric Pressure Reading | 0.00 | % | Transmission Calibration |
| RPM Threshold For Low Barometric Pressure Reading | 0.00 | RPM | Transmission Calibration |
| Low Barometric Pressure Time Limit | 0.00 | SEC | Transmission Calibration |
| If MPH < CAL, Look For Hi MPH Brake On | 93.50 | MPH | Transmission Calibration |
| If MPH > CAL, Brake Still On, Time Malf | 93.50 | MPH | Transmission Calibration |
| If Conditions Met For > This CAL Set M37 | 18.70 | SEC | Transmission Calibration |
| If Conditions Met For > This CAL Set M37 | 18.70 | SEC | Transmission Calibration |
| If Conditions Met For > This CAL Set M37 | 187.00 | CNTS | Transmission Calibration |
| If M37 CNT > This, Disable M37 Recovery | 187.00 | CNTS | Transmission Calibration |
| If MPH > CAL, Look For Lo MPH Brake Off | 93.50 | MPH | Transmission Calibration |
| If MPH < CAL, Brake Still Off, Time Malf | 93.50 | MPH | Transmission Calibration |
| If Conditions Met For > This CAL Set M38 | 18.70 | SEC | Transmission Calibration |
| If Conditions Met For > This CAL Set M38 | 18.70 | SEC | Transmission Calibration |
| If Conditions Met For > This CAL Set M38 | 187.00 | CNTS | Transmission Calibration |
| If M38 CNT > This, Disable M38 Recovery | 187.00 | CNTS | Transmission Calibration |
| If System Voltage > This Enable M52 | 16.00 | VOLTS | Transmission Calibration |
| If Conditions Met For > This CAL Set M52 | 6553.50 | SEC | Transmission Calibration |
| If System Voltage > This Enable M53 | 19.50 | VOLTS | Transmission Calibration |
| If Conditions Met For > This CAL Set M53 | 2.00 | SEC | Transmission Calibration |
| If Trans Temp A/D < This Enable M58 (Trans Temp Too High) | 17.00 | CNTS | Transmission Calibration |
| If Conditions Met For > This CAL Set M58 | 10.00 | SEC | Transmission Calibration |
| Default Trans Temp For Malfunction | 130.25 | DEG/C | Transmission Calibration |
| If Trans Temp A/D > This Enable M59 (Trans Temp Too Low) | 251.00 | CNTS | Transmission Calibration |
| If Conditions Met For > This CAL Set M59 | 10.00 | SEC | Transmission Calibration |
| If Conditions Met For > This CAL Set M66 | 4.00 | SEC | Transmission Calibration |
| If M66 CNT > This, Disable M66 Recovery | 255.00 | CNTS | Transmission Calibration |
| If Conditions Met For > This CAL Set M67 | 4.00 | SEC | Transmission Calibration |
| If M67 CNT > This, Disable M67 Recovery | 255.00 | CNTS | Transmission Calibration |
| If Slip > CAL Then TCC Not Locked | 80.00 | RPM | Transmission Calibration |
| If M85 CNT > This, Disable M85 Recovery | 10.00 | CNTS | Transmission Calibration |
| Minimum Modified Throttle For Malf 85 | 19.92 | % | Transmission Calibration |
| Maximum Modified Throttle For Malf 85 | 99.61 | % | Transmission Calibration |
| Minimum Transmission Fluid Temperature For Malf 85 | 59.75 | DEG | Transmission Calibration |
| Maximum Transmission Fluid Temperature For Malf 85 | 151.25 | DEG | Transmission Calibration |
| If Conditions Met For > This CAL, Set M85 | 0.10 | SEC | Transmission Calibration |
| If Slip > CAL Then TCC Unlocked | 20.00 | RPM | Transmission Calibration |
| If Slip <= CAL Then TCC Unlocked | 8172.00 | RPM | Transmission Calibration |
| If Conditions Met For > This CAL Set M69 | 4.00 | SEC | Transmission Calibration |
| If Throtmod <= This Disable M69 | 25.00 | % | Transmission Calibration |
| If Engine Speed < This Enable M71 | 6007.38 | RPM | Transmission Calibration |
| If Conditions Met For > This CAL Set M71 | 4.67 | SEC | Transmission Calibration |
| If Engine Speed > This Enable Malfs | 23.38 | RPM | Transmission Calibration |
| If ABS (Nolast-Noraw) > This Enable M72 | 6007.38 | RPM | Transmission Calibration |
| If ABS (Nolast-Noraw) > This Enable M72 Used In Park/Neutral | 6007.38 | RPM | Transmission Calibration |
| If NE < This Skip Test Of Malf M72 | 6007.38 | RPM | Transmission Calibration |
| If M72 CNT > This, Disable M72 Recovery | 187.00 | CNTS | Transmission Calibration |
| If Condition Met > This Time Set M72 | 4.67 | SEC | Transmission Calibration |
| If Act Command Current > CAL, Flag Malf | 0.16 | AMPS | Transmission Calibration |
| If Conditions Met For > This CAL Set M73 | 2.00 | SEC | Transmission Calibration |
| If M73 CNT > This, Disable M73 Recovery | 255.00 | CNTS | Transmission Calibration |
| Low Temperature Voltage Point | 7.30 | VOLTS | Transmission Calibration |
| High Temperature Voltage Point | 10.00 | VOLTS | Transmission Calibration |
| Low Temperature Recovery Voltage | 8.40 | VOLTS | Transmission Calibration |
| High Temperature Recovery Voltage | 11.00 | VOLTS | Transmission Calibration |
| If Conditions Met For > This CAL Set M75 | 4.00 | SEC | Transmission Calibration |
| If NE < This Disable M72 Test | 1000.00 | RPM | Transmission Calibration |
| If Conditions Met For > This CAL Set M77 | 4.67 | SEC | Transmission Calibration |
| Temperature Below Which Diag Is Cleared | 137.00 | DEG/C | Transmission Calibration |
| Temperature Above Which Diag Is Set | 146.00 | DEG/C | Transmission Calibration |
| If Conditions Met For > This CAL Set M79 | 1800.00 | SEC | Transmission Calibration |
| If Condition Met For > This CAL Set M81 | 4.00 | SEC | Transmission Calibration |
| If M85 CNT > This, Disable M81 Recovery | 255.00 | CNTS | Transmission Calibration |
| If Condition Met For > This CAL Set M82 | 4.00 | SEC | Transmission Calibration |
| If M85 CNT > This, Disable M82 Recovery | 255.00 | CNTS | Transmission Calibration |
| If Condition Met For > This CAL Set M83 | 4.00 | SEC | Transmission Calibration |
| If M85 CNT > This, Disable M83 Recovery | 255.00 | CNTS | Transmission Calibration |
| If Conditions Met For > This CAL Set M86 | 4.00 | SEC | Transmission Calibration |
| If M66 CNT > This, Disable M86 Recovery | 255.00 | CNTS | Transmission Calibration |
| If Conditions Met For > This CAL Set M87 | 4.00 | SEC | Transmission Calibration |
| If M67 CNT > This, Disable M87 Recovery | 255.00 | CNTS | Transmission Calibration |
| If Trans Temp <= CAL, Skip M89 | 100.25 | DEG/C | Transmission Calibration |
| If TPS <= CAL, Skip M89 | 73.05 | % | Transmission Calibration |
| If MPH <= CAL, Skip M89 | 93.50 | MPH | Transmission Calibration |
| If 1-2 Time <= CAL, Skip M89 | 4.67 | SEC | Transmission Calibration |
| If 2-3 Time <= CAL, Skip M89 | 4.67 | SEC | Transmission Calibration |
| If 3-4 Time <= CAL, Skip M89 | 4.67 | SEC | Transmission Calibration |
| If Condition Met For > This CAL Set M89 (1-2) | 187.00 | CNTS | Transmission Calibration |
| If Condition Met For > This CAL Set M89 (2-3) | 187.00 | CNTS | Transmission Calibration |
| If Condition Met For > This CAL Set M89 (3-4) | 187.00 | CNTS | Transmission Calibration |
| If 9A CNT > This, Disable M89 Recovery | 187.00 | CNTS | Transmission Calibration |
| Lag Filter Coefficient For NMPH, N.D. (0-1) | 0.75 | COEFF | Transmission Calibration |
| Fourth Highest Gear Attained By The Transmission | 4.00 | GEAR | Transmission Calibration |
| Third Default Gear For Failure Conditions | 3.00 | GEAR | Transmission Calibration |
| Second Output Speed Malfunction Default Gear | 2.00 | GEAR | Transmission Calibration |
| Delay Indicating Loss Of Serial Comm | 1.00 | SEC | Transmission Calibration |
| Anti-Theft Attempts To Disable Start | 50.00 | CNTS | Transmission Calibration |
| Anti-Theft Override Time To Start If This Is Set To $FFFF, The Override Time Is Infinite. | 51.00 | SEC | Transmission Calibration |
| Anti-Theft PCM-BCM Link Time If This Is Set To $FFFF, The Override Time Is Infinite | 51.00 | SEC | Transmission Calibration |
| Engine Cranking For This Length Of Time At Startup Without Checking ATM Staus. | 0.00 | SEC | Transmission Calibration |
| Fuel Used | 1002.00 | CONST | Transmission Calibration |
| Litre/HR Fuel Rate | 20585.00 | 0.0I | Transmission Calibration |
| Fuel Used - About 27% Greater | 0.00 | CONST | Transmission Calibration |
| Litre/HR Fuel Rate | 0.00 | 0.0I | Transmission Calibration |
| Fuel Remaining In Fuel Tank | 6.00 | LITRES | Transmission Calibration |
| MSG A1 Airbag Deploy Timer To Fueldis | 10.00 | SEC | Transmission Calibration |
| Serial Data High Coolant Threshold | 116.75 | DEG | Transmission Calibration |
| Malfunction Logging Delay Time #1 | 0.20 | SEC | Transmission Calibration |
| Malfunction Logging Delay Time #2 | 0.50 | SEC | Transmission Calibration |
| Malfunction Logging Delay Time #3 | 10.00 | SEC | Transmission Calibration |
| Malfunction Logging Delay Time #4 | 10.50 | SEC | Transmission Calibration |
| # Of Writes to Eeprom Malf Logging | 99.00 | CTS | Transmission Calibration |
| Delay Before Checking For Malf | 250.00 | SEC | Transmission Calibration |
| O2 Sensor Low Limit | 0.41 | VOLTS | Transmission Calibration |
| O2 Sensor High Limit | 0.48 | VOLTS | Transmission Calibration |
| Throttle Postion Limit | 14.84 | % | Transmission Calibration |
| KKO2OLTM Time Limit | 32.00 | SEC | Transmission Calibration |
| Coolant Threshold | 85.25 | DEG/C | Transmission Calibration |
| Default Engine Temp For Malf 14/15 | 143.00 | DEG/C | Transmission Calibration |
| Malf 14 Coolant Hot Malf 14 Time Since Run Enable | 20.00 | SEC | Transmission Calibration |
| Malf 14 Coolant Temp Hot Limit | 140.00 | DEG/C | Transmission Calibration |
| Malf 15 Coolant Cold Malf 15 Time Since Run Enable | 10.00 | SEC | Transmission Calibration |
| Malf 15 ADCOOL Cold Limit | 237.00 | A/D | Transmission Calibration |
| Malf 14/15 Max Default Coolant | 91.25 | DEG/C | Transmission Calibration |
| Cooldeg Change Comparator | 8.00 | COUNTS | Transmission Calibration |
| Malf 16 Delay Timer | 11.00 | SEC | Transmission Calibration |
| Malf 17 Malf Counter | 6.00 | COUNTS | Transmission Calibration |
| Malf 17 Enable Delay Time | 0.00 | SEC | Transmission Calibration |
| Max TPS Delta For Malf 19 Entry | 1.17 | % | Transmission Calibration |
| Min Air For Malf 19 Clear | 300.78 | MG/CYL | Transmission Calibration |
| Time Thresh For Malf 19 Active-Log | 20.00 | SEC | Transmission Calibration |
| Default Throttle Position For Failure | 35.16 | % | Transmission Calibration |
| Malf 21 High TPS Limit | 97.27 | % | Transmission Calibration |
| Malf 21 Time Limit | 2.00 | SEC | Transmission Calibration |
| Malf 22 Low TPS Limit | 2.34 | % | Transmission Calibration |
| Low Temp Limit See F9ATSTBL | 5.00 | AD CNT | Transmission Calibration |
| # Of Occurreences Of Malf 23 To Log | 10.00 | CNTS | Transmission Calibration |
| Default ATS Temp, See F9ATSTBL | 120.00 | AD CNTS | Transmission Calibration |
| High Temp Limit, See F9ATSTBL | 250.00 | AD CNTS | Transmission Calibration |
| # Of Occurrences Of Malf 25 To Log | 10.00 | CNTS | Transmission Calibration |
| Max ADMAT Counts Jumps In 100ms | 7.00 | CTS | Transmission Calibration |
| Delay Timer | 10.00 | SEC | Transmission Calibration |
| Malf 26 Active Threshold | 10.00 | CTS | Transmission Calibration |
| Battery Voltage Threshold For M27 'B' | 9.90 | VOLTS | Transmission Calibration |
| Manifold Pressure Threshold For M27 'B' | 6.25 | KPA | Transmission Calibration |
| Time Threshold For M27 'B' | 0.30 | SEC | Transmission Calibration |
| Lower Speed Ratio Threshold For M27 'C' | 0.00 | RATIO | Transmission Calibration |
| Upper Speed Ratio Threshold For M27 'C' | 0.00 | RATIO | Transmission Calibration |
| Time Threshold For M27 'C' | 20.00 | SEC | Transmission Calibration |
| Message 31 Timer Threshold | 10.00 | SEC | Transmission Calibration |
| Minimum Airflow For Default Air | 3.50 | GM/SEC | Transmission Calibration |
| GM/SEC Per IAC Step For DEF. Air | 0.06 | GM/S/S | Transmission Calibration |
| Maximum Air Due To IAC Position | 9.30 | GM/SEC | Transmission Calibration |
| If Freq. Delta < This It's Broken | 3.00 | COUNTS | Transmission Calibration |
| Malf 32 Timer | 2.00 | SEC | Transmission Calibration |
| Minimum Airflow (Closed TPS Leakage) For DEF. TPS | 2.40 | GM/SEC | Transmission Calibration |
| GM/SEC Per IAC Step For Default TPS | 0.09 | MULT | Transmission Calibration |
| ESC Failure Default Retard | 5.01 | DEG | Transmission Calibration |
| Time That Initial Condition Must Be Met For M35/36 Test | 0.05 | SEC | Transmission Calibration |
| Time That Allows M35 Fault Condition | 5.00 | SEC | Transmission Calibration |
| Maximum Allowable IAT For M35/36 Test | 73.25 | DEG | Transmission Calibration |
| Negative RPM Offset From ISESDD | 200.00 | RPM | Transmission Calibration |
| Increase Required To Not Set M35 Fault If Possible Vacuum Leak Flagged | 50.00 | RPM | Transmission Calibration |
| Idle Speed Filter Constant For M35/36 Test | 31.25 | RPM | Transmission Calibration |
| Time Till M36 Fault Set If KK35RPMI Condition  Not Met | 2.70 | SEC | Transmission Calibration |
| Time That Allows M36 Fault Condition | 5.00 | SEC | Transmission Calibration |
| Rate At Which IACV Is Opened For M36 Test | 0.05 | SEC/STEP | Transmission Calibration |
| Positive RPM Offset From ISESDD To Flag Possible Vacuum Leak | 200.00 | RPM | Transmission Calibration |
| # Of IACV Steps To Be Taken For M36 Test | 50.00 | STEP | Transmission Calibration |
| If EST Fall Counts >= This, Set M41 | 0.00 | FALCTS | Transmission Calibration |
| Number Of REFS Required To Check Fall Counts | 0.00 | REFS | Transmission Calibration |
| Low RPM For M42 Enabling | 33.98 | RPM | Transmission Calibration |
| Hi RPM For M42 To Switch Between 2 Win | 4.25 | RPM | Transmission Calibration |
| Short Error Window Length | 100.00 | MS | Transmission Calibration |
| Long Error Window Length | 1593.75 | MS | Transmission Calibration |
| o2 Sensor Low Limit | 0.20 | VOLTS | Transmission Calibration |
| Malf 44 High MAT Limit | 74.75 | DEG | Transmission Calibration |
| Time Limit | 248.00 | SEC | Transmission Calibration |
| o2 Sensor High Limit | 0.78 | VOLTS | Transmission Calibration |
| Time Limit | 40.00 | SEC | Transmission Calibration |
| TPS High Limit | 30.08 | % | Transmission Calibration |
| TPS Low Limit | 8.98 | % | Transmission Calibration |
| Mal 46 - Time Threshold | 2.00 | SEC | Transmission Calibration |
| Malf 46 - Battery Voltage Threshold | 11.00 | VOLTS | Transmission Calibration |
| MAF Threshold For M46 | 2048.00 | HERTZ | Transmission Calibration |
| Number Of 3X Ref Pulses, Without 18X Needed To Set Malf 47 | 253.00 | REFS | Transmission Calibration |
| Time W/O Cam Pulses > KKM48TME Set M48 | 5.00 | SEC | Transmission Calibration |
| Number Of Times Cam Sensor Intermittent | 30.00 | COUNTS | Transmission Calibration |
| M49 Timer | 2.00 | SEC | Transmission Calibration |
| Increment Steps For Malf 54 Counter | 4.00 | COUNTS | Transmission Calibration |
| Malf 54 Counter Threshold | 25.00 | COUNTS | Transmission Calibration |
| Malf 54 Voltage Delta Threshold | 2.50 | VOLTS | Transmission Calibration |
| Malf 54 Decay Count Threshold | 3.00 | COUNTS | Transmission Calibration |
| Threshold For AD Failures Before Malf | 5.00 | CTS | Transmission Calibration |
| High Malf Threshold For AD VREFLOW | 0.10 | VOLTS | Transmission Calibration |
| Low Malf Threshold For AD VREFHIGH | 4.88 | VOLTS | Transmission Calibration |
| Engine Runtime Threshold For Malf 56 | 0.00 | SEC | Transmission Calibration |
| Low Cylair Threshold | 36.10 | MG/CYL | Transmission Calibration |
| Time Threshold For Malf 56 Active Log | 10.00 | SEC | Transmission Calibration |
| Air/Fuel Ratio Threshold For Malf 56 | 13.00 | RATIO | Transmission Calibration |
| If ADINJ < (ADBAT - KKM57VLT) Then Log M57 | 2.20 | VOLTS | Transmission Calibration |
| Time Threshold For Malf 57 Active Log | 3.00 | SEC | Transmission Calibration |
| Max Closed Loop Correction Delta | 80.00 | COUNT | Transmission Calibration |
| Time To Set Code 76 | 32.00 | SEC | Transmission Calibration |
| Max Block Learn Multiplier Delta | 75.00 | COUNT | Transmission Calibration |
| Time To Set Malf 84 | 1.00 | SEC | Transmission Calibration |
| Time To Set Malf 91 | 0.00 | SEC | Transmission Calibration |
| # Of Sending Message W/O Responce | 100.00 | CNTS | Transmission Calibration |
| Time To Wait For Setting Malf 94 | 4.00 | SEC | Transmission Calibration |
| Malf 94 RPM > CAL (Low Limit) | 1400.00 | RPM | Transmission Calibration |
| Malf 94 RPM < CAL (High Limit) | 3000.00 | RPM | Transmission Calibration |
| Malf 94 TPS < CAL Threshold For Malf 94 | 1.17 | % | Transmission Calibration |
| Cylair < CAL Threshold For Malf 94 | 95.10 | MG/CYL | Transmission Calibration |
| Time To Wait For Setting Malf 95 | 2.00 | SEC | Transmission Calibration |
| Delay Time To Wait For Slow Hardware To Read PWM Input From Ignition On | 0.00 | SEC | Transmission Calibration |
| Maximum Engine Temperature For Detect | 119.75 | DEG | Transmission Calibration |
| Maximum Manifold Air Temp For Detect | 89.75 | DEG | Transmission Calibration |
| Maximum RPM For Detection | 2000.00 | RPM | Transmission Calibration |
| Maximum Engine Run Time For Detection | 2.00 | SEC | Transmission Calibration |
| Minimum Time For Fault To Occure | 10.00 | SEC | Transmission Calibration |
| Time To Wait For Setting Malf 97 | 5.00 | SEC | Transmission Calibration |
| Malf 97 Counter | 240.00 | CNTS | Transmission Calibration |
| Airflow Filter Constant | 0.19 | - | Transmission Calibration |
| Airflow Drop To Pass Test | 472.66 | MG/CYL/CYCLE | Transmission Calibration |
| Idle Settle Time Before Check Max/Min Band | 1.00 | SEC | Transmission Calibration |
| Idle Time Before Commencing Test | 4.00 | SEC | Transmission Calibration |
| Intergrator Filter Constant | 0.06 | COEFF | Transmission Calibration |
| Intergrator Delta To Pass Test | 5.00 | CNTS | Transmission Calibration |
| Time To Hold CCP At KK98MXCP | 4.80 | SEC | Transmission Calibration |
| Max Allowable RPM During Test | 800.00 | RPM | Transmission Calibration |
| Max CCP DC For Test | 93.75 | %DC | Transmission Calibration |
| Number Of Failures Before Malf Logged | 3.00 | CNTS | Transmission Calibration |
| Time To Hold CCP Off During Test | 4.00 | SEC | Transmission Calibration |
| CCP Test Ramp Down Rate | 0.73 | %DC/SEC | Transmission Calibration |
| Allowable RPM Delta During Test | 50.00 | RPM | Transmission Calibration |
| CCP Test Ramp Up Rate | 0.49 | %DC/SEC | Transmission Calibration |
| Engine Run Time Threshold For Stall Detect | 0.00 | SEC | Transmission Calibration |
| Lo Hyst KPH | 2.01 | KPH | Engine/Transmission Diagnostics |
| Hi Hyst KPH | 2.51 | KPH | Engine/Transmission Diagnostics |
| TPS Low Hyst | 1.17 | TPS% | Engine/Transmission Diagnostics |
| TPS Hi Hyst | 1.56 | TPS% | Engine/Transmission Diagnostics |
| Airflow Lo Hyst | 8.00 | - | Engine/Transmission Diagnostics |
| Airflow Hi Hyst | 9.00 | - | Engine/Transmission Diagnostics |
| If Coolant <= This - Disable Hot Open Loop | 151.25 | DEG/C | Engine/Transmission Diagnostics |
| Coolant Must Be > This - To Enable Hot Open Loop | 151.25 | DEG/C | Engine/Transmission Diagnostics |
| If KPH <= This - Disable Hot Open Loop | 6.44 | KPH | Engine/Transmission Diagnostics |
| KPH Must Be > This - To Enable Hot Open Loop | 8.05 | KPH | Engine/Transmission Diagnostics |
| If Air Temp <= This - Disable Hot Open Loop | 151.25 | DEG/C | Engine/Transmission Diagnostics |
| If Cylair <= This - Disable Hot Open Loop | 351.56 | MG/CYL | Engine/Transmission Diagnostics |
| If All Conditions Met > This - Enable Hot Open Loop | 0.20 | SEC | Engine/Transmission Diagnostics |
| If Hot Open Loop Enabled, Multiply Open Loop AFR By This | 1.25 | MULT | Engine/Transmission Diagnostics |
| Hot Open Loop AFR | 12.51 | RATIO | Engine/Transmission Diagnostics |
| Injector Flow Rate Gram/Sec Of Fuel | 3.66 | CONSTANT | Engine/Transmission Diagnostics |
| If Coolant < This - Disable Cat Protection Mode | 56.00 | DEG/C | Engine/Transmission Diagnostics |
| If Airflow > This - And Timer > Cat High Time, Enable High Airflow Cat Protection | 255.00 | GM/S | Engine/Transmission Diagnostics |
| If Airflow < This - Disable High Airflow Cat Protection | 255.00 | GM/S | Engine/Transmission Diagnostics |
| If Conditions Met Longer Than CAL, Then Enable High Airflow Cat Protection | 51.00 | SEC | Engine/Transmission Diagnostics |
| If Airflow > CAL, INC CAT. PROT. TIMER. Also If Airflow > CAL And Timer > KCATLOTM, Then Enable Low Airflow Cat Protection | 70.00 | GM/S | Engine/Transmission Diagnostics |
| If Airflow < This - Dec Cat Protection Timer & Disable Low Flow Cat Protection If Timer < Cat Low Time | 65.00 | GM/S | Engine/Transmission Diagnostics |
| If Conditions Met >= This - Enable Low Airflow Cat Protection | 0.00 | SEC | Engine/Transmission Diagnostics |
| Base Air Fuel Ratio When In Cat Protection Mode | 14.76 | RATIO | Engine/Transmission Diagnostics |
| Delay Dec Of Cat Protection Timer This CAL Each Loop | 1.20 | SEC | Engine/Transmission Diagnostics |
| DFCO Disabled Until This Time After Cat Protection Ended | 0.00 | SEC | Engine/Transmission Diagnostics |
| Trans Temperature Filter Time Constant | 101.00 | SEC | Transmission Diagnostics |
| Engine Temperature Filter Time Constant | 12.00 | SEC | Transmission Diagnostics |
| Converter Slip Filter Time Constant | 52.00 | SEC | Transmission Diagnostics |
| Number Of NE Samples For Derivative Calculation | 21.00 | - | Transmission Diagnostics |
| Engine Speed Filter Time Constant | 64.00 | SEC | Transmission Diagnostics |
| Input Speed Filter Time Constant | 252.00 | SEC | Transmission Diagnostics |
| XMSN Input Speed Filter Time Constant | 252.00 | SEC | Transmission Diagnostics |
| Max Time Between XMSN Output Pulses | 1.00 | SEC | Transmission Diagnostics |
| XMSN Output Speed Filter Time Constant | 252.00 | SEC | Transmission Diagnostics |
| Four Wheel Drive Low Ratio | 9.00 | RATIO | Transmission Diagnostics |
| NO/VS Ratio | 0.16 | 60RPMI | Transmission Diagnostics |
| Vehicle Speed Filter Time Constant | 252.00 | SEC | Transmission Diagnostics |
| High Kickdown Throttle Threshold | 94.90 | % | Transmission Diagnostics |
| Low Kickdown Throttle Threshold | 89.80 | % | Transmission Diagnostics |
| If Engine Speed >= This Set Power Train In Motion | 200.00 | RPM | Transmission Diagnostics |
| If Vehicle Speed >= This Set Power Train In Motion | 8191.88 | RPM | Transmission Diagnostics |
| If Tur Speed >= This Set Power Train In Motion | 8191.88 | RPM | Transmission Diagnostics |
| Disable Diagnastic M72 For K4WDTME During Transition 4WD Lo-Hi/Hi-Lo | 6.38 | SEC | Transmission Diagnostics |
| Time Passed Since Range Induced Shift | 0.00 | SEC | Transmission Diagnostics |
| Lower Speed Threshold To Enable Noise Pass-by | 127.50 | MPH | Transmission Diagnostics |
| Upper Speed Threshold To Enable Noise Pass-by | 127.00 | MPH | Transmission Diagnostics |
| Lower Baro Pressure Threshold For Noise Pass-by | 200.00 | KPA | Transmission Diagnostics |
| Lower Engine Temperature Threshold For Noise Pass-by | 151.25 | DEG/C | Transmission Diagnostics |
| Lower Throttle Position Threshold For Noise Pass-by | 100.00 | % | Transmission Diagnostics |
| Valid Time To Enable Noise Pass-by | 12.75 | SEC | Transmission Diagnostics |
| Time 3-2 Downshift Will Be Inhibited | 0.00 | SEC | Transmission Diagnostics |
| Time 2-1 Downshift Will Be Inhibited | 0.00 | SEC | Transmission Diagnostics |
| TCC Off Time Before Downshift | 0.00 | SEC | Transmission Diagnostics |
| 3-2 Downshift Delay | 12.75 | SEC | Transmission Diagnostics |
| 4-2 Downshift Delay Low Limit | 0.25 | SEC | Transmission Diagnostics |
| 4-2 Downshift Delay High Limit | 1.00 | SEC | Transmission Diagnostics |
| 2-1 Downshift Inhibit Throttle Enabling Threshold | 100.00 | % | Transmission Diagnostics |
| 2-1 Downshift Inhibit Delta Throttle Enabling Threshold | 0.00 | %/SEC | Transmission Diagnostics |
| 2-1 Downshift Inhibit Delta Vehicle Speed Enabling Threshold | 2550.00 | MPH/SE | Transmission Diagnostics |
| 3-2 Downshift Delay Low Speed Threshold | 48.00 | MPH | Transmission Diagnostics |
| 3-2 Downshift Delay High Speed Threshold | 58.00 | MPH | Transmission Diagnostics |
| 3-2 Downshift Max Delay | 0.75 | SEC | Transmission Diagnostics |
| 3-2 Downshift Min Delay | 0.40 | SEC | Transmission Diagnostics |
| Engine Temp < This - Inhibit 4th Gear | -40.00 | DEG/C | Transmission Diagnostics |
| Engine Temp > This - Enable 4th Gear | -38.50 | DEG/C | Transmission Diagnostics |
| Engine Temp <= This - Use Cold Shift Pattern | -40.00 | DEG/C | Transmission Diagnostics |
| Engine Temp >= This - Use Normal Shift Pattern | -38.50 | DEG/C | Transmission Diagnostics |
| Active 4-3-2 Time Since Change From D4 | 0.00 | SEC | Transmission Diagnostics |
| 4-3-2 Downshift Slip Value | 200.00 | RPM | Transmission Diagnostics |
| 4-3-2 Downshift Seq Lower Speed Threshold | 127.50 | MPH | Transmission Diagnostics |
| 4-3-2 Downshift Seq Upper Speed Threshold | 127.00 | MPH | Transmission Diagnostics |
| Indefinitely Lock-out 2nd Gear Lower Speed Threshold | 127.50 | MPH | Transmission Diagnostics |
| In Case of Copeslnd & Vehicle speed >= This CAL & Current Gear = Gear Default Then Set Desired Gear to Gearmax | 127.50 | MPH | Transmission Diagnostics |
| Min CAL. For Shift Point (Must Be 0) | 0.00 | MPH | Transmission Diagnostics |
| Max CAL. For Shift Point (Must Be 255) | 127.50 | MPH | Transmission Diagnostics |
| Low Mode Upshift Threshold If Vehicle Speed >= This & PRNDL Is 'Low', Shift From 1st To 2nd | 42.00 | MPH | Transmission Diagnostics |
| Low Mode Upshift Threshold If Vehicle Speed >= This & PRNDL Is 'Low', Shift From 2nd To 3rd | 127.50 | MPH | Transmission Diagnostics |
| Low Mode Downshift Threshold If Vehicle Speed < This & PRNDL Is 'Low', Shift From 2nd To 1st | 36.00 | MPH | Transmission Diagnostics |
| Low Mode Downshift Threshold If Vehicle Speed < This & PRNDL Is 'Low", Shift From 3rd To 2nd | 93.50 | MPH | Transmission Diagnostics |
| D2 Mode Upshift Threshold If Vehicle Speed >= This & PRNDL Is 'D2', Shift From 2nd To 3rd | 127.50 | MPH | Transmission Diagnostics |
| D2 Mode Downshift Threshold If Vehicle Speed < This & PRNDL Is 'D2', Shift From 3rd To 2nd | 93.50 | MPH | Transmission Diagnostics |
| D2 Mode Upshift Threshold If Vehicle Speed >= This & PRNDL Is 'D2', Shift From 1st To 2nd | 127.50 | MPH | Transmission Diagnostics |
| D2 Mode Downshift Threshold If Vehicle Speed < This & PRNDL Is 'D2', Shift From 2nd To 1st | 93.50 | MPH | Transmission Diagnostics |
| Detent Mode 1-2 Upshift Threshold If Vehicle Speed >= This & Mode Is Active & NE >= CAL & Normal Mode & Gear Is 1st, Go To 2nd | 41.50 | MPH | Transmission Diagnostics |
| Detent Mode 2-3 Upshift Threshold If Vehicle Speed >= This & Mode Is Active & NE >= CAL & Normal Mode & Gear Is 2nd, Go To 3rd | 76.50 | MPH | Transmission Diagnostics |
| Detent Mode 3-4 Upshift Threshold If Vehicle Speed >= This & Mode Is Active & NE >= CAL & Normal Mode & Gear Is 3rd, Go To 4th | 127.50 | MPH | Transmission Diagnostics |
| Detent Mode 2-1 Downshift Threshold If Vehicle Speed < This & Mode Is Active & Normal Mode & Gear Is 2nd, Go To 1st | 28.50 | MPH | Transmission Diagnostics |
| Detent Mode 3-2 Downshift Threshold If Vehicle Speed < This & Mode Is Active & Normal Mode & Gear Is 3rd, Go To 2nd | 71.00 | MPH | Transmission Diagnostics |
| Detent Mode 4-3 Downshift Threshold If Vehicle Speed < This & Mode Is Active & Normal Mode & Gear Is 4th, Go To 3rd | 127.00 | MPH | Transmission Diagnostics |
| Cold Kickdown Mode 1-2 Upshift Threshold If Vehicle Speed >= This & Kickdown Mode Is Active & NE >= CAL & Cold Mode & Gear Is 1st, Go To 2nd | -64.00 | MPH | Transmission Diagnostics |
| Cold Kickdown Mode 2-3 Upshift Threshold If Vehicle Speed >= This & Kickdown Mode Is Active & NE >= CAL& Cold Mode & Gear Is 2nd, Go To 3rd | -64.00 | MPH | Transmission Diagnostics |
| Cold Kickdown Mode 3-4 Upshift Threshold If Vehicle Speed >= This & Kickdown Mode Is Active & NE >= CAL & Cold Mode & Gear Is 3rd, Go To 4th | -64.00 | MPH | Transmission Diagnostics |
| Cold Kickdown Mode 2-1 Downshift Threshold If Vehicle Speed < This & Kickdown Mode Is Active & Cold Mode & Gear Is 2nd, Go To 1st | -64.00 | MPH | Transmission Diagnostics |
| Cold Kickdown Mode 3-2 Downshift Threshold If Vehicle Speed < This & Kickdown Mode Is Active & Cold Mode & Gear Is 3rd, Go To 2nd | -64.00 | MPH | Transmission Diagnostics |
| Cold Kickdown Mode 4-3 Downshift Threshold Vehicle Speed < This & Kickdown Mode Is Active & Cold Mode & Gear Is 4th, Go To 3rd | -64.00 | MPH | Transmission Diagnostics |
| Kickdown Mode 1-2 Upshift Threshold If NE >= This & Kickdown Mode Is Active & Vehicle Speed >= CAL & Normal Mode & In 1st, Go To 2nd | 19.50 | RPM | Transmission Diagnostics |
| Kickdown Mode 2-3 Upshift Threshold If NE >= This & Kickdown Mode Is Active & Vehicle Speed >= CAL & Normal Mode & In 2nd, Go To 3rd | 19.50 | RPM | Transmission Diagnostics |
| Kickdown Mode 3-4 Upshift Threshold If NE >= This & Kickdown Mode Is Active & Vehicle Speed >= CAL & Normal Mode & In 3rd, Go To 4th | 18.62 | RPM | Transmission Diagnostics |
| Cold Kickdown Mode 1-2 Upshift Threshold If NE >= This & Kickdown Mode Is Active & Cold Mode & Gear Is 1st, Go To 2nd | 0.00 | RPM | Transmission Diagnostics |
| Cold Kickdown Mode 2-3 Upshift Threshold If NE >= This & Kickdown Mode Is Active & Cold Mode & Gear Is 2nd, Go To 3rd | 0.00 | RPM | Transmission Diagnostics |
| Cold Kickdown Mode 3-4 Upshift Threshold If NE >= This & Kickdown Mode Is Active & Cold Mode & Gear Is 3rd, Go To 4th | 0.00 | RPM | Transmission Diagnostics |
| Desired Gear = Second When SEQ234TM < KSEQ13DL | 0.50 | LIMITED | Transmission Diagnostics |
| Desired Gear = Third When <Limited> Desired Gear = Fourth And SEQ234TM < KSEQ14DL Or SEQ34TM < KSEQ24DL | 0.50 | LIMITED | Transmission Diagnostics |
| Desired Gear = Third When <Limited> Desired Gear = Fourth And SEQ234TM < KSEQ14DL Or SEQ34TM < KSEQ24DL | 0.50 | LIMITED | Transmission Diagnostics |
| Engine Speed Threshold For 3-2 Shift. During Output Speed Loss | 65535.00 | RPM | Transmission Diagnostics |
| Kickdown Upshift Timer For 1-2 Shift, Used To Disable Next Shift | 0.00 | SEC | Transmission Diagnostics |
| Kickdown Upshift Timer For 2-3 Shift, Used To Disable Next Shift | 0.00 | SEC | Transmission Diagnostics |
| Kickdown Upshift Timer For 3-4 Shift, Used To Disable Next Shift | 0.00 | SEC | Transmission Diagnostics |
| Second Lo Gear Max | 1.00 | - | Transmission Diagnostics |
| Second D2 Gear Max | 1.00 | - | Transmission Diagnostics |
| Third D3 Gear Max | 2.00 | - | Transmission Diagnostics |
| Fourth D4 Gear Max | 3.00 | - | Transmission Diagnostics |
| NE Limit For Abusive Garage Shift | 1300.00 | RPM | Transmission Diagnostics |
| Throttle For Abusive Garage Shift | 7.84 | % | Transmission Diagnostics |
| NI Limit To Determin The End Of Garage Shift | 0.00 | RPM | Transmission Diagnostics |
| Time Limit For Garage Shift Conditions | 0.30 | SEC | Transmission Diagnostics |
| Ramp Down Timer Calibration During Garage Torque Management Manuvers | 2.00 | SEC | Transmission Diagnostics |
| Vehicle Speed Threshold To Enable Garage Shift Conditions | 4.00 | MPH | Transmission Diagnostics |
| Vehicle Speed To Disable Stall Conditions | 8.00 | MPH | Transmission Diagnostics |
| NE Limit For Disabling Stall Conditions Garage Shift | 4000.00 | RPM | Transmission Diagnostics |
| Throttle Limit For Disabling Stall Conditions | 7.06 | % | Transmission Diagnostics |
| Vehicle Speed To Enable Stall Conditions | 0.00 | MPH | Transmission Diagnostics |
| NE Limit For Enabling Stall Conditions Garage Shift | 1000.00 | RPM | Transmission Diagnostics |
| Throttle Limit For Enabling Stall Conditions | 10.20 | % | Transmission Diagnostics |
| Saftey Timer Threshold | 0.00 | SEC | Transmission Diagnostics |
| Accel Vs Ratio Based SEM Gear Threshold | 1.00 | COUNTS | Transmission Diagnostics |
| Negative Delta Throttle Condition Limit For 1-2 Upshift | 10.16 | % | Transmission Diagnostics |
| Negative Delta Throttle Condition Limit For 2-3 Upshift | 10.16 | % | Transmission Diagnostics |
| Negative Delta Throttle Condition Limit For 3-4 Upshift | 10.16 | % | Transmission Diagnostics |
| Enabling Throttle Threshold During 1-2 Upshift | 99.61 | % | Transmission Diagnostics |
| Enabling Throttle Threshold During 2-3 Upshift | 99.61 | % | Transmission Diagnostics |
| Enabling Throttle Threshold During 3-4 Upshift | 99.61 | % | Transmission Diagnostics |
| Enabling Engine Speed Threshold During 1-2 Upshift | 8191.88 | RPM | Transmission Diagnostics |
| Enabling Engine Speed Threshold During 2-3 Upshift | 8191.88 | RPM | Transmission Diagnostics |
| Enabling Engine Speed Threshold During 3-4 Upshift | 8191.88 | RPM | Transmission Diagnostics |
| Time After The Begining Of An Upshift During Which The Torque Management Is Enabled | 6.38 | SEC | Transmission Diagnostics |
| MPH Threshold For 3-2 Table Selection | 44.00 | MPH | Transmission Diagnostics |
| Adaptive & Engine Acceleration Table Resolution High Speed | 34.50 | MPH | Transmission Diagnostics |
| Adaptive & Engine Acceleration Table Minimum Low Speed | 32.50 | MPH | Transmission Diagnostics |
| Adaptive & Engine Acceleration Table Resolution Low Speed | 30.00 | MPH | Transmission Diagnostics |
| Upper Engine Acceleration Time Threshold For A Flare | 1.40 | SEC | Transmission Diagnostics |
| Upper Time Window Value For Engine Flare Detection | 1.30 | SEC | Transmission Diagnostics |
| Lower Time Window Value For Engine Flare Detection | 1.25 | SEC | Transmission Diagnostics |
| Lower Vehicle Speed Threshold To Enable 3-2 Adaptive Updating | 25.00 | MPH | Transmission Diagnostics |
| Lower Delta TPS Threshold To Enable 3-2 Adaptive Updating | 0.49 | %/SEC | Transmission Diagnostics |
| Lower Time Threshold To Enable 3-2 Adaptive Updating | 1.25 | SEC | Transmission Diagnostics |
| Maximum Transmission Temperature To Enable 3-2 Adaptive Updating | -2.50 | DEG/C | Transmission Diagnostics |
| Minimum Transmission Temperature To Enable 3-2 Adaptive Updating | 151.25 | DEG/C | Transmission Diagnostics |
| Minimum Time To Enable 3-2 Adaptive Updating | 2.00 | SEC | Transmission Diagnostics |
| Minimum TPS To Enable 3-2 Adaptive Updating | 14.84 | TPS% | Transmission Diagnostics |
| Lowest Allowable 3-2 Adaptive Cell Value | 0.00 | PSI | Transmission Diagnostics |
| Highest Allowable 3-2 Adaptive Cell Value | 0.00 | PSI | Transmission Diagnostics |
| 3-2 Adaptive Cell Term No Engine Flare Detection | 0.00 | PSI | Transmission Diagnostics |
| 3-2 Adaptive Cell Term Engine Flare Detected | 10.00 | PSI | Transmission Diagnostics |
| Transmission Temperature Threshold For 3-2 Solenoid State | 2.75 | DEG/C | Transmission Diagnostics |
| Default 3-2 Downshift Pressure Diag Fault | 90.00 | PSI | Transmission Diagnostics |
| Default 3-2 Downshift Pressure Range Mode | 90.00 | PSI | Transmission Diagnostics |
| Subtracted 3-2 Downshift Pressure A/C On | 6.00 | PSI | Transmission Diagnostics |
| High Limit Of High Pressure For Compressor 3140 KPA | 2896.00 | - | Speedometer |
| Low Limit Of High Pressure For Compressor 590 KPA | 2400.00 | - | Speedometer |
| High Limit Of Low Pressure For Compressor 225 KPA | 240.00 | - | Speedometer |
| Low Limit Of Low Pressure For Compressor 196 KPA | 176.00 | - | Speedometer |
| Base Injector Rate E85 (CC/MIN) | 210.46 | CC/MIN | Charlay86 Mods |
| Base Injector Rate Methanol (CC/MIN) | 209.72 | CC/MIN | Charlay86 Mods |
| Base Injector Rate Petrol (CC/MIN) | 225.25 | CC/MIN | Charlay86 Mods |
| Road Speed Constant | 13824000.00 | PUL/KM | Speedometer |
| If ACUMDIST > K1KM, INC Odometer | 63776.00 | PUL/KM | Speedometer |
| If MPH < CAL, Enable Perf Timer | 2.00 | MPH | Engine/Transmission Diagnostics |
| POS Delta TPS > CAL, Enable Perf Timer | 5.08 | DTPS | Engine/Transmission Diagnostics |
| POS Delta TPS > CAL,Enable Perf Timer | 5.08 | DTPS | Engine/Transmission Diagnostics |
| MPH To Enable Passing Gear Timer | 50.00 | MPH | Engine/Transmission Diagnostics |
| MPH To Disable Passing Gear Timer | 80.00 | MPH | Engine/Transmission Diagnostics |
| Plus/Minus Hysteresis Limit On KPTMPHEN | 1.00 | MPH | Engine/Transmission Diagnostics |
| 50Ms Timer For Debouncing Of P/N SW | 0.15 | SEC | Engine/Transmission Diagnostics |
| Engine Run Time Before Engaging Crank Lockout Strategy. If Time < CAL, Disable Lockout | 1.00 | SEC | Engine/Transmission Diagnostics |
| Crank Engage Lock-Out Engine RPM Limit | 88.00 | RPM | Engine/Transmission Diagnostics |
| If SU Coolant <= CAL Use Cold Erun Thresholds | -33.25 | DEG/C | Engine/Transmission Diagnostics |
| Non Fuel Engine Run RPM | 116.00 | RPM | Engine/Transmission Diagnostics |
| Non Fuel Engine Run Counter For Start-up | 13.00 | COUNTS | Engine/Transmission Diagnostics |
| Fuel Engine Run RPM | 0.00 | RPM | Engine/Transmission Diagnostics |
| Fuel Engine Run Counter For Start-up | 9.00 | COUNTS | Engine/Transmission Diagnostics |
| Non Fuel Engine Run RPM | 116.00 | RPM | Engine/Transmission Diagnostics |
| Non Fuel Engine Run Counter For Start-up | 13.00 | COUNTS | Engine/Transmission Diagnostics |
| Fuel Engine Run RPM | 0.00 | RPM | Engine/Transmission Diagnostics |
| Fuel Engine Run Counter For Start-up | 21.00 | COUNTS | Engine/Transmission Diagnostics |
| If RPM < CAL, Then Clear Erun Flags | 3200.00 | RPM | Engine/Transmission Diagnostics |
| Time Domain Correction To Spark | 0.00 | USEC | Engine/Transmission Diagnostics |
| Max Rate Of Advance Increase Except In DE | 14.06 | DEG/S | Engine/Transmission Diagnostics |
| Maximum Spark Advance Limit For DFCO Exit. Tip-out Detect During DFCO Exit Will Use This Rate | 0.00 | DEG/S | Engine/Transmission Diagnostics |
| Maximum Rate Of Advance Increase In Bump Spark | 14.06 | DEG/S | Engine/Transmission Diagnostics |
| Maximum Advance Relative To TDC ( 2's Comp) Limited Between 70 And -20 Degrees | 54.84 | DEG | Engine/Transmission Diagnostics |
| Maximum Retard Relative To TDC ( 2's Comp) Limited Between 70 And -20 Degrees | 69.96 | DEG | Engine/Transmission Diagnostics |
| Maximum Retard While RDSC Tip In Bump Spark Active ( 2's Complement) Limited Between 70 And -20 Degrees | 69.96 | DEG | Engine/Transmission Diagnostics |
| If MPH > CAL Don't Use P/N Spark Advance | 3.00 | MPH | Engine/Transmission Diagnostics |
| P/N Spark Advance | 84.73 | DEG | Engine/Transmission Diagnostics |
| Initialization Value For O2A, Volts | 0.45 | VOLTS | Engine/Transmission Diagnostics |
| Init Value For Slowtrim, Volts | 0.55 | VOLTS | Engine/Transmission Diagnostics |
| Cooldeg Filter Coefficient, 0-1 | 0.12 | COEFF | Engine/Transmission Diagnostics |
| Time Domain Correction To Spark | 100.00 | USEC | Engine/Transmission Diagnostics |
| Maximum Rate of Advance Increase Except in DE | 14.06 | DEG/S | Engine/Transmission Diagnostics |
| Maximum Spark Advance Limit for DFCO Exit. Tip-out Detect During DFCO Exit Will Use This Rate | 112.50 | DEG/S | Engine/Transmission Diagnostics |
| Maximum Rate of Advance Increase in Bump Spark | 14.06 | DEG/S | Engine/Transmission Diagnostics |
| Maximum Advance Relative to TDC | 54.84 | DEG | Engine/Transmission Diagnostics |
| If MPH > CAL Don't use P/N Spark Advance | 3.00 | MPH | Engine/Transmission Diagnostics |
| Park/Neutral Spark Advance | 23034.73 | DEG | Engine/Transmission Diagnostics |

---

## Flags

| Flag | Status | Category |
|------|--------|----------|
| Process DTC 13 RH O2 Sensor Open | ✅ Set | Unknown |
| Process DTC 14 Coolant High Temp | ✅ Set | Unknown |
| Process DTC 15 Coolant Low Temp | ✅ Set | Unknown |
| Process DTC 16 Coolant Sensor Unstable | ✅ Set | Unknown |
| Process DTC 17 Coolant Pull-up Failure | ✅ Set | Unknown |
| Process DTC 18 Linear EGR Flow Check | ❌ Not Set | Unknown |
| Process DTC 19 TPS Sensor Stuck | ✅ Set | Unknown |
| Process DTC 21 TPS Sensor High | ✅ Set | Unknown |
| Process DTC 22 TPS Sensor Low | ✅ Set | Unknown |
| Process DTC 23 IAT Sensor Low | ✅ Set | Unknown |
| Process DTC 24 Vehicle Speed Sensor | ✅ Set | Unknown |
| Process DTC 25 IAT Sensor High | ✅ Set | Unknown |
| Process DTC 26 IAT Sensor Unstable | ✅ Set | Unknown |
| Process DTC 27 PSM Open | ❌ Not Set | Unknown |
| Process DTC 28 PSM | ✅ Set | Unknown |
| Process DTC 29 EGR Pintle Position | ✅ Set | Unknown |
| Process DTC 31 Theft Deterrent Missing | ✅ Set | Unknown |
| Process DTC 32 MAF Out of Range | ✅ Set | Unknown |
| Process DTC 33 BAP High | ❌ Not Set | Unknown |
| Process DTC 34 BAP Low | ❌ Not Set | Unknown |
| Process DTC 35 IAC Failure | ✅ Set | Unknown |
| Process DTC 36 Vacuum Leak | ✅ Set | Unknown |
| Process DTC 39 TCC Off | ❌ Not Set | Unknown |
| Process DTC 41 EST Open / Shorted | ✅ Set | Unknown |
| Process DTC 42 Bypass Open / Shorted | ✅ Set | Unknown |
| Process DTC 43 LH ESC Failure | ❌ Not Set | Unknown |
| Process DTC 44 RH O2 Sensor Lean | ✅ Set | Unknown |
| Process DTC 45 RH O2 Sensor Rich | ✅ Set | Unknown |
| Process DTC 46 Crank Reference Pulses | ✅ Set | Unknown |
| Process DTC 47 No 18x Signal | ✅ Set | Unknown |
| Process DTC 48 Cam Signal Missing / Grounded | ✅ Set | Unknown |
| Process DTC 49 Cam / Crank Signal Error | ✅ Set | Unknown |
| Process DTC 51 Prom Checksum Error | ✅ Set | Unknown |
| Process DTC 52 Voltage High - Long Test | ✅ Set | Unknown |
| Process DTC 53 Voltage High | ✅ Set | Unknown |
| Process DTC 54 Voltage Unstable | ✅ Set | Unknown |
| Process DTC 55 A/D Conversion Error | ✅ Set | Unknown |
| Process DTC 56 Fuel Starvation Under Load (Lean) | ❌ Not Set | Unknown |
| Process DTC 57 Injector Monitor Failure | ✅ Set | Unknown |
| Process DTC 58 Trans. Temp. High | ✅ Set | Unknown |
| Process DTC 59 Trans. Temp. Low | ✅ Set | Unknown |
| Process DTC 63 LH O2 Sensor Open | ✅ Set | Unknown |
| Process DTC 64 LH O2 Sensor Lean | ✅ Set | Unknown |
| Process DTC 65 LH O2 Sensor Rich | ✅ Set | Unknown |
| Process DTC 66 3-2 DS QDM2/Solenoid Failure | ✅ Set | Unknown |
| Process DTC 67 TCC QDM2/Solenoid Failure | ✅ Set | Unknown |
| Process DTC 68 Trans. Component Slipping | ❌ Not Set | Unknown |
| Process DTC 69 TCC Stuck On | ✅ Set | Unknown |
| Process DTC 72 VSS Output Speed Loss (Auto) | ✅ Set | Unknown |
| Process DTC 73 Force Motor Current | ✅ Set | Unknown |
| Process DTC 75 Voltage Low | ✅ Set | Unknown |
| Process DTC 76 STFT Delta Integrator High | ✅ Set | Unknown |
| Process DTC 78 LTFT Delta BLM High | ✅ Set | Unknown |
| Process DTC 79 Transmission Hot | ✅ Set | Unknown |
| Process DTC 81 Solenoid B Failure (2-3) | ✅ Set | Unknown |
| Process DTC 82 Solenoid A Failure (1-2) | ✅ Set | Unknown |
| Process DTC 83 TCC Solenoid Failure | ✅ Set | Unknown |
| Process DTC 84 QDM2 Failure | ✅ Set | Unknown |
| Process DTC 86 Solenoid B Stuck On | ✅ Set | Unknown |
| Process DTC 87 Solenoid B Stuck Off | ✅ Set | Unknown |
| Process DTC 91 QDM Failure | ✅ Set | Unknown |
| Process DTC 92 Low Speed Fan Comms | ✅ Set | Unknown |
| Process DTC 93 RH ESC Failure (Knock Circuit) | ✅ Set | Unknown |
| Process DTC 94 Loss of PWM from ASR (VSS Manual) | ❌ Not Set | Unknown |
| Process DTC 95 Loss of Serial Data from ASR | ✅ Set | Unknown |
| Process DTC 96 A/C Pressure Transducer | ✅ Set | Unknown |
| Process DTC 97 Purge Valve Continuity | ✅ Set | Unknown |
| Process DTC 98 Purge Valve Function Test | ❌ Not Set | Unknown |
| Engine MIL DTC 13 RH O2 Sensor Open | ✅ Set | Unknown |
| Engine MIL DTC 14 Coolant High Temp | ✅ Set | Unknown |
| Engine MIL DTC 15 Coolant Low Temp | ✅ Set | Unknown |
| Engine MIL DTC 16 Coolant Sensor Unstable | ❌ Not Set | Unknown |
| Engine MIL DTC 17 Coolant Pull-up Failure | ❌ Not Set | Unknown |
| Engine MIL DTC 18 Linear EGR Flow Check | ❌ Not Set | Unknown |
| Engine MIL DTC 19 TPS Sensor Stuck | ✅ Set | Unknown |
| Engine MIL DTC 21 TPS Sensor High | ✅ Set | Unknown |
| Engine MIL DTC 22 TPS Sensor Low | ✅ Set | Unknown |
| Engine MIL DTC 23 IAT Sensor Low | ❌ Not Set | Unknown |
| Engine MIL DTC 24 Vehicle Speed Sensor | ✅ Set | Unknown |
| Engine MIL DTC 25 IAT Sensor High | ❌ Not Set | Unknown |
| Engine MIL DTC 26 IAT Sensor Unstable | ❌ Not Set | Unknown |
| Engine MIL DTC 27 PSM Open | ❌ Not Set | Unknown |
| Engine MIL DTC 28 PSM | ✅ Set | Unknown |
| Engine MIL DTC 29 EGR Pintle Position | ❌ Not Set | Unknown |
| Engine MIL DTC 31 Theft Deterrent Missing | ✅ Set | Unknown |
| Engine MIL DTC 32 MAF Out of Range | ✅ Set | Unknown |
| Engine MIL DTC 33 BAP High | ❌ Not Set | Unknown |
| Engine MIL DTC 34 BAP Low | ❌ Not Set | Unknown |
| Engine MIL DTC 35 IAC Failure | ❌ Not Set | Unknown |
| Engine MIL DTC 36 Vacuum Leak | ❌ Not Set | Unknown |
| Engine MIL DTC 39 TCC Off | ❌ Not Set | Unknown |
| Engine MIL DTC 41 EST Open / Shorted | ✅ Set | Unknown |
| Engine MIL DTC 42 Bypass Open / Shorted | ✅ Set | Unknown |
| Engine MIL DTC 43 LH ESC Failure | ❌ Not Set | Unknown |
| Engine MIL DTC 44 RH O2 Sensor Lean | ✅ Set | Unknown |
| Engine MIL DTC 45 RH O2 Sensor Rich | ✅ Set | Unknown |
| Engine MIL DTC 46 Crank Reference Pulses | ✅ Set | Unknown |
| Engine MIL DTC 47 No 18x Signal | ❌ Not Set | Unknown |
| Engine MIL DTC 48 Cam Signal Missing / Grounded | ❌ Not Set | Unknown |
| Engine MIL DTC 49 Cam / Crank Signal Error | ❌ Not Set | Unknown |
| Engine MIL DTC 51 Prom Checksum Error | ✅ Set | Unknown |
| Engine MIL DTC 52 Voltage High - Long Test | ❌ Not Set | Unknown |
| Engine MIL DTC 53 Voltage High | ❌ Not Set | Unknown |
| Engine MIL DTC 54 Voltage Unstable | ✅ Set | Unknown |
| Engine MIL DTC 55 A/D Conversion Error | ✅ Set | Unknown |
| Engine MIL DTC 57 Injector Monitor Failure | ❌ Not Set | Unknown |
| Engine MIL DTC 58 Trans. Temp. High | ❌ Not Set | Unknown |
| Engine MIL DTC 59 Trans. Temp. Low | ❌ Not Set | Unknown |
| Engine MIL DTC 63 LH O2 Sensor Open | ✅ Set | Unknown |
| Engine MIL DTC 64 LH O2 Sensor Lean | ✅ Set | Unknown |
| Engine MIL DTC 65 LH O2 Sensor Rich | ✅ Set | Unknown |
| Engine MIL DTC 66 3-2 DS QDM2/Solenoid Failure | ✅ Set | Unknown |
| Engine MIL DTC 67 TCC QDM2/Solenoid Failure | ✅ Set | Unknown |
| Engine MIL DTC 68 Trans. Component Slipping | ❌ Not Set | Unknown |
| Engine MIL DTC 69 TCC Stuck On | ✅ Set | Unknown |
| Engine MIL DTC 72 VSS Output Speed Loss (Auto) | ❌ Not Set | Unknown |
| Engine MIL DTC 73 Force Motor Current | ❌ Not Set | Unknown |
| Engine MIL DTC 75 Voltage Low | ❌ Not Set | Unknown |
| Engine MIL DTC 76 STFT Delta Integrator High | ❌ Not Set | Unknown |
| Engine MIL DTC 78 LTFT Delta BLM High | ❌ Not Set | Unknown |
| Engine MIL DTC 79 Transmission Hot | ✅ Set | Unknown |
| Engine MIL DTC 81 Solenoid B Failure (2-3) | ✅ Set | Unknown |
| Engine MIL DTC 82 Solenoid A Failure (1-2) | ✅ Set | Unknown |
| Engine MIL DTC 83 TCC Solenoid Failure | ✅ Set | Unknown |
| Engine MIL DTC 84 QDM2 Failure | ✅ Set | Unknown |
| Engine MIL DTC 86 Solenoid B Stuck On | ✅ Set | Unknown |
| Engine MIL DTC 87 Solenoid B Stuck Off | ✅ Set | Unknown |
| Engine MIL DTC 91 QDM Failure | ✅ Set | Unknown |
| Engine MIL DTC 92 Low Speed Fan Comms | ❌ Not Set | Unknown |
| Engine MIL DTC 93 RH ESC Failure (Knock Circuit) | ✅ Set | Unknown |
| Engine MIL DTC 94 Loss of PWM from ASR (VSS Manual) | ❌ Not Set | Unknown |
| Engine MIL DTC 95 Loss of Serial Data from ASR | ✅ Set | Unknown |
| Engine MIL DTC 96 A/C Pressure Transducer | ❌ Not Set | Unknown |
| Engine MIL DTC 97 Purge Valve Continuity | ❌ Not Set | Unknown |
| Engine MIL DTC 98 Purge Valve Function Test | ❌ Not Set | Unknown |
| Powertrain MIL DTC 13 RH O2 Sensor Open | ❌ Not Set | Unknown |
| Powertrain MIL DTC 14 Coolant High Temp | ✅ Set | Unknown |
| Powertrain MIL DTC 15 Coolant Low Temp | ✅ Set | Unknown |
| Powertrain MIL DTC 16 Coolant Sensor Unstable | ❌ Not Set | Unknown |
| Powertrain MIL DTC 17 Coolant Pull-up Failure | ❌ Not Set | Unknown |
| Powertrain MIL DTC 18 Linear EGR Flow Check | ❌ Not Set | Unknown |
| Powertrain MIL DTC 19 TPS Sensor Stuck | ✅ Set | Unknown |
| Powertrain MIL DTC 21 TPS Sensor High | ✅ Set | Unknown |
| Powertrain MIL DTC 22 TPS Sensor Low | ✅ Set | Unknown |
| Powertrain MIL DTC 23 IAT Sensor Low | ❌ Not Set | Unknown |
| Powertrain MIL DTC 24 Vehicle Speed Sensor | ✅ Set | Unknown |
| Powertrain MIL DTC 25 IAT Sensor High | ❌ Not Set | Unknown |
| Powertrain MIL DTC 26 IAT Sensor Unstable | ❌ Not Set | Unknown |
| Powertrain MIL DTC 27 PSM Open | ❌ Not Set | Unknown |
| Powertrain MIL DTC 28 PSM | ✅ Set | Unknown |
| Powertrain MIL DTC 29 EGR Pintle Position | ❌ Not Set | Unknown |
| Powertrain MIL DTC 31 Theft Deterrent Missing | ❌ Not Set | Unknown |
| Powertrain MIL DTC 32 MAF Out of Range | ❌ Not Set | Unknown |
| Powertrain MIL DTC 33 BAP High | ❌ Not Set | Unknown |
| Powertrain MIL DTC 34 BAP Low | ❌ Not Set | Unknown |
| Powertrain MIL DTC 35 IAC Failure | ❌ Not Set | Unknown |
| Powertrain MIL DTC 36 Vacuum Leak | ❌ Not Set | Unknown |
| Powertrain MIL DTC 39 TCC Off | ❌ Not Set | Unknown |
| Powertrain MIL DTC 41 EST Open / Shorted | ❌ Not Set | Unknown |
| Powertrain MIL DTC 42 Bypass Open / Shorted | ❌ Not Set | Unknown |
| Powertrain MIL DTC 43 LH ESC Failure | ❌ Not Set | Unknown |
| Powertrain MIL DTC 44 RH O2 Sensor Lean | ❌ Not Set | Unknown |
| Powertrain MIL DTC 45 RH O2 Sensor Rich | ❌ Not Set | Unknown |
| Powertrain MIL DTC 46 Crank Reference Pulses | ❌ Not Set | Unknown |
| Powertrain MIL DTC 47 No 18x Signal | ❌ Not Set | Unknown |
| Powertrain MIL DTC 48 Cam Signal Missing / Grounded | ❌ Not Set | Unknown |
| Powertrain MIL DTC 49 Cam / Crank Signal Error | ❌ Not Set | Unknown |
| Powertrain MIL DTC 51 Prom Checksum Error | ❌ Not Set | Unknown |
| Powertrain MIL DTC 52 Voltage High - Long Test | ✅ Set | Unknown |
| Powertrain MIL DTC 53 Voltage High | ✅ Set | Unknown |
| Powertrain MIL DTC 54 Voltage Unstable | ❌ Not Set | Unknown |
| Powertrain MIL DTC 55 A/D Conversion Error | ❌ Not Set | Unknown |
| Powertrain MIL DTC 56 Fuel Starvation Under Load (Lean) | ❌ Not Set | Unknown |
| Powertrain MIL DTC 57 Injector Monitor Failure | ❌ Not Set | Unknown |
| Powertrain MIL DTC 58 Trans. Temp. High | ✅ Set | Unknown |
| Powertrain MIL DTC 59 Trans. Temp. Low | ✅ Set | Unknown |
| Powertrain MIL DTC 63 LH O2 Sensor Open | ❌ Not Set | Unknown |
| Powertrain MIL DTC 64 LH O2 Sensor Lean | ❌ Not Set | Unknown |
| Powertrain MIL DTC 65 LH O2 Sensor Rich | ❌ Not Set | Unknown |
| Powertrain MIL DTC 66 3-2 DS QDM2/Solenoid Failure | ✅ Set | Unknown |
| Powertrain MIL DTC 67 TCC QDM2/Solenoid Failure | ✅ Set | Unknown |
| Powertrain MIL DTC 68 Trans. Component Slipping | ✅ Set | Unknown |
| Powertrain MIL DTC 69 TCC Stuck On | ✅ Set | Unknown |
| Powertrain MIL DTC 72 VSS Output Speed Loss (Auto) | ❌ Not Set | Unknown |
| Powertrain MIL DTC 73 Force Motor Current | ✅ Set | Unknown |
| Powertrain MIL DTC 75 Voltage Low | ✅ Set | Unknown |
| Powertrain MIL DTC 76 STFT Delta Integrator High | ❌ Not Set | Unknown |
| Powertrain MIL DTC 78 LTFT Delta BLM High | ❌ Not Set | Unknown |
| Powertrain MIL DTC 79 Transmission Hot | ✅ Set | Unknown |
| Powertrain MIL DTC 81 Solenoid B Failure (2-3) | ✅ Set | Unknown |
| Powertrain MIL DTC 82 Solenoid A Failure (1-2) | ✅ Set | Unknown |
| Powertrain MIL DTC 83 TCC Solenoid Failure | ✅ Set | Unknown |
| Powertrain MIL DTC 84 QDM2 Failure | ❌ Not Set | Unknown |
| Powertrain MIL DTC 86 Solenoid B Stuck On | ❌ Not Set | Unknown |
| Powertrain MIL DTC 87 Solenoid B Stuck Off | ❌ Not Set | Unknown |
| Powertrain MIL DTC 91 QDM Failure | ❌ Not Set | Unknown |
| Powertrain MIL DTC 92 Low Speed Fan Comms | ❌ Not Set | Unknown |
| Enable TCC Conditions (1=...) | ❌ Not Set | Transmission Diagnostics |
| Enable TCC Conditions (1=...) | ✅ Set | Transmission Diagnostics |
| Enable TCC Conditions (1=...) | ❌ Not Set | Transmission Diagnostics |
| Enable TCC Conditions (1=...) | ❌ Not Set | Transmission Diagnostics |
| Enable TCC Conditions (1=...) | ❌ Not Set | Transmission Diagnostics |
| Enable TCC Conditions (1=...) | ✅ Set | Transmission Diagnostics |
| Enable TCC Conditions (1=...) | ✅ Set | Transmission Diagnostics |
| Enable TCC Conditions (1=...) | ❌ Not Set | Transmission Diagnostics |
| Enable TCC Conditions (1=...) | ❌ Not Set | Transmission Diagnostics |
| Enable TCC Conditions (1=...) | ❌ Not Set | Transmission Diagnostics |
| Enable TCC Conditions (1=...) | ✅ Set | Transmission Diagnostics |
| Enable TCC Conditions (1=...) | ✅ Set | Transmission Diagnostics |
| Enable TCC Conditions (1=...) | ❌ Not Set | Transmission Diagnostics |
| Enable TCC Conditions (1=...) | ❌ Not Set | Transmission Diagnostics |
| Enable TCC Conditions (1=...) | ❌ Not Set | Transmission Diagnostics |
| Enable TCC Conditions (1=...) | ❌ Not Set | Transmission Diagnostics |
| Enable TCC Conditions (1=...) | ❌ Not Set | Transmission Diagnostics |
| Enable TCC Conditions (1=...) | ✅ Set | Transmission Diagnostics |
| Malf 92 - Low Speed Fan Communication Failure | ✅ Set | Transmission Calibration |
| 1 = MANUAL TRANSMISSION OPTION | ❌ Not Set | Injector |
| 0 = NO POWER STEERING PRESSURE SWITCH | ❌ Not Set | Injector |
| 0 = Skip crank to run sparkramp logic | ✅ Set | Injector |
| 1 = STALL SAVER A/C CLEAR FUNCTION ENABLED | ✅ Set | Injector |
| 1 = BYPASS MAF FILTERING LOGIC DURING CRANK | ✅ Set | Injector |
| 1 = LEAN CRUISE OPTION SELECTED | ✅ Set | Engine/Transmission Diagnostics |
| 0 = DRIVERS O2 / 1 = DUAL O2 SYSTEM | ✅ Set | Injector |
| 1 = 6 CYLINDER / 0 RESERVED FOR FUTURE V8 | ✅ Set | Injector |
| 1 = THROTTLE FOLLOWER RPM DEPENDENT / 0 = THROTTLE FOLLOWER KPH DEPENDENT | ✅ Set | Injector |
| 1 = NOT SELECT OPEN LOOP IDLE LOGIC | ✅ Set | Injector |
| 1 = F/P Speed Control Enabled | ❌ Not Set | Injector |
| VATS | ✅ Set | Speedometer |
| DFCOCATP | ❌ Not Set | Engine/Transmission Diagnostics |
| 1 = GETRAG TRANSMISSION | ❌ Not Set | Injector |
| KMANENBL | ❌ Not Set | Transmission Calibration |
| M21 Throttle Position High | ✅ Set | Transmission Calibration |
| M19 TPS Stuck | ✅ Set | Transmission Calibration |
| M17 Coolant Pullup Resister Failure | ✅ Set | Transmission Calibration |
| M16 Coolant Sensor Unstable | ✅ Set | Transmission Calibration |
| M15 Coolant Sensor Low Temperature | ✅ Set | Transmission Calibration |
| M14 Coolant Sensor High Temperature | ✅ Set | Transmission Calibration |
| M13 Oxygen Sensor Open (Right Hand Side) | ✅ Set | Transmission Calibration |
| M29 | ✅ Set | Transmission Calibration |
| M28 Pressure Switch Manifold | ✅ Set | Transmission Calibration |
| M27 Pressure Switch Manifold Open | ❌ Not Set | Transmission Calibration |
| M26 MAT Sensor Unstable | ✅ Set | Transmission Calibration |
| M25 MAT Sensor High | ✅ Set | Transmission Calibration |
| M24 Vehicle Speed Sensor Fail (Auto) | ✅ Set | Transmission Calibration |
| M23 MAT Sensor Low | ✅ Set | Transmission Calibration |
| M22Throttle Position Low | ✅ Set | Transmission Calibration |
| M38 | ❌ Not Set | Transmission Calibration |
| M37 | ❌ Not Set | Transmission Calibration |
| M36 Vacuum Leak | ✅ Set | Transmission Calibration |
| M35 Idle Air Control Motor Error | ✅ Set | Transmission Calibration |
| M34 MAP Low | ❌ Not Set | Transmission Calibration |
| M33 MAP High | ❌ Not Set | Transmission Calibration |
| M32 MAF Failure | ✅ Set | Transmission Calibration |
| M31 Serial Data Communication Failure | ✅ Set | Transmission Calibration |
| M47 18x Input Missing Or Grounded | ✅ Set | Transmission Calibration |
| M46 No Ref Pulses | ✅ Set | Transmission Calibration |
| M45 RH Oxygen Sensor Rich | ✅ Set | Transmission Calibration |
| M44 RH Oxygen Sensor Lean | ✅ Set | Transmission Calibration |
| M43 | ❌ Not Set | Transmission Calibration |
| M42 EST Test Failed | ✅ Set | Transmission Calibration |
| M41 EST Line Open | ✅ Set | Transmission Calibration |
| M39 | ❌ Not Set | Transmission Calibration |
| M56 Fuel Starvation Under Load (Supercharger) | ❌ Not Set | Transmission Calibration |
| M55 A/D Conversion Error | ✅ Set | Transmission Calibration |
| M54 Battery Voltage Unstable | ✅ Set | Transmission Calibration |
| M53 System Voltage High | ✅ Set | Transmission Calibration |
| M52 System Voltage High-Long Test | ✅ Set | Transmission Calibration |
| M51 Prom Checksum Failure | ✅ Set | Transmission Calibration |
| M49 Cam/Crank Signal Error | ✅ Set | Transmission Calibration |
| M48 Cam Sensor Input Missing Or Grounded | ✅ Set | Transmission Calibration |
| M65 LH Oxygen Sensor Rich | ✅ Set | Transmission Calibration |
| M64 LH Oxygen Sensor Lean | ✅ Set | Transmission Calibration |
| M63 Left Hand Side o2 Open | ✅ Set | Transmission Calibration |
| M62 LH Knock Sensor Failure | ✅ Set | Transmission Calibration |
| M61 RH Knock Sensor Failure | ✅ Set | Transmission Calibration |
| M59 Transmission Temperature Low | ✅ Set | Transmission Calibration |
| M58 Transmission Temperature High | ✅ Set | Transmission Calibration |
| M57 Injector Monitor Line Failure | ✅ Set | Transmission Calibration |
| M74 | ❌ Not Set | Transmission Calibration |
| M73 Force Motor Current | ✅ Set | Transmission Calibration |
| M72 Output Speed Loss | ✅ Set | Transmission Calibration |
| M71 Engine Speed Sensor Low | ❌ Not Set | Transmission Calibration |
| M69 TCC Stuck On | ✅ Set | Transmission Calibration |
| M68 | ❌ Not Set | Transmission Calibration |
| M67 TCC Enable QDM1/Solenoid Failure | ✅ Set | Transmission Calibration |
| M66 3-2 DS QDM2/Solenoid Failure | ✅ Set | Transmission Calibration |
| M83 TCC Solenoid Failure | ✅ Set | Transmission Calibration |
| M82 Shift A Shorted | ✅ Set | Transmission Calibration |
| M81 Shift B Shorted | ✅ Set | Transmission Calibration |
| M79 Transmission Hot | ✅ Set | Transmission Calibration |
| M78 BLM Delta Cell Calculation Error | ✅ Set | Transmission Calibration |
| M77 MNP Switch Failure | ❌ Not Set | Transmission Calibration |
| M76 Closed Loop Integrator/Delta High | ✅ Set | Transmission Calibration |
| M75 System Voltage Low | ✅ Set | Transmission Calibration |
| M92 Low Speed Fan Communication Failure | ✅ Set | Transmission Calibration |
| M89 Maximum Adaptive Long Shift | ❌ Not Set | Transmission Calibration |
| M88 | ❌ Not Set | Transmission Calibration |
| M87 Shift B Open | ✅ Set | Transmission Calibration |
| M86 Shift A Open | ✅ Set | Transmission Calibration |
| M85 Transmission Component Slipping | ✅ Set | Transmission Calibration |
| M99 | ❌ Not Set | Transmission Calibration |
| M98 CCP Failure | ❌ Not Set | Transmission Calibration |
| M97 CCP Driver Failure | ✅ Set | Transmission Calibration |
| M96 AC Pressure Input Missing | ✅ Set | Transmission Calibration |
| M95 Traction Control PWM Input Out Of Range | ✅ Set | Transmission Calibration |
| M94 | ❌ Not Set | Transmission Calibration |
| M93 ESC System Failure | ✅ Set | Transmission Calibration |
| M21 Throttle Position High | ✅ Set | Transmission Calibration |
| M19 TPS Stuck | ✅ Set | Transmission Calibration |
| M17 Coolant Pullup Resister Failure | ❌ Not Set | Transmission Calibration |
| M16 Coolant Sensor Unstable | ❌ Not Set | Transmission Calibration |
| M15 Coolant Sensor Low Temperature | ✅ Set | Transmission Calibration |
| M14 Coolant Sensor High Temperature | ✅ Set | Transmission Calibration |
| M13 Oxygen Sensor Open (Right Hand Side) | ✅ Set | Transmission Calibration |
| M29 | ❌ Not Set | Transmission Calibration |
| M28 Pressure Switch Manifold | ✅ Set | Transmission Calibration |
| M27 Pressure Switch Manifold Open | ❌ Not Set | Transmission Calibration |
| M26 MAT Sensor Unstable | ❌ Not Set | Transmission Calibration |
| M25 MAT Sensor High | ❌ Not Set | Transmission Calibration |
| M24 Vehicle Speed Sensor Failure | ✅ Set | Transmission Calibration |
| M23 MAT Sensor Low | ❌ Not Set | Transmission Calibration |
| M22 Throttle Position Low | ✅ Set | Transmission Calibration |
| M38 | ❌ Not Set | Transmission Calibration |
| M37 | ❌ Not Set | Transmission Calibration |
| M36 Vacuum Leak | ❌ Not Set | Transmission Calibration |
| M35 Idle Air Control Motor Error | ❌ Not Set | Transmission Calibration |
| M34 MAP Low | ❌ Not Set | Transmission Calibration |
| M33 MAP High | ❌ Not Set | Transmission Calibration |
| M32 | ✅ Set | Transmission Calibration |
| M31 Serial Data Communication Failure | ✅ Set | Transmission Calibration |
| M47 18x Input Missing Or Grounded | ❌ Not Set | Transmission Calibration |
| M46 No Ref Pulses | ✅ Set | Transmission Calibration |
| M45 RH Oxygen Sensor Rich | ✅ Set | Transmission Calibration |
| M44 RH Oxygen Sensor Lean | ✅ Set | Transmission Calibration |
| M43 | ❌ Not Set | Transmission Calibration |
| M42 EST Test Failed | ✅ Set | Transmission Calibration |
| M41 EST Line Open | ✅ Set | Transmission Calibration |
| M39 | ❌ Not Set | Transmission Calibration |
| M56 Fuel Starvation Under Load (Supercharger) | ❌ Not Set | Transmission Calibration |
| M55 A/D Conversion Error | ✅ Set | Transmission Calibration |
| M54 Battery Voltage Unstable | ✅ Set | Transmission Calibration |
| M53 System Voltage High | ❌ Not Set | Transmission Calibration |
| M52 System Voltage High-Long Test | ❌ Not Set | Transmission Calibration |
| M51 Prom Checksum Failure | ✅ Set | Transmission Calibration |
| M49 Cam/Crank Signal Error | ❌ Not Set | Transmission Calibration |
| M48 Cam Sensor Input Missing Or Grounded | ❌ Not Set | Transmission Calibration |
| M65 LH Oxygen Sensor Rich | ✅ Set | Transmission Calibration |
| M64 LH Oxygen Sensor Lean | ✅ Set | Transmission Calibration |
| M63 Left Hand Side o2 Open | ✅ Set | Transmission Calibration |
| M62 LH Knock Sensor Failure | ✅ Set | Transmission Calibration |
| M61 RH Knock Sensor Failure | ✅ Set | Transmission Calibration |
| M59 Transmission Temperature Low | ❌ Not Set | Transmission Calibration |
| M58 Transmission Temperature High | ❌ Not Set | Transmission Calibration |
| M57 Injector Monitor Line Failure | ❌ Not Set | Transmission Calibration |
| M74 | ❌ Not Set | Transmission Calibration |
| M73 Force Motor Current | ❌ Not Set | Transmission Calibration |
| M72 Output Speed Loss | ❌ Not Set | Transmission Calibration |
| M71 Engine Speed Sensor Low | ❌ Not Set | Transmission Calibration |
| M69 TCC Stuck On | ✅ Set | Transmission Calibration |
| M68 | ❌ Not Set | Transmission Calibration |
| M67 TCC Enable Solenoid Failure | ✅ Set | Transmission Calibration |
| M66 3-2 Solenoid Failure | ✅ Set | Transmission Calibration |
| M83 ESC System Failure | ✅ Set | Transmission Calibration |
| M82 Shift A Shorted | ✅ Set | Transmission Calibration |
| M81 Shift B Shorted | ✅ Set | Transmission Calibration |
| M79 Transmission Hot | ✅ Set | Transmission Calibration |
| M78 BLM Delta Cell Calculation Error | ❌ Not Set | Transmission Calibration |
| M77 MNP Switch Failure | ❌ Not Set | Transmission Calibration |
| M76 Closed Loop Integrator/Delta High | ❌ Not Set | Transmission Calibration |
| M75 System Voltage Low | ❌ Not Set | Transmission Calibration |
| M92 Low Speed Fan Communication Failure | ❌ Not Set | Transmission Calibration |
| M89 Maximum Adaptive Long Shift | ❌ Not Set | Transmission Calibration |
| M88 | ❌ Not Set | Transmission Calibration |
| M87 Shift B Open | ✅ Set | Transmission Calibration |
| M86 Shift A Open | ✅ Set | Transmission Calibration |
| M85 Transmission Component Slipping | ✅ Set | Transmission Calibration |
| M99 | ❌ Not Set | Transmission Calibration |
| M98 CCP Failure | ❌ Not Set | Transmission Calibration |
| M97 CCP Driver Failure | ❌ Not Set | Transmission Calibration |
| M96 AC Pressure Input Missing | ❌ Not Set | Transmission Calibration |
| M95 TCS PWM Input Out Of Range | ✅ Set | Transmission Calibration |
| M94 | ❌ Not Set | Transmission Calibration |
| M93 ESC System Failure | ✅ Set | Transmission Calibration |
| M21 Throttle Position High | ✅ Set | Transmission Calibration |
| M19 TPS Stuck | ✅ Set | Transmission Calibration |
| M28 Pressure Switch Manifold | ✅ Set | Transmission Calibration |
| M24 Vehicle Speed Sensor Failure (Auto) | ✅ Set | Transmission Calibration |
| M22 Throttle Position Low | ✅ Set | Transmission Calibration |
| M38 | ❌ Not Set | Transmission Calibration |
| M37 | ❌ Not Set | Transmission Calibration |
| M32 | ❌ Not Set | Transmission Calibration |
| M39 | ❌ Not Set | Transmission Calibration |
| M53 System Voltage High | ✅ Set | Transmission Calibration |
| M52 System Voltage High-Long Test | ✅ Set | Transmission Calibration |
| M63 Left Hand Side o2 Open | ❌ Not Set | Transmission Calibration |
| M59 Transmission Temperature Low | ✅ Set | Transmission Calibration |
| M58 Transmission Temperature High | ✅ Set | Transmission Calibration |
| M74 | ❌ Not Set | Transmission Calibration |
| M73 Force Motor Current | ✅ Set | Transmission Calibration |
| M72 Output Speed Loss | ❌ Not Set | Transmission Calibration |
| M71 Engine Speed Sensor Low | ❌ Not Set | Transmission Calibration |
| M69 TCC Stuck On | ✅ Set | Transmission Calibration |
| M68 | ✅ Set | Transmission Calibration |
| M67 TCC Enable Solenoid Failure | ✅ Set | Transmission Calibration |
| M66 3-2 Downshift Solenoid Failure | ✅ Set | Transmission Calibration |
| M83 | ✅ Set | Transmission Calibration |
| M79 Transmission Hot | ✅ Set | Transmission Calibration |
| M78 BLM Delta Cell Calculation Error | ❌ Not Set | Transmission Calibration |
| M77 MNP Switch Failure | ❌ Not Set | Transmission Calibration |
| M76 Closed Loop Integrator/Delta High | ❌ Not Set | Transmission Calibration |
| M75 System Voltage Low | ✅ Set | Transmission Calibration |
| M92 Low Speed Fan Communication Failure | ❌ Not Set | Transmission Calibration |
| M89 Maximum Adaptive Long Shift | ❌ Not Set | Transmission Calibration |
| M88 | ❌ Not Set | Transmission Calibration |
| M85 Transmission Component Slipping | ❌ Not Set | Transmission Calibration |
| M21 Throttle Position High | ❌ Not Set | Transmission Calibration |
| M19 TPS Stuck | ❌ Not Set | Transmission Calibration |
| M28 Pressure Switch Manifold | ❌ Not Set | Transmission Calibration |
| M24 Vehicle Speed Sensor Failure | ❌ Not Set | Transmission Calibration |
| M22 Throttle Position Low | ❌ Not Set | Transmission Calibration |
| M38 | ❌ Not Set | Transmission Calibration |
| M37 | ❌ Not Set | Transmission Calibration |
| M32 | ❌ Not Set | Transmission Calibration |
| M39 | ❌ Not Set | Transmission Calibration |
| M53 System Voltage High | ❌ Not Set | Transmission Calibration |
| M52 System Voltage High-Long Test | ❌ Not Set | Transmission Calibration |
| M63 Left Hand Side o2 Open | ❌ Not Set | Transmission Calibration |
| M59 Transmission Temperature Low | ❌ Not Set | Transmission Calibration |
| M58 Transmission Temperature High | ❌ Not Set | Transmission Calibration |
| M74 | ❌ Not Set | Transmission Calibration |
| M73 Force Motor Current | ❌ Not Set | Transmission Calibration |
| M72 Output Speed Loss | ❌ Not Set | Transmission Calibration |
| M71 Engine Speed Sensor Low | ❌ Not Set | Transmission Calibration |
| M69 TCC Stuck On | ❌ Not Set | Transmission Calibration |
| M85 | ❌ Not Set | Transmission Calibration |
| M67 TCC Enable Solenoid Failure | ❌ Not Set | Transmission Calibration |
| M66 3-2 Downshift Solenoid Failure | ❌ Not Set | Transmission Calibration |
| M83 | ❌ Not Set | Transmission Calibration |
| M79 Transmission Hot | ❌ Not Set | Transmission Calibration |
| M78 BLM Delta Cell Calculation Error | ❌ Not Set | Transmission Calibration |
| M77 MNP Switch Failure | ❌ Not Set | Transmission Calibration |
| M76 Closed Loop Integrator/Delta High | ❌ Not Set | Transmission Calibration |
| M75 System Voltage Low | ❌ Not Set | Transmission Calibration |
| M92 Low Speed Fan Communication Failure | ❌ Not Set | Transmission Calibration |
| M89 Maximum Adaptive Long Shift | ❌ Not Set | Transmission Calibration |
| M88 | ❌ Not Set | Transmission Calibration |
| M85 Transmission Component Slipping | ❌ Not Set | Transmission Calibration |
| VX VY Communications | ❌ Not Set | Uncategorized |
| 1 = Enable Retarded Idle Spark | ❌ Not Set | Engine/Transmission Diagnostics |
| 1 = SAATS SUBTRACTION IN EXTENDED IDLE ALL | ❌ Not Set | Engine/Transmission Diagnostics |
| 1 = CLUTCH CONTROLLED SPARK ADVANCE ENABLED | ❌ Not Set | Engine/Transmission Diagnostics |
| 1 = CLOSED THROTTLE SPARK ENABLED | ❌ Not Set | Engine/Transmission Diagnostics |
| 1 = SELECT SHIFT FLARE DETECT FOR CLOSED THROTTLE SPARK | ❌ Not Set | Engine/Transmission Diagnostics |
| 1 = SELECT ENGINE RUN TIMSPK, AND SELECT P/N CMDAIR OFFSET | ❌ Not Set | Engine/Transmission Diagnostics |
| 1 = SELECT PID ONLY APPLICATION OF KPNSPK FOR P/N AND NEUTRAL | ❌ Not Set | Engine/Transmission Diagnostics |
| 1 = Add Cold Spark - Cold Spark Multiplier Offset To Main Spark | ✅ Set | Engine/Transmission Diagnostics |
| 1 = RDSC ENABLE | ✅ Set | Engine/Transmission Diagnostics |
| 1 = Knock Sensor Control Logic Enable | ✅ Set | Engine/Transmission Diagnostics |
| SPIOPT KNOCK VARIABLE OPTION | ❌ Not Set | Engine/Transmission Diagnostics |
| CYLINDER 1 NOK SENSOR PRESENT | ❌ Not Set | Engine/Transmission Diagnostics |
| CYLINDER 2 NOK SENSOR PRESENT | ✅ Set | Engine/Transmission Diagnostics |
| CYLINDER 3 NOK SENSOR PRESENT | ❌ Not Set | Engine/Transmission Diagnostics |
| CYLINDER 4 NOK SENSOR PRESENT | ✅ Set | Engine/Transmission Diagnostics |
| CYLINDER 5 NOK SENSOR PRESENT | ❌ Not Set | Engine/Transmission Diagnostics |
| CYLINDER 6 NOK SENSOR PRESENT | ✅ Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #1 Byte | ❌ Not Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #1 HPFBYP | ❌ Not Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #1 OFFCNCL | ✅ Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #1 FILTSEL | ❌ Not Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #1 AV0 | ✅ Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #1 AV1 | ❌ Not Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #1 AV2 | ✅ Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #1 AV3 | ✅ Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #2 FC0 | ❌ Not Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #2 FC1 | ✅ Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #2 FC2 | ❌ Not Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #2 FC3 | ❌ Not Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #2 Q0 | ✅ Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #2 Q1 | ❌ Not Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #2 Diag1-0 Select Output For Diagnostic MUX1 | ✅ Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #2 Diag1-1 Select Output For Diagnostic MUX1 | ❌ Not Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #3 Diag2-0 Select Output For Diagnostic MUX2 | ❌ Not Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #3 Diag2-1 Select Output For Diagnostic MUX2 | ✅ Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #3 Mode | ❌ Not Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #3 NCO0 | ❌ Not Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #3 NCO1 | ❌ Not Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #3 NCO2 | ❌ Not Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #3 NCO3 | ✅ Set | Engine/Transmission Diagnostics |
| IRIC SPI Byte #3 NCO4 | ❌ Not Set | Engine/Transmission Diagnostics |
| IRIC Mode | ❌ Not Set | Engine/Transmission Diagnostics |
| DSNEF Filter Q - Q0 | ✅ Set | Engine/Transmission Diagnostics |
| DSNEF Filter Q - Q1 | ❌ Not Set | Engine/Transmission Diagnostics |
| Bandpass Filter Centre Frequency FC0 | ❌ Not Set | Engine/Transmission Diagnostics |
| Bandpass Filter Centre Frequency FC1 | ✅ Set | Engine/Transmission Diagnostics |
| Bandpass Filter Centre Frequency FC2 | ❌ Not Set | Engine/Transmission Diagnostics |
| Bandpass Filter Centre Frequency FC3 | ❌ Not Set | Engine/Transmission Diagnostics |
| 1 = Set ADPSKM2 to KADPSPK | ❌ Not Set | Injector |
| 1 = CLUTCH SWITCH OPEN IF DISENGAGED / 0 = CLUTCH SWITCH CLOSED IF DISENGAGED | ❌ Not Set | Injector |
| DSNEF Initial Gain AV0 | ✅ Set | Engine/Transmission Diagnostics |
| DSNEF Initial Gain AV1 | ❌ Not Set | Engine/Transmission Diagnostics |
| DSNEF Initial Gain AV2 | ✅ Set | Engine/Transmission Diagnostics |
| DSNEF Initial Gain AV3 | ✅ Set | Engine/Transmission Diagnostics |
| ESC Gain Adjustment To BPF 2 DB | ✅ Set | Engine/Transmission Diagnostics |
| ESC Gain Adjustment To BPF 4 DB | ❌ Not Set | Engine/Transmission Diagnostics |
| ESC Gain Adjustment To BPF 6 DB | ✅ Set | Engine/Transmission Diagnostics |
| Non Zero = IAC Motor Slew, 0 = Command SPD Slew | ✅ Set | Engine/Transmission Diagnostics |
| FSROFTMS | ❌ Not Set | Engine/Transmission Diagnostics |
| KOPTN002 Non-Zero = Allow Lean-Cruise Operation For Non-EOS Application | ❌ Not Set | Engine/Transmission Diagnostics |
| Adaptive Contingency Selection | ✅ Set | Transmission Diagnostics |
| Adaptive Contingency Selection | ❌ Not Set | Transmission Diagnostics |
| Adaptive Contingency Selection | ✅ Set | Transmission Diagnostics |
| KENBLTPS | ❌ Not Set | Transmission Diagnostics |
| D32AVAIL | ✅ Set | Transmission Diagnostics |
| NORMOPT | ❌ Not Set | Transmission Diagnostics |
| KTPSLRN | ✅ Set | Transmission Diagnostics |
| KDRANO | ❌ Not Set | Transmission Diagnostics |
| KMAND2 | ❌ Not Set | Transmission Diagnostics |
| ETSENBL | ✅ Set | Transmission Diagnostics |
| INSPDSEN | ❌ Not Set | Transmission Diagnostics |
| FWDAVAIL | ❌ Not Set | Transmission Diagnostics |
| TRQBASED | ❌ Not Set | Transmission Diagnostics |
| NOSLAND | ❌ Not Set | Transmission Diagnostics |
| NOIMLAND | ✅ Set | Transmission Diagnostics |
| ETSATWOT | ❌ Not Set | Transmission Diagnostics |
| ENBLSOL | ✅ Set | Transmission Diagnostics |
| INVTCCDC | ❌ Not Set | Transmission Diagnostics |
| NIAFTOD | ❌ Not Set | Transmission Diagnostics |
| RNGFILT | ✅ Set | Transmission Diagnostics |
| PATFILT | ✅ Set | Transmission Diagnostics |
| ACFILT | ✅ Set | Transmission Diagnostics |
| CRUSFILT | ❌ Not Set | Transmission Diagnostics |
| FWDFILT | ❌ Not Set | Transmission Diagnostics |
| 1 = Low TPS Will Disable CCP | ❌ Not Set | Engine/Transmission Diagnostics |
| 1 = Allow CCP In Open Loop | ✅ Set | Engine/Transmission Diagnostics |
| 1 = Heavy Purge - Use Fixed CCP (F9CCPHVY) | ✅ Set | Engine/Transmission Diagnostics |
| FF = Hot Open Loop Disabled By Malf 32. 0 = No Hot Open Loop Disable By Malf 32 | ✅ Set | Transmission Calibration |
| FF = AE Disabled By Malf 32. 0 = No AE Disable By Malf 32 | ✅ Set | Transmission Calibration |
| Non Zero = Disable P.E If In Hot Open Loop | ❌ Not Set | Engine/Transmission Diagnostics |
| Torque Management Option Flag Word | ❌ Not Set | Transmission Diagnostics |
| Enable SEM Condition (1=...) | ❌ Not Set | Transmission Diagnostics |
| Air Fuel Option Flag Word 3 Set IAC Pos To IACPARKP During A/C Slugging | ✅ Set | Engine/Transmission Diagnostics |
| Air Fuel Option Flag Word 3 Set C/L Int To 128 For Delta TPS AE | ❌ Not Set | Engine/Transmission Diagnostics |
| Air Fuel Option Flag Word 3 Set C/L Int To 128 For Delta TPS DE | ❌ Not Set | Engine/Transmission Diagnostics |
| Air Fuel Option Flag Word 3 Set SLWTRIM Initialised To KSLTINIT In AE | ❌ Not Set | Engine/Transmission Diagnostics |
| Air Fuel Option Flag Word 3 Set Enable In-phase Integrator Strategy | ❌ Not Set | Engine/Transmission Diagnostics |
| Air Fuel Option Flag Word 3 SLAIRBPW | ✅ Set | Engine/Transmission Diagnostics |
| Air Fuel Option Flag Word 3 EXTIDLEN | ✅ Set | Engine/Transmission Diagnostics |
| Air Fuel Option Flag Word 3 CLDFA | ✅ Set | Engine/Transmission Diagnostics |

---

## Tables

### 1. Min TCC Capacity

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (PSI)
- Y-Axis: 1 points (%)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 8.00 | 16.00 | 24.00 | 32.00 | 40.00 | 48.00 | 56.00 | 64.00 | 72.00 | 80.00 | 88.00 | 96.00 | 104.00 | 112.00 | 120.00 | 128.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 2. Max TCC Capacity

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (PSI)
- Y-Axis: 1 points (%)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 96.0784 
- Max: 96.0784 
- Avg: 96.0784 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 8.00 | 16.00 | 24.00 | 32.00 | 40.00 | 48.00 | 56.00 | 64.00 | 72.00 | 80.00 | 88.00 | 96.00 | 104.00 | 112.00 | 120.00 | 128.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 96.08 | 96.08 | 96.08 | 96.08 | 96.08 | 96.08 | 96.08 | 96.08 | 96.08 | 96.08 | 96.08 | 96.08 | 96.08 | 96.08 | 96.08 | 96.08 | 96.08 |

### 3. F6RMPDEC Vs Coolant Temperature

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (DEG/C)
- Y-Axis: 1 points
- Z-Axis (Data): 1 points (DEG/C)

**Statistics:**
- Min: 10.0000 DEG/C
- Max: 200.0000 DEG/C
- Avg: 76.6667 DEG/C
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | -40.00 | -16.00 | 8.00 | 32.00 | 56.00 | 80.00 | 104.00 | 128.00 | 152.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 200.00 | 180.00 | 140.00 | 80.00 | 40.00 | 20.00 | 10.00 | 10.00 | 10.00 |

### 4. Crank Fuel PW Vs Coolant

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (Milligram)
- Y-Axis: 27 points (Coolant)
- Z-Axis (Data): 27 points

**Statistics:**
- Min: 13.0000 
- Max: 254.0000 
- Avg: 73.9259 
- Dimensions: 27 × 1

**Full Data Table** (27 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| -40.00 | 254.00 |
| -34.00 | 230.00 |
| -28.00 | 206.00 |
| -22.00 | 184.00 |
| -16.00 | 163.00 |
| -10.00 | 143.00 |
| -4.00 | 123.00 |
| 2.00 | 105.00 |
| 8.00 | 88.00 |
| 14.00 | 75.00 |
| 20.00 | 62.00 |
| 26.00 | 52.00 |
| 32.00 | 43.00 |
| 38.00 | 36.00 |
| 44.00 | 31.00 |
| 50.00 | 26.00 |
| 56.00 | 23.00 |
| 62.00 | 20.00 |
| 68.00 | 18.00 |
| 74.00 | 17.00 |
| 80.00 | 16.00 |
| 86.00 | 15.00 |
| 92.00 | 14.00 |
| 98.00 | 13.00 |
| 104.00 | 13.00 |
| 110.00 | 13.00 |
| 116.00 | 13.00 |

### 5. % Of Enleanment Of Crank Fuel BPW Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (RPM)
- Y-Axis: 1 points (SCALER)
- Z-Axis (Data): 1 points (SCALER)

**Statistics:**
- Min: 0.0000 SCALER
- Max: 62.5000 SCALER
- Avg: 33.0882 SCALER
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 50.00 | 100.00 | 150.00 | 200.00 | 250.00 | 300.00 | 350.00 | 400.00 | 450.00 | 500.00 | 550.00 | 600.00 | 650.00 | 700.00 | 750.00 | 800.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 3.91 | 11.72 | 23.44 | 39.06 | 50.78 | 58.59 | 62.50 | 62.50 | 62.50 | 62.50 | 62.50 | 62.50 |

### 6. 0-1 Multiplier Of F64RCAL Vs Coolant Temperature

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 8 points (CLT)
- Y-Axis: 1 points (SCALER)
- Z-Axis (Data): 1 points (SCALER)

**Statistics:**
- Min: 0.5000 SCALER
- Max: 0.5000 SCALER
- Avg: 0.5000 SCALER
- Dimensions: 1 × 8

**Full Data Table** (1 rows × 8 cols):

| Y \ X | -40.00 | -16.00 | 8.00 | 32.00 | 56.00 | 80.00 | 104.00 | 128.00 |
|-----|------|------|------|------|------|------|------|------|
| 0.00 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 |

### 7. Crank Fuel PW Multiplier Vs Reference Pulses

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (REF/PULSE)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 0.5000 MULT
- Max: 0.9961 MULT
- Avg: 0.7645 MULT
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 8.00 | 16.00 | 24.00 | 32.00 | 40.00 | 48.00 | 56.00 | 64.00 | 72.00 | 80.00 | 88.00 | 96.00 | 104.00 | 112.00 | 120.00 | 128.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 1.00 | 0.80 | 0.75 | 0.90 | 0.81 | 0.75 | 0.67 | 0.58 | 0.50 | 0.50 | 0.58 | 0.67 | 0.75 | 0.75 | 1.00 | 1.00 | 1.00 |

### 8. Enleanment Multiplier Of F64XC BPW Vs Coolant For Short Run Cranking

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 8 points (DEG/C)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 0.0000 MULT
- Max: 39.8438 MULT
- Avg: 19.9707 MULT
- Dimensions: 1 × 8

**Full Data Table** (1 rows × 8 cols):

| Y \ X | -40.00 | -16.00 | 8.00 | 32.00 | 56.00 | 80.00 | 104.00 | 128.00 |
|-----|------|------|------|------|------|------|------|------|
| 0.00 | 39.84 | 39.84 | 35.94 | 28.12 | 16.02 | 0.00 | 0.00 | 0.00 |

### 9. % Enleanment Of Crank Fuel BPW Vs Load Selector

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 11 points (ENG PERF)
- Y-Axis: 1 points (%)
- Z-Axis (Data): 1 points (%)

**Statistics:**
- Min: 159.0000 %
- Max: 255.0000 %
- Avg: 234.8182 %
- Dimensions: 1 × 11

**Full Data Table** (1 rows × 11 cols):

| Y \ X | 96.00 | 112.00 | 128.00 | 144.00 | 160.00 | 176.00 | 192.00 | 208.00 | 224.00 | 240.00 | 256.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 159.00 | 189.00 | 215.00 | 235.00 | 255.00 | 255.00 | 255.00 | 255.00 | 255.00 | 255.00 | 255.00 |

### 10. Key On Prime Pulse 0-2 Multiplier Of F64XC Coolant Temperature

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (DEG/C)
- Y-Axis: 1 points
- Z-Axis (Data): 1 points (DEG/C)

**Statistics:**
- Min: 0.8984 DEG/C
- Max: 1.0000 DEG/C
- Avg: 0.9609 DEG/C
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | 20.00 | 32.00 | 44.00 | 56.00 | 68.00 | 80.00 | 92.00 | 104.00 | 116.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.95 | 0.90 | 0.90 | 0.90 |

### 11. Injector Offset Vs Battery Voltage

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (MSEC)
- Y-Axis: 17 points (VOLTS)
- Z-Axis (Data): 17 points (MSEC)

**Statistics:**
- Min: 0.0000 MSEC
- Max: 3.8311 MSEC
- Avg: 1.4520 MSEC
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 3.83 |
| 1.60 | 3.83 |
| 3.20 | 3.83 |
| 4.80 | 3.83 |
| 6.40 | 3.83 |
| 8.00 | 1.80 |
| 9.60 | 1.10 |
| 11.20 | 0.90 |
| 12.80 | 0.69 |
| 14.40 | 0.47 |
| 16.00 | 0.30 |
| 17.60 | 0.15 |
| 19.20 | 0.09 |
| 20.80 | 0.03 |
| 22.40 | 0.00 |
| 24.00 | 0.00 |
| 25.50 | 0.00 |

### 12. Low Pulse Width Injector Offset Vs Base Pulse Width

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (Msec)
- Y-Axis: 16 points (Msec)
- Z-Axis (Data): 16 points (Msec)

**Statistics:**
- Min: 0.0000 Msec
- Max: 0.4056 Msec
- Avg: 0.0939 Msec
- Dimensions: 16 × 1

**Full Data Table** (16 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.98 | 0.41 |
| 1.22 | 0.38 |
| 1.46 | 0.21 |
| 1.71 | 0.21 |
| 1.95 | 0.11 |
| 2.20 | 0.08 |
| 2.44 | 0.08 |
| 2.69 | 0.03 |
| 2.93 | 0.02 |
| 3.17 | 0.00 |
| 3.41 | 0.00 |
| 3.66 | 0.00 |
| 12 | 0.00 |
| 13 | 0.00 |
| 14 | 0.00 |
| 15 | 0.00 |

### 13. Injector - End of injection Target Vs Coolant Temp

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (Degrees)
- Y-Axis: 9 points (DegC)
- Z-Axis (Data): 9 points (Degrees)

**Statistics:**
- Min: 390.0000 Degrees
- Max: 390.0000 Degrees
- Avg: 390.0000 Degrees
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| -40.00 | 390.00 |
| -16.00 | 390.00 |
| 8.00 | 390.00 |
| 32.00 | 390.00 |
| 56.00 | 390.00 |
| 80.00 | 390.00 |
| 104.00 | 390.00 |
| 128.00 | 390.00 |
| 152.00 | 390.00 |

### 14. Fuel Trim Factor/ Injector Multiplier Vs RPM & Cylair

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (MGC)
- Y-Axis: 16 points (RPM)
- Z-Axis (Data): 272 points (MULTI)

**Statistics:**
- Min: 0.9141 MULTI
- Max: 1.0078 MULTI
- Avg: 0.9866 MULTI
- Dimensions: 16 × 17

**Full Data Table** (16 rows × 17 cols):

| Y \ X | 50.000 | 100.000 | 150.000 | 200.000 | 250.000 | 300.000 | 350.000 | 400.000 | 450.000 | 500.000 | 550.000 | 600.000 | 650.000 | 700.000 | 750.000 | 800.000 | 850.000 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 400.000 | 0.945 | 0.945 | 0.961 | 0.969 | 0.984 | 1.000 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 800.000 | 0.938 | 0.938 | 0.953 | 0.961 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 |
| 1200.000 | 0.922 | 0.938 | 0.953 | 0.961 | 0.977 | 0.977 | 0.977 | 0.977 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 |
| 1600.000 | 0.914 | 0.930 | 0.953 | 0.961 | 0.977 | 0.977 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 |
| 2000.000 | 0.914 | 0.930 | 0.953 | 0.961 | 0.969 | 0.977 | 0.977 | 0.984 | 0.992 | 0.992 | 0.992 | 0.992 | 0.992 | 0.992 | 0.992 | 0.992 | 0.992 |
| 2400.000 | 0.922 | 0.938 | 0.953 | 0.961 | 0.969 | 0.977 | 0.984 | 0.992 | 1.000 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 2800.000 | 0.922 | 0.938 | 0.953 | 0.961 | 0.969 | 0.977 | 0.984 | 1.000 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 3200.000 | 0.922 | 0.938 | 0.945 | 0.961 | 0.977 | 0.984 | 1.000 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 3600.000 | 0.938 | 0.938 | 0.945 | 0.961 | 0.984 | 1.000 | 1.000 | 1.000 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 4000.000 | 0.938 | 0.938 | 0.945 | 0.969 | 0.992 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 4400.000 | 0.938 | 0.938 | 0.945 | 0.969 | 0.992 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 4800.000 | 0.938 | 0.938 | 0.945 | 0.969 | 0.992 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 5200.000 | 0.938 | 0.938 | 0.945 | 0.969 | 0.992 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 5600.000 | 0.938 | 0.938 | 0.945 | 0.969 | 0.992 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 6000.000 | 0.938 | 0.938 | 0.945 | 0.969 | 0.992 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 6400.000 | 0.938 | 0.938 | 0.945 | 0.969 | 0.992 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |

### 15. Fuel Trim Factor / Injector Multiplier Vs RPM & Cylair > 850-1650

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (CYLAIR50)
- Y-Axis: 16 points (RPM)
- Z-Axis (Data): 272 points (MULT)

**Statistics:**
- Min: 0.9766 MULT
- Max: 1.0078 MULT
- Avg: 1.0020 MULT
- Dimensions: 16 × 17

**Full Data Table** (16 rows × 17 cols):

| Y \ X | 850.000 | 900.000 | 950.000 | 1000.000 | 1050.000 | 1100.000 | 1150.000 | 1200.000 | 1250.000 | 1300.000 | 1350.000 | 1400.000 | 1450.000 | 1500.000 | 1550.000 | 1600.000 | 1650.000 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 400.000 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 800.000 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 | 0.977 |
| 1200.000 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 |
| 1600.000 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 | 0.984 |
| 2000.000 | 0.992 | 0.992 | 0.992 | 0.992 | 0.992 | 0.992 | 0.992 | 0.992 | 0.992 | 0.992 | 0.992 | 0.992 | 0.992 | 0.992 | 0.992 | 0.992 | 0.992 |
| 2400.000 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 2800.000 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 3200.000 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 3600.000 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 4000.000 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 4400.000 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 4800.000 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 5200.000 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 5600.000 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 6000.000 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |
| 6400.000 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 | 1.008 |

### 16. If RPM >= CAL, Shut Off Fuel & Don't Turn Fuel Back On - Drive - P/N - Reverse

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 3 points
- Y-Axis: 2 points
- Z-Axis (Data): 6 points

**Statistics:**
- Min: 5875.0000 
- Max: 5900.0000 
- Avg: 5887.5000 
- Dimensions: 2 × 3

**Full Data Table** (2 rows × 3 cols):

| Row | C0 | C1 | C2 |
|-----|------|------|------|
| 0 | 5900.00 | 5875.00 | 5900.00 |
| 1 | 5875.00 | 5900.00 | 5875.00 |

### 17. Fuel Cutoff Air Fuel Ratio 0-2 Multiplier Vs Coolant Temp

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 14 points (DEG/C)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 1.0000 MULT
- Max: 1.9844 MULT
- Avg: 1.4453 MULT
- Dimensions: 1 × 14

**Full Data Table** (1 rows × 14 cols):

| Y \ X | -40.00 | -28.00 | -16.00 | -4.00 | 8.00 | 20.00 | 32.00 | 44.00 | 56.00 | 68.00 | 80.00 | 92.00 | 104.00 | 116.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 1.98 | 1.98 | 1.98 | 1.98 | 1.88 | 1.55 | 1.41 | 1.23 | 1.12 | 1.07 | 1.03 | 1.00 | 1.00 | 1.00 |

### 18. % Efficiency Values for Torque Conversion

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 5 points
- Y-Axis: 1 points
- Z-Axis (Data): 1 points (%)

**Statistics:**
- Min: 96.0938 %
- Max: 97.2656 %
- Avg: 96.6406 %
- Dimensions: 1 × 5

**Full Data Table** (1 rows × 5 cols):

| Y \ X | 0.00 | 1.00 | 2.00 | 3.00 | 4.00 |
|-----|------|------|------|------|------|
| 0 | 96.09 | 97.27 | 96.88 | 96.88 | 96.09 |

### 19. Engine Efficiency RPM Vs AFR

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 6 points (AFR)
- Y-Axis: 13 points (RPM)
- Z-Axis (Data): 78 points (EFFIC)

**Statistics:**
- Min: 0.4062 EFFIC
- Max: 1.1250 EFFIC
- Avg: 0.9118 EFFIC
- Dimensions: 13 × 6

**Full Data Table** (13 rows × 6 cols):

| Y \ X | 17.20 | 14.70 | 12.90 | 11.50 | 10.30 | 9.30 |
|-----|------|------|------|------|------|------|
| 800.00 | 0.63 | 0.72 | 0.75 | 0.62 | 0.52 | 0.41 |
| 1200.00 | 0.74 | 0.89 | 0.91 | 0.80 | 0.73 | 0.66 |
| 1600.00 | 0.83 | 0.98 | 1.02 | 0.95 | 0.91 | 0.85 |
| 2000.00 | 0.87 | 1.02 | 1.04 | 0.98 | 0.92 | 0.87 |
| 2400.00 | 0.86 | 1.00 | 1.05 | 0.98 | 0.92 | 0.87 |
| 2800.00 | 0.86 | 1.02 | 1.07 | 0.98 | 0.92 | 0.87 |
| 3200.00 | 0.86 | 1.02 | 1.08 | 0.97 | 0.91 | 0.86 |
| 3600.00 | 0.83 | 1.02 | 1.07 | 0.96 | 0.91 | 0.85 |
| 4000.00 | 0.81 | 1.01 | 1.08 | 0.95 | 0.90 | 0.84 |
| 4400.00 | 0.86 | 1.02 | 1.06 | 0.95 | 0.87 | 0.79 |
| 4800.00 | 0.88 | 1.03 | 1.07 | 0.95 | 0.89 | 0.82 |
| 5200.00 | 0.90 | 1.05 | 1.10 | 0.98 | 0.93 | 0.88 |
| 5600.00 | 0.93 | 1.08 | 1.12 | 1.04 | 1.00 | 0.96 |

### 20. Friction Torque Loss - RPM Vs Coolant

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 7 points (DEG/C)
- Y-Axis: 13 points (RPM)
- Z-Axis (Data): 91 points (FT-LBS)

**Statistics:**
- Min: 13.0000 FT-LBS
- Max: 68.0000 FT-LBS
- Avg: 40.5604 FT-LBS
- Dimensions: 13 × 7

**Full Data Table** (13 rows × 7 cols):

| Y \ X | -28.00 | -4.00 | 20.00 | 44.00 | 68.00 | 92.00 | 116.00 |
|-----|------|------|------|------|------|------|------|
| 800.00 | 68.00 | 24.00 | 18.00 | 15.00 | 13.00 | 13.00 | 14.00 |
| 1200.00 | 50.00 | 27.00 | 22.00 | 19.00 | 15.00 | 13.00 | 13.00 |
| 1600.00 | 43.00 | 31.00 | 24.00 | 20.00 | 16.00 | 15.00 | 14.00 |
| 2000.00 | 44.00 | 33.00 | 28.00 | 24.00 | 20.00 | 17.00 | 17.00 |
| 2400.00 | 47.00 | 39.00 | 34.00 | 29.00 | 24.00 | 22.00 | 20.00 |
| 2800.00 | 48.00 | 44.00 | 40.00 | 36.00 | 31.00 | 28.00 | 26.00 |
| 3200.00 | 67.00 | 50.00 | 43.00 | 39.00 | 35.00 | 33.00 | 31.00 |
| 3600.00 | 68.00 | 57.00 | 52.00 | 46.00 | 41.00 | 38.00 | 36.00 |
| 4000.00 | 62.00 | 56.00 | 54.00 | 51.00 | 49.00 | 47.00 | 44.00 |
| 4400.00 | 67.00 | 61.00 | 57.00 | 53.00 | 49.00 | 49.00 | 48.00 |
| 4800.00 | 67.00 | 61.00 | 58.00 | 55.00 | 52.00 | 49.00 | 48.00 |
| 5200.00 | 67.00 | 61.00 | 58.00 | 55.00 | 52.00 | 49.00 | 48.00 |
| 5600.00 | 67.00 | 61.00 | 58.00 | 55.00 | 52.00 | 49.00 | 48.00 |

### 21. Torque Pumping Loss - RPM Vs TPS

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 10 points (TPS%)
- Y-Axis: 13 points (RPM)
- Z-Axis (Data): 130 points (FT-LBS)

**Statistics:**
- Min: 0.0000 FT-LBS
- Max: 13.0000 FT-LBS
- Avg: 3.1308 FT-LBS
- Dimensions: 13 × 10

**Full Data Table** (13 rows × 10 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 25.00 | 37.50 | 50.00 | 62.50 | 75.00 | 87.50 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|
| 800.00 | 11.00 | 7.00 | 5.00 | 3.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 1200.00 | 12.00 | 10.00 | 8.00 | 4.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| 1600.00 | 13.00 | 12.00 | 11.00 | 9.00 | 5.00 | 2.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| 2000.00 | 10.00 | 10.00 | 10.00 | 8.00 | 5.00 | 2.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| 2400.00 | 10.00 | 10.00 | 10.00 | 8.00 | 6.00 | 3.00 | 3.00 | 2.00 | 1.00 | 0.00 |
| 2800.00 | 8.00 | 8.00 | 8.00 | 8.00 | 5.00 | 4.00 | 2.00 | 1.00 | 1.00 | 0.00 |
| 3200.00 | 7.00 | 7.00 | 7.00 | 6.00 | 4.00 | 3.00 | 2.00 | 1.00 | 1.00 | 0.00 |
| 3600.00 | 6.00 | 6.00 | 6.00 | 5.00 | 4.00 | 3.00 | 2.00 | 1.00 | 1.00 | 0.00 |
| 4000.00 | 4.00 | 3.00 | 3.00 | 3.00 | 2.00 | 2.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| 4400.00 | 3.00 | 2.00 | 2.00 | 2.00 | 2.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| 4800.00 | 3.00 | 2.00 | 2.00 | 2.00 | 2.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| 5200.00 | 3.00 | 2.00 | 2.00 | 2.00 | 2.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| 5600.00 | 3.00 | 2.00 | 2.00 | 2.00 | 2.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 22. Torque Multiplier Vs Speed Ratio - When Speed Ratio < 1

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (SPEED - RATIO)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 1.0000 MULT
- Max: 1.5781 MULT
- Avg: 1.2693 MULT
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 0.06 | 0.12 | 0.19 | 0.25 | 0.31 | 0.38 | 0.44 | 0.50 | 0.56 | 0.62 | 0.69 | 0.75 | 0.81 | 0.88 | 0.94 | 1.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 1.58 | 1.55 | 1.52 | 1.48 | 1.44 | 1.41 | 1.36 | 1.33 | 1.27 | 1.23 | 1.19 | 1.12 | 1.08 | 1.03 | 1.00 | 1.00 | 1.00 |

### 23. TPS For ENGPERF100 Learn Window Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 5 points (RPM)
- Y-Axis: 1 points (TPS%)
- Z-Axis (Data): 1 points (TPS%)

**Statistics:**
- Min: 35.1562 TPS%
- Max: 42.9688 TPS%
- Avg: 39.8438 TPS%
- Dimensions: 1 × 5

**Full Data Table** (1 rows × 5 cols):

| Y \ X | 1600.00 | 2000.00 | 2400.00 | 2800.00 | 3200.00 |
|-----|------|------|------|------|------|
| 0.00 | 35.16 | 37.11 | 41.41 | 42.58 | 42.97 |

### 24. Maximum Airflow Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (GRAMS SEC)
- Y-Axis: 17 points (RPM)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 14.0000 
- Max: 218.0000 
- Avg: 119.8824 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0 |
|-----|------|
| 0 | 14 |
| 400 | 20 |
| 800 | 30 |
| 1200 | 40 |
| 1600 | 50 |
| 2000 | 82 |
| 2400 | 96 |
| 2800 | 112 |
| 3200 | 128 |
| 3600 | 142 |
| 4000 | 150 |
| 4400 | 164 |
| 4800 | 178 |
| 5200 | 192 |
| 5600 | 204 |
| 6000 | 218 |
| 6400 | 218 |

### 25. Maximum Airflow Modifier (0-2) Vs ATSDEG

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 5 points (DEG/C)
- Y-Axis: 1 points (MULTIPLIER)
- Z-Axis (Data): 1 points (MULTIPLIER)

**Statistics:**
- Min: 1.0000 MULTIPLIER
- Max: 1.2578 MULTIPLIER
- Avg: 1.0594 MULTIPLIER
- Dimensions: 1 × 5

**Full Data Table** (1 rows × 5 cols):

| Y \ X | -40.00 | 8.00 | 56.00 | 104.00 | 152.00 |
|-----|------|------|------|------|------|
| 0.00 | 1.26 | 1.04 | 1.00 | 1.00 | 1.00 |

### 26. Stall Saver RPM Change Threshold Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 7 points (RPM)
- Y-Axis: 1 points (RPM)
- Z-Axis (Data): 1 points (RPM)

**Statistics:**
- Min: 0.0000 RPM
- Max: 6375.0000 RPM
- Avg: 1467.8571 RPM
- Dimensions: 1 × 7

**Full Data Table** (1 rows × 7 cols):

| Y \ X | 0.00 | 400.00 | 800.00 | 1200.00 | 1600.00 | 2000.00 | 2400.00 |
|-----|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 400.00 | 625.00 | 875.00 | 2000.00 | 6375.00 |

### 27. Warm-up Timer Countdown Value Vs Mode

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 24 points (MODE)
- Y-Axis: 1 points (SEC)
- Z-Axis (Data): 1 points (SEC)

**Statistics:**
- Min: 0.0000 SEC
- Max: 374.4000 SEC
- Avg: 137.2583 SEC
- Dimensions: 1 × 24

**Full Data Table** (1 rows × 24 cols):

| Y \ X | 1.00 | 2.00 | 3.00 | 4.00 | 5.00 | 6.00 | 7.00 | 8.00 | 9.00 | 10.00 | 11.00 | 12.00 | 13.00 | 14.00 | 15.00 | 16.00 | 17.00 | 18.00 | 19.00 | 20.00 | 21.00 | 22.00 | 23.00 | 24.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 374.40 | 351.00 | 328.00 | 305.60 | 283.20 | 260.80 | 238.40 | 216.00 | 193.60 | 172.00 | 150.40 | 127.20 | 104.00 | 81.60 | 59.20 | 36.00 | 12.80 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 28. Time Delay For TCS Vs Coolant Temp At Startup

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (DEG/C)
- Y-Axis: 1 points (SEC)
- Z-Axis (Data): 1 points (SEC)

**Statistics:**
- Min: 8.4375 SEC
- Max: 61.5625 SEC
- Avg: 23.1066 SEC
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | -40.00 | -28.00 | -16.00 | -4.00 | 8.00 | 20.00 | 32.00 | 44.00 | 56.00 | 68.00 | 80.00 | 92.00 | 104.00 | 116.00 | 128.00 | 140.00 | 152.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 61.56 | 55.31 | 52.19 | 43.44 | 34.06 | 27.50 | 19.69 | 14.69 | 12.81 | 10.94 | 10.00 | 8.44 | 8.44 | 8.44 | 8.44 | 8.44 | 8.44 |

### 29. TCS Warm-Up Timer Decrement Value Vs Airflow 12.5ms Per Count

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (GPS)
- Y-Axis: 1 points (COUNTS)
- Z-Axis (Data): 1 points (CNTS)

**Statistics:**
- Min: 1.0000 CNTS
- Max: 21.0000 CNTS
- Avg: 9.0588 CNTS
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 16.00 | 32.00 | 48.00 | 64.00 | 80.00 | 96.00 | 112.00 | 128.00 | 144.00 | 160.00 | 176.00 | 192.00 | 208.00 | 224.00 | 240.00 | 256.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 1.00 | 3.00 | 3.00 | 3.00 | 4.00 | 4.00 | 6.00 | 7.00 | 7.00 | 8.00 | 9.00 | 10.00 | 12.00 | 16.00 | 19.00 | 21.00 | 21.00 |

### 30. Traction Control Spark Retard Vs TCS Mode

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 24 points (MODE)
- Y-Axis: 1 points (DEG)
- Z-Axis (Data): 1 points (DEG)

**Statistics:**
- Min: 4.9219 DEG
- Max: 11.9531 DEG
- Avg: 7.0605 DEG
- Dimensions: 1 × 24

**Full Data Table** (1 rows × 24 cols):

| Y \ X | 1.00 | 2.00 | 3.00 | 4.00 | 5.00 | 6.00 | 7.00 | 8.00 | 9.00 | 10.00 | 11.00 | 12.00 | 13.00 | 14.00 | 15.00 | 16.00 | 17.00 | 18.00 | 19.00 | 20.00 | 21.00 | 22.00 | 23.00 | 24.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 4.92 | 4.92 | 8.09 | 4.92 | 8.09 | 4.92 | 9.84 | 4.92 | 9.84 | 4.92 | 9.14 | 8.09 | 11.95 | 4.92 | 8.09 | 4.92 | 9.84 | 4.92 | 8.09 | 4.92 | 8.09 | 8.09 | 8.09 | 4.92 |

### 31. Traction Control AFR Vs TCS Mode

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 24 points (MODE)
- Y-Axis: 1 points (RATIO)
- Z-Axis (Data): 1 points (RATIO)

**Statistics:**
- Min: 11.5380 RATIO
- Max: 13.2129 RATIO
- Avg: 12.4310 RATIO
- Dimensions: 1 × 24

**Full Data Table** (1 rows × 24 cols):

| Y \ X | 1.00 | 2.00 | 3.00 | 4.00 | 5.00 | 6.00 | 7.00 | 8.00 | 9.00 | 10.00 | 11.00 | 12.00 | 13.00 | 14.00 | 15.00 | 16.00 | 17.00 | 18.00 | 19.00 | 20.00 | 21.00 | 22.00 | 23.00 | 24.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 13.21 | 12.80 | 12.80 | 12.80 | 12.80 | 11.54 | 12.80 | 13.21 | 11.54 | 12.80 | 11.54 | 11.54 | 11.54 | 12.80 | 12.80 | 12.80 | 11.54 | 13.21 | 12.80 | 12.80 | 11.54 | 11.54 | 12.80 | 12.80 |

### 32. % Of Available Engine Torque - Mode Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (RPM)
- Y-Axis: 24 points (MODE)
- Z-Axis (Data): 408 points (TORQUE%)

**Statistics:**
- Min: 0.0000 TORQUE%
- Max: 599.0400 TORQUE%
- Avg: 237.4086 TORQUE%
- Dimensions: 24 × 17

**Full Data Table** (24 rows × 17 cols):

| Y \ X | 0.00 | 400.00 | 800.00 | 1200.00 | 1600.00 | 2000.00 | 2400.00 | 2800.00 | 3200.00 | 3600.00 | 4000.00 | 4400.00 | 4800.00 | 5200.00 | 5600.00 | 6000.00 | 6400.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 1.00 | 550.40 | 550.40 | 560.64 | 565.76 | 578.56 | 583.68 | 591.36 | 599.04 | 599.04 | 593.92 | 591.36 | 583.68 | 581.12 | 596.48 | 591.36 | 591.36 | 591.36 |
| 2.00 | 514.56 | 514.56 | 527.36 | 524.80 | 537.60 | 540.16 | 547.84 | 565.76 | 565.76 | 558.08 | 560.64 | 550.40 | 552.96 | 560.64 | 552.96 | 550.40 | 550.40 |
| 3.00 | 478.72 | 478.72 | 496.64 | 483.84 | 496.64 | 501.76 | 504.32 | 532.48 | 532.48 | 522.24 | 532.48 | 519.68 | 527.36 | 527.36 | 517.12 | 512.00 | 512.00 |
| 4.00 | 445.44 | 445.44 | 465.92 | 463.36 | 481.28 | 486.40 | 483.84 | 501.76 | 494.08 | 494.08 | 496.64 | 486.40 | 488.96 | 491.52 | 486.40 | 473.60 | 473.60 |
| 5.00 | 412.16 | 412.16 | 432.64 | 442.88 | 463.36 | 473.60 | 463.36 | 471.04 | 473.60 | 463.36 | 458.24 | 453.12 | 450.56 | 458.24 | 453.12 | 432.64 | 432.64 |
| 6.00 | 371.20 | 371.20 | 399.36 | 399.36 | 424.96 | 437.76 | 445.44 | 450.56 | 435.20 | 445.44 | 437.76 | 422.40 | 409.60 | 417.28 | 419.84 | 399.36 | 399.36 |
| 7.00 | 332.80 | 332.80 | 366.08 | 358.40 | 386.56 | 399.36 | 424.96 | 427.52 | 399.36 | 424.96 | 414.72 | 391.68 | 368.64 | 378.88 | 386.56 | 366.08 | 366.08 |
| 8.00 | 294.40 | 294.40 | 330.24 | 335.36 | 358.40 | 378.88 | 391.68 | 391.68 | 376.32 | 386.56 | 378.88 | 363.52 | 348.16 | 355.84 | 348.16 | 330.24 | 330.24 |
| 9.00 | 256.00 | 256.00 | 294.40 | 312.32 | 332.80 | 358.40 | 358.40 | 355.84 | 353.28 | 345.60 | 345.60 | 337.92 | 327.68 | 332.80 | 312.32 | 294.40 | 294.40 |
| 10.00 | 230.40 | 230.40 | 271.36 | 291.84 | 317.44 | 332.80 | 337.92 | 325.12 | 322.56 | 309.76 | 309.76 | 309.76 | 294.40 | 296.96 | 286.72 | 256.00 | 256.00 |
| 11.00 | 204.80 | 204.80 | 248.32 | 268.80 | 304.64 | 309.76 | 320.00 | 294.40 | 294.40 | 273.92 | 281.60 | 281.60 | 263.68 | 263.68 | 261.12 | 215.04 | 215.04 |
| 12.00 | 179.20 | 179.20 | 225.28 | 253.44 | 279.04 | 286.72 | 286.72 | 271.36 | 268.80 | 258.56 | 253.44 | 250.88 | 235.52 | 227.84 | 220.16 | 176.64 | 176.64 |
| 13.00 | 151.04 | 151.04 | 202.24 | 235.52 | 253.44 | 261.12 | 250.88 | 250.88 | 245.76 | 240.64 | 235.52 | 220.16 | 204.80 | 192.00 | 179.20 | 135.68 | 135.68 |
| 14.00 | 130.56 | 130.56 | 176.64 | 207.36 | 222.72 | 227.84 | 227.84 | 230.40 | 222.72 | 217.60 | 202.24 | 181.76 | 174.08 | 161.28 | 128.00 | 102.40 | 102.40 |
| 15.00 | 110.08 | 110.08 | 151.04 | 179.20 | 194.56 | 194.56 | 204.80 | 209.92 | 202.24 | 194.56 | 168.96 | 145.92 | 145.92 | 130.56 | 76.80 | 66.56 | 66.56 |
| 16.00 | 87.04 | 87.04 | 128.00 | 151.04 | 163.84 | 166.40 | 168.96 | 171.52 | 163.84 | 158.72 | 138.24 | 117.76 | 112.64 | 97.28 | 58.88 | 33.28 | 33.28 |
| 17.00 | 64.00 | 64.00 | 104.96 | 122.88 | 133.12 | 140.80 | 130.56 | 130.56 | 122.88 | 122.88 | 110.08 | 92.16 | 81.92 | 61.44 | 38.40 | 0.00 | 0.00 |
| 18.00 | 30.72 | 30.72 | 71.68 | 89.60 | 99.84 | 107.52 | 102.40 | 94.72 | 87.04 | 84.48 | 81.92 | 53.76 | 46.08 | 30.72 | 17.92 | 0.00 | 0.00 |
| 19.00 | 0.00 | 0.00 | 38.40 | 56.32 | 64.00 | 74.24 | 71.68 | 61.44 | 51.20 | 43.52 | 56.32 | 12.80 | 10.24 | 0.00 | 0.00 | 0.00 | 0.00 |
| 20.00 | 0.00 | 0.00 | 17.92 | 28.16 | 35.84 | 46.08 | 43.52 | 35.84 | 28.16 | 20.48 | 28.16 | 5.12 | 5.12 | 0.00 | 0.00 | 0.00 | 0.00 |
| 21.00 | 0.00 | 0.00 | 0.00 | 0.00 | 10.24 | 15.36 | 12.80 | 10.24 | 5.12 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 22.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 23.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 24.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 33. Adaptive Adjustment Factor For TCMAXTRQ, Based On Adaptive Spark Multiplier

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 10 points (MGC)
- Y-Axis: 15 points (RPM)
- Z-Axis (Data): 150 points (FACTOR)

**Statistics:**
- Min: 0.0000 FACTOR
- Max: 72.0000 FACTOR
- Avg: 24.3067 FACTOR
- Dimensions: 15 × 10

**Full Data Table** (15 rows × 10 cols):

| Y \ X | 400.00 | 450.00 | 500.00 | 550.00 | 600.00 | 650.00 | 700.00 | 750.00 | 800.00 | 850.00 |
|-----|------|------|------|------|------|------|------|------|------|------|
| 800.00 | 72.00 | 59.00 | 50.00 | 49.00 | 49.00 | 49.00 | 49.00 | 49.00 | 49.00 | 49.00 |
| 1200.00 | 40.00 | 35.00 | 30.00 | 51.00 | 51.00 | 51.00 | 51.00 | 51.00 | 51.00 | 51.00 |
| 1600.00 | 48.00 | 40.00 | 40.00 | 44.00 | 44.00 | 44.00 | 44.00 | 44.00 | 44.00 | 44.00 |
| 2000.00 | 28.00 | 34.00 | 34.00 | 39.00 | 39.00 | 39.00 | 39.00 | 39.00 | 39.00 | 39.00 |
| 2400.00 | 26.00 | 25.00 | 21.00 | 31.00 | 31.00 | 31.00 | 31.00 | 31.00 | 31.00 | 31.00 |
| 2800.00 | 21.00 | 20.00 | 15.00 | 26.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 |
| 3200.00 | 20.00 | 19.00 | 23.00 | 17.00 | 17.00 | 17.00 | 17.00 | 17.00 | 17.00 | 17.00 |
| 3600.00 | 20.00 | 15.00 | 18.00 | 19.00 | 19.00 | 19.00 | 19.00 | 19.00 | 19.00 | 19.00 |
| 4000.00 | 23.00 | 24.00 | 21.00 | 21.00 | 17.00 | 17.00 | 17.00 | 17.00 | 17.00 | 17.00 |
| 4400.00 | 35.00 | 30.00 | 25.00 | 25.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 |
| 4800.00 | 28.00 | 21.00 | 18.00 | 22.00 | 20.00 | 20.00 | 20.00 | 20.00 | 20.00 | 20.00 |
| 5200.00 | 20.00 | 20.00 | 15.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 |
| 5600.00 | 20.00 | 11.00 | 14.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 6000.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 6400.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 34. Amount To INC TCSCATTM By When Conditions Meet Vs Airflow 12.5ms Per Count

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (AIRFLOW GPS)
- Y-Axis: 1 points (COUNTS)
- Z-Axis (Data): 1 points (CNTS)

**Statistics:**
- Min: 0.0000 CNTS
- Max: 5.0000 CNTS
- Avg: 2.6471 CNTS
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 16.00 | 32.00 | 48.00 | 64.00 | 80.00 | 96.00 | 112.00 | 128.00 | 144.00 | 160.00 | 176.00 | 192.00 | 208.00 | 224.00 | 240.00 | 256.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 2.00 | 2.00 | 3.00 | 3.00 | 3.00 | 4.00 | 4.00 | 4.00 | 5.00 | 5.00 | 5.00 | 5.00 |

### 35. TCS Torque Reduction Mode Fuel Injector Cylinder U Suppression Table

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 50 points
- Y-Axis: 1 points (CNTS)
- Z-Axis (Data): 1 points (CNTS)

**Statistics:**
- Min: 0.0000 CNTS
- Max: 63.0000 CNTS
- Avg: 18.6400 CNTS
- Dimensions: 1 × 50

**Full Data Table** (1 rows × 50 cols):

| Row | C0 | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 | C13 | C14 | C15 | C16 | C17 | C18 | C19 | C20 | C21 | C22 | C23 | C24 | C25 | C26 | C27 | C28 | C29 | C30 | C31 | C32 | C33 | C34 | C35 | C36 | C37 | C38 | C39 | C40 | C41 | C42 | C43 | C44 | C45 | C46 | C47 | C48 | C49 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 5.00 | 1.00 | 5.00 | 1.00 | 5.00 | 5.00 | 5.00 | 5.00 | 21.00 | 5.00 | 21.00 | 5.00 | 21.00 | 21.00 | 21.00 | 21.00 | 23.00 | 21.00 | 23.00 | 21.00 | 23.00 | 23.00 | 23.00 | 23.00 | 31.00 | 23.00 | 31.00 | 23.00 | 31.00 | 31.00 | 31.00 | 31.00 | 63.00 | 31.00 | 63.00 | 63.00 | 63.00 | 63.00 |

### 36. Table For Shift Delay 1st to 2nd Change Vs Transmission Oil Temperature

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (DEG/C)
- Y-Axis: 1 points (SEC)
- Z-Axis (Data): 1 points (SEC)

**Statistics:**
- Min: 3.0000 SEC
- Max: 3.0000 SEC
- Avg: 3.0000 SEC
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | -40.00 | -16.00 | 8.00 | 32.00 | 56.00 | 80.00 | 104.00 | 128.00 | 156.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 |

### 37. Table For Shift Delay 2nd to 1st Change Vs Transmission Oil Temperature

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (DEG/C)
- Y-Axis: 1 points (SEC)
- Z-Axis (Data): 1 points (SEC)

**Statistics:**
- Min: 8.0000 SEC
- Max: 8.0000 SEC
- Avg: 8.0000 SEC
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | -40.00 | -16.00 | 8.00 | 32.00 | 56.00 | 80.00 | 104.00 | 128.00 | 156.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 |

### 38. Table For Shift Delay 2nd to 3rd Change Vs Transmission Oil Temperature

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (DEG/C)
- Y-Axis: 1 points (SEC)
- Z-Axis (Data): 1 points (SEC)

**Statistics:**
- Min: 8.0000 SEC
- Max: 8.0000 SEC
- Avg: 8.0000 SEC
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | -40.00 | -16.00 | 8.00 | 32.00 | 56.00 | 80.00 | 104.00 | 128.00 | 156.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 |

### 39. Table For Shift Delay 3rd to 2nd Change Vs Transmission Oil Temperature

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (DEG/C)
- Y-Axis: 1 points (SEC)
- Z-Axis (Data): 1 points (SEC)

**Statistics:**
- Min: 3.0000 SEC
- Max: 3.0000 SEC
- Avg: 3.0000 SEC
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | -40.00 | -16.00 | 8.00 | 32.00 | 56.00 | 80.00 | 104.00 | 128.00 | 156.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 |

### 40. Filter Coefficient For Multiplier Vs RPM For CYLAIR

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (RPM)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 0.1250 MULT
- Max: 1.6719 MULT
- Avg: 0.9030 MULT
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 400.00 | 800.00 | 1200.00 | 1600.00 | 2000.00 | 2400.00 | 2800.00 | 3200.00 | 3600.00 | 4000.00 | 4400.00 | 4800.00 | 5200.00 | 5600.00 | 6000.00 | 6400.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.12 | 0.12 | 0.25 | 0.38 | 0.50 | 0.62 | 0.73 | 0.84 | 0.94 | 1.03 | 1.12 | 1.22 | 1.31 | 1.41 | 1.50 | 1.59 | 1.67 |

### 41. MAF Complete Offset, Divider and Tables.

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 12 points (Raw Data)
- Y-Axis: 14 points (Table Number)
- Z-Axis (Data): 168 points

**Statistics:**
- Min: 0.0000 
- Max: 255.0000 
- Avg: 148.7321 
- Dimensions: 14 × 12

**Full Data Table** (14 rows × 12 cols):

| Y \ X | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 2 | 255 | 6 | 0 | 18 | 39 | 62 | 88 | 116 | 146 | 179 | 213 |
| 1 | 8 | 0 | 10 | 0 | 22 | 45 | 70 | 98 | 127 | 160 | 194 | 231 |
| 2 | 17 | 8 | 15 | 0 | 26 | 53 | 83 | 114 | 146 | 180 | 216 | 253 |
| 3 | 31 | 233 | 22 | 0 | 26 | 54 | 83 | 114 | 146 | 180 | 215 | 252 |
| 4 | 53 | 149 | 32 | 0 | 26 | 55 | 85 | 116 | 148 | 182 | 216 | 252 |
| 5 | 85 | 45 | 42 | 0 | 28 | 57 | 87 | 118 | 150 | 184 | 218 | 253 |
| 6 | 126 | 215 | 53 | 0 | 28 | 58 | 88 | 120 | 152 | 184 | 218 | 253 |
| 7 | 179 | 78 | 67 | 0 | 28 | 57 | 87 | 118 | 150 | 184 | 218 | 254 |
| 8 | 245 | 178 | 56 | 0 | 30 | 61 | 88 | 122 | 154 | 191 | 219 | 253 |
| 9 | 255 | 255 | 92 | 125 | 142 | 158 | 175 | 191 | 207 | 222 | 238 | 255 |
| 10 | 255 | 255 | 139 | 169 | 179 | 192 | 202 | 212 | 223 | 233 | 244 | 254 |
| 11 | 255 | 255 | 179 | 197 | 203 | 211 | 218 | 226 | 234 | 241 | 248 | 255 |
| 12 | 255 | 255 | 225 | 203 | 211 | 217 | 224 | 230 | 237 | 243 | 249 | 255 |
| 13 | 255 | 255 | 255 | 225 | 229 | 233 | 237 | 242 | 248 | 252 | 254 | 255 |

### 42. MAF Scaler Table 1-Scaled Hz

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (GRAMS SEC)
- Y-Axis: 9 points (Hz)
- Z-Axis (Data): 9 points (GPS)

**Statistics:**
- Min: 0.0000 GPS
- Max: 6.6562 GPS
- Avg: 2.1905 GPS
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 1890.00 | 0.00 |
| 2018.00 | 0.07 |
| 2146.00 | 0.30 |
| 2274.00 | 0.73 |
| 2402.00 | 1.38 |
| 2530.00 | 2.27 |
| 2658.00 | 3.42 |
| 2786.00 | 4.89 |
| 2914.00 | 6.66 |

### 43. MAF Scaler Table 2 -Scaled Hz

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (GRAMS SEC)
- Y-Axis: 9 points (Hz)
- Z-Axis (Data): 9 points (GRAMS SEC)

**Statistics:**
- Min: 0.0000 GRAMS SEC
- Max: 7.2188 GRAMS SEC
- Avg: 2.3937 GRAMS SEC
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 2914.00 | 0.00 |
| 3042.00 | 0.09 |
| 3170.00 | 0.35 |
| 3298.00 | 0.82 |
| 3426.00 | 1.53 |
| 3554.00 | 2.48 |
| 3682.00 | 3.75 |
| 3810.00 | 5.30 |
| 3938.00 | 7.22 |

### 44. MAF Scaler Table 3 -Scaled Hz

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (GRAMS SEC)
- Y-Axis: 9 points (Hz)
- Z-Axis (Data): 9 points (GRAMS SEC)

**Statistics:**
- Min: 0.0000 GRAMS SEC
- Max: 7.9062 GRAMS SEC
- Avg: 2.6836 GRAMS SEC
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 3938.00 | 0.00 |
| 4066.00 | 0.10 |
| 4194.00 | 0.41 |
| 4322.00 | 0.97 |
| 4450.00 | 1.78 |
| 4578.00 | 2.85 |
| 4706.00 | 4.22 |
| 4834.00 | 5.91 |
| 4962.00 | 7.91 |

### 45. MAF Scaler Table 4 -Scaled Hz

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (GRAMS SEC)
- Y-Axis: 9 points (Hz)
- Z-Axis (Data): 9 points (GRAMS SEC)

**Statistics:**
- Min: 0.0000 GRAMS SEC
- Max: 7.8750 GRAMS SEC
- Avg: 2.6780 GRAMS SEC
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 4962.00 | 0.00 |
| 5090.00 | 0.10 |
| 5218.00 | 0.42 |
| 5346.00 | 0.97 |
| 5474.00 | 1.78 |
| 5602.00 | 2.85 |
| 5730.00 | 4.22 |
| 5858.00 | 5.88 |
| 5986.00 | 7.88 |

### 46. MAF Scaler Table 5 -Scaled Hz

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (GRAMS SEC)
- Y-Axis: 9 points (Hz)
- Z-Axis (Data): 9 points (GRAMS SEC)

**Statistics:**
- Min: 0.0000 GRAMS SEC
- Max: 7.8750 GRAMS SEC
- Avg: 2.6975 GRAMS SEC
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 5986.00 | 0.00 |
| 6114.00 | 0.10 |
| 6242.00 | 0.43 |
| 6370.00 | 1.00 |
| 6498.00 | 1.81 |
| 6626.00 | 2.89 |
| 6754.00 | 4.27 |
| 6882.00 | 5.91 |
| 7010.00 | 7.88 |

### 47. MAF Scaler Table 6 -Scaled Hz

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (GRAMS SEC)
- Y-Axis: 9 points (Hz)
- Z-Axis (Data): 9 points (GRAMS SEC)

**Statistics:**
- Min: 0.0000 GRAMS SEC
- Max: 7.9062 GRAMS SEC
- Avg: 2.7253 GRAMS SEC
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 7010.00 | 0.00 |
| 7138.00 | 0.11 |
| 7266.00 | 0.45 |
| 7394.00 | 1.02 |
| 7522.00 | 1.84 |
| 7650.00 | 2.93 |
| 7778.00 | 4.31 |
| 7906.00 | 5.96 |
| 8034.00 | 7.91 |

### 48. MAF Scaler Table 7 -Scaled Hz

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (GRAMS SEC)
- Y-Axis: 9 points (Hz)
- Z-Axis (Data): 9 points (GRAMS SEC)

**Statistics:**
- Min: 0.0000 GRAMS SEC
- Max: 7.9062 GRAMS SEC
- Avg: 2.7352 GRAMS SEC
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 8034.00 | 0.00 |
| 8162.00 | 0.11 |
| 8290.00 | 0.45 |
| 8418.00 | 1.03 |
| 8546.00 | 1.88 |
| 8674.00 | 2.97 |
| 8802.00 | 4.31 |
| 8930.00 | 5.96 |
| 9058.00 | 7.91 |

### 49. MAF Scaler Table 8 -Scaled Hz

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (GRAMS SEC)
- Y-Axis: 9 points (Hz)
- Z-Axis (Data): 9 points (GRAMS SEC)

**Statistics:**
- Min: 0.0000 GRAMS SEC
- Max: 7.9375 GRAMS SEC
- Avg: 2.7287 GRAMS SEC
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 9058.00 | 0.00 |
| 9186.00 | 0.11 |
| 9314.00 | 0.45 |
| 9442.00 | 1.02 |
| 9570.00 | 1.84 |
| 9698.00 | 2.93 |
| 9826.00 | 4.31 |
| 9954.00 | 5.96 |
| 10082.00 | 7.94 |

### 50. MAF Scaler Table 9 -Scaled Hz

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (GRAMS SEC)
- Y-Axis: 9 points (Hz)
- Z-Axis (Data): 9 points (GRAMS SEC)

**Statistics:**
- Min: 0.0000 GRAMS SEC
- Max: 7.9062 GRAMS SEC
- Avg: 2.7678 GRAMS SEC
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 10082.00 | 0.00 |
| 10210.00 | 0.12 |
| 10338.00 | 0.48 |
| 10466.00 | 1.03 |
| 10594.00 | 1.91 |
| 10722.00 | 3.01 |
| 10850.00 | 4.48 |
| 10978.00 | 5.99 |
| 11106.00 | 7.91 |

### 51. MAF Scaler Table 10 -Scaled Hz

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (GRAMS SEC)
- Y-Axis: 9 points (Hz)
- Z-Axis (Data): 9 points (GRAMS SEC)

**Statistics:**
- Min: 0.0000 GRAMS SEC
- Max: 7.9688 GRAMS SEC
- Avg: 3.3941 GRAMS SEC
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 11106.00 | 0.00 |
| 11234.00 | 0.55 |
| 11362.00 | 1.23 |
| 11490.00 | 2.05 |
| 11618.00 | 2.98 |
| 11746.00 | 4.04 |
| 11874.00 | 5.20 |
| 12002.00 | 6.51 |
| 12130.00 | 7.97 |

### 52. MAF Scaler Table 11 -Scaled Hz

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (GRAMS SEC)
- Y-Axis: 9 points (Hz)
- Z-Axis (Data): 9 points (GRAMS SEC)

**Statistics:**
- Min: 0.0000 GRAMS SEC
- Max: 7.9375 GRAMS SEC
- Avg: 3.5894 GRAMS SEC
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 12130.00 | 0.00 |
| 12258.00 | 0.70 |
| 12386.00 | 1.50 |
| 12514.00 | 2.37 |
| 12642.00 | 3.31 |
| 12770.00 | 4.36 |
| 12898.00 | 5.46 |
| 13026.00 | 6.67 |
| 13154.00 | 7.94 |

### 53. MAF Scaler Table 12 -Scaled Hz

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (GRAMS SEC)
- Y-Axis: 9 points (Hz)
- Z-Axis (Data): 9 points (GRAMS SEC)

**Statistics:**
- Min: 0.0000 GRAMS SEC
- Max: 7.9688 GRAMS SEC
- Avg: 3.7218 GRAMS SEC
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 13154.00 | 0.00 |
| 13282.00 | 0.79 |
| 13410.00 | 1.65 |
| 13538.00 | 2.55 |
| 13666.00 | 3.53 |
| 13794.00 | 4.57 |
| 13922.00 | 5.65 |
| 14050.00 | 6.78 |
| 14178.00 | 7.97 |

### 54. MAF Scaler Table 13 -Scaled Hz

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (GRAMS SEC)
- Y-Axis: 9 points (Hz)
- Z-Axis (Data): 9 points (GRAMS SEC)

**Statistics:**
- Min: 0.0000 GRAMS SEC
- Max: 7.9688 GRAMS SEC
- Avg: 3.7600 GRAMS SEC
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 14178.00 | 0.00 |
| 14306.00 | 0.82 |
| 14434.00 | 1.70 |
| 14562.00 | 2.62 |
| 14690.00 | 3.59 |
| 14818.00 | 4.63 |
| 14946.00 | 5.70 |
| 15074.00 | 6.81 |
| 15202.00 | 7.97 |

### 55. MAF Scaler Table 14 -Scaled Hz

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (GRAMS SEC)
- Y-Axis: 9 points (Hz)
- Z-Axis (Data): 9 points (GRAMS SEC)

**Statistics:**
- Min: 0.0000 GRAMS SEC
- Max: 7.9688 GRAMS SEC
- Avg: 3.8819 GRAMS SEC
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 15202.00 | 0.00 |
| 15330.00 | 0.89 |
| 15458.00 | 1.82 |
| 15586.00 | 2.78 |
| 15714.00 | 3.78 |
| 15842.00 | 4.84 |
| 15970.00 | 5.91 |
| 16098.00 | 6.95 |
| 16226.00 | 7.97 |

### 56. Compensation Multiplier Vs Engine Speed For EDELTMAF = DELTMAF * FDMAFRML

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (RPM)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 0.2500 MULT
- Max: 3.9844 MULT
- Avg: 1.0285 MULT
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 400.00 | 800.00 | 1200.00 | 1600.00 | 2000.00 | 2400.00 | 2800.00 | 3200.00 | 3600.00 | 4000.00 | 4400.00 | 4800.00 | 5200.00 | 5600.00 | 6000.00 | 6400.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 3.98 | 3.98 | 2.00 | 1.33 | 1.00 | 0.80 | 0.67 | 0.58 | 0.50 | 0.44 | 0.41 | 0.36 | 0.33 | 0.31 | 0.28 | 0.27 | 0.25 |

### 57. Filtered Airflow Adjustment Vs EDELTMAF, For TAILMAF, For Increasing DELTMAF And Increasing Throttle

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (EDELTMAF MG/SEC)
- Y-Axis: 1 points
- Z-Axis (Data): 1 points (COEFF)

**Statistics:**
- Min: 0.1250 COEFF
- Max: 0.1641 COEFF
- Avg: 0.1296 COEFF
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 2.00 | 4.00 | 6.00 | 8.00 | 10.00 | 12.00 | 14.00 | 16.00 | 18.00 | 20.00 | 22.00 | 24.00 | 26.00 | 28.00 | 30.00 | 32.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.16 | 0.15 | 0.14 | 0.13 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 |

### 58. Filtered Airflow Adjustment Vs EDELTMAF For TAILMAF, For Decreasing DELTAMAF And Increasing Throttle

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (EDELTMAF MG/SEC)
- Y-Axis: 1 points
- Z-Axis (Data): 1 points (COEFF)

**Statistics:**
- Min: 0.1250 COEFF
- Max: 0.1250 COEFF
- Avg: 0.1250 COEFF
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 2.00 | 4.00 | 6.00 | 8.00 | 10.00 | 12.00 | 14.00 | 16.00 | 18.00 | 20.00 | 22.00 | 24.00 | 26.00 | 28.00 | 30.00 | 32.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 |

### 59. Filtered Airflow Adjustment Vs EDELTMAF For TAILMAF, For Increasing DELTAMAF And Decreasing Throttle

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (EDELTMAF MG/SEC)
- Y-Axis: 1 points
- Z-Axis (Data): 1 points (COEFF)

**Statistics:**
- Min: 0.1172 COEFF
- Max: 0.1172 COEFF
- Avg: 0.1172 COEFF
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 2.00 | 4.00 | 6.00 | 8.00 | 10.00 | 12.00 | 14.00 | 16.00 | 18.00 | 20.00 | 22.00 | 24.00 | 26.00 | 28.00 | 30.00 | 32.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 |

### 60. Filtered Airflow Adjustment Vs EDELTMAF For TAILMAF, For Decreasing DELTAMAF And Decreasing Throttle

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (EDELTMAF MG/SEC)
- Y-Axis: 1 points
- Z-Axis (Data): 1 points (COEFF)

**Statistics:**
- Min: 0.1172 COEFF
- Max: 0.1406 COEFF
- Avg: 0.1220 COEFF
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 2.00 | 4.00 | 6.00 | 8.00 | 10.00 | 12.00 | 14.00 | 16.00 | 18.00 | 20.00 | 22.00 | 24.00 | 26.00 | 28.00 | 30.00 | 32.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.14 | 0.14 | 0.14 | 0.13 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 |

### 61. Compensation Multiplier Vs Engine Speed For Increasing Flow

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (RPM)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 0.7188 MULT
- Max: 1.2500 MULT
- Avg: 1.0551 MULT
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 400.00 | 800.00 | 1200.00 | 1600.00 | 2000.00 | 2400.00 | 2800.00 | 3200.00 | 3600.00 | 4000.00 | 4400.00 | 4800.00 | 5200.00 | 5600.00 | 6000.00 | 6400.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.72 | 0.72 | 0.86 | 0.95 | 1.00 | 1.02 | 1.03 | 1.05 | 1.06 | 1.09 | 1.12 | 1.16 | 1.19 | 1.22 | 1.25 | 1.25 | 1.25 |

### 62. Compensation Multiplier Vs Engine Speed For Decreasing Flow

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (RPM)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 0.8281 MULT
- Max: 3.0000 MULT
- Avg: 1.8787 MULT
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 400.00 | 800.00 | 1200.00 | 1600.00 | 2000.00 | 2400.00 | 2800.00 | 3200.00 | 3600.00 | 4000.00 | 4400.00 | 4800.00 | 5200.00 | 5600.00 | 6000.00 | 6400.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.83 | 0.83 | 0.88 | 0.94 | 1.00 | 1.08 | 1.17 | 1.33 | 1.56 | 1.92 | 2.41 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 |

### 63. Compensation Multiplier Vs Temperature For Increasing Flow

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (DEG/C)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 1.0000 MULT
- Max: 2.0000 MULT
- Avg: 1.4053 MULT
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | -40.00 | -28.00 | -16.00 | -4.00 | 8.00 | 20.00 | 32.00 | 44.00 | 56.00 | 68.00 | 80.00 | 92.00 | 104.00 | 116.00 | 128.00 | 140.00 | 152.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 1.73 | 1.52 | 1.33 | 1.19 | 1.09 | 1.03 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

### 64. Compensation Multiplier Vs Temperature For Decreasing Flow

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (DEG/C)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 1.0000 MULT
- Max: 3.9844 MULT
- Avg: 2.1774 MULT
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | -40.00 | -28.00 | -16.00 | -4.00 | 8.00 | 20.00 | 32.00 | 44.00 | 56.00 | 68.00 | 80.00 | 92.00 | 104.00 | 116.00 | 128.00 | 140.00 | 152.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 3.98 | 3.98 | 3.98 | 3.98 | 3.98 | 3.12 | 2.42 | 1.86 | 1.45 | 1.19 | 1.05 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

### 65. Filtered Airflow Coefficient Vs EDELTMAF For SPIKEMAF Increasing DMAF/Flow

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (EDELTMAF MG/SEC)
- Y-Axis: 1 points
- Z-Axis (Data): 1 points (COEFF)

**Statistics:**
- Min: 0.1641 COEFF
- Max: 0.2031 COEFF
- Avg: 0.1893 COEFF
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 4.00 | 8.00 | 12.00 | 16.00 | 20.00 | 24.00 | 28.00 | 32.00 | 36.00 | 40.00 | 44.00 | 48.00 | 52.00 | 56.00 | 60.00 | 64.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.17 | 0.18 | 0.19 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 |

### 66. Filtered Airflow Coefficient Vs EDELTMAF For SPIKEMAF Increasing Flow/ Decreasing DMAF

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (EDELTMAF MG/SEC)
- Y-Axis: 1 points
- Z-Axis (Data): 1 points (COEFF)

**Statistics:**
- Min: 0.1250 COEFF
- Max: 0.1250 COEFF
- Avg: 0.1250 COEFF
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 4.00 | 8.00 | 12.00 | 16.00 | 20.00 | 24.00 | 28.00 | 32.00 | 36.00 | 40.00 | 44.00 | 48.00 | 52.00 | 56.00 | 60.00 | 64.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 |

### 67. Filtered Airflow Coefficient Vs EDELTMAF For SPIKEMAF Iincreasing DMAF/ Decreasing Flow

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (EDELTMAF MG/SEC)
- Y-Axis: 1 points
- Z-Axis (Data): 1 points (COEFF)

**Statistics:**
- Min: 0.1875 COEFF
- Max: 0.3438 COEFF
- Avg: 0.2645 COEFF
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 2.00 | 4.00 | 6.00 | 8.00 | 10.00 | 12.00 | 14.00 | 16.00 | 18.00 | 20.00 | 22.00 | 24.00 | 26.00 | 28.00 | 30.00 | 32.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.19 | 0.20 | 0.23 | 0.28 | 0.34 | 0.34 | 0.34 | 0.33 | 0.32 | 0.30 | 0.29 | 0.27 | 0.25 | 0.23 | 0.21 | 0.19 | 0.19 |

### 68. Filtered Airflow Coefficient Vs EDELTMAF For SPIKEMAF Decreasing DMAF/ Decreasing Flow

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (EDELTMAF MG/SEC)
- Y-Axis: 1 points
- Z-Axis (Data): 1 points (COEFF)

**Statistics:**
- Min: 0.1172 COEFF
- Max: 0.1758 COEFF
- Avg: 0.1461 COEFF
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 2.00 | 4.00 | 6.00 | 8.00 | 10.00 | 12.00 | 14.00 | 16.00 | 18.00 | 20.00 | 22.00 | 24.00 | 26.00 | 28.00 | 30.00 | 32.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.12 | 0.14 | 0.15 | 0.16 | 0.17 | 0.18 | 0.18 | 0.17 | 0.16 | 0.16 | 0.15 | 0.14 | 0.13 | 0.12 | 0.12 | 0.12 | 0.12 |

### 69. Compensation Multiplier Vs TPSRATEX For Increasing Flow SPIKEMAF

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 33 points (TPSRATEX)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 1.0000 MULT
- Max: 1.0000 MULT
- Avg: 1.0000 MULT
- Dimensions: 1 × 33

**Full Data Table** (1 rows × 33 cols):

| Y \ X | 0.00 | 1.00 | 2.00 | 3.00 | 4.00 | 5.00 | 6.00 | 7.00 | 8.00 | 9.00 | 10.00 | 11.00 | 12.00 | 13.00 | 14.00 | 15.00 | 16.00 | 17.00 | 18.00 | 19.00 | 20.00 | 21.00 | 22.00 | 23.00 | 24.00 | 25.00 | 26.00 | 27.00 | 28.00 | 29.00 | 30.00 | 31.00 | 32.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

### 70. Compensation Multiplier Vs TPSRATEX For Decreasing Flow SPIKEMAF

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 33 points (TPSRATEX)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 0.6016 MULT
- Max: 0.6016 MULT
- Avg: 0.6016 MULT
- Dimensions: 1 × 33

**Full Data Table** (1 rows × 33 cols):

| Y \ X | 0.00 | 1.00 | 2.00 | 3.00 | 4.00 | 5.00 | 6.00 | 7.00 | 8.00 | 9.00 | 10.00 | 11.00 | 12.00 | 13.00 | 14.00 | 15.00 | 16.00 | 17.00 | 18.00 | 19.00 | 20.00 | 21.00 | 22.00 | 23.00 | 24.00 | 25.00 | 26.00 | 27.00 | 28.00 | 29.00 | 30.00 | 31.00 | 32.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 |

### 71. Blending Multiplier Vs INCNTR (12.5MS LOOP) For Increasing Flow

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 33 points (INCNTR)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 0.0000 MULT
- Max: 0.9961 MULT
- Avg: 0.0907 MULT
- Dimensions: 1 × 33

**Full Data Table** (1 rows × 33 cols):

| Y \ X | 0.00 | 1.00 | 2.00 | 3.00 | 4.00 | 5.00 | 6.00 | 7.00 | 8.00 | 9.00 | 10.00 | 11.00 | 12.00 | 13.00 | 14.00 | 15.00 | 16.00 | 17.00 | 18.00 | 19.00 | 20.00 | 21.00 | 22.00 | 23.00 | 24.00 | 25.00 | 26.00 | 27.00 | 28.00 | 29.00 | 30.00 | 31.00 | 32.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 1.00 | 0.90 | 0.70 | 0.40 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 72. Blending Multiplier Vs OUTCNTR (3X LOOP) For Decreasing Flow

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 33 points (OUTCNTR)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 0.0000 MULT
- Max: 0.9961 MULT
- Avg: 0.4305 MULT
- Dimensions: 1 × 33

**Full Data Table** (1 rows × 33 cols):

| Y \ X | 0.00 | 1.00 | 2.00 | 3.00 | 4.00 | 5.00 | 6.00 | 7.00 | 8.00 | 9.00 | 10.00 | 11.00 | 12.00 | 13.00 | 14.00 | 15.00 | 16.00 | 17.00 | 18.00 | 19.00 | 20.00 | 21.00 | 22.00 | 23.00 | 24.00 | 25.00 | 26.00 | 27.00 | 28.00 | 29.00 | 30.00 | 31.00 | 32.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.95 | 0.85 | 0.70 | 0.50 | 0.25 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 73. Spark Retard Vs Reference Pulses After Shift to P/N

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (REF PULSES IN P/N)
- Y-Axis: 1 points (DEG)
- Z-Axis (Data): 1 points (DEG)

**Statistics:**
- Min: 0.0000 DEG
- Max: 0.0000 DEG
- Avg: 0.0000 DEG
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | 0.00 | 8.00 | 16.00 | 24.00 | 32.00 | 40.00 | 48.00 | 56.00 | 64.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 74. Base ECT Spark Table

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 14 points (CYLAIR50)
- Y-Axis: 12 points (Deg/C)
- Z-Axis (Data): 168 points (DEG)

**Statistics:**
- Min: -4.4141 DEG
- Max: 1.5625 DEG
- Avg: -0.1242 DEG
- Dimensions: 12 × 14

**Full Data Table** (12 rows × 14 cols):

| Y \ X | 50.00 | 100.00 | 150.00 | 200.00 | 250.00 | 300.00 | 350.00 | 400.00 | 450.00 | 500.00 | 550.00 | 600.00 | 650.00 | 700.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| -4.00 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | 0.51 | 0.86 | 1.56 | 0.86 | 0.86 | 0.86 | 0.86 |
| 8.00 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | 0.51 | 0.86 | 1.56 | 0.86 | 0.86 | 0.86 | 0.86 |
| 20.00 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | 0.51 | 0.86 | 1.56 | 0.86 | 0.86 | 0.86 | 0.86 |
| 32.00 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | 0.51 | 0.86 | 1.56 | 0.86 | 0.86 | 0.86 | 0.86 |
| 44.00 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | 0.51 | 0.86 | 1.56 | 0.86 | 0.86 | 0.86 | 0.86 |
| 56.00 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | 0.51 | 0.86 | 1.56 | 0.86 | 0.86 | 0.86 | 0.86 |
| 68.00 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | 0.51 | 0.86 | 1.56 | 0.86 | 0.86 | 0.86 | 0.86 |
| 80.00 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | 0.51 | 0.86 | 1.56 | 0.86 | 0.86 | 0.86 | 0.86 |
| 92.00 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 |
| 104.00 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -1.25 | -1.60 | -1.60 | -0.90 | -0.90 | -0.90 | -0.90 |
| 116.00 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -0.55 | -1.95 | -3.01 | -3.01 | -3.01 | -1.95 | -1.60 | -1.60 | -1.60 |
| 128.00 | -0.20 | -0.20 | -0.20 | -0.20 | -0.20 | -1.25 | -3.01 | -4.41 | -4.41 | -4.41 | -3.01 | -2.66 | -2.66 | -2.66 |

### 75. Cold Spark Offset Table

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 14 points (MG/CYL)
- Y-Axis: 7 points (RPM)
- Z-Axis (Data): 98 points (DEG)

**Statistics:**
- Min: 0.1562 DEG
- Max: 5.0781 DEG
- Avg: 1.4047 DEG
- Dimensions: 7 × 14

**Full Data Table** (7 rows × 14 cols):

| Y \ X | 50.00 | 100.00 | 150.00 | 200.00 | 250.00 | 300.00 | 350.00 | 400.00 | 450.00 | 500.00 | 550.00 | 600.00 | 650.00 | 700.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 400.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 2.97 | 4.02 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 600.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 2.27 | 4.02 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 800.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 2.27 | 2.97 | 2.97 | 3.67 | 4.02 | 4.02 | 4.02 | 4.02 |
| 1000.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 2.27 | 2.27 | 2.27 | 2.27 | 2.27 | 2.27 | 2.27 |
| 1200.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.86 | 1.21 | 1.21 | 1.21 | 1.21 | 1.21 | 1.21 |
| 1400.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.51 | 0.51 | 0.51 | 0.51 | 0.51 | 0.51 |
| 1600.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 |

### 76. Cold Spark Multiplier

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (MULT)
- Y-Axis: 6 points (DEG/C)
- Z-Axis (Data): 6 points (Spark Advance)

**Statistics:**
- Min: 0.0000 Spark Advance
- Max: 0.9961 Spark Advance
- Avg: 0.6647 Spark Advance
- Dimensions: 6 × 1

**Full Data Table** (6 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| -40.00 | 1.00 |
| -16.00 | 1.00 |
| 8.00 | 1.00 |
| 32.00 | 0.67 |
| 56.00 | 0.33 |
| 80.00 | 0.00 |

### 77. Run Time Advance Correction Table

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 11 points (CYLAIR50)
- Y-Axis: 1 points (DEG)
- Z-Axis (Data): 1 points (DEG)

**Statistics:**
- Min: 0.1562 DEG
- Max: 0.1562 DEG
- Avg: 0.1562 DEG
- Dimensions: 1 × 11

**Full Data Table** (1 rows × 11 cols):

| Y \ X | 50.00 | 100.00 | 150.00 | 200.00 | 250.00 | 300.00 | 350.00 | 400.00 | 450.00 | 500.00 | 550.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 |

### 78. Run Time Advance Multiplier

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 7 points (RUN TIME)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 0.0000 MULT
- Max: 0.0000 MULT
- Avg: 0.0000 MULT
- Dimensions: 1 × 7

**Full Data Table** (1 rows × 7 cols):

| Y \ X | 0.00 | 8.00 | 16.00 | 24.00 | 32.00 | 40.00 | 48.00 |
|-----|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 79. Run Time Advance Multiplier P/N

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 8 points (DEG/C)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 0.0000 MULT
- Max: 0.0000 MULT
- Avg: 0.0000 MULT
- Dimensions: 1 × 8

**Full Data Table** (1 rows × 8 cols):

| Y \ X | 8.00 | 20.00 | 32.00 | 44.00 | 56.00 | 68.00 | 80.00 | 92.00 |
|-----|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 80. Run Time Advance Multiplier Drive & M/T

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 8 points (DEG/C)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 0.0000 MULT
- Max: 0.0000 MULT
- Avg: 0.0000 MULT
- Dimensions: 1 × 8

**Full Data Table** (1 rows × 8 cols):

| Y \ X | 8.00 | 20.00 | 32.00 | 44.00 | 56.00 | 68.00 | 80.00 | 92.00 |
|-----|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 81. Main High-Octane Spark Table < 4800 RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (CYLAIR50)
- Y-Axis: 17 points (RPM)
- Z-Axis (Data): 289 points (DEG)

**Statistics:**
- Min: -10.0391 DEG
- Max: 50.0781 DEG
- Avg: 22.1149 DEG
- Dimensions: 17 × 17

**Full Data Table** (17 rows × 17 cols):

| Y \ X | 50.00 | 100.00 | 150.00 | 200.00 | 250.00 | 300.00 | 350.00 | 400.00 | 450.00 | 500.00 | 550.00 | 600.00 | 650.00 | 700.00 | 750.00 | 800.00 | 850.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 400.00 | 34.96 | 34.96 | 30.74 | 20.20 | 12.11 | 7.19 | 1.91 | -2.30 | -5.47 | -8.28 | -10.04 | -10.04 | -10.04 | -10.04 | -10.04 | -10.04 | -10.04 |
| 600.00 | 37.07 | 37.07 | 32.15 | 23.71 | 17.38 | 13.52 | 9.30 | 4.73 | 0.86 | -1.95 | -4.77 | -6.52 | -6.52 | -6.52 | -6.52 | -6.52 | -6.52 |
| 800.00 | 38.48 | 38.48 | 33.20 | 27.23 | 22.66 | 19.49 | 15.62 | 11.76 | 8.24 | 4.38 | 0.86 | -1.25 | -2.30 | -2.30 | -2.30 | -2.30 | -2.30 |
| 1000.00 | 39.88 | 39.88 | 34.61 | 28.98 | 24.41 | 23.01 | 21.25 | 15.98 | 12.46 | 8.95 | 6.13 | 4.02 | 3.32 | 3.32 | 3.32 | 3.32 | 3.32 |
| 1200.00 | 40.94 | 40.94 | 36.02 | 30.39 | 25.47 | 24.06 | 22.30 | 19.84 | 16.68 | 13.16 | 10.00 | 7.89 | 7.19 | 7.19 | 7.19 | 7.19 | 7.19 |
| 1400.00 | 41.99 | 41.99 | 37.07 | 31.09 | 26.52 | 24.77 | 23.71 | 22.66 | 19.49 | 16.33 | 13.16 | 11.05 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 |
| 1600.00 | 43.05 | 43.05 | 37.42 | 31.80 | 27.93 | 26.17 | 25.12 | 24.06 | 21.95 | 19.14 | 15.98 | 13.52 | 12.81 | 12.81 | 12.81 | 12.81 | 12.81 |
| 1800.00 | 44.10 | 44.10 | 38.12 | 32.15 | 28.98 | 27.58 | 26.17 | 25.12 | 23.71 | 20.90 | 17.73 | 15.62 | 14.92 | 14.92 | 14.92 | 14.92 | 14.92 |
| 2000.00 | 45.16 | 45.16 | 38.12 | 32.15 | 30.39 | 28.28 | 26.88 | 26.17 | 25.12 | 23.01 | 19.84 | 17.73 | 16.68 | 16.68 | 16.68 | 16.68 | 16.68 |
| 2200.00 | 45.86 | 45.86 | 38.12 | 32.85 | 31.09 | 29.34 | 27.58 | 26.52 | 26.17 | 24.06 | 21.25 | 19.14 | 18.09 | 17.38 | 17.38 | 17.38 | 17.38 |
| 2400.00 | 46.56 | 46.56 | 38.83 | 32.85 | 31.09 | 29.34 | 27.93 | 26.88 | 26.17 | 25.47 | 22.30 | 20.20 | 18.79 | 18.09 | 18.09 | 18.09 | 18.09 |
| 2800.00 | 47.27 | 48.32 | 38.83 | 32.85 | 31.09 | 28.98 | 27.93 | 26.88 | 26.52 | 26.17 | 23.71 | 21.95 | 19.84 | 18.44 | 18.44 | 18.44 | 18.44 |
| 3200.00 | 46.91 | 49.38 | 39.88 | 32.85 | 31.09 | 28.98 | 27.93 | 27.58 | 26.52 | 26.17 | 24.06 | 22.30 | 20.55 | 18.79 | 18.79 | 18.79 | 18.79 |
| 3600.00 | 46.21 | 49.73 | 38.83 | 33.55 | 31.09 | 28.98 | 28.63 | 27.58 | 26.88 | 26.17 | 24.06 | 21.95 | 19.84 | 18.09 | 18.09 | 18.09 | 18.09 |
| 4000.00 | 45.16 | 50.08 | 38.12 | 33.55 | 32.15 | 30.04 | 28.63 | 27.93 | 27.58 | 26.88 | 23.71 | 21.25 | 19.49 | 17.73 | 17.73 | 17.73 | 17.73 |
| 4400.00 | 44.10 | 50.08 | 37.07 | 33.55 | 32.15 | 30.04 | 28.98 | 28.28 | 27.58 | 26.17 | 23.36 | 21.25 | 19.49 | 17.73 | 17.73 | 17.73 | 17.73 |
| 4800.00 | 43.05 | 50.08 | 40.23 | 35.66 | 32.85 | 31.09 | 30.04 | 29.34 | 28.28 | 26.52 | 23.71 | 21.60 | 19.84 | 18.44 | 18.44 | 18.44 | 18.44 |

### 82. Main High-Octane Spark Table > 4800 RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (CYLAIR50)
- Y-Axis: 5 points (RPM)
- Z-Axis (Data): 85 points (DEG)

**Statistics:**
- Min: 0.1562 DEG
- Max: 50.0781 DEG
- Avg: 24.5381 DEG
- Dimensions: 5 × 17

**Full Data Table** (5 rows × 17 cols):

| Y \ X | 50.00 | 100.00 | 150.00 | 200.00 | 250.00 | 300.00 | 350.00 | 400.00 | 450.00 | 500.00 | 550.00 | 600.00 | 650.00 | 700.00 | 750.00 | 800.00 | 850.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 4800.00 | 43.05 | 50.08 | 40.23 | 35.66 | 32.85 | 31.09 | 30.04 | 29.34 | 28.28 | 26.52 | 23.71 | 21.60 | 19.84 | 18.44 | 18.44 | 18.44 | 18.44 |
| 5200.00 | 41.99 | 50.08 | 45.16 | 40.59 | 36.37 | 32.85 | 31.09 | 30.04 | 28.98 | 27.93 | 25.82 | 23.71 | 21.95 | 20.55 | 20.55 | 20.55 | 20.55 |
| 5600.00 | 41.99 | 50.08 | 47.97 | 43.05 | 38.12 | 34.26 | 31.80 | 30.74 | 29.69 | 28.28 | 25.47 | 24.41 | 22.66 | 21.25 | 21.25 | 21.25 | 21.25 |
| 6000.00 | 41.99 | 50.08 | 47.97 | 43.05 | 38.12 | 34.26 | 32.15 | 30.74 | 29.69 | 28.63 | 27.58 | 25.82 | 24.06 | 22.66 | 22.66 | 22.66 | 22.66 |
| 6400.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 |

### 83. Main High-Octane Spark Table > 850-1650mg

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (CYLAIR50)
- Y-Axis: 16 points (RPM)
- Z-Axis (Data): 272 points (DEG)

**Statistics:**
- Min: -10.0391 DEG
- Max: 22.6562 DEG
- Avg: 5.2849 DEG
- Dimensions: 16 × 17

**Full Data Table** (16 rows × 17 cols):

| Y \ X | 850.00 | 900.00 | 950.00 | 1000.00 | 1050.00 | 1100.00 | 1150.00 | 1200.00 | 1250.00 | 1300.00 | 1350.00 | 1400.00 | 1450.00 | 1500.00 | 1550.00 | 1600.00 | 1650.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 400.00 | -10.04 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 800.00 | -2.30 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 1200.00 | 7.19 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 1600.00 | 12.81 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 2000.00 | 16.68 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 2400.00 | 18.09 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 2800.00 | 18.44 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 3200.00 | 18.79 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 3600.00 | 18.09 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 4000.00 | 17.73 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 4400.00 | 17.73 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 4800.00 | 18.44 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 5200.00 | 20.55 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 5600.00 | 21.25 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 6000.00 | 22.66 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 6400.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 |

### 84. Main Low-Octane Spark Table < 4800 RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (CYLAIR50)
- Y-Axis: 17 points (RPM)
- Z-Axis (Data): 289 points (DEG)

**Statistics:**
- Min: -23.0469 DEG
- Max: 50.0781 DEG
- Avg: 13.9073 DEG
- Dimensions: 17 × 17

**Full Data Table** (17 rows × 17 cols):

| Y \ X | 50.00 | 100.00 | 150.00 | 200.00 | 250.00 | 300.00 | 350.00 | 400.00 | 450.00 | 500.00 | 550.00 | 600.00 | 650.00 | 700.00 | 750.00 | 800.00 | 850.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 400.00 | 34.96 | 34.96 | 30.74 | 17.73 | 7.19 | -1.25 | -7.93 | -13.20 | -17.77 | -20.94 | -22.70 | -23.05 | -23.05 | -23.05 | -23.05 | -23.05 | -23.05 |
| 600.00 | 37.07 | 37.07 | 32.15 | 21.25 | 12.11 | 4.38 | -1.60 | -7.23 | -11.45 | -14.61 | -17.07 | -18.83 | -18.83 | -18.83 | -18.83 | -18.83 | -18.83 |
| 800.00 | 38.48 | 38.48 | 33.20 | 24.77 | 16.33 | 9.65 | 4.02 | -0.90 | -5.12 | -8.63 | -11.09 | -13.55 | -14.96 | -14.96 | -14.96 | -14.96 | -14.96 |
| 1000.00 | 39.88 | 39.88 | 34.61 | 27.58 | 20.20 | 13.87 | 8.24 | 3.32 | -0.55 | -3.71 | -6.52 | -8.63 | -8.98 | -8.98 | -8.98 | -8.98 | -8.98 |
| 1200.00 | 40.94 | 40.94 | 36.02 | 30.39 | 24.06 | 17.73 | 12.11 | 7.19 | 3.32 | 0.16 | -2.30 | -4.06 | -5.12 | -5.12 | -5.12 | -5.12 | -5.12 |
| 1400.00 | 41.99 | 41.99 | 37.07 | 31.09 | 26.52 | 20.55 | 14.57 | 10.35 | 6.84 | 3.67 | 0.86 | -1.25 | -1.95 | -1.95 | -1.95 | -1.95 | -1.95 |
| 1600.00 | 43.05 | 43.05 | 37.42 | 31.80 | 27.93 | 22.30 | 16.68 | 12.46 | 8.95 | 5.78 | 3.32 | 1.21 | 0.51 | 0.51 | 0.51 | 0.51 | 0.51 |
| 1800.00 | 44.10 | 44.10 | 38.12 | 32.15 | 28.98 | 24.06 | 18.44 | 14.57 | 10.70 | 7.54 | 5.08 | 3.32 | 2.27 | 2.27 | 2.27 | 2.27 | 2.27 |
| 2000.00 | 45.16 | 45.16 | 38.12 | 32.15 | 29.34 | 24.77 | 19.84 | 15.62 | 12.11 | 8.95 | 6.84 | 5.08 | 4.02 | 4.02 | 4.02 | 4.02 | 4.02 |
| 2200.00 | 45.86 | 45.86 | 38.12 | 32.85 | 30.04 | 25.12 | 20.55 | 16.33 | 13.52 | 10.35 | 8.24 | 6.48 | 5.08 | 4.73 | 4.73 | 4.73 | 4.73 |
| 2400.00 | 46.56 | 46.56 | 38.83 | 32.85 | 30.04 | 25.47 | 20.90 | 17.03 | 13.87 | 11.41 | 9.30 | 7.54 | 6.13 | 5.43 | 5.43 | 5.43 | 5.43 |
| 2800.00 | 47.27 | 48.32 | 38.83 | 32.85 | 31.09 | 26.17 | 20.90 | 17.73 | 15.27 | 13.16 | 11.05 | 9.30 | 7.54 | 6.13 | 6.13 | 6.13 | 6.13 |
| 3200.00 | 46.91 | 49.38 | 39.88 | 32.85 | 31.09 | 25.82 | 20.90 | 17.38 | 15.62 | 13.52 | 11.05 | 9.65 | 7.89 | 6.13 | 6.13 | 6.13 | 6.13 |
| 3600.00 | 46.21 | 49.73 | 38.83 | 33.55 | 30.39 | 24.77 | 20.55 | 17.03 | 15.27 | 13.16 | 11.05 | 9.30 | 7.54 | 6.13 | 6.13 | 6.13 | 6.13 |
| 4000.00 | 45.16 | 50.08 | 38.12 | 33.55 | 30.74 | 25.12 | 20.55 | 17.03 | 14.57 | 12.81 | 11.05 | 8.95 | 7.54 | 6.13 | 6.13 | 6.13 | 6.13 |
| 4400.00 | 44.10 | 50.08 | 37.07 | 33.55 | 31.09 | 25.12 | 20.55 | 17.38 | 14.92 | 12.81 | 10.70 | 8.95 | 7.54 | 6.13 | 6.13 | 6.13 | 6.13 |
| 4800.00 | 43.05 | 50.08 | 40.23 | 35.66 | 32.85 | 26.88 | 22.66 | 19.14 | 16.33 | 14.22 | 12.11 | 10.00 | 8.24 | 6.84 | 6.84 | 6.84 | 6.84 |

### 85. Main Low-Octane Spark Table > 4800 RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (CYLAIR50)
- Y-Axis: 5 points (RPM)
- Z-Axis (Data): 85 points (DEG)

**Statistics:**
- Min: 0.1562 DEG
- Max: 50.0781 DEG
- Avg: 19.9182 DEG
- Dimensions: 5 × 17

**Full Data Table** (5 rows × 17 cols):

| Y \ X | 50.00 | 100.00 | 150.00 | 200.00 | 250.00 | 300.00 | 350.00 | 400.00 | 450.00 | 500.00 | 550.00 | 600.00 | 650.00 | 700.00 | 750.00 | 800.00 | 850.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 4800.00 | 43.05 | 50.08 | 40.23 | 35.66 | 32.85 | 26.88 | 22.66 | 19.14 | 16.33 | 14.22 | 12.11 | 10.00 | 8.24 | 6.84 | 6.84 | 6.84 | 6.84 |
| 5200.00 | 41.99 | 50.08 | 45.16 | 40.59 | 36.37 | 30.04 | 25.12 | 20.90 | 18.09 | 15.98 | 14.22 | 12.46 | 10.70 | 9.65 | 9.65 | 9.65 | 9.65 |
| 5600.00 | 41.99 | 50.08 | 47.97 | 43.05 | 38.12 | 32.50 | 28.28 | 24.77 | 21.95 | 19.49 | 17.38 | 15.62 | 13.87 | 12.46 | 12.46 | 12.46 | 12.46 |
| 6000.00 | 41.99 | 50.08 | 47.97 | 43.05 | 38.12 | 34.26 | 30.74 | 27.93 | 25.12 | 23.36 | 21.25 | 19.49 | 17.73 | 16.33 | 16.33 | 16.33 | 16.33 |
| 6400.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 |

### 86. Main Low-Octane Spark Table > 850-1650mg

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (CYLAIR50)
- Y-Axis: 16 points (RPM)
- Z-Axis (Data): 272 points (DEG)

**Statistics:**
- Min: -23.0469 DEG
- Max: 16.3281 DEG
- Avg: 4.6477 DEG
- Dimensions: 16 × 17

**Full Data Table** (16 rows × 17 cols):

| Y \ X | 850.00 | 900.00 | 950.00 | 1000.00 | 1050.00 | 1100.00 | 1150.00 | 1200.00 | 1250.00 | 1300.00 | 1350.00 | 1400.00 | 1450.00 | 1500.00 | 1550.00 | 1600.00 | 1650.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 400.00 | -23.05 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 800.00 | -14.96 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 1200.00 | -5.12 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 1600.00 | 0.51 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 2000.00 | 4.02 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 2400.00 | 5.43 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 2800.00 | 6.13 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 3200.00 | 6.13 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 3600.00 | 6.13 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 4000.00 | 6.13 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 4400.00 | 6.13 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 4800.00 | 6.84 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 5200.00 | 9.65 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 5600.00 | 12.46 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 6000.00 | 16.33 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| 6400.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 |

### 87. Spark IAT Table

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 14 points (CYLAIR50)
- Y-Axis: 8 points (DEG/C)
- Z-Axis (Data): 112 points (DEG)

**Statistics:**
- Min: -12.8516 DEG
- Max: 1.5625 DEG
- Avg: -1.9657 DEG
- Dimensions: 8 × 14

**Full Data Table** (8 rows × 14 cols):

| Y \ X | 50.00 | 100.00 | 150.00 | 200.00 | 250.00 | 300.00 | 350.00 | 400.00 | 450.00 | 500.00 | 550.00 | 600.00 | 650.00 | 700.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| -25.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.86 | 1.56 | 1.56 | 1.56 | 1.56 | 1.56 | 1.56 | 1.21 | 1.21 |
| -3.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.86 | 1.56 | 1.56 | 1.56 | 1.56 | 1.56 | 1.56 | 1.21 | 1.21 |
| 11.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.86 | 1.56 | 1.56 | 1.56 | 1.56 | 1.56 | 1.56 | 1.21 | 1.21 |
| 22.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 |
| 33.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | -1.60 | -1.60 | -1.60 | -1.60 | -1.60 | -1.60 | -1.25 | -1.25 | -1.25 |
| 46.00 | -1.25 | -1.25 | -1.25 | -1.25 | -1.25 | -3.71 | -3.36 | -3.36 | -3.36 | -3.36 | -3.36 | -3.01 | -2.66 | -2.66 |
| 65.00 | -3.71 | -3.71 | -3.71 | -3.71 | -3.71 | -6.88 | -6.17 | -6.17 | -6.17 | -6.17 | -5.82 | -5.47 | -5.12 | -5.12 |
| 78.00 | -8.98 | -8.98 | -8.98 | -8.98 | -8.98 | -12.85 | -11.45 | -11.09 | -11.45 | -11.80 | -11.09 | -10.04 | -9.34 | -9.34 |

### 88. Spark IAT Multiplier

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (RPM)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.9961 
- Max: 0.9961 
- Avg: 0.9961 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 400.00 | 800.00 | 1200.00 | 1600.00 | 2000.00 | 2400.00 | 2800.00 | 3200.00 | 3600.00 | 4000.00 | 4400.00 | 4800.00 | 5200.00 | 5600.00 | 6000.00 | 6400.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

### 89. Individual Cylinder Spark Modification Table

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 6 points (CYLINDER)
- Y-Axis: 1 points (DEG)
- Z-Axis (Data): 1 points (DEG)

**Statistics:**
- Min: 0.0000 DEG
- Max: 0.0000 DEG
- Avg: 0.0000 DEG
- Dimensions: 1 × 6

**Full Data Table** (1 rows × 6 cols):

| Y \ X | 6.00 | 5.00 | 4.00 | 3.00 | 2.00 | 1.00 |
|-----|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 90. Individual Cylinder Spark Multiplier

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (RPM)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 0.0000 MULT
- Max: 0.0000 MULT
- Avg: 0.0000 MULT
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 400.00 | 800.00 | 1200.00 | 1600.00 | 2000.00 | 2400.00 | 2800.00 | 3200.00 | 3600.00 | 4000.00 | 4400.00 | 4800.00 | 5200.00 | 5600.00 | 6000.00 | 6400.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 91. Individual Cylinder Spark Multiplier

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 14 points (CYLAIR50)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 0.0000 MULT
- Max: 0.0000 MULT
- Avg: 0.0000 MULT
- Dimensions: 1 × 14

**Full Data Table** (1 rows × 14 cols):

| Y \ X | 50.00 | 100.00 | 150.00 | 200.00 | 250.00 | 300.00 | 350.00 | 400.00 | 450.00 | 500.00 | 550.00 | 600.00 | 650.00 | 700.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 92. Idle Spark Advance Vs Coolant Deg

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (SPARK DEG)
- Y-Axis: 11 points (DEG/C)
- Z-Axis (Data): 11 points

**Statistics:**
- Min: 26.5234 
- Max: 26.5234 
- Avg: 26.5234 
- Dimensions: 11 × 1

**Full Data Table** (11 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 8.00 | 26.52 |
| 20.00 | 26.52 |
| 32.00 | 26.52 |
| 44.00 | 26.52 |
| 56.00 | 26.52 |
| 68.00 | 26.52 |
| 80.00 | 26.52 |
| 92.00 | 26.52 |
| 104.00 | 26.52 |
| 116.00 | 26.52 |
| 128.00 | 26.52 |

### 93. Retarded Idle Spark Advance Vs Coolant Deg

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (SPARK DEG)
- Y-Axis: 11 points (DEG/C)
- Z-Axis (Data): 11 points

**Statistics:**
- Min: 26.5234 
- Max: 26.5234 
- Avg: 26.5234 
- Dimensions: 11 × 1

**Full Data Table** (11 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 8.00 | 26.52 |
| 20.00 | 26.52 |
| 32.00 | 26.52 |
| 44.00 | 26.52 |
| 56.00 | 26.52 |
| 68.00 | 26.52 |
| 80.00 | 26.52 |
| 92.00 | 26.52 |
| 104.00 | 26.52 |
| 116.00 | 26.52 |
| 128.00 | 26.52 |

### 94. Idle Spark Multiplier Vs CYLAIR50

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 11 points (CYLAIR50)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 1.0000 
- Max: 1.0000 
- Avg: 1.0000 
- Dimensions: 1 × 11

**Full Data Table** (1 rows × 11 cols):

| Y \ X | 50.00 | 100.00 | 150.00 | 200.00 | 250.00 | 300.00 | 350.00 | 400.00 | 450.00 | 500.00 | 550.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

### 95. Spark Timing when Cranking Low RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (RPM)
- Y-Axis: 6 points (DEG/C)
- Z-Axis (Data): 102 points (SPARK DEG)

**Statistics:**
- Min: 15.1562 SPARK DEG
- Max: 15.1562 SPARK DEG
- Avg: 15.1562 SPARK DEG
- Dimensions: 6 × 17

**Full Data Table** (6 rows × 17 cols):

| Y \ X | 0.00 | 32.00 | 64.00 | 96.00 | 128.00 | 160.00 | 192.00 | 224.00 | 256.00 | 288.00 | 320.00 | 352.00 | 384.00 | 416.00 | 448.00 | 480.00 | 512.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| -4.00 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 |
| 20.00 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 |
| 44.00 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 |
| 68.00 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 |
| 92.00 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 |
| 116.00 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 |

### 96. Spark Timing when Cranking High RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (RPM)
- Y-Axis: 6 points (DEG/C)
- Z-Axis (Data): 102 points (SPARK DEG)

**Statistics:**
- Min: 15.1562 SPARK DEG
- Max: 15.1562 SPARK DEG
- Avg: 15.1562 SPARK DEG
- Dimensions: 6 × 17

**Full Data Table** (6 rows × 17 cols):

| Y \ X | 512.00 | 544.00 | 576.00 | 608.00 | 640.00 | 672.00 | 704.00 | 736.00 | 768.00 | 800.00 | 832.00 | 864.00 | 896.00 | 928.00 | 960.00 | 992.00 | 1024.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| -4.00 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 |
| 20.00 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 |
| 44.00 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 |
| 68.00 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 |
| 92.00 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 |
| 116.00 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 | 15.16 |

### 97. Spark Advance/Retard Vs Time In Power Enrichment

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (SEC)
- Y-Axis: 1 points (DEG)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 1.5625 
- Max: 1.5625 
- Avg: 1.5625 
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | 0.00 | 3.20 | 6.40 | 9.60 | 12.80 | 16.00 | 19.20 | 22.40 | 25.60 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 1.56 | 1.56 | 1.56 | 1.56 | 1.56 | 1.56 | 1.56 | 1.56 | 1.56 |

### 98. Power Enrichment Spark Trim Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 8 points (RPM)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 0.9961 
- Avg: 0.5605 
- Dimensions: 1 × 8

**Full Data Table** (1 rows × 8 cols):

| Y \ X | 800.00 | 1600.00 | 2400.00 | 3200.00 | 4000.00 | 4800.00 | 5600.00 | 6400.00 |
|-----|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.50 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |

### 99. Power Enrichment Spark Trim Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 8 points (RPM)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 1 × 8

**Full Data Table** (1 rows × 8 cols):

| Y \ X | 800.00 | 1600.00 | 2400.00 | 3200.00 | 4000.00 | 4800.00 | 5600.00 | 6400.00 |
|-----|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 100. Table Bias for Bump Spark Vs Coolant

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (DEGREES CELSIUS)
- Y-Axis: 1 points
- Z-Axis (Data): 1 points (DEG/C)

**Statistics:**
- Min: 23.9062 DEG/C
- Max: 31.6406 DEG/C
- Avg: 26.9531 DEG/C
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | -40.00 | -28.00 | -16.00 | -4.00 | 8.00 | 20.00 | 32.00 | 44.00 | 56.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 23.91 | 23.91 | 23.91 | 23.91 | 24.61 | 29.53 | 30.23 | 30.94 | 31.64 |

### 101. Table Bias for Bump Spark Vs Air Temp

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 6 points (IAT)
- Y-Axis: 1 points
- Z-Axis (Data): 1 points (DEG/C)

**Statistics:**
- Min: 0.0000 DEG/C
- Max: 2.4609 DEG/C
- Avg: 0.8203 DEG/C
- Dimensions: 1 × 6

**Full Data Table** (1 rows × 6 cols):

| Y \ X | -40.00 | -16.00 | 8.00 | 32.00 | 56.00 | 80.00 |
|-----|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.35 | 0.70 | 1.41 | 2.46 |

### 102. Table Bias for Bump Spark Vs TPS

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points
- Z-Axis (Data): 1 points (DEG/C)

**Statistics:**
- Min: 0.0000 DEG/C
- Max: 3.5156 DEG/C
- Avg: 2.6884 DEG/C
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.70 | 1.41 | 2.11 | 2.81 | 3.52 | 3.52 | 3.52 | 3.52 | 3.52 | 3.52 | 3.52 | 3.52 | 3.52 | 3.52 | 3.52 |

### 103. Tip-in Bump Spark Vs TPS & RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (%TPS)
- Y-Axis: 8 points (RPM)
- Z-Axis (Data): 136 points (DEG)

**Statistics:**
- Min: 34.4531 DEG
- Max: 76.9922 DEG
- Avg: 52.4785 DEG
- Dimensions: 8 × 17

**Full Data Table** (8 rows × 17 cols):

| Y \ X | 0.00 | 4.00 | 8.00 | 12.00 | 16.00 | 20.00 | 24.00 | 28.00 | 32.00 | 36.00 | 40.00 | 44.00 | 48.00 | 52.00 | 56.00 | 60.00 | 64.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 800.00 | 64.34 | 52.38 | 46.76 | 42.89 | 40.08 | 37.97 | 36.21 | 35.16 | 34.80 | 34.45 | 34.45 | 34.45 | 34.45 | 34.45 | 34.45 | 34.45 | 34.45 |
| 1200.00 | 68.20 | 61.88 | 56.60 | 52.03 | 48.52 | 46.05 | 43.95 | 42.54 | 41.84 | 41.48 | 41.48 | 41.13 | 41.13 | 41.13 | 41.13 | 41.13 | 41.13 |
| 1600.00 | 69.61 | 66.09 | 61.88 | 58.01 | 54.49 | 51.68 | 49.57 | 47.81 | 46.76 | 46.05 | 45.35 | 45.35 | 45.00 | 45.00 | 45.00 | 45.00 | 45.00 |
| 2000.00 | 72.77 | 68.55 | 64.69 | 60.82 | 57.30 | 54.49 | 52.03 | 50.27 | 49.22 | 48.52 | 48.16 | 47.81 | 47.46 | 47.46 | 47.46 | 47.46 | 47.46 |
| 2400.00 | 74.88 | 71.37 | 67.50 | 62.58 | 59.06 | 56.25 | 54.14 | 52.38 | 51.33 | 50.62 | 49.92 | 49.57 | 49.22 | 48.87 | 48.87 | 48.87 | 48.87 |
| 2800.00 | 74.18 | 74.18 | 72.07 | 67.50 | 61.88 | 57.30 | 54.49 | 52.73 | 51.68 | 50.98 | 50.27 | 49.92 | 49.57 | 49.22 | 49.22 | 49.22 | 49.22 |
| 3200.00 | 73.12 | 76.64 | 76.99 | 72.42 | 65.74 | 59.77 | 55.90 | 54.14 | 52.73 | 51.68 | 50.98 | 50.62 | 50.62 | 50.27 | 50.27 | 50.27 | 50.27 |
| 3600.00 | 71.72 | 74.53 | 75.94 | 75.59 | 68.55 | 61.52 | 57.30 | 54.84 | 53.44 | 52.38 | 51.33 | 50.62 | 50.62 | 50.27 | 50.27 | 50.27 | 50.27 |

### 104. Tip-in Bump Decay Vs TPS

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (%TPS)
- Y-Axis: 1 points (DEG/SEC)
- Z-Axis (Data): 1 points (DEG/SEC)

**Statistics:**
- Min: 10.5469 DEG/SEC
- Max: 21.0938 DEG/SEC
- Avg: 12.5000 DEG/SEC
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | 0.00 | 12.50 | 25.00 | 37.50 | 50.00 | 62.50 | 75.00 | 87.50 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 21.09 | 15.82 | 12.30 | 10.55 | 10.55 | 10.55 | 10.55 | 10.55 | 10.55 |

### 105. Start-Up Adaptive Spark Multiplier Correction Vs Coolant

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (COOLDEG DEG/C)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.8984 
- Max: 0.9844 
- Avg: 0.9523 
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | 8.00 | 20.00 | 32.00 | 44.00 | 56.00 | 68.00 | 80.00 | 92.00 | 104.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.90 | 0.91 | 0.93 | 0.95 | 0.96 | 0.97 | 0.98 | 0.98 | 0.98 |

### 106. High Octane Adaptive Spark Decrease Load Threshold Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (RPM)
- Y-Axis: 1 points (MG/CYL)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 312.5000 
- Max: 996.0938 
- Avg: 495.6342 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 400.00 | 800.00 | 1200.00 | 1600.00 | 2000.00 | 2400.00 | 2800.00 | 3200.00 | 3600.00 | 4000.00 | 4400.00 | 4800.00 | 5200.00 | 5600.00 | 6000.00 | 6400.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 996.09 | 406.25 | 375.00 | 343.75 | 312.50 | 312.50 | 312.50 | 312.50 | 343.75 | 375.00 | 406.25 | 437.50 | 468.75 | 500.00 | 531.25 | 996.09 | 996.09 |

### 107. Low Octane Adaptive Spark Decrease Load Threshold Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (RPM)
- Y-Axis: 1 points (MG/CYL)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 218.7500 
- Max: 996.0938 
- Avg: 389.9357 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 400.00 | 800.00 | 1200.00 | 1600.00 | 2000.00 | 2400.00 | 2800.00 | 3200.00 | 3600.00 | 4000.00 | 4400.00 | 4800.00 | 5200.00 | 5600.00 | 6000.00 | 6400.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 996.09 | 312.50 | 281.25 | 250.00 | 218.75 | 218.75 | 218.75 | 218.75 | 250.00 | 281.25 | 312.50 | 343.75 | 375.00 | 406.25 | 449.22 | 500.00 | 996.09 |

### 108. Neighbour Cell Adaptive Spark Multiplier Update Table

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 6 points (BLM CELL)
- Y-Axis: 2 points (CELL #)
- Z-Axis (Data): 12 points

**Statistics:**
- Min: 0.0000 
- Max: 102.0000 
- Avg: 23.7500 
- Dimensions: 2 × 6

**Full Data Table** (2 rows × 6 cols):

| Y \ X | 1.00 | 2.00 | 3.00 | 4.00 | 5.00 | 6.00 |
|-----|------|------|------|------|------|------|
| 1.00 | 1.00 | 2.00 | 3.00 | 4.00 | 5.00 | 6.00 |
| 2.00 | 8.00 | 0.00 | 26.00 | 51.00 | 77.00 | 102.00 |

### 109. Adaptive Spark 0-2 Multiplier Vs Coolant Temp

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (DEG/C COOLANT TEMP)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 1.0000 
- Avg: 0.6667 
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | -40.00 | -16.00 | 8.00 | 32.00 | 56.00 | 80.00 | 104.00 | 128.00 | 152.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.20 | 0.40 | 0.60 | 0.80 | 1.00 | 1.00 | 1.00 | 1.00 |

### 110. ESC Attack Rate Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (RPM)
- Y-Axis: 1 points (DEG/V)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.6504 
- Max: 1.3184 
- Avg: 1.1798 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 400.00 | 800.00 | 1200.00 | 1600.00 | 2000.00 | 2400.00 | 2800.00 | 3200.00 | 3600.00 | 4000.00 | 4400.00 | 4800.00 | 5200.00 | 5600.00 | 6000.00 | 6400.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.65 | 0.77 | 0.90 | 1.00 | 1.11 | 1.20 | 1.27 | 1.30 | 1.32 | 1.32 | 1.32 | 1.32 | 1.32 | 1.32 | 1.32 | 1.32 | 1.32 |

### 111. ESC Attack Rate 0-2 Multiplier Vs ADSPKRT (RTD From Hi Oct Table)

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 18 points (DEG OF ADSPKRT)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 1.0000 
- Max: 1.0000 
- Avg: 1.0000 
- Dimensions: 1 × 18

**Full Data Table** (1 rows × 18 cols):

| Y \ X | 0.00 | 0.70 | 1.41 | 2.11 | 2.81 | 3.52 | 4.22 | 4.92 | 5.62 | 6.33 | 7.03 | 7.74 | 8.44 | 9.14 | 9.84 | 10.55 | 11.25 | 11.95 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

### 112. ESC Recovery Rate During High Cylair Downshift - DEG Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (DEG)
- Y-Axis: 17 points (RPM)
- Z-Axis (Data): 17 points (Deg/Sec)

**Statistics:**
- Min: 0.3516 Deg/Sec
- Max: 0.3516 Deg/Sec
- Avg: 0.3516 Deg/Sec
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 0.35 |
| 400.00 | 0.35 |
| 800.00 | 0.35 |
| 1200.00 | 0.35 |
| 1600.00 | 0.35 |
| 2000.00 | 0.35 |
| 2400.00 | 0.35 |
| 2800.00 | 0.35 |
| 3200.00 | 0.35 |
| 3600.00 | 0.35 |
| 4000.00 | 0.35 |
| 4400.00 | 0.35 |
| 4800.00 | 0.35 |
| 5200.00 | 0.35 |
| 5600.00 | 0.35 |
| 6000.00 | 0.35 |
| 6400.00 | 0.35 |

### 113. ESC Recovery Rate Durring High Cylair And RPM - DEG Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (DEG)
- Y-Axis: 17 points (RPM)
- Z-Axis (Data): 17 points (DEG/Sec)

**Statistics:**
- Min: 0.3516 DEG/Sec
- Max: 0.3516 DEG/Sec
- Avg: 0.3516 DEG/Sec
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 0.35 |
| 400.00 | 0.35 |
| 800.00 | 0.35 |
| 1200.00 | 0.35 |
| 1600.00 | 0.35 |
| 2000.00 | 0.35 |
| 2400.00 | 0.35 |
| 2800.00 | 0.35 |
| 3200.00 | 0.35 |
| 3600.00 | 0.35 |
| 4000.00 | 0.35 |
| 4400.00 | 0.35 |
| 4800.00 | 0.35 |
| 5200.00 | 0.35 |
| 5600.00 | 0.35 |
| 6000.00 | 0.35 |
| 6400.00 | 0.35 |

### 114. ESC Normal Recovery Rate DEG Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (DEG)
- Y-Axis: 17 points (RPM)
- Z-Axis (Data): 17 points (Deg/Sec)

**Statistics:**
- Min: 1.4008 Deg/Sec
- Max: 1.4008 Deg/Sec
- Avg: 1.4008 Deg/Sec
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 1.40 |
| 400.00 | 1.40 |
| 800.00 | 1.40 |
| 1200.00 | 1.40 |
| 1600.00 | 1.40 |
| 2000.00 | 1.40 |
| 2400.00 | 1.40 |
| 2800.00 | 1.40 |
| 3200.00 | 1.40 |
| 3600.00 | 1.40 |
| 4000.00 | 1.40 |
| 4400.00 | 1.40 |
| 4800.00 | 1.40 |
| 5200.00 | 1.40 |
| 5600.00 | 1.40 |
| 6000.00 | 1.40 |
| 6400.00 | 1.40 |

### 115. ESC Window Beginning Offset in Degrees Vs RPM & Load

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 14 points (RPM)
- Y-Axis: 8 points (MG/CYL)
- Z-Axis (Data): 112 points (DEG)

**Statistics:**
- Min: 1.9141 DEG
- Max: 38.0469 DEG
- Avg: 13.8839 DEG
- Dimensions: 8 × 14

**Full Data Table** (8 rows × 14 cols):

| Y \ X | 400.00 | 800.00 | 1200.00 | 1600.00 | 2000.00 | 2400.00 | 2800.00 | 3200.00 | 3600.00 | 4000.00 | 4400.00 | 4800.00 | 5200.00 | 5600.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 100.00 | 6.02 | 5.43 | 4.84 | 4.06 | 3.09 | 2.50 | 1.91 | 1.91 | 1.91 | 1.91 | 1.91 | 1.91 | 1.91 | 1.91 |
| 200.00 | 6.02 | 5.43 | 4.84 | 4.06 | 3.09 | 2.50 | 1.91 | 1.91 | 1.91 | 1.91 | 1.91 | 1.91 | 1.91 | 1.91 |
| 300.00 | 11.29 | 9.53 | 7.97 | 7.19 | 6.99 | 6.99 | 6.99 | 6.99 | 6.99 | 6.99 | 6.99 | 6.99 | 6.99 | 6.99 |
| 400.00 | 30.04 | 20.08 | 16.37 | 14.02 | 12.66 | 12.46 | 12.27 | 12.27 | 12.27 | 12.27 | 12.27 | 12.27 | 12.27 | 12.27 |
| 500.00 | 23.59 | 31.02 | 24.57 | 20.47 | 17.93 | 16.95 | 16.37 | 15.98 | 15.78 | 15.78 | 15.78 | 15.78 | 15.78 | 15.78 |
| 600.00 | 30.04 | 38.05 | 30.04 | 25.94 | 22.81 | 20.27 | 18.91 | 17.73 | 16.76 | 15.98 | 15.98 | 15.98 | 15.98 | 15.98 |
| 700.00 | 30.04 | 38.05 | 30.04 | 25.94 | 22.81 | 20.27 | 18.91 | 17.73 | 16.76 | 15.98 | 15.98 | 15.98 | 15.98 | 15.98 |
| 800.00 | 30.04 | 38.05 | 30.04 | 25.94 | 22.81 | 20.27 | 18.91 | 17.73 | 16.76 | 15.98 | 15.98 | 15.98 | 15.98 | 15.98 |

### 116. ESC Window Length In Degrees Vs RPM Window Enable Table

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (RPM)
- Y-Axis: 1 points (M/SEC)
- Z-Axis (Data): 1 points (M/sec)

**Statistics:**
- Min: 2.5541 M/sec
- Max: 9.5778 M/sec
- Avg: 3.6853 M/sec
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 400.00 | 800.00 | 1200.00 | 1600.00 | 2000.00 | 2400.00 | 2800.00 | 3200.00 | 3600.00 | 4000.00 | 4400.00 | 4800.00 | 5200.00 | 5600.00 | 6000.00 | 6400.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 9.58 | 6.99 | 5.48 | 4.51 | 3.72 | 3.31 | 3.00 | 2.82 | 2.70 | 2.63 | 2.59 | 2.55 | 2.55 | 2.55 | 2.55 | 2.55 | 2.55 |

### 117. Engine Load Knock Control Enable Threshold Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (MG/CYL)
- Y-Axis: 17 points (RPM)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 175.0000 
- Max: 250.0000 
- Avg: 189.7059 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0 |
|-----|------|
| 0 | 250 |
| 400 | 250 |
| 800 | 250 |
| 1200 | 200 |
| 1600 | 175 |
| 2000 | 175 |
| 2400 | 175 |
| 2800 | 175 |
| 3200 | 175 |
| 3600 | 175 |
| 4000 | 175 |
| 4400 | 175 |
| 4800 | 175 |
| 5200 | 175 |
| 5600 | 175 |
| 6000 | 175 |
| 6400 | 175 |

### 118. Transient Mode Knock Threshold Multiplier Offset Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 15 points (RPM)
- Y-Axis: 1 points (FACT)
- Z-Axis (Data): 1 points (FACT)

**Statistics:**
- Min: 5.0000 FACT
- Max: 7.0000 FACT
- Avg: 6.1333 FACT
- Dimensions: 1 × 15

**Full Data Table** (1 rows × 15 cols):

| Y \ X | 400.00 | 800.00 | 1200.00 | 1600.00 | 2000.00 | 2400.00 | 2800.00 | 3200.00 | 3600.00 | 4000.00 | 4400.00 | 4800.00 | 5200.00 | 5600.00 | 6000.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 7.00 | 7.00 | 7.00 | 7.00 | 7.00 | 7.00 | 7.00 | 7.00 | 6.00 | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 |

### 119. Load Component Of Knock Multiplier CYL_AIR Vs Factor

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (MG/CYL CYLAIR50)
- Y-Axis: 1 points (FACT)
- Z-Axis (Data): 1 points (FACT)

**Statistics:**
- Min: 1.0000 FACT
- Max: 1.0000 FACT
- Avg: 1.0000 FACT
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | 50.00 | 150.00 | 250.00 | 350.00 | 450.00 | 550.00 | 650.00 | 750.00 | 850.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

### 120. RPM Component Of Knock Multiplier For PE

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 15 points (RPM)
- Y-Axis: 1 points (MULTIPLIER)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 1.1484 MULT
- Max: 1.1484 MULT
- Avg: 1.1484 MULT
- Dimensions: 1 × 15

**Full Data Table** (1 rows × 15 cols):

| Y \ X | 400.00 | 800.00 | 1200.00 | 1600.00 | 2000.00 | 2400.00 | 2800.00 | 3200.00 | 3600.00 | 4000.00 | 4400.00 | 4800.00 | 5200.00 | 5600.00 | 6000.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 1.15 | 1.15 | 1.15 | 1.15 | 1.15 | 1.15 | 1.15 | 1.15 | 1.15 | 1.15 | 1.15 | 1.15 | 1.15 | 1.15 | 1.15 |

### 121. Multiplication Factor To Cylmul 1-6 As A Function Of Engine Coolant

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 5 points (ECT)
- Y-Axis: 1 points
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 1.2031 
- Avg: 0.6016 
- Dimensions: 1 × 5

**Full Data Table** (1 rows × 5 cols):

| Y \ X | 104.00 | 116.00 | 128.00 | 140.00 | 152.00 |
|-----|------|------|------|------|------|
| 0.00 | 1.20 | 1.20 | 0.60 | 0.00 | 0.00 |

### 122. RPM Component Of Knock Multiplier For Cylinders 1 - 6

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 15 points (RPM)
- Y-Axis: 6 points (CYLINDER#)
- Z-Axis (Data): 90 points (MULTIPLIER)

**Statistics:**
- Min: 2.7500 MULTIPLIER
- Max: 8.0000 MULTIPLIER
- Avg: 5.0250 MULTIPLIER
- Dimensions: 6 × 15

**Full Data Table** (6 rows × 15 cols):

| Y \ X | 400.000 | 800.000 | 1200.000 | 1600.000 | 2000.000 | 2400.000 | 2800.000 | 3200.000 | 3600.000 | 4000.000 | 4400.000 | 4800.000 | 5200.000 | 5600.000 | 6000.000 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 2.750 | 4.500 | 5.000 | 5.750 | 4.750 | 4.750 | 5.250 | 4.750 | 4.750 | 4.000 | 3.750 | 3.750 | 3.500 | 5.500 | 6.250 |
| 1 | 4.000 | 3.750 | 4.500 | 5.750 | 5.000 | 5.750 | 5.250 | 5.000 | 5.000 | 4.750 | 4.000 | 4.500 | 4.500 | 7.000 | 7.250 |
| 2 | 3.500 | 5.000 | 5.250 | 6.000 | 5.750 | 6.750 | 6.750 | 5.750 | 6.000 | 6.250 | 6.250 | 5.250 | 6.250 | 7.500 | 7.750 |
| 3 | 2.750 | 3.750 | 4.500 | 5.250 | 5.250 | 4.750 | 5.500 | 5.000 | 4.750 | 4.500 | 5.250 | 5.250 | 5.000 | 7.000 | 7.000 |
| 4 | 3.000 | 4.500 | 3.500 | 4.500 | 4.250 | 5.000 | 4.750 | 4.750 | 3.750 | 4.250 | 4.500 | 5.000 | 6.000 | 8.000 | 5.500 |
| 5 | 3.000 | 2.750 | 4.250 | 4.000 | 4.750 | 4.250 | 4.500 | 4.500 | 4.000 | 4.250 | 4.500 | 4.500 | 6.500 | 7.500 | 7.250 |

### 123. M93 Enable Load Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (RPM)
- Y-Axis: 1 points (MG/CYL)
- Z-Axis (Data): 1 points (MG/CYL)

**Statistics:**
- Min: 362.5000 MG/CYL
- Max: 450.0000 MG/CYL
- Avg: 444.8529 MG/CYL
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 400.00 | 800.00 | 1200.00 | 1600.00 | 2000.00 | 2400.00 | 2800.00 | 3200.00 | 3600.00 | 4000.00 | 4400.00 | 4800.00 | 5200.00 | 5600.00 | 6000.00 | 6400.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 362.50 | 450.00 | 450.00 | 450.00 | 450.00 | 450.00 | 450.00 | 450.00 | 450.00 | 450.00 | 450.00 | 450.00 | 450.00 | 450.00 | 450.00 | 450.00 | 450.00 |

### 124. Desired Idle Speed (DRIVE) Vs Coolant Temp

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (RPM)
- Y-Axis: 17 points (Degrees C)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 650.0000 
- Max: 1000.0000 
- Avg: 774.2647 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| -40.00 | 1000.00 |
| -28.00 | 1000.00 |
| -16.00 | 1000.00 |
| -4.00 | 962.50 |
| 8.00 | 900.00 |
| 20.00 | 837.50 |
| 32.00 | 787.50 |
| 44.00 | 737.50 |
| 56.00 | 700.00 |
| 68.00 | 675.00 |
| 80.00 | 662.50 |
| 92.00 | 650.00 |
| 104.00 | 650.00 |
| 116.00 | 650.00 |
| 128.00 | 650.00 |
| 140.00 | 650.00 |
| 152.00 | 650.00 |

### 125. Desired Idle Speed (PARK) Vs Coolant Temp

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (RPM)
- Y-Axis: 17 points (Degrees C)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 725.0000 
- Max: 1075.0000 
- Avg: 849.2647 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| -40.00 | 1075.00 |
| -28.00 | 1075.00 |
| -16.00 | 1075.00 |
| -4.00 | 1037.50 |
| 8.00 | 975.00 |
| 20.00 | 912.50 |
| 32.00 | 862.50 |
| 44.00 | 812.50 |
| 56.00 | 775.00 |
| 68.00 | 750.00 |
| 80.00 | 737.50 |
| 92.00 | 725.00 |
| 104.00 | 725.00 |
| 116.00 | 725.00 |
| 128.00 | 725.00 |
| 140.00 | 725.00 |
| 152.00 | 725.00 |

### 126. IAC Motor Park Position Vs Load Selector

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (Steps)
- Y-Axis: 11 points (Eng Perf)
- Z-Axis (Data): 11 points

**Statistics:**
- Min: 120.0000 
- Max: 150.0000 
- Avg: 131.3636 
- Dimensions: 11 × 1

**Full Data Table** (11 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 96.00 | 150.00 |
| 112.00 | 150.00 |
| 128.00 | 150.00 |
| 144.00 | 140.00 |
| 160.00 | 130.00 |
| 176.00 | 125.00 |
| 192.00 | 120.00 |
| 208.00 | 120.00 |
| 224.00 | 120.00 |
| 240.00 | 120.00 |
| 256.00 | 120.00 |

### 127. IAC Motor Position During Crank Vs Coolant Temp

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (STEPS)
- Y-Axis: 17 points (DEG/C)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 50.0000 
- Max: 170.0000 
- Avg: 90.0000 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| -40.00 | 170.00 |
| -28.00 | 170.00 |
| -16.00 | 150.00 |
| -4.00 | 130.00 |
| 8.00 | 110.00 |
| 28.00 | 100.00 |
| 32.00 | 90.00 |
| 44.00 | 80.00 |
| 56.00 | 70.00 |
| 68.00 | 60.00 |
| 80.00 | 50.00 |
| 92.00 | 50.00 |
| 104.00 | 50.00 |
| 116.00 | 55.00 |
| 128.00 | 60.00 |
| 140.00 | 65.00 |
| 152.00 | 70.00 |

### 128. Altitude Compensation For Startup IAC Motor Position Vs Load Selector (0-2 Multiplier)

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 11 points (ENG PERF)
- Y-Axis: 1 points (SCALER)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 1.0000 
- Max: 1.2109 
- Avg: 1.0504 
- Dimensions: 1 × 11

**Full Data Table** (1 rows × 11 cols):

| Y \ X | 96.00 | 112.00 | 128.00 | 144.00 | 160.00 | 176.00 | 192.00 | 208.00 | 224.00 | 240.00 | 256.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 1.21 | 1.16 | 1.10 | 1.06 | 1.02 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

### 129. Runtime Disable Of Hot Idle Speed Offset Vs Coolant Temp

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (DEG/C)
- Y-Axis: 1 points (SEC)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | -40.00 | -28.00 | -16.00 | -4.00 | 8.00 | 20.00 | 32.00 | 44.00 | 56.00 | 68.00 | 80.00 | 92.00 | 104.00 | 116.00 | 128.00 | 140.00 | 152.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 130. Hot Idle Speed Offset Value Vs Coolant Temp

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (DEG/C)
- Y-Axis: 1 points (RPM)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | -40.00 | -28.00 | -16.00 | -4.00 | 8.00 | 20.00 | 32.00 | 44.00 | 56.00 | 68.00 | 80.00 | 92.00 | 104.00 | 116.00 | 128.00 | 140.00 | 152.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 131. RPM Offset To Drive And P/N Vs CLT When Low Battery Charging Condition Is Necessary

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 7 points (DEG/C)
- Y-Axis: 1 points (RPM)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 50.0000 
- Avg: 25.0000 
- Dimensions: 1 × 7

**Full Data Table** (1 rows × 7 cols):

| Y \ X | 56.00 | 68.00 | 80.00 | 92.00 | 104.00 | 116.00 | 128.00 |
|-----|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 25.00 | 50.00 | 50.00 | 50.00 | 0.00 |

### 132. Overspeed Deadband Vs MPH

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 16 points (MPH)
- Y-Axis: 1 points (RPM)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 12.5000 
- Max: 325.0000 
- Avg: 154.6875 
- Dimensions: 1 × 16

**Full Data Table** (1 rows × 16 cols):

| Y \ X | 0.00 | 1.00 | 2.00 | 3.00 | 4.00 | 5.00 | 6.00 | 7.00 | 8.00 | 9.00 | 10.00 | 11.00 | 12.00 | 13.00 | 14.00 | 15.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 12.50 | 12.50 | 25.00 | 50.00 | 100.00 | 112.50 | 125.00 | 137.50 | 150.00 | 175.00 | 200.00 | 225.00 | 250.00 | 275.00 | 300.00 | 325.00 |

### 133. Throttle Follower Gain Vs. KPH

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (Gain)
- Y-Axis: 17 points (KPH)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 2.0000 
- Max: 2.0000 
- Avg: 2.0000 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Row | C0 |
|-----|------|
| 0.00 | 2.00 |
| 12.00 | 2.00 |
| 25.00 | 2.00 |
| 38.00 | 2.00 |
| 51.00 | 2.00 |
| 64.00 | 2.00 |
| 77.00 | 2.00 |
| 90.00 | 2.00 |
| 102.00 | 2.00 |
| 115.00 | 2.00 |
| 128.00 | 2.00 |
| 141.00 | 2.00 |
| 154.00 | 2.00 |
| 167.00 | 2.00 |
| 180.00 | 2.00 |
| 193.00 | 2.00 |
| 205.00 | 2.00 |

### 134. Max T/F Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (RPM)
- Y-Axis: 1 points (STEPS)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 3.0000 
- Max: 3.0000 
- Avg: 3.0000 
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | 0.00 | 400.00 | 800.00 | 1200.00 | 1600.00 | 2000.00 | 2400.00 | 2800.00 | 3200.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 |

### 135. IAC Offset Steps For Anticipation For A/C Load Increase

**Category:** Speedometer

**Axes:**
- X-Axis: 17 points (PRESSURE KPA)
- Y-Axis: 1 points (STEPS)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 20.0000 
- Avg: 14.8824 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 256.00 | 512.00 | 768.00 | 1024.00 | 1280.00 | 1536.00 | 1792.00 | 2048.00 | 2304.00 | 2560.00 | 2816.00 | 3072.00 | 3328.00 | 3584.00 | 3840.00 | 4096.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 1.00 | 2.00 | 6.00 | 10.00 | 14.00 | 20.00 | 20.00 | 20.00 | 20.00 | 20.00 | 20.00 | 20.00 | 20.00 | 20.00 | 20.00 | 20.00 |

### 136. IAC Offset For Steady State A/C Load Increase

**Category:** Speedometer

**Axes:**
- X-Axis: 17 points (PRESSURE KPA)
- Y-Axis: 1 points (STEPS)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 2.0000 
- Max: 31.0000 
- Avg: 15.1176 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 256.00 | 512.00 | 768.00 | 1024.00 | 1280.00 | 1536.00 | 1792.00 | 2048.00 | 2304.00 | 2560.00 | 2816.00 | 3072.00 | 3328.00 | 3584.00 | 3840.00 | 4096.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 2.00 | 2.00 | 3.00 | 4.00 | 6.00 | 9.00 | 11.00 | 13.00 | 15.00 | 17.00 | 19.00 | 21.00 | 23.00 | 25.00 | 27.00 | 29.00 | 31.00 |

### 137. A/C Shut Off When ISESDD - ISES > This RPM Vs ISESDD

**Category:** Speedometer

**Axes:**
- X-Axis: 17 points (COMMAND RPM)
- Y-Axis: 1 points (RPM)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 12.5000 
- Max: 200.0000 
- Avg: 169.1176 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 200.00 | 400.00 | 600.00 | 800.00 | 1000.00 | 1200.00 | 1400.00 | 1600.00 | 1800.00 | 2000.00 | 2200.00 | 2400.00 | 2600.00 | 2800.00 | 3000.00 | 3200.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 12.50 | 12.50 | 100.00 | 150.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 |

### 138. IAC Step to Add for P/N to Drive Transition with A/C OFF Vs Coolant

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (Steps)
- Y-Axis: 9 points (DegC)
- Z-Axis (Data): 9 points (Steps)

**Statistics:**
- Min: 6.0000 Steps
- Max: 10.0000 Steps
- Avg: 7.3333 Steps
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| -40.00 | 10.00 |
| -16.00 | 10.00 |
| 8.00 | 10.00 |
| 32.00 | 6.00 |
| 56.00 | 6.00 |
| 80.00 | 6.00 |
| 104.00 | 6.00 |
| 128.00 | 6.00 |
| 152.00 | 6.00 |

### 139. IAC Step to Add for P/N to Drive Transitions with A/C ON Vs Coolant

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (Steps)
- Y-Axis: 9 points (DegC)
- Z-Axis (Data): 9 points (Steps)

**Statistics:**
- Min: 6.0000 Steps
- Max: 10.0000 Steps
- Avg: 7.3333 Steps
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| -40.00 | 10.00 |
| -16.00 | 10.00 |
| 8.00 | 10.00 |
| 32.00 | 6.00 |
| 56.00 | 6.00 |
| 80.00 | 6.00 |
| 104.00 | 6.00 |
| 128.00 | 6.00 |
| 152.00 | 6.00 |

### 140. IAC Steps to Remove for Drive to P/N Transitions with A/C OFF Vs Coolant

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (Steps)
- Y-Axis: 9 points (DegC)
- Z-Axis (Data): 9 points (Steps)

**Statistics:**
- Min: 0.0000 Steps
- Max: 10.0000 Steps
- Avg: 4.0000 Steps
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| -40.00 | 10.00 |
| -16.00 | 10.00 |
| 8.00 | 10.00 |
| 32.00 | 6.00 |
| 56.00 | 0.00 |
| 80.00 | 0.00 |
| 104.00 | 0.00 |
| 128.00 | 0.00 |
| 152.00 | 0.00 |

### 141. IAC Steps to Remove for Drive to P/N Transitions with A/C ON Vs Coolant

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (Steps)
- Y-Axis: 9 points (DegC)
- Z-Axis (Data): 9 points (Steps)

**Statistics:**
- Min: 0.0000 Steps
- Max: 10.0000 Steps
- Avg: 4.0000 Steps
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| -40.00 | 10.00 |
| -16.00 | 10.00 |
| 8.00 | 10.00 |
| 32.00 | 6.00 |
| 56.00 | 0.00 |
| 80.00 | 0.00 |
| 104.00 | 0.00 |
| 128.00 | 0.00 |
| 152.00 | 0.00 |

### 142. Number Of IAC Steps To Be Added For Power Steering Cramp Vs Load Selector

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 11 points (ENG PERF)
- Y-Axis: 1 points (STEPS)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 7.0000 
- Max: 10.0000 
- Avg: 7.5455 
- Dimensions: 1 × 11

**Full Data Table** (1 rows × 11 cols):

| Y \ X | 96.00 | 112.00 | 128.00 | 144.00 | 160.00 | 176.00 | 192.00 | 208.00 | 224.00 | 240.00 | 256.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 10.00 | 9.00 | 8.00 | 7.00 | 7.00 | 7.00 | 7.00 | 7.00 | 7.00 | 7.00 | 7.00 |

### 143. Number Of IAC Steps To Be Added When Power Steering Pressure Switch Load Is Increasing Vs Altitude

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 11 points (ENG PERF50)
- Y-Axis: 1 points (STEPS)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 1 × 11

**Full Data Table** (1 rows × 11 cols):

| Y \ X | 96.00 | 112.00 | 128.00 | 144.00 | 160.00 | 176.00 | 192.00 | 208.00 | 224.00 | 240.00 | 256.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 144. RPM Below Which Learn Air Increase Is Enabled And RPM Control Is Forced

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (COMMAND RPM)
- Y-Axis: 1 points (RPM)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 250.0000 
- Avg: 130.8824 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 400.00 | 500.00 | 600.00 | 700.00 | 800.00 | 900.00 | 1000.00 | 1100.00 | 1200.00 | 1300.00 | 1400.00 | 1500.00 | 1600.00 | 1700.00 | 1800.00 | 1900.00 | 2000.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 12.50 | 25.00 | 50.00 | 75.00 | 87.50 | 100.00 | 125.00 | 150.00 | 175.00 | 200.00 | 225.00 | 250.00 | 250.00 | 250.00 | 250.00 |

### 145. Airflow Vs RPM in Gear 1-4

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 4 points (GEAR)
- Y-Axis: 17 points (RPM)
- Z-Axis (Data): 68 points (G/S)

**Statistics:**
- Min: 24.0000 G/S
- Max: 115.0000 G/S
- Avg: 69.8824 G/S
- Dimensions: 17 × 4

**Full Data Table** (17 rows × 4 cols):

| Y \ X | 1.00 | 2.00 | 3.00 | 4.00 |
|-----|------|------|------|------|
| 400.00 | 47.00 | 37.00 | 26.00 | 26.00 |
| 500.00 | 26.00 | 35.00 | 46.00 | 58.00 |
| 600.00 | 69.00 | 82.00 | 94.00 | 115.00 |
| 700.00 | 115.00 | 115.00 | 115.00 | 115.00 |
| 800.00 | 115.00 | 47.00 | 40.00 | 37.00 |
| 900.00 | 37.00 | 38.00 | 41.00 | 46.00 |
| 1000.00 | 55.00 | 66.00 | 79.00 | 91.00 |
| 1100.00 | 112.00 | 112.00 | 112.00 | 112.00 |
| 1200.00 | 112.00 | 112.00 | 47.00 | 37.00 |
| 1300.00 | 24.00 | 24.00 | 24.00 | 31.00 |
| 1400.00 | 39.00 | 51.00 | 62.00 | 75.00 |
| 1500.00 | 87.00 | 108.00 | 108.00 | 108.00 |
| 1600.00 | 108.00 | 108.00 | 108.00 | 47.00 |
| 1700.00 | 37.00 | 24.00 | 24.00 | 24.00 |
| 1800.00 | 31.00 | 38.00 | 48.00 | 59.00 |
| 1900.00 | 72.00 | 84.00 | 105.00 | 105.00 |
| 2000.00 | 105.00 | 105.00 | 105.00 | 105.00 |

### 146. Airflow Vs RPM in 5th Gear (This Table Is For Manual Transmission Only)

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (G/S)
- Y-Axis: 17 points (RPM)
- Z-Axis (Data): 17 points (G/S)

**Statistics:**
- Min: 24.0000 G/S
- Max: 105.0000 G/S
- Avg: 65.7647 G/S
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 400.00 | 47.00 |
| 500.00 | 37.00 |
| 600.00 | 24.00 |
| 700.00 | 24.00 |
| 800.00 | 24.00 |
| 900.00 | 31.00 |
| 1000.00 | 38.00 |
| 1100.00 | 48.00 |
| 1200.00 | 59.00 |
| 1300.00 | 72.00 |
| 1400.00 | 84.00 |
| 1500.00 | 105.00 |
| 1600.00 | 105.00 |
| 1700.00 | 105.00 |
| 1800.00 | 105.00 |
| 1900.00 | 105.00 |
| 2000.00 | 105.00 |

### 147. Airflow Vs RPM in P/N

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (G/S)
- Y-Axis: 17 points (RPM)
- Z-Axis (Data): 17 points (G/S)

**Statistics:**
- Min: 25.0000 G/S
- Max: 47.0000 G/S
- Avg: 27.0000 G/S
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 400.00 | 47.00 |
| 500.00 | 37.00 |
| 600.00 | 25.00 |
| 700.00 | 25.00 |
| 800.00 | 25.00 |
| 900.00 | 25.00 |
| 1000.00 | 25.00 |
| 1100.00 | 25.00 |
| 1200.00 | 25.00 |
| 1300.00 | 25.00 |
| 1400.00 | 25.00 |
| 1500.00 | 25.00 |
| 1600.00 | 25.00 |
| 1700.00 | 25.00 |
| 1800.00 | 25.00 |
| 1900.00 | 25.00 |
| 2000.00 | 25.00 |

### 148. Airflow Vs Coolant Temp & Time

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 5 points (TIME MINUTES)
- Y-Axis: 17 points (DEG/C)
- Z-Axis (Data): 85 points (G/S)

**Statistics:**
- Min: 0.0000 G/S
- Max: 14.5000 G/S
- Avg: 3.3847 G/S
- Dimensions: 17 × 5

**Full Data Table** (17 rows × 5 cols):

| Y \ X | 0.00 | 16.00 | 32.00 | 48.00 | 64.00 |
|-----|------|------|------|------|------|
| -40.00 | 14.50 | 12.50 | 10.10 | 9.40 | 9.40 |
| -28.00 | 12.80 | 11.10 | 9.40 | 8.80 | 8.80 |
| -16.00 | 11.10 | 9.60 | 8.70 | 8.30 | 8.10 |
| -4.00 | 8.90 | 7.70 | 7.50 | 7.30 | 7.00 |
| 8.00 | 6.40 | 5.90 | 5.40 | 5.40 | 5.20 |
| 20.00 | 4.50 | 4.00 | 3.80 | 3.80 | 3.70 |
| 32.00 | 3.40 | 3.00 | 2.80 | 2.80 | 2.60 |
| 44.00 | 2.20 | 1.90 | 1.90 | 1.80 | 1.80 |
| 56.00 | 1.60 | 1.40 | 1.30 | 1.20 | 1.10 |
| 68.00 | 1.40 | 1.10 | 1.10 | 1.00 | 0.80 |
| 80.00 | 1.10 | 0.80 | 0.50 | 0.50 | 0.50 |
| 92.00 | 0.60 | 0.40 | 0.30 | 0.20 | 0.00 |
| 104.00 | 0.60 | 0.40 | 0.30 | 0.20 | 0.00 |
| 116.00 | 0.60 | 0.40 | 0.30 | 0.20 | 0.00 |
| 128.00 | 0.60 | 0.40 | 0.30 | 0.20 | 0.00 |
| 140.00 | 0.60 | 0.40 | 0.30 | 0.20 | 0.00 |
| 152.00 | 0.60 | 0.40 | 0.30 | 0.20 | 0.00 |

### 149. Commanded Air Offset For P/N When Run Time Spark Is Active

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 8 points (DEG/C)
- Y-Axis: 1 points (GM/SEC)
- Z-Axis (Data): 1 points (G/S)

**Statistics:**
- Min: 27.0000 G/S
- Max: 27.0000 G/S
- Avg: 27.0000 G/S
- Dimensions: 1 × 8

**Full Data Table** (1 rows × 8 cols):

| Y \ X | 8.00 | 20.00 | 32.00 | 44.00 | 56.00 | 68.00 | 80.00 | 92.00 |
|-----|------|------|------|------|------|------|------|------|
| 0.00 | 27.00 | 27.00 | 27.00 | 27.00 | 27.00 | 27.00 | 27.00 | 27.00 |

### 150. Offset to Commanded Air When Using Retarded Idle Spark

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 11 points (DEG/C)
- Y-Axis: 1 points
- Z-Axis (Data): 1 points (DEG)

**Statistics:**
- Min: 0.0000 DEG
- Max: 0.0000 DEG
- Avg: 0.0000 DEG
- Dimensions: 1 × 11

**Full Data Table** (1 rows × 11 cols):

| Y \ X | 8.00 | 20.00 | 32.00 | 44.00 | 56.00 | 68.00 | 80.00 | 92.00 | 104.00 | 116.00 | 128.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 151. Airflow Offset For Low Battery Idle Up Vs Coolant

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 6 points (DEG/C)
- Y-Axis: 1 points (G/S)
- Z-Axis (Data): 1 points (G/S)

**Statistics:**
- Min: 0.0000 G/S
- Max: 0.4000 G/S
- Avg: 0.2333 G/S
- Dimensions: 1 × 6

**Full Data Table** (1 rows × 6 cols):

| Y \ X | 56.00 | 68.00 | 80.00 | 92.00 | 104.00 | 128.00 |
|-----|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.20 | 0.40 | 0.40 | 0.40 |

### 152. Power Enrichment Enable TPS Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (TPS %)
- Y-Axis: 17 points (RPM)
- Z-Axis (Data): 17 points (MGC)

**Statistics:**
- Min: 60.1562 MGC
- Max: 64.8438 MGC
- Avg: 63.1893 MGC
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.0 |
|-----|------|
| 400.0 | 64.8 |
| 600.0 | 64.8 |
| 800.0 | 64.8 |
| 1000.0 | 64.8 |
| 1200.0 | 64.8 |
| 1400.0 | 64.8 |
| 1600.0 | 64.8 |
| 1800.0 | 64.8 |
| 2000.0 | 64.8 |
| 2200.0 | 64.8 |
| 2400.0 | 64.8 |
| 2800.0 | 60.2 |
| 3200.0 | 60.2 |
| 3600.0 | 60.2 |
| 4000.0 | 60.2 |
| 4400.0 | 60.2 |
| 4800.0 | 60.2 |

### 153. Power Enrichment Enable MGC Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (MGC)
- Y-Axis: 17 points (RPM)
- Z-Axis (Data): 17 points (MGC)

**Statistics:**
- Min: 539.0625 MGC
- Max: 992.1875 MGC
- Avg: 778.9522 MGC
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0 |
|-----|------|
| 400 | 992 |
| 600 | 992 |
| 800 | 992 |
| 1000 | 992 |
| 1200 | 992 |
| 1400 | 992 |
| 1600 | 992 |
| 1800 | 992 |
| 2000 | 992 |
| 2200 | 539 |
| 2400 | 539 |
| 2800 | 539 |
| 3200 | 539 |
| 3600 | 539 |
| 4000 | 539 |
| 4400 | 539 |
| 4800 | 539 |

### 154. PE Commanded AFR Vs Coolant Temperature

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (AFR)
- Y-Axis: 9 points (DEG C)
- Z-Axis (Data): 9 points (AFR)

**Statistics:**
- Min: 12.8000 AFR
- Max: 12.8000 AFR
- Avg: 12.8000 AFR
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| -40.00 | 12.80 |
| -16.00 | 12.80 |
| 8.00 | 12.80 |
| 32.00 | 12.80 |
| 56.00 | 12.80 |
| 80.00 | 12.80 |
| 104.00 | 12.80 |
| 128.00 | 12.80 |
| 152.00 | 12.80 |

### 155. PE Commanded AFR Multiplier Vs Time

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (MULTIPLIER)
- Y-Axis: 17 points (SEC)
- Z-Axis (Data): 17 points (AFR)

**Statistics:**
- Min: 0.9997 AFR
- Max: 1.0622 AFR
- Avg: 1.0125 AFR
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.000 |
|-----|------|
| 0.000 | 1.000 |
| 1.600 | 1.000 |
| 3.200 | 1.000 |
| 4.800 | 1.000 |
| 6.400 | 1.000 |
| 8.000 | 1.000 |
| 9.600 | 1.000 |
| 11.200 | 1.000 |
| 12.800 | 1.000 |
| 14.400 | 1.000 |
| 16.000 | 1.000 |
| 17.600 | 1.000 |
| 19.200 | 1.000 |
| 20.800 | 1.031 |
| 22.400 | 1.062 |
| 24.000 | 1.062 |
| 25.600 | 1.062 |

### 156. PE Commanded AFR Multiplier Vs RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (MULTIPLIER)
- Y-Axis: 8 points (RPM)
- Z-Axis (Data): 8 points (AFR)

**Statistics:**
- Min: 0.9997 AFR
- Max: 1.0309 AFR
- Avg: 1.0036 AFR
- Dimensions: 8 × 1

**Full Data Table** (8 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 800.00 | 1.03 |
| 1600.00 | 1.00 |
| 2400.00 | 1.00 |
| 3200.00 | 1.00 |
| 4000.00 | 1.00 |
| 4800.00 | 1.00 |
| 5600.00 | 1.00 |
| 6400.00 | 1.00 |

### 157. Power Enrichment Trim Vs TPS (NTPSLD)

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (%CHG)
- Y-Axis: 9 points (%TPS)
- Z-Axis (Data): 9 points (CHG%)

**Statistics:**
- Min: 0.0000 CHG%
- Max: 0.0000 CHG%
- Avg: 0.0000 CHG%
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 0.00 |
| 12.50 | 0.00 |
| 25.00 | 0.00 |
| 37.50 | 0.00 |
| 50.00 | 0.00 |
| 62.50 | 0.00 |
| 75.00 | 0.00 |
| 87.50 | 0.00 |
| 100.00 | 0.00 |

### 158. Open Loop AFR Vs Cylair50 & RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 14 points (MG/CYL)
- Y-Axis: 17 points (RPM)
- Z-Axis (Data): 238 points (AFRTIO)

**Statistics:**
- Min: 12.8000 AFRTIO
- Max: 15.1704 AFRTIO
- Avg: 14.5359 AFRTIO
- Dimensions: 17 × 14

**Full Data Table** (17 rows × 14 cols):

| Y \ X | 50.00 | 100.00 | 150.00 | 200.00 | 250.00 | 300.00 | 350.00 | 400.00 | 450.00 | 500.00 | 550.00 | 600.00 | 650.00 | 700.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 400.00 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 |
| 600.00 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 |
| 800.00 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 |
| 1000.00 | 15.17 | 15.17 | 15.03 | 14.89 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 |
| 1200.00 | 15.17 | 15.17 | 15.03 | 14.89 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 |
| 1400.00 | 15.17 | 15.17 | 15.03 | 14.89 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 |
| 1600.00 | 15.17 | 15.17 | 15.03 | 14.89 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 |
| 1800.00 | 15.17 | 15.17 | 15.03 | 14.89 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 |
| 2000.00 | 15.17 | 15.17 | 15.03 | 14.89 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 12.80 | 12.80 | 12.80 | 12.80 |
| 2200.00 | 15.17 | 15.17 | 15.03 | 14.89 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 12.80 | 12.80 | 12.80 | 12.80 |
| 2400.00 | 15.17 | 15.17 | 15.03 | 14.89 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 12.80 | 12.80 | 12.80 | 12.80 |
| 2800.00 | 15.17 | 15.17 | 15.03 | 14.89 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 12.80 | 12.80 | 12.80 | 12.80 |
| 3200.00 | 15.17 | 15.17 | 15.03 | 14.89 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 12.80 | 12.80 | 12.80 | 12.80 |
| 3600.00 | 15.17 | 15.17 | 15.03 | 14.89 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 12.80 | 12.80 | 12.80 | 12.80 |
| 4000.00 | 15.17 | 15.17 | 15.03 | 14.89 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 12.80 | 12.80 | 12.80 | 12.80 |
| 4400.00 | 15.17 | 15.17 | 15.03 | 14.89 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 12.80 | 12.80 | 12.80 | 12.80 |
| 4800.00 | 15.17 | 15.17 | 15.03 | 14.89 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 14.76 | 12.80 | 12.80 | 12.80 | 12.80 |

### 159. Open Loop, Coolant Offset AFR Vs RPM & Cylair

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 14 points (RPM)
- Y-Axis: 7 points (RPM)
- Z-Axis (Data): 98 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0171 
- Avg: 0.0078 
- Dimensions: 7 × 14

**Full Data Table** (7 rows × 14 cols):

| Y \ X | 50.00 | 100.00 | 150.00 | 200.00 | 250.00 | 300.00 | 350.00 | 400.00 | 450.00 | 500.00 | 550.00 | 600.00 | 650.00 | 700.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 400.00 | 0.00 | 0.00 | 0.00 | 0.01 | 0.01 | 0.01 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 |
| 600.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | 0.01 | 0.01 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 |
| 800.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | 0.01 | 0.01 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 |
| 1000.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | 0.01 | 0.01 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 |
| 1200.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 |
| 1400.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 |
| 1600.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 |

### 160. 0-1 Multiplier Of F60CLDFA Vs Coolant

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (MULT)
- Y-Axis: 6 points (DEG/C)
- Z-Axis (Data): 6 points (Multi)

**Statistics:**
- Min: 0.0000 Multi
- Max: 0.6641 Multi
- Avg: 0.4434 Multi
- Dimensions: 6 × 1

**Full Data Table** (6 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| -40.00 | 0.66 |
| -16.00 | 0.66 |
| 8.00 | 0.60 |
| 32.00 | 0.46 |
| 56.00 | 0.27 |
| 80.00 | 0.00 |

### 161. Open Loop AFR Vs Coolant Temperature

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (AFR)
- Y-Axis: 17 points (DEG/C)
- Z-Axis (Data): 17 points (AFRTIO)

**Statistics:**
- Min: 14.2470 AFRTIO
- Max: 14.7604 AFRTIO
- Avg: 14.4584 AFRTIO
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| -40.00 | 14.76 |
| -28.00 | 14.76 |
| -16.00 | 14.76 |
| -4.00 | 14.76 |
| 8.00 | 14.76 |
| 20.00 | 14.76 |
| 32.00 | 14.76 |
| 44.00 | 14.25 |
| 56.00 | 14.25 |
| 68.00 | 14.25 |
| 80.00 | 14.25 |
| 92.00 | 14.25 |
| 104.00 | 14.25 |
| 116.00 | 14.25 |
| 128.00 | 14.25 |
| 140.00 | 14.25 |
| 152.00 | 14.25 |

### 162. Air/Fuel Time Out Vs Startup Coolant Temperature For Idle

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 33 points (DEG/C)
- Y-Axis: 1 points (%CHG)
- Z-Axis (Data): 1 points (%CHG)

**Statistics:**
- Min: 7.0312 %CHG
- Max: 136.7188 %CHG
- Avg: 44.5786 %CHG
- Dimensions: 1 × 33

**Full Data Table** (1 rows × 33 cols):

| Y \ X | -40.00 | -34.00 | -28.00 | -22.00 | -16.00 | -10.00 | -4.00 | 2.00 | 8.00 | 14.00 | 20.00 | 26.00 | 32.00 | 38.00 | 44.00 | 50.00 | 56.00 | 62.00 | 68.00 | 74.00 | 80.00 | 86.00 | 92.00 | 98.00 | 104.00 | 110.00 | 116.00 | 122.00 | 128.00 | 134.00 | 140.00 | 146.00 | 152.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 136.72 | 132.03 | 126.56 | 120.31 | 114.06 | 105.47 | 95.31 | 81.25 | 63.28 | 49.22 | 39.84 | 34.38 | 30.47 | 28.12 | 25.78 | 23.44 | 21.09 | 18.75 | 16.41 | 14.06 | 11.72 | 9.38 | 7.03 | 7.03 | 9.38 | 18.75 | 18.75 | 18.75 | 18.75 | 18.75 | 18.75 | 18.75 | 18.75 |

### 163. Air/Fuel Time Out Vs Startup Coolant Temp For WOT

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 33 points (DEG/C)
- Y-Axis: 1 points (%CHG)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 7.0312 
- Max: 199.2188 
- Avg: 63.6600 
- Dimensions: 1 × 33

**Full Data Table** (1 rows × 33 cols):

| Y \ X | -40.00 | -34.00 | -28.00 | -22.00 | -16.00 | -10.00 | -4.00 | 2.00 | 8.00 | 14.00 | 20.00 | 26.00 | 32.00 | 38.00 | 44.00 | 50.00 | 56.00 | 62.00 | 68.00 | 74.00 | 80.00 | 86.00 | 92.00 | 98.00 | 104.00 | 110.00 | 116.00 | 122.00 | 128.00 | 134.00 | 140.00 | 146.00 | 152.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 199.22 | 190.62 | 181.25 | 171.88 | 161.72 | 150.78 | 137.50 | 117.97 | 96.88 | 79.69 | 67.19 | 59.38 | 53.12 | 47.66 | 42.97 | 38.28 | 33.59 | 28.91 | 24.22 | 20.31 | 14.84 | 9.38 | 7.03 | 7.03 | 9.38 | 18.75 | 18.75 | 18.75 | 18.75 | 18.75 | 18.75 | 18.75 | 18.75 |

### 164. Ratio Of FATIIDLE To FATIWOT For Calculation Of FATI Vs Load

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 8 points (CYLAIR)
- Y-Axis: 1 points (%CHG)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 99.6094 
- Avg: 58.1543 
- Dimensions: 1 × 8

**Full Data Table** (1 rows × 8 cols):

| Y \ X | 0.00 | 125.00 | 250.00 | 375.00 | 500.00 | 625.00 | 750.00 | 875.00 |
|-----|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 16.80 | 50.00 | 99.61 | 99.61 | 99.61 | 99.61 |

### 165. Air/Fuel Time Out Vs Startup Coolant Temperature For Idle

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 33 points (DEG/C)
- Y-Axis: 1 points (%CHG)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 128.0000 
- Max: 150.0000 
- Avg: 134.7879 
- Dimensions: 1 × 33

**Full Data Table** (1 rows × 33 cols):

| Y \ X | -40.00 | -34.00 | -28.00 | -22.00 | -16.00 | -10.00 | -4.00 | 2.00 | 8.00 | 14.00 | 20.00 | 26.00 | 32.00 | 38.00 | 44.00 | 50.00 | 56.00 | 62.00 | 68.00 | 74.00 | 80.00 | 86.00 | 92.00 | 98.00 | 104.00 | 110.00 | 116.00 | 122.00 | 128.00 | 134.00 | 140.00 | 146.00 | 152.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 150.00 | 148.00 | 146.00 | 144.00 | 142.00 | 140.00 | 138.00 | 136.00 | 134.00 | 132.00 | 130.00 | 128.00 | 128.00 | 128.00 | 128.00 | 128.00 | 128.00 | 128.00 | 128.00 | 128.00 | 128.00 | 128.00 | 128.00 | 128.00 | 130.00 | 134.00 | 140.00 | 140.00 | 140.00 | 140.00 | 140.00 | 140.00 | 140.00 |

### 166. Cold Engine Dependent Air/Fuel Ratio Vs Coolant For WOT

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 33 points (DEG/C)
- Y-Axis: 1 points (%CHG)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 128.0000 
- Max: 158.0000 
- Avg: 138.0606 
- Dimensions: 1 × 33

**Full Data Table** (1 rows × 33 cols):

| Y \ X | -40.00 | -34.00 | -28.00 | -22.00 | -16.00 | -10.00 | -4.00 | 2.00 | 8.00 | 14.00 | 20.00 | 26.00 | 32.00 | 38.00 | 44.00 | 50.00 | 56.00 | 62.00 | 68.00 | 74.00 | 80.00 | 86.00 | 92.00 | 98.00 | 104.00 | 110.00 | 116.00 | 122.00 | 128.00 | 134.00 | 140.00 | 146.00 | 152.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 158.00 | 156.00 | 154.00 | 152.00 | 150.00 | 148.00 | 146.00 | 144.00 | 142.00 | 140.00 | 138.00 | 136.00 | 134.00 | 132.00 | 130.00 | 128.00 | 128.00 | 128.00 | 128.00 | 128.00 | 128.00 | 128.00 | 128.00 | 128.00 | 130.00 | 134.00 | 140.00 | 140.00 | 140.00 | 140.00 | 140.00 | 140.00 | 140.00 |

### 167. Ratio Of FATCIDLE To FATCWOT For Calculation Of FATC Vs Load

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 8 points (CYLAIR)
- Y-Axis: 1 points (%CHG)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 99.6094 
- Avg: 53.9551 
- Dimensions: 1 × 8

**Full Data Table** (1 rows × 8 cols):

| Y \ X | 0.00 | 125.00 | 250.00 | 375.00 | 500.00 | 625.00 | 750.00 | 875.00 |
|-----|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 33.20 | 99.61 | 99.61 | 99.61 | 99.61 |

### 168. Fuel Air Time Out Reduction Freq. (Sec) Vs NTRPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 11 points (RPM)
- Y-Axis: 1 points (SEC)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 43.0000 
- Max: 171.0000 
- Avg: 90.1818 
- Dimensions: 1 × 11

**Full Data Table** (1 rows × 11 cols):

| Y \ X | 400.00 | 600.00 | 800.00 | 1000.00 | 1200.00 | 1400.00 | 1600.00 | 1800.00 | 2000.00 | 2200.00 | 2400.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 171.00 | 171.00 | 128.00 | 102.00 | 85.00 | 73.00 | 64.00 | 57.00 | 51.00 | 47.00 | 43.00 |

### 169. Fuel Air Time Out Reduction Frequency Multiplier (0-4) Vs Coolant Temperature

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (DEG/C)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 1.0000 
- Max: 3.0000 
- Avg: 1.5694 
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | -40.00 | -16.00 | 8.00 | 32.00 | 56.00 | 80.00 | 104.00 | 128.00 | 152.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 3.00 | 2.50 | 2.00 | 1.50 | 1.12 | 1.00 | 1.00 | 1.00 | 1.00 |

### 170. Time Out A/F Decay Multiplier Vs Startup Coolant Temperature For Idle

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (DEG/C)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 228.0000 
- Max: 240.0000 
- Avg: 231.8235 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | -40.00 | -28.00 | -16.00 | -4.00 | 8.00 | 20.00 | 32.00 | 44.00 | 56.00 | 68.00 | 80.00 | 92.00 | 104.00 | 116.00 | 128.00 | 140.00 | 152.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 228.00 | 228.00 | 228.00 | 228.00 | 228.00 | 228.00 | 228.00 | 228.00 | 228.00 | 229.00 | 230.00 | 234.00 | 237.00 | 239.00 | 240.00 | 240.00 | 240.00 |

### 171. Time Out A/F Decay Multiplier Vs Startup Coolant Temperature For WOT

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (DEG/C)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.8984 
- Max: 0.9375 
- Avg: 0.9226 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | -40.00 | -28.00 | -16.00 | -4.00 | 8.00 | 20.00 | 32.00 | 44.00 | 56.00 | 68.00 | 80.00 | 92.00 | 104.00 | 116.00 | 128.00 | 140.00 | 152.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.94 | 0.93 | 0.93 | 0.93 | 0.92 | 0.92 | 0.91 | 0.91 | 0.91 | 0.90 | 0.90 | 0.91 | 0.93 | 0.93 | 0.94 | 0.94 | 0.94 |

### 172. Time Out Fuel Decay Delay Vs Coolant Temperature

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 14 points (DEG/C)
- Y-Axis: 1 points (SEC)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 2.0000 
- Max: 10.0000 
- Avg: 4.0000 
- Dimensions: 1 × 14

**Full Data Table** (1 rows × 14 cols):

| Y \ X | -40.00 | -28.00 | -16.00 | -4.00 | 8.00 | 20.00 | 32.00 | 44.00 | 56.00 | 68.00 | 80.00 | 92.00 | 104.00 | 116.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 10.00 | 10.00 | 10.00 | 5.00 | 3.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 |

### 173. Enleanment Multiplier Of FATI For Shortrun Afterstart Fuelling Vs Coolant

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 8 points (DEG/C)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 50.0000 
- Avg: 25.0000 
- Dimensions: 1 × 8

**Full Data Table** (1 rows × 8 cols):

| Y \ X | -40.00 | -16.00 | 8.00 | 32.00 | 56.00 | 80.00 | 104.00 | 128.00 |
|-----|------|------|------|------|------|------|------|------|
| 0.00 | 50.00 | 50.00 | 44.92 | 35.16 | 19.92 | 0.00 | 0.00 | 0.00 |

### 174. Shortrun Enleanment Multiplier For Reduction Of FATI Vs Engine Off Time

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 16 points (MINUTES)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 0.6641 
- Avg: 0.1440 
- Dimensions: 1 × 16

**Full Data Table** (1 rows × 16 cols):

| Y \ X | 0.00 | 1.00 | 2.00 | 3.00 | 4.00 | 5.00 | 6.00 | 7.00 | 8.00 | 9.00 | 10.00 | 11.00 | 12.00 | 13.00 | 14.00 | 15.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.66 | 0.53 | 0.40 | 0.29 | 0.20 | 0.12 | 0.07 | 0.03 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 175. Delta TPS Multiplier of Last BPW

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (%DELTA TPS)
- Y-Axis: 1 points (%CHG)
- Z-Axis (Data): 1 points (%/CHANGE)

**Statistics:**
- Min: 19.9219 %/CHANGE
- Max: 99.6094 %/CHANGE
- Avg: 78.9931 %/CHANGE
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | 0.00 | 12.50 | 25.00 | 37.50 | 50.00 | 62.50 | 75.00 | 87.50 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 19.92 | 33.20 | 60.16 | 99.61 | 99.61 | 99.61 | 99.61 | 99.61 | 99.61 |

### 176. SYNC Delta TPS Multiplier Vs Coolant Temperature

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (DMULT)
- Y-Axis: 17 points (DEG C)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 0.0000 
- Max: 1.9531 
- Avg: 0.4545 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.000 |
|-----|------|
| -40.000 | 1.953 |
| -28.000 | 1.562 |
| -16.000 | 1.188 |
| -4.000 | 0.875 |
| 8.000 | 0.641 |
| 20.000 | 0.477 |
| 32.000 | 0.359 |
| 44.000 | 0.266 |
| 56.000 | 0.195 |
| 68.000 | 0.133 |
| 80.000 | 0.078 |
| 92.000 | 0.000 |
| 104.000 | 0.000 |
| 116.000 | 0.000 |
| 128.000 | 0.000 |
| 140.000 | 0.000 |
| 152.000 | 0.000 |

### 177. DTPSAE Multiplier Vs Reference Pulses

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (MULT)
- Y-Axis: 33 points (REF PULSES)
- Z-Axis (Data): 33 points

**Statistics:**
- Min: 0.0000 
- Max: 0.9961 
- Avg: 0.3142 
- Dimensions: 33 × 1

**Full Data Table** (33 rows × 1 cols):

| Y \ X | 0.000 |
|-----|------|
| 0.000 | 0.996 |
| 2.000 | 0.996 |
| 4.000 | 0.945 |
| 6.000 | 0.852 |
| 8.000 | 0.723 |
| 10.000 | 0.617 |
| 12.000 | 0.535 |
| 14.000 | 0.477 |
| 16.000 | 0.430 |
| 18.000 | 0.391 |
| 20.000 | 0.355 |
| 22.000 | 0.324 |
| 24.000 | 0.297 |
| 26.000 | 0.273 |
| 28.000 | 0.250 |
| 30.000 | 0.230 |
| 32.000 | 0.211 |
| 34.000 | 0.195 |
| 36.000 | 0.180 |
| 38.000 | 0.164 |
| 40.000 | 0.148 |
| 42.000 | 0.133 |
| 44.000 | 0.117 |
| 46.000 | 0.105 |
| 48.000 | 0.094 |
| 50.000 | 0.082 |
| 52.000 | 0.070 |
| 54.000 | 0.059 |
| 56.000 | 0.047 |
| 58.000 | 0.035 |
| 60.000 | 0.023 |
| 62.000 | 0.012 |
| 64.000 | 0.000 |

### 178. TPS AE Altitude Correction Multiplier 0-2 Vs Engine Performance

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 11 points (ENGPERF)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULTIPLIER)

**Statistics:**
- Min: 0.6250 MULTIPLIER
- Max: 1.0000 MULTIPLIER
- Avg: 0.9212 MULTIPLIER
- Dimensions: 1 × 11

**Full Data Table** (1 rows × 11 cols):

| Y \ X | 96.00 | 112.00 | 128.00 | 144.00 | 160.00 | 176.00 | 192.00 | 208.00 | 224.00 | 240.00 | 256.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.62 | 0.74 | 0.84 | 0.92 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

### 179. Multiplier Of TPSAE Factor As A Function Of Throttle Position 0-1 Factor

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (TPS)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.9961 
- Max: 0.9961 
- Avg: 0.9961 
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | 0.00 | 12.50 | 25.00 | 37.50 | 50.00 | 62.50 | 75.00 | 87.50 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

### 180. SYNCH Delta TPS DE Multiplier Vs Coolant Temp

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (MULTI)
- Y-Axis: 17 points (DEG/C)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 0.0000 
- Max: 1.5625 
- Avg: 0.6351 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.000 |
|-----|------|
| -40.000 | 1.562 |
| -28.000 | 1.562 |
| -16.000 | 1.562 |
| -4.000 | 1.562 |
| 8.000 | 1.562 |
| 20.000 | 1.094 |
| 32.000 | 0.766 |
| 44.000 | 0.523 |
| 56.000 | 0.336 |
| 68.000 | 0.188 |
| 80.000 | 0.078 |
| 92.000 | 0.000 |
| 104.000 | 0.000 |
| 116.000 | 0.000 |
| 128.000 | 0.000 |
| 140.000 | 0.000 |
| 152.000 | 0.000 |

### 181. Multiplier Of DE Factor As A Function Of Throttle Position 0-1 Factor

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (% TPS)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 99.6094 
- Avg: 25.5208 
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | 0.00 | 12.50 | 25.00 | 37.50 | 50.00 | 62.50 | 75.00 | 87.50 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 99.61 | 78.91 | 34.77 | 10.55 | 3.12 | 1.56 | 0.78 | 0.39 | 0.00 |

### 182. Delta TPS DE Multiplier Of Last BPW

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (%DELTA TPS)
- Y-Axis: 1 points (%CHG)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 99.6094 
- Avg: 77.8646 
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | 0.00 | 12.50 | 25.00 | 37.50 | 50.00 | 62.50 | 75.00 | 87.50 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 36.33 | 72.66 | 93.75 | 99.61 | 99.61 | 99.61 | 99.61 | 99.61 |

### 183. DTPSDE Multiplier Vs Reference Pulses

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (MULTI)
- Y-Axis: 17 points (REF PULSES)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 0.0000 
- Max: 0.4023 
- Avg: 0.1503 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.000 |
|-----|------|
| 0.000 | 0.199 |
| 16.000 | 0.301 |
| 32.000 | 0.402 |
| 48.000 | 0.340 |
| 64.000 | 0.277 |
| 80.000 | 0.227 |
| 96.000 | 0.184 |
| 112.000 | 0.148 |
| 128.000 | 0.121 |
| 144.000 | 0.098 |
| 160.000 | 0.078 |
| 176.000 | 0.062 |
| 192.000 | 0.047 |
| 208.000 | 0.035 |
| 224.000 | 0.023 |
| 240.000 | 0.012 |
| 256.000 | 0.000 |

### 184. Time Delay After Idle To Enter Lean Cruise Vs ATS

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 5 points (AIR TEMP)
- Y-Axis: 1 points (SEC)
- Z-Axis (Data): 1 points (SEC)

**Statistics:**
- Min: 140.0000 SEC
- Max: 1800.0000 SEC
- Avg: 686.0000 SEC
- Dimensions: 1 × 5

**Full Data Table** (1 rows × 5 cols):

| Y \ X | 8.00 | 32.00 | 56.00 | 80.00 | 104.00 |
|-----|------|------|------|------|------|
| 0.00 | 140.00 | 140.00 | 450.00 | 900.00 | 1800.00 |

### 185. Lean Cruise (0-1)  Multiplier Table Vs Coolant

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (ECT)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (MULT)

**Statistics:**
- Min: 0.0000 MULT
- Max: 0.9961 MULT
- Avg: 0.6094 MULT
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | -40.00 | -16.00 | 8.00 | 32.00 | 56.00 | 80.00 | 104.00 | 128.00 | 152.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.25 | 0.50 | 0.75 | 1.00 | 1.00 | 1.00 | 1.00 |

### 186. Time In Lean Cruise Before Exit TP KCLRATIO For BLM Maintenance

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 5 points (AIR TEMP DEG/C)
- Y-Axis: 1 points (SEC)
- Z-Axis (Data): 1 points (SEC)

**Statistics:**
- Min: 75.0000 SEC
- Max: 1200.0000 SEC
- Avg: 465.0000 SEC
- Dimensions: 1 × 5

**Full Data Table** (1 rows × 5 cols):

| Y \ X | 8.00 | 32.00 | 56.00 | 80.00 | 104.00 |
|-----|------|------|------|------|------|
| 0.00 | 1200.00 | 600.00 | 300.00 | 150.00 | 75.00 |

### 187. Exit From KCLRATIO To Lean Cruise For CAL Time When BLM Fueling Maintenance Is Required

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 5 points (AIR TEMP DEG/C)
- Y-Axis: 1 points (SEC)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 1.5000 
- Max: 6.0000 
- Avg: 3.0000 
- Dimensions: 1 × 5

**Full Data Table** (1 rows × 5 cols):

| Y \ X | 8.00 | 32.00 | 56.00 | 80.00 | 104.00 |
|-----|------|------|------|------|------|
| 0.00 | 1.50 | 1.50 | 2.25 | 3.75 | 6.00 |

### 188. Startup Air Fuel Timeout - Reduction Freq. Multiplier V's Coolant

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (Multiplier)
- Y-Axis: 9 points (DEG/C)
- Z-Axis (Data): 9 points

**Statistics:**
- Min: 1.0000 
- Max: 3.0000 
- Avg: 1.5694 
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Row | C0 |
|-----|------|
| -40.00 | 3.00 |
| -16.00 | 2.50 |
| 8.00 | 2.00 |
| 32.00 | 1.50 |
| 56.00 | 1.12 |
| 80.00 | 1.00 |
| 104.00 | 1.00 |
| 128.00 | 1.00 |
| 152.00 | 1.00 |

### 189. Lean Cruise A/F Delta Vs RPM & CYLAIREL

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 15 points (MGC)
- Y-Axis: 10 points (RPM)
- Z-Axis (Data): 150 points

**Statistics:**
- Min: 0.0000 
- Max: 2.3063 
- Avg: 0.5742 
- Dimensions: 10 × 15

**Full Data Table** (10 rows × 15 cols):

| Y \ X | 93.00 | 125.00 | 156.00 | 187.00 | 218.00 | 250.00 | 281.00 | 312.00 | 343.00 | 375.00 | 406.00 | 437.00 | 468.00 | 500.00 | 593.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 400.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 800.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 1200.00 | 0.00 | 0.00 | 0.00 | 0.41 | 0.55 | 0.70 | 0.99 | 1.30 | 1.46 | 1.79 | 1.79 | 1.79 | 0.84 | 0.00 | 0.00 |
| 1600.00 | 0.00 | 0.00 | 0.00 | 0.41 | 0.55 | 0.70 | 0.99 | 1.30 | 1.79 | 2.31 | 2.31 | 2.31 | 1.15 | 0.00 | 0.00 |
| 2000.00 | 0.00 | 0.00 | 0.00 | 0.27 | 0.41 | 0.55 | 0.84 | 1.30 | 1.79 | 2.31 | 2.31 | 2.31 | 1.15 | 0.00 | 0.00 |
| 2400.00 | 0.00 | 0.00 | 0.00 | 0.27 | 0.41 | 0.70 | 0.99 | 1.30 | 1.79 | 2.31 | 2.31 | 2.31 | 1.15 | 0.00 | 0.00 |
| 2800.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.41 | 0.70 | 0.99 | 1.30 | 1.79 | 2.31 | 2.31 | 2.31 | 1.15 | 0.00 | 0.00 |
| 3200.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.41 | 0.70 | 0.99 | 1.30 | 1.46 | 1.79 | 2.31 | 2.31 | 1.15 | 0.00 | 0.00 |
| 3600.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.41 | 0.55 | 0.70 | 0.84 | 0.99 | 1.15 | 1.46 | 1.46 | 0.70 | 0.00 | 0.00 |
| 4000.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 190. High Octane Spark Advance Lean Cruise Trim Value Vs Cylair3 & RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 15 points (CYLAIR3)
- Y-Axis: 14 points (RPM)
- Z-Axis (Data): 210 points (DEG)

**Statistics:**
- Min: 0.1562 DEG
- Max: 5.4297 DEG
- Avg: 1.1674 DEG
- Dimensions: 14 × 15

**Full Data Table** (14 rows × 15 cols):

| Y \ X | 93.75 | 125.00 | 156.25 | 187.50 | 218.75 | 250.00 | 281.25 | 312.50 | 343.75 | 375.00 | 406.25 | 437.50 | 468.75 | 500.00 | 531.25 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 600.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 |
| 800.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 |
| 1000.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.86 | 1.91 | 2.62 | 1.91 | 0.86 | 0.16 | 0.16 |
| 1200.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 1.21 | 2.97 | 2.97 | 2.62 | 2.62 | 2.97 | 2.62 | 1.21 | 0.16 | 0.16 |
| 1400.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.86 | 2.27 | 2.97 | 2.62 | 3.67 | 3.67 | 2.97 | 1.21 | 0.16 | 0.16 |
| 1600.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 1.21 | 2.27 | 1.91 | 2.62 | 4.02 | 4.38 | 3.67 | 1.21 | 0.16 | 0.16 |
| 1800.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.86 | 2.97 | 4.02 | 2.27 | 3.67 | 5.08 | 4.38 | 1.21 | 0.16 | 0.16 |
| 2000.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 4.02 | 4.02 | 2.62 | 4.38 | 5.43 | 4.38 | 1.21 | 0.16 | 0.16 |
| 2200.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 1.21 | 3.67 | 4.02 | 2.62 | 4.02 | 5.08 | 4.02 | 1.21 | 0.16 | 0.16 |
| 2400.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 1.91 | 2.27 | 2.62 | 1.91 | 3.32 | 5.08 | 4.02 | 1.21 | 0.16 | 0.16 |
| 2800.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 1.21 | 2.27 | 1.21 | 1.91 | 3.67 | 5.08 | 4.02 | 1.56 | 0.16 | 0.16 |
| 3200.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 1.56 | 2.27 | 1.91 | 2.97 | 3.32 | 3.67 | 3.67 | 1.91 | 0.16 | 0.16 |
| 3600.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.86 | 1.91 | 2.62 | 1.91 | 1.56 | 1.56 | 1.56 | 1.91 | 1.91 | 0.16 | 0.16 |
| 4000.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 |

### 191. Low Octane Spark Advance Lean Cruise Trim Value Vs Cylair3 & RPM

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 15 points (Cylair3)
- Y-Axis: 14 points (RPM)
- Z-Axis (Data): 210 points (DEG)

**Statistics:**
- Min: 0.1562 DEG
- Max: 5.4297 DEG
- Avg: 1.0151 DEG
- Dimensions: 14 × 15

**Full Data Table** (14 rows × 15 cols):

| Y \ X | 93.75 | 125.00 | 156.25 | 187.50 | 218.75 | 250.00 | 281.25 | 312.50 | 343.75 | 375.00 | 406.25 | 437.50 | 468.75 | 500.00 | 531.25 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 600.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 |
| 800.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 |
| 1000.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.86 | 1.91 | 1.91 | 1.91 | 0.86 | 0.16 | 0.16 |
| 1200.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 1.21 | 1.21 | 1.56 | 2.62 | 2.97 | 2.97 | 2.62 | 1.21 | 0.16 | 0.16 |
| 1400.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.86 | 1.21 | 1.56 | 2.97 | 4.02 | 3.67 | 2.97 | 1.21 | 0.16 | 0.16 |
| 1600.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.86 | 1.21 | 1.56 | 3.32 | 4.73 | 4.38 | 3.67 | 1.21 | 0.16 | 0.16 |
| 1800.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.51 | 1.21 | 1.56 | 3.32 | 4.73 | 5.08 | 4.38 | 1.21 | 0.16 | 0.16 |
| 2000.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 1.21 | 1.21 | 3.32 | 4.38 | 5.43 | 4.38 | 1.21 | 0.16 | 0.16 |
| 2200.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.51 | 1.56 | 1.56 | 3.32 | 4.02 | 5.08 | 4.02 | 1.21 | 0.16 | 0.16 |
| 2400.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 1.21 | 1.56 | 1.56 | 3.32 | 4.02 | 5.08 | 4.02 | 1.21 | 0.16 | 0.16 |
| 2800.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 1.21 | 1.21 | 1.56 | 2.27 | 3.67 | 4.02 | 3.67 | 1.56 | 0.16 | 0.16 |
| 3200.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.86 | 0.86 | 1.56 | 1.91 | 2.27 | 2.62 | 2.62 | 1.56 | 0.16 | 0.16 |
| 3600.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.86 | 0.86 | 0.86 | 0.86 | 0.86 | 0.86 | 1.56 | 1.91 | 1.91 | 0.16 | 0.16 |
| 4000.00 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 |

### 192. Altitude Compensation for Lean Cruise Spark Vs Load Selector (0-2 Multiplier)

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 11 points (ENGPERF)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (SCALER)

**Statistics:**
- Min: 0.5000 SCALER
- Max: 1.0000 SCALER
- Avg: 0.9318 SCALER
- Dimensions: 1 × 11

**Full Data Table** (1 rows × 11 cols):

| Y \ X | 96.00 | 112.00 | 128.00 | 144.00 | 160.00 | 176.00 | 192.00 | 208.00 | 224.00 | 240.00 | 256.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.50 | 0.75 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

### 193. 0-2 Multiplier Lean Cruise Spark Compensation Vs Coolant Temperature

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 9 points (DEG/C)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points (DEG/C)

**Statistics:**
- Min: 1.0000 DEG/C
- Max: 1.0000 DEG/C
- Avg: 1.0000 DEG/C
- Dimensions: 1 × 9

**Full Data Table** (1 rows × 9 cols):

| Y \ X | -40.00 | -16.00 | 8.00 | 32.00 | 56.00 | 80.00 | 104.00 | 128.00 | 152.00 |
|-----|------|------|------|------|------|------|------|------|------|
| 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

### 194. 1-2-3-4 Reference Average Ratio Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (%TPS)
- Y-Axis: 3 points (GEAR CHANGE)
- Z-Axis (Data): 51 points (RATIO)

**Statistics:**
- Min: 0.0000 RATIO
- Max: 0.0000 RATIO
- Avg: 0.0000 RATIO
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 2 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 195. 1-2-3-4 Adaptive Modifier MOD Force Motor Pressure Vs Shift Time Error

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (SEC)
- Y-Axis: 3 points (GEAR - CHANGE)
- Z-Axis (Data): 51 points (PSI)

**Statistics:**
- Min: 14.0000 PSI
- Max: 18.0000 PSI
- Avg: 16.0000 PSI
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | -0.20 | -0.17 | -0.15 | -0.12 | -0.10 | -0.07 | -0.05 | -0.03 | 0.00 | 0.03 | 0.05 | 0.07 | 0.10 | 0.12 | 0.15 | 0.17 | 0.20 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 18.00 | 17.50 | 17.25 | 17.00 | 16.75 | 16.50 | 16.25 | 16.00 | 16.00 | 16.00 | 15.75 | 15.50 | 15.25 | 15.00 | 14.75 | 14.50 | 14.00 |
| 1 | 17.25 | 17.00 | 16.75 | 16.50 | 16.38 | 16.25 | 16.12 | 16.00 | 16.00 | 16.00 | 15.88 | 15.75 | 15.62 | 15.50 | 15.25 | 15.00 | 14.75 |
| 2 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 |

### 196. 1-2-3-4 Pressure Low Limit Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 3 points (GEAR - CHANGE)
- Z-Axis (Data): 51 points (PSI)

**Statistics:**
- Min: 11.0000 PSI
- Max: 16.0000 PSI
- Avg: 14.1765 PSI
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 16.00 | 16.00 | 16.00 | 14.00 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 |
| 1 | 16.00 | 16.00 | 16.00 | 16.00 | 14.00 | 14.00 | 14.00 | 14.00 | 14.00 | 14.00 | 14.00 | 14.00 | 14.00 | 14.00 | 14.00 | 14.00 | 14.00 |
| 2 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 |

### 197. 1-2-3-4 Pressure High Limit Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 3 points (GEAR - CHANGE)
- Z-Axis (Data): 51 points (PSI)

**Statistics:**
- Min: 16.0000 PSI
- Max: 26.0000 PSI
- Avg: 21.1961 PSI
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 16.00 | 16.00 | 16.00 | 21.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 |
| 1 | 16.00 | 16.00 | 16.00 | 16.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 | 26.00 |
| 2 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 |

### 198. 1-2-3-4 Pressure Modifier Loaded During ALDL Mode 4 Request

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points
- Y-Axis: 3 points (GEAR CHANGE)
- Z-Axis (Data): 51 points (PSI)

**Statistics:**
- Min: 16.0000 PSI
- Max: 18.0000 PSI
- Avg: 16.2549 PSI
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Row | C0 | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 | C13 | C14 | C15 | C16 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 16.00 | 16.00 | 16.00 | 16.00 | 18.00 | 18.00 | 18.00 | 18.00 | 18.00 | 17.00 | 17.00 | 17.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 |
| 1 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 |
| 2 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 | 16.00 |

### 199. Normal 1-2-3-4 Shift Low - Time Vs TPS

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 3 points (GEAR - CHANGE)
- Z-Axis (Data): 51 points (SECONDS)

**Statistics:**
- Min: 0.7500 SECONDS
- Max: 4.6750 SECONDS
- Avg: 2.0907 SECONDS
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 0.75 | 0.75 | 0.78 | 0.82 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.85 | 0.85 | 0.85 |
| 1 | 0.75 | 0.75 | 0.75 | 0.75 | 0.80 | 0.80 | 0.85 | 0.82 | 0.82 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 |
| 2 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 |

### 200. Normal 1-2-3-4 Shift High - Time Vs TPS

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 3 points (GEAR - CHANGE)
- Z-Axis (Data): 51 points (SECONDS)

**Statistics:**
- Min: 0.7500 SECONDS
- Max: 4.6750 SECONDS
- Avg: 2.0907 SECONDS
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 0.75 | 0.75 | 0.78 | 0.82 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.85 | 0.85 | 0.85 |
| 1 | 0.75 | 0.75 | 0.75 | 0.75 | 0.80 | 0.80 | 0.85 | 0.82 | 0.82 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 |
| 2 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 |

### 201. Performance 1-2-3-4 Shift Low - Time Vs TPS

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 3 points (GEAR - CHANGE)
- Z-Axis (Data): 51 points (SECONDS)

**Statistics:**
- Min: 0.7750 SECONDS
- Max: 4.6750 SECONDS
- Avg: 2.1000 SECONDS
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 0.80 | 0.80 | 0.78 | 0.82 | 0.82 | 0.80 | 0.80 | 0.82 | 0.82 | 0.82 | 0.82 | 0.80 | 0.82 | 0.82 | 0.82 | 0.85 | 0.85 |
| 1 | 0.80 | 0.80 | 0.82 | 0.80 | 0.85 | 0.85 | 0.88 | 0.85 | 0.82 | 0.80 | 0.80 | 0.78 | 0.78 | 0.78 | 0.78 | 0.78 | 0.78 |
| 2 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 |

### 202. Performance 1-2-3-4 Shift High - Time Vs TPS

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 3 points (GEAR - CHANGE)
- Z-Axis (Data): 51 points (SECONDS)

**Statistics:**
- Min: 4.6750 SECONDS
- Max: 4.6750 SECONDS
- Avg: 4.6750 SECONDS
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 |
| 1 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 |
| 2 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 | 4.67 |

### 203. Light Purge Fixed Duty Cycle Vs Airflow Or Cylair

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (GM/S)
- Y-Axis: 1 points (%DC)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 76.9531 
- Avg: 37.1094 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 4.00 | 8.00 | 12.00 | 16.00 | 20.00 | 24.00 | 28.00 | 32.00 | 36.00 | 40.00 | 44.00 | 48.00 | 52.00 | 56.00 | 60.00 | 64.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 7.42 | 10.55 | 12.50 | 15.62 | 18.75 | 24.22 | 29.69 | 35.55 | 40.23 | 46.09 | 50.78 | 56.64 | 62.50 | 69.14 | 74.22 | 76.95 |

### 204. Heavy Purge Fixed Duty Cycle Vs Airflow Or Cylair

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (GM/S)
- Y-Axis: 1 points (%DC)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 99.6094 
- Avg: 59.3520 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 4.00 | 8.00 | 12.00 | 16.00 | 20.00 | 24.00 | 28.00 | 32.00 | 36.00 | 40.00 | 44.00 | 48.00 | 52.00 | 56.00 | 60.00 | 64.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 11.72 | 19.14 | 25.39 | 29.30 | 35.16 | 41.80 | 51.56 | 61.33 | 70.31 | 79.30 | 87.89 | 97.66 | 99.61 | 99.61 | 99.61 | 99.61 |

### 205. Light/Heavy Purge Duty Cycle 0-2 Multiplier Vs Cylair

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 14 points (CYLAIR50)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.9844 
- Max: 1.9922 
- Avg: 1.3499 
- Dimensions: 1 × 14

**Full Data Table** (1 rows × 14 cols):

| Y \ X | 50.00 | 100.00 | 150.00 | 200.00 | 250.00 | 300.00 | 350.00 | 400.00 | 450.00 | 500.00 | 550.00 | 600.00 | 650.00 | 700.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.98 | 0.99 | 1.00 | 1.01 | 1.02 | 1.03 | 1.05 | 1.07 | 1.21 | 1.57 | 1.99 | 1.99 | 1.99 | 1.99 |

### 206. Normal Ramp Rate Vs Engine Load

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 10 points (CYL_AIR)
- Y-Axis: 1 points (DEG/S)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 14.0625 
- Max: 28.1250 
- Avg: 22.8516 
- Dimensions: 1 × 10

**Full Data Table** (1 rows × 10 cols):

| Y \ X | 50.00 | 100.00 | 150.00 | 200.00 | 250.00 | 300.00 | 350.00 | 400.00 | 450.00 | 500.00 |
|-----|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 14.06 | 14.06 | 21.09 | 28.12 | 28.12 | 28.12 | 26.37 | 24.61 | 22.85 | 21.09 |

### 207. Apply Speed 3rd Gear - Normal

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 53.1084 
- Max: 205.1914 
- Avg: 131.3509 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.0 |
|-----|------|
| 0.0 | 53.1 |
| 6.2 | 53.1 |
| 12.5 | 53.1 |
| 18.8 | 53.1 |
| 25.0 | 54.7 |
| 31.2 | 58.7 |
| 37.5 | 69.2 |
| 43.8 | 86.9 |
| 50.0 | 109.4 |
| 56.2 | 205.2 |
| 62.5 | 205.2 |
| 68.8 | 205.2 |
| 75.0 | 205.2 |
| 81.2 | 205.2 |
| 87.5 | 205.2 |
| 93.8 | 205.2 |
| 100.0 | 205.2 |

### 208. Apply Speed 4th Gear -  Normal

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 70.8111 
- Max: 205.1914 
- Avg: 147.5390 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.0 |
|-----|------|
| 0.0 | 70.8 |
| 6.2 | 70.8 |
| 12.5 | 70.8 |
| 18.8 | 70.8 |
| 25.0 | 72.4 |
| 31.2 | 80.5 |
| 37.5 | 96.6 |
| 43.8 | 128.7 |
| 50.0 | 205.2 |
| 56.2 | 205.2 |
| 62.5 | 205.2 |
| 68.8 | 205.2 |
| 75.0 | 205.2 |
| 81.2 | 205.2 |
| 87.5 | 205.2 |
| 93.8 | 205.2 |
| 100.0 | 205.2 |

### 209. Apply Speed 3rd Gear -  Power

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 61.1551 
- Max: 205.1914 
- Avg: 138.8769 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.0 |
|-----|------|
| 0.0 | 61.2 |
| 6.2 | 61.2 |
| 12.5 | 61.2 |
| 18.8 | 61.2 |
| 25.0 | 64.4 |
| 31.2 | 80.5 |
| 37.5 | 96.6 |
| 43.8 | 104.6 |
| 50.0 | 128.7 |
| 56.2 | 205.2 |
| 62.5 | 205.2 |
| 68.8 | 205.2 |
| 75.0 | 205.2 |
| 81.2 | 205.2 |
| 87.5 | 205.2 |
| 93.8 | 205.2 |
| 100.0 | 205.2 |

### 210. Apply Speed 4th Gear -  Power

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 88.5139 
- Max: 205.1914 
- Avg: 161.8811 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.0 |
|-----|------|
| 0.0 | 88.5 |
| 6.2 | 88.5 |
| 12.5 | 88.5 |
| 18.8 | 88.5 |
| 25.0 | 93.3 |
| 31.2 | 112.7 |
| 37.5 | 140.0 |
| 43.8 | 205.2 |
| 50.0 | 205.2 |
| 56.2 | 205.2 |
| 62.5 | 205.2 |
| 68.8 | 205.2 |
| 75.0 | 205.2 |
| 81.2 | 205.2 |
| 87.5 | 205.2 |
| 93.8 | 205.2 |
| 100.0 | 205.2 |

### 211. Apply Speed 2nd Gear - Hot

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 205.1914 
- Max: 205.1914 
- Avg: 205.1914 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 205.19 |
| 6.25 | 205.19 |
| 12.50 | 205.19 |
| 18.75 | 205.19 |
| 25.00 | 205.19 |
| 31.25 | 205.19 |
| 37.50 | 205.19 |
| 43.75 | 205.19 |
| 50.00 | 205.19 |
| 56.25 | 205.19 |
| 62.50 | 205.19 |
| 68.75 | 205.19 |
| 75.00 | 205.19 |
| 81.25 | 205.19 |
| 87.50 | 205.19 |
| 93.75 | 205.19 |
| 100.00 | 205.19 |

### 212. Apply Speed 3rd Gear - Hot

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 54.7177 
- Max: 54.7177 
- Avg: 54.7177 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 54.72 |
| 6.25 | 54.72 |
| 12.50 | 54.72 |
| 18.75 | 54.72 |
| 25.00 | 54.72 |
| 31.25 | 54.72 |
| 37.50 | 54.72 |
| 43.75 | 54.72 |
| 50.00 | 54.72 |
| 56.25 | 54.72 |
| 62.50 | 54.72 |
| 68.75 | 54.72 |
| 75.00 | 54.72 |
| 81.25 | 54.72 |
| 87.50 | 54.72 |
| 93.75 | 54.72 |
| 100.00 | 54.72 |

### 213. Apply Speed 4th Gear - Hot

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 205.1914 
- Max: 205.1914 
- Avg: 205.1914 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 205.19 |
| 6.25 | 205.19 |
| 12.50 | 205.19 |
| 18.75 | 205.19 |
| 25.00 | 205.19 |
| 31.25 | 205.19 |
| 37.50 | 205.19 |
| 43.75 | 205.19 |
| 50.00 | 205.19 |
| 56.25 | 205.19 |
| 62.50 | 205.19 |
| 68.75 | 205.19 |
| 75.00 | 205.19 |
| 81.25 | 205.19 |
| 87.50 | 205.19 |
| 93.75 | 205.19 |
| 100.00 | 205.19 |

### 214. Apply Speed 3rd Gear - Cruise

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 61.1551 
- Max: 205.1914 
- Avg: 143.8470 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.0 |
|-----|------|
| 0.0 | 61.2 |
| 6.2 | 61.2 |
| 12.5 | 61.2 |
| 18.8 | 61.2 |
| 25.0 | 64.4 |
| 31.2 | 80.5 |
| 37.5 | 96.6 |
| 43.8 | 112.7 |
| 50.0 | 205.2 |
| 56.2 | 205.2 |
| 62.5 | 205.2 |
| 68.8 | 205.2 |
| 75.0 | 205.2 |
| 81.2 | 205.2 |
| 87.5 | 205.2 |
| 93.8 | 205.2 |
| 100.0 | 205.2 |

### 215. Apply Speed 4th Gear -  Cruise

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 80.4672 
- Max: 205.1914 
- Avg: 161.2184 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.0 |
|-----|------|
| 0.0 | 80.5 |
| 6.2 | 80.5 |
| 12.5 | 80.5 |
| 18.8 | 80.5 |
| 25.0 | 93.3 |
| 31.2 | 112.7 |
| 37.5 | 160.9 |
| 43.8 | 205.2 |
| 50.0 | 205.2 |
| 56.2 | 205.2 |
| 62.5 | 205.2 |
| 68.8 | 205.2 |
| 75.0 | 205.2 |
| 81.2 | 205.2 |
| 87.5 | 205.2 |
| 93.8 | 205.2 |
| 100.0 | 205.2 |

### 216. Apply Speed 2-4 Gear - Altitude Normal

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 102.9980 
- Max: 102.9980 
- Avg: 102.9980 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 103.00 |
| 6.25 | 103.00 |
| 12.50 | 103.00 |
| 18.75 | 103.00 |
| 25.00 | 103.00 |
| 31.25 | 103.00 |
| 37.50 | 103.00 |
| 43.75 | 103.00 |
| 50.00 | 103.00 |
| 56.25 | 103.00 |
| 62.50 | 103.00 |
| 68.75 | 103.00 |
| 75.00 | 103.00 |
| 81.25 | 103.00 |
| 87.50 | 103.00 |
| 93.75 | 103.00 |
| 100.00 | 103.00 |

### 217. Release Speed 2-4 Gear - Altitude Normal

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 102.9980 
- Max: 102.9980 
- Avg: 102.9980 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 103.00 |
| 6.25 | 103.00 |
| 12.50 | 103.00 |
| 18.75 | 103.00 |
| 25.00 | 103.00 |
| 31.25 | 103.00 |
| 37.50 | 103.00 |
| 43.75 | 103.00 |
| 50.00 | 103.00 |
| 56.25 | 103.00 |
| 62.50 | 103.00 |
| 68.75 | 103.00 |
| 75.00 | 103.00 |
| 81.25 | 103.00 |
| 87.50 | 103.00 |
| 93.75 | 103.00 |
| 100.00 | 103.00 |

### 218. Release Speed 3rd Gear - Normal

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 48.2803 
- Max: 204.3867 
- Avg: 119.1861 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.0 |
|-----|------|
| 0.0 | 48.3 |
| 6.2 | 48.3 |
| 12.5 | 48.3 |
| 18.8 | 48.3 |
| 25.0 | 48.3 |
| 31.2 | 48.3 |
| 37.5 | 52.3 |
| 43.8 | 62.0 |
| 50.0 | 82.1 |
| 56.2 | 109.4 |
| 62.5 | 204.4 |
| 68.8 | 204.4 |
| 75.0 | 204.4 |
| 81.2 | 204.4 |
| 87.5 | 204.4 |
| 93.8 | 204.4 |
| 100.0 | 204.4 |

### 219. Release Speed 4th Gear -  Normal

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 68.3971 
- Max: 204.3867 
- Avg: 137.3622 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.0 |
|-----|------|
| 0.0 | 68.4 |
| 6.2 | 68.4 |
| 12.5 | 68.4 |
| 18.8 | 68.4 |
| 25.0 | 68.4 |
| 31.2 | 68.4 |
| 37.5 | 77.2 |
| 43.8 | 91.7 |
| 50.0 | 120.7 |
| 56.2 | 204.4 |
| 62.5 | 204.4 |
| 68.8 | 204.4 |
| 75.0 | 204.4 |
| 81.2 | 204.4 |
| 87.5 | 204.4 |
| 93.8 | 204.4 |
| 100.0 | 204.4 |

### 220. Release Speed 3rd Gear -  Power

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 53.1084 
- Max: 204.3867 
- Avg: 125.1502 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.0 |
|-----|------|
| 0.0 | 53.1 |
| 6.2 | 53.1 |
| 12.5 | 53.1 |
| 18.8 | 53.1 |
| 25.0 | 53.1 |
| 31.2 | 53.1 |
| 37.5 | 53.1 |
| 43.8 | 83.7 |
| 50.0 | 96.6 |
| 56.2 | 144.8 |
| 62.5 | 204.4 |
| 68.8 | 204.4 |
| 75.0 | 204.4 |
| 81.2 | 204.4 |
| 87.5 | 204.4 |
| 93.8 | 204.4 |
| 100.0 | 204.4 |

### 221. Release Speed 4th Gear -  Power

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 78.8579 
- Max: 204.3867 
- Avg: 135.9422 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.0 |
|-----|------|
| 0.0 | 78.9 |
| 6.2 | 78.9 |
| 12.5 | 78.9 |
| 18.8 | 78.9 |
| 25.0 | 78.9 |
| 31.2 | 78.9 |
| 37.5 | 82.1 |
| 43.8 | 83.7 |
| 50.0 | 96.6 |
| 56.2 | 144.8 |
| 62.5 | 204.4 |
| 68.8 | 204.4 |
| 75.0 | 204.4 |
| 81.2 | 204.4 |
| 87.5 | 204.4 |
| 93.8 | 204.4 |
| 100.0 | 204.4 |

### 222. Release Speed 2nd Gear - Hot

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 150.4737 
- Max: 150.4737 
- Avg: 150.4737 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 150.47 |
| 6.25 | 150.47 |
| 12.50 | 150.47 |
| 18.75 | 150.47 |
| 25.00 | 150.47 |
| 31.25 | 150.47 |
| 37.50 | 150.47 |
| 43.75 | 150.47 |
| 50.00 | 150.47 |
| 56.25 | 150.47 |
| 62.50 | 150.47 |
| 68.75 | 150.47 |
| 75.00 | 150.47 |
| 81.25 | 150.47 |
| 87.50 | 150.47 |
| 93.75 | 150.47 |
| 100.00 | 150.47 |

### 223. Release Speed 3rd Gear - Hot

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 48.2803 
- Max: 48.2803 
- Avg: 48.2803 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 48.28 |
| 6.25 | 48.28 |
| 12.50 | 48.28 |
| 18.75 | 48.28 |
| 25.00 | 48.28 |
| 31.25 | 48.28 |
| 37.50 | 48.28 |
| 43.75 | 48.28 |
| 50.00 | 48.28 |
| 56.25 | 48.28 |
| 62.50 | 48.28 |
| 68.75 | 48.28 |
| 75.00 | 48.28 |
| 81.25 | 48.28 |
| 87.50 | 48.28 |
| 93.75 | 48.28 |
| 100.00 | 48.28 |

### 224. Release Speed 4th Gear - Hot

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 204.3867 
- Max: 204.3867 
- Avg: 204.3867 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 204.39 |
| 6.25 | 204.39 |
| 12.50 | 204.39 |
| 18.75 | 204.39 |
| 25.00 | 204.39 |
| 31.25 | 204.39 |
| 37.50 | 204.39 |
| 43.75 | 204.39 |
| 50.00 | 204.39 |
| 56.25 | 204.39 |
| 62.50 | 204.39 |
| 68.75 | 204.39 |
| 75.00 | 204.39 |
| 81.25 | 204.39 |
| 87.50 | 204.39 |
| 93.75 | 204.39 |
| 100.00 | 204.39 |

### 225. Release Speed 3rd Gear -  Cruise

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 53.1084 
- Max: 204.3867 
- Avg: 121.0795 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.0 |
|-----|------|
| 0.0 | 53.1 |
| 6.2 | 53.1 |
| 12.5 | 53.1 |
| 18.8 | 53.1 |
| 25.0 | 53.1 |
| 31.2 | 53.1 |
| 37.5 | 61.2 |
| 43.8 | 70.8 |
| 50.0 | 83.7 |
| 56.2 | 93.3 |
| 62.5 | 204.4 |
| 68.8 | 204.4 |
| 75.0 | 204.4 |
| 81.2 | 204.4 |
| 87.5 | 204.4 |
| 93.8 | 204.4 |
| 100.0 | 204.4 |

### 226. Release Speed 4th Gear -  Cruise

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (KPH)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 70.8111 
- Max: 204.3867 
- Avg: 127.8955 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.0 |
|-----|------|
| 0.0 | 70.8 |
| 6.2 | 70.8 |
| 12.5 | 70.8 |
| 18.8 | 70.8 |
| 25.0 | 70.8 |
| 31.2 | 70.8 |
| 37.5 | 70.8 |
| 43.8 | 70.8 |
| 50.0 | 83.7 |
| 56.2 | 93.3 |
| 62.5 | 204.4 |
| 68.8 | 204.4 |
| 75.0 | 204.4 |
| 81.2 | 204.4 |
| 87.5 | 204.4 |
| 93.8 | 204.4 |
| 100.0 | 204.4 |

### 227. Release 3rd Gear - Normal - Duty Cycle Vs TPS

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (DUTY CYCLE)
- Z-Axis (Data): 1 points (%)

**Statistics:**
- Min: 70.1961 %
- Max: 70.1961 %
- Avg: 70.1961 %
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 70.20 | 70.20 | 70.20 | 70.20 | 70.20 | 70.20 | 70.20 | 70.20 | 70.20 | 70.20 | 70.20 | 70.20 | 70.20 | 70.20 | 70.20 | 70.20 | 70.20 |

### 228. Release 4th Gear - Normal - Duty Cycle Vs TPS

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (DUTY CYCLE)
- Z-Axis (Data): 1 points (%)

**Statistics:**
- Min: 56.4706 %
- Max: 56.4706 %
- Avg: 56.4706 %
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 |

### 229. Release 2nd Gear - Hot - Duty Cycle Vs TPS

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (DUTY CYCLE)
- Z-Axis (Data): 1 points (%)

**Statistics:**
- Min: 56.4706 %
- Max: 56.4706 %
- Avg: 56.4706 %
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 |

### 230. Release 3rd Gear - Hot - Duty Cycle Vs TPS

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (DUTY CYCLE)
- Z-Axis (Data): 1 points (%)

**Statistics:**
- Min: 56.4706 %
- Max: 56.4706 %
- Avg: 56.4706 %
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 |

### 231. Release 4th Gear - Hot - Duty Cycle Vs TPS

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points
- Y-Axis: 1 points (DUTY CYCLE)
- Z-Axis (Data): 1 points (%)

**Statistics:**
- Min: 56.4706 %
- Max: 56.4706 %
- Avg: 56.4706 %
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 | 56.47 |

### 232. Release Rate Time - Normal - 3rd Gear

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (%TPS)
- Y-Axis: 1 points (%/SEC)
- Z-Axis (Data): 1 points (%/SEC)

**Statistics:**
- Min: 49.0196 %/SEC
- Max: 57.3529 %/SEC
- Avg: 55.8824 %/SEC
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 49.02 | 49.02 | 49.02 | 57.35 | 57.35 | 57.35 | 57.35 | 57.35 | 57.35 | 57.35 | 57.35 | 57.35 | 57.35 | 57.35 | 57.35 | 57.35 | 57.35 |

### 233. Release Rate Time - Normal - 4th Gear

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (%TPS)
- Y-Axis: 1 points (%/SEC)
- Z-Axis (Data): 1 points (%/SEC)

**Statistics:**
- Min: 24.5098 %/SEC
- Max: 98.0392 %/SEC
- Avg: 72.7509 %/SEC
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 24.51 | 25.00 | 57.35 | 57.35 | 57.35 | 57.35 | 57.35 | 57.35 | 73.53 | 83.33 | 98.04 | 98.04 | 98.04 | 98.04 | 98.04 | 98.04 | 98.04 |

### 234. Release Rate Time - Hot - 2nd Gear

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (%TPS)
- Y-Axis: 1 points (%/SEC)
- Z-Axis (Data): 1 points (%/SEC)

**Statistics:**
- Min: 83.3333 %/SEC
- Max: 83.3333 %/SEC
- Avg: 83.3333 %/SEC
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 |

### 235. Release Rate Time - Hot - 3rd Gear

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (%TPS)
- Y-Axis: 1 points (%/SEC)
- Z-Axis (Data): 1 points (%/SEC)

**Statistics:**
- Min: 83.3333 %/SEC
- Max: 83.3333 %/SEC
- Avg: 83.3333 %/SEC
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 |

### 236. Release Rate Time - Hot - 4th Gear

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (%TPS)
- Y-Axis: 1 points (%/SEC)
- Z-Axis (Data): 1 points (%/SEC)

**Statistics:**
- Min: 83.3333 %/SEC
- Max: 83.3333 %/SEC
- Avg: 83.3333 %/SEC
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 | 83.33 |

### 237. Apply 3rd Gear - Normal - Duty Cycle Vs TPS

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (DUTY CYCLE)
- Z-Axis (Data): 1 points (%)

**Statistics:**
- Min: 30.1961 %
- Max: 47.0588 %
- Avg: 41.7070 %
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 30.20 | 30.20 | 30.20 | 30.20 | 34.51 | 39.22 | 43.92 | 47.06 | 47.06 | 47.06 | 47.06 | 47.06 | 47.06 | 47.06 | 47.06 | 47.06 | 47.06 |

### 238. Apply 4th Gear - Normal - Duty Cycle Vs TPS

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (DUTY CYCLE)
- Z-Axis (Data): 1 points (%)

**Statistics:**
- Min: 39.2157 %
- Max: 56.8627 %
- Avg: 51.4418 %
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 39.22 | 39.22 | 39.22 | 39.22 | 45.10 | 49.02 | 54.90 | 56.86 | 56.86 | 56.86 | 56.86 | 56.86 | 56.86 | 56.86 | 56.86 | 56.86 | 56.86 |

### 239. Apply 2nd Gear - Hot - Duty Cycle Vs TPS

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (DUTY CYCLE)
- Z-Axis (Data): 1 points (%)

**Statistics:**
- Min: 50.1961 %
- Max: 50.1961 %
- Avg: 50.1961 %
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 |

### 240. Apply 3rd Gear - Hot - Duty Cycle Vs TPS

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (DUTY CYCLE)
- Z-Axis (Data): 1 points (%)

**Statistics:**
- Min: 30.1961 %
- Max: 50.1961 %
- Avg: 43.3679 %
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 30.20 | 30.20 | 30.20 | 30.20 | 34.51 | 39.22 | 43.92 | 47.06 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 |

### 241. Apply 4th Gear - Hot - Duty Cycle Vs TPS

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (DUTY CYCLE)
- Z-Axis (Data): 1 points (%)

**Statistics:**
- Min: 30.1961 %
- Max: 50.1961 %
- Avg: 43.3679 %
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 30.20 | 30.20 | 30.20 | 30.20 | 34.51 | 39.22 | 43.92 | 47.06 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 | 50.20 |

### 242. Apply Rate Time - Normal - 3rd Gear

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (%/SEC)
- Z-Axis (Data): 1 points (%/SEC)

**Statistics:**
- Min: 28.4314 %/SEC
- Max: 49.5098 %/SEC
- Avg: 41.9839 %/SEC
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 28.43 | 28.43 | 28.43 | 28.43 | 31.37 | 36.27 | 40.20 | 46.57 | 49.51 | 49.51 | 49.51 | 49.51 | 49.51 | 49.51 | 49.51 | 49.51 | 49.51 |

### 243. Apply Rate Time - Normal - 4th Gear

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (%/SEC)
- Z-Axis (Data): 1 points (%/SEC)

**Statistics:**
- Min: 28.4314 %/SEC
- Max: 49.5098 %/SEC
- Avg: 41.9839 %/SEC
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 28.43 | 28.43 | 28.43 | 28.43 | 31.37 | 36.27 | 40.20 | 46.57 | 49.51 | 49.51 | 49.51 | 49.51 | 49.51 | 49.51 | 49.51 | 49.51 | 49.51 |

### 244. Apply Rate Time - Hot - 2nd Gear

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (%/SEC)
- Z-Axis (Data): 1 points (%/SEC)

**Statistics:**
- Min: 50.0000 %/SEC
- Max: 50.0000 %/SEC
- Avg: 50.0000 %/SEC
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 |

### 245. Apply Rate Time - Hot - 3rd Gear

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (%/SEC)
- Z-Axis (Data): 1 points (%/SEC)

**Statistics:**
- Min: 50.0000 %/SEC
- Max: 50.0000 %/SEC
- Avg: 50.0000 %/SEC
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 |

### 246. Apply Rate Time - Hot - 4th Gear

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (%/SEC)
- Z-Axis (Data): 1 points (%/SEC)

**Statistics:**
- Min: 50.0000 %/SEC
- Max: 50.0000 %/SEC
- Avg: 50.0000 %/SEC
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 |

### 247. OP PT Multiplier Due To Pressure

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points
- Y-Axis: 17 points
- Z-Axis (Data): 17 points (FRACT)

**Statistics:**
- Min: 1.0000 FRACT
- Max: 1.0000 FRACT
- Avg: 1.0000 FRACT
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 1.00 |
| 8.00 | 1.00 |
| 16.00 | 1.00 |
| 24.00 | 1.00 |
| 32.00 | 1.00 |
| 40.00 | 1.00 |
| 48.00 | 1.00 |
| 56.00 | 1.00 |
| 64.00 | 1.00 |
| 72.00 | 1.00 |
| 80.00 | 1.00 |
| 88.00 | 1.00 |
| 96.00 | 1.00 |
| 104.00 | 1.00 |
| 112.00 | 1.00 |
| 120.00 | 1.00 |
| 128.00 | 1.00 |

### 248. OP PT Due To Throtmod

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (%)
- Y-Axis: 17 points (TPS%)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 96.0784 
- Max: 96.0784 
- Avg: 96.0784 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 96.08 |
| 6.25 | 96.08 |
| 12.50 | 96.08 |
| 18.75 | 96.08 |
| 25.00 | 96.08 |
| 31.25 | 96.08 |
| 37.50 | 96.08 |
| 43.75 | 96.08 |
| 50.00 | 96.08 |
| 56.25 | 96.08 |
| 62.50 | 96.08 |
| 68.75 | 96.08 |
| 75.00 | 96.08 |
| 81.25 | 96.08 |
| 87.50 | 96.08 |
| 93.75 | 96.08 |
| 100.00 | 96.08 |

### 249. Altitude Compensation Shift Compensation Baro Pressure Input Vs Shift Compensation 0-100% Factor

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (FACT)
- Y-Axis: 17 points (KPA)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 50.00 | 0.00 |
| 54.00 | 0.00 |
| 58.00 | 0.00 |
| 62.00 | 0.00 |
| 66.00 | 0.00 |
| 70.00 | 0.00 |
| 74.00 | 0.00 |
| 78.00 | 0.00 |
| 82.00 | 0.00 |
| 86.00 | 0.00 |
| 90.00 | 0.00 |
| 94.00 | 0.00 |
| 98.00 | 0.00 |
| 102.00 | 0.00 |
| 106.00 | 0.00 |
| 110.00 | 0.00 |
| 114.00 | 0.00 |

### 250. HOT 1-2-3-4 Upshift - TPS Vs KPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 3 points (GEAR - CHANGE)
- Z-Axis (Data): 51 points (KPH)

**Statistics:**
- Min: 20.9215 KPH
- Max: 205.1914 KPH
- Avg: 113.7112 KPH
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.0 | 6.2 | 12.5 | 18.8 | 25.0 | 31.2 | 37.5 | 43.8 | 50.0 | 56.2 | 62.5 | 68.8 | 75.0 | 81.2 | 87.5 | 93.8 | 100.0 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 20.9 | 20.9 | 24.1 | 27.4 | 32.2 | 37.0 | 40.2 | 46.7 | 53.1 | 57.9 | 59.5 | 61.2 | 64.4 | 66.0 | 66.0 | 66.0 | 66.0 |
| 1 | 37.0 | 37.0 | 41.8 | 51.5 | 61.2 | 70.8 | 77.2 | 85.3 | 93.3 | 103.0 | 111.0 | 119.1 | 120.7 | 123.1 | 123.1 | 123.1 | 123.1 |
| 2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 |

### 251. HOT 4-3-2-1 Downshift - TPS Vs KPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 3 points (GEAR - CHANGE)
- Z-Axis (Data): 51 points (KPH)

**Statistics:**
- Min: 19.3121 KPH
- Max: 204.3867 KPH
- Avg: 101.8936 KPH
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.0 | 6.2 | 12.5 | 18.8 | 25.0 | 31.2 | 37.5 | 43.8 | 50.0 | 56.2 | 62.5 | 68.8 | 75.0 | 81.2 | 87.5 | 93.8 | 100.0 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 20.1 | 19.3 | 19.3 | 19.3 | 19.3 | 24.1 | 24.1 | 24.1 | 24.1 | 40.2 | 40.2 | 40.2 | 40.2 | 40.2 | 45.9 | 45.9 | 45.9 |
| 1 | 35.4 | 33.8 | 33.8 | 33.8 | 35.4 | 43.5 | 51.5 | 59.5 | 67.6 | 74.0 | 80.5 | 88.5 | 99.8 | 109.4 | 114.3 | 114.3 | 114.3 |
| 2 | 204.4 | 204.4 | 204.4 | 204.4 | 204.4 | 204.4 | 204.4 | 204.4 | 204.4 | 204.4 | 204.4 | 204.4 | 204.4 | 204.4 | 204.4 | 204.4 | 204.4 |

### 252. PERFORMANCE 1-2-3-4 Upshift - TPS Vs KPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 3 points (GEAR - CHANGE)
- Z-Axis (Data): 51 points (KPH)

**Statistics:**
- Min: 20.9215 KPH
- Max: 205.1914 KPH
- Avg: 96.8446 KPH
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.0 | 6.2 | 12.5 | 18.8 | 25.0 | 31.2 | 37.5 | 43.8 | 50.0 | 56.2 | 62.5 | 68.8 | 75.0 | 81.2 | 87.5 | 93.8 | 100.0 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 20.9 | 20.9 | 20.9 | 24.1 | 29.0 | 33.8 | 38.6 | 45.1 | 51.5 | 56.3 | 57.9 | 59.5 | 61.2 | 62.8 | 64.4 | 64.4 | 64.4 |
| 1 | 35.4 | 35.4 | 35.4 | 41.8 | 49.9 | 59.5 | 72.4 | 82.1 | 91.7 | 99.8 | 104.6 | 111.0 | 115.9 | 119.1 | 119.1 | 119.1 | 119.1 |
| 2 | 88.5 | 88.5 | 88.5 | 88.5 | 93.3 | 112.7 | 140.0 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 |

### 253. PERFORMANCE 4-3-2-1 Downshift - TPS Vs KPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 3 points (GEAR - CHANGE)
- Z-Axis (Data): 51 points (KPH)

**Statistics:**
- Min: 18.5075 KPH
- Max: 204.3867 KPH
- Avg: 75.9389 KPH
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.0 | 6.2 | 12.5 | 18.8 | 25.0 | 31.2 | 37.5 | 43.8 | 50.0 | 56.2 | 62.5 | 68.8 | 75.0 | 81.2 | 87.5 | 93.8 | 100.0 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 20.1 | 18.5 | 18.5 | 18.5 | 18.5 | 18.5 | 18.5 | 18.5 | 18.5 | 18.5 | 18.5 | 24.1 | 32.2 | 40.2 | 45.9 | 45.9 | 45.9 |
| 1 | 34.6 | 32.2 | 32.2 | 32.2 | 32.2 | 37.0 | 46.7 | 53.1 | 61.2 | 69.2 | 78.9 | 85.3 | 96.6 | 103.0 | 109.4 | 109.4 | 109.4 |
| 2 | 78.9 | 78.9 | 78.9 | 78.9 | 78.9 | 78.9 | 82.1 | 83.7 | 96.6 | 144.8 | 204.4 | 204.4 | 204.4 | 204.4 | 204.4 | 204.4 | 204.4 |

### 254. NORMAL 1-2-3-4 Upshift - TPS Vs KPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 3 points (GEAR - CHANGE)
- Z-Axis (Data): 51 points (KPH)

**Statistics:**
- Min: 18.5075 KPH
- Max: 205.1914 KPH
- Avg: 87.3464 KPH
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.0 | 6.2 | 12.5 | 18.8 | 25.0 | 31.2 | 37.5 | 43.8 | 50.0 | 56.2 | 62.5 | 68.8 | 75.0 | 81.2 | 87.5 | 93.8 | 100.0 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 19.3 | 18.5 | 18.5 | 20.9 | 24.1 | 29.0 | 33.8 | 37.0 | 42.6 | 46.7 | 49.9 | 53.1 | 54.7 | 56.3 | 57.9 | 64.4 | 64.4 |
| 1 | 33.0 | 32.2 | 33.0 | 37.0 | 41.8 | 49.9 | 57.9 | 66.0 | 75.6 | 82.1 | 88.5 | 96.6 | 103.0 | 107.8 | 112.7 | 119.1 | 119.1 |
| 2 | 70.8 | 70.8 | 70.8 | 70.8 | 72.4 | 80.5 | 96.6 | 128.7 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 | 205.2 |

### 255. NORMAL 4-3-2-1 Downshift - TPS Vs KPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 3 points (GEAR - CHANGE)
- Z-Axis (Data): 51 points (KPH)

**Statistics:**
- Min: 16.0934 KPH
- Max: 204.3867 KPH
- Avg: 67.4189 KPH
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.0 | 6.2 | 12.5 | 18.8 | 25.0 | 31.2 | 37.5 | 43.8 | 50.0 | 56.2 | 62.5 | 68.8 | 75.0 | 81.2 | 87.5 | 93.8 | 100.0 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 18.5 | 16.1 | 16.1 | 16.1 | 16.1 | 16.1 | 16.1 | 16.1 | 16.1 | 16.1 | 16.1 | 16.1 | 16.1 | 24.1 | 32.2 | 45.9 | 45.9 |
| 1 | 32.2 | 29.0 | 29.0 | 29.0 | 29.0 | 33.8 | 40.2 | 43.5 | 48.3 | 51.5 | 57.9 | 64.4 | 72.4 | 80.5 | 96.6 | 109.4 | 109.4 |
| 2 | 62.8 | 62.8 | 62.8 | 62.8 | 62.8 | 62.8 | 62.8 | 69.2 | 80.5 | 103.0 | 204.4 | 204.4 | 204.4 | 204.4 | 204.4 | 204.4 | 204.4 |

### 256. CRUISE 2-3 Upshift %TPS Vs KPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (kph)
- Y-Axis: 17 points (TPS)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 35.4056 
- Max: 119.0915 
- Avg: 80.1832 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.0 |
|-----|------|
| 0.0 | 35.4 |
| 6.2 | 35.4 |
| 12.5 | 35.4 |
| 18.8 | 38.6 |
| 25.0 | 45.1 |
| 31.2 | 56.3 |
| 37.5 | 66.0 |
| 43.8 | 75.6 |
| 50.0 | 83.7 |
| 56.2 | 93.3 |
| 62.5 | 99.8 |
| 68.8 | 106.2 |
| 75.0 | 115.9 |
| 81.2 | 119.1 |
| 87.5 | 119.1 |
| 93.8 | 119.1 |
| 100.0 | 119.1 |

### 257. CRUISE 3-4 Upshift %TPS Vs KPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (kph)
- Y-Axis: 17 points (TPS)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 80.4672 
- Max: 205.1914 
- Avg: 161.2184 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.0 |
|-----|------|
| 0.0 | 80.5 |
| 6.2 | 80.5 |
| 12.5 | 80.5 |
| 18.8 | 80.5 |
| 25.0 | 93.3 |
| 31.2 | 112.7 |
| 37.5 | 160.9 |
| 43.8 | 205.2 |
| 50.0 | 205.2 |
| 56.2 | 205.2 |
| 62.5 | 205.2 |
| 68.8 | 205.2 |
| 75.0 | 205.2 |
| 81.2 | 205.2 |
| 87.5 | 205.2 |
| 93.8 | 205.2 |
| 100.0 | 205.2 |

### 258. CRUISE 3-2 Downshift %TPS Vs KPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (kph)
- Y-Axis: 17 points (TPS)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 32.1869 
- Max: 109.4354 
- Avg: 57.0844 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.0 |
|-----|------|
| 0.0 | 33.8 |
| 6.2 | 32.2 |
| 12.5 | 32.2 |
| 18.8 | 32.2 |
| 25.0 | 32.2 |
| 31.2 | 33.8 |
| 37.5 | 40.2 |
| 43.8 | 43.5 |
| 50.0 | 48.3 |
| 56.2 | 51.5 |
| 62.5 | 57.9 |
| 68.8 | 64.4 |
| 75.0 | 72.4 |
| 81.2 | 80.5 |
| 87.5 | 96.6 |
| 93.8 | 109.4 |
| 100.0 | 109.4 |

### 259. CRUISE 4-3 Downshift %TPS Vs KPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (kph)
- Y-Axis: 17 points (TPS)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 70.8111 
- Max: 204.3867 
- Avg: 127.8955 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.0 |
|-----|------|
| 0.0 | 70.8 |
| 6.2 | 70.8 |
| 12.5 | 70.8 |
| 18.8 | 70.8 |
| 25.0 | 70.8 |
| 31.2 | 70.8 |
| 37.5 | 70.8 |
| 43.8 | 70.8 |
| 50.0 | 83.7 |
| 56.2 | 93.3 |
| 62.5 | 204.4 |
| 68.8 | 204.4 |
| 75.0 | 204.4 |
| 81.2 | 204.4 |
| 87.5 | 204.4 |
| 93.8 | 204.4 |
| 100.0 | 204.4 |

### 260. COLD 1-2 Upshift - TPS Vs KPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (KPH)
- Z-Axis (Data): 1 points (KPH)

**Statistics:**
- Min: 102.9980 KPH
- Max: 102.9980 KPH
- Avg: 102.9980 KPH
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 |

### 261. COLD 2-3 Upshift - TPS Vs KPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (KPH)
- Z-Axis (Data): 1 points (KPH)

**Statistics:**
- Min: 102.9980 KPH
- Max: 102.9980 KPH
- Avg: 102.9980 KPH
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 92.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 |

### 262. COLD 3-4 Upshift - TPS Vs KPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (KPH)
- Z-Axis (Data): 1 points (KPH)

**Statistics:**
- Min: 102.9980 KPH
- Max: 102.9980 KPH
- Avg: 102.9980 KPH
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 |

### 263. COLD 2-1 Downshift - TPS Vs KPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (KPH)
- Z-Axis (Data): 1 points (KPH)

**Statistics:**
- Min: 102.9980 KPH
- Max: 102.9980 KPH
- Avg: 102.9980 KPH
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 |

### 264. COLD 3-2 Downshift - TPS Vs KPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (KPH)
- Z-Axis (Data): 1 points (KPH)

**Statistics:**
- Min: 102.9980 KPH
- Max: 102.9980 KPH
- Avg: 102.9980 KPH
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 |

### 265. COLD 4-3 Downshift - TPS Vs KPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 1 points (KPH)
- Z-Axis (Data): 1 points (KPH)

**Statistics:**
- Min: 102.9980 KPH
- Max: 102.9980 KPH
- Avg: 102.9980 KPH
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 | 103.00 |

### 266. 1-2-3 Gear Engine Braking Force Motor Pressure Vs KPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 3 points (GEAR)
- Y-Axis: 17 points (KPH)
- Z-Axis (Data): 51 points (PSI)

**Statistics:**
- Min: 0.0000 PSI
- Max: 90.0000 PSI
- Avg: 40.9020 PSI
- Dimensions: 17 × 3

**Full Data Table** (17 rows × 3 cols):

| Row | C0 | C1 | C2 |
|-----|------|------|------|
| 0.00 | 0.00 | 0.00 | 19.00 |
| 13.00 | 28.00 | 28.00 | 37.00 |
| 26.00 | 46.00 | 56.00 | 90.00 |
| 39.00 | 90.00 | 90.00 | 90.00 |
| 51.00 | 90.00 | 90.00 | 90.00 |
| 64.00 | 90.00 | 90.00 | 0.00 |
| 77.00 | 0.00 | 19.00 | 28.00 |
| 90.00 | 37.00 | 46.00 | 56.00 |
| 103.00 | 66.00 | 90.00 | 90.00 |
| 116.00 | 90.00 | 90.00 | 90.00 |
| 129.00 | 90.00 | 90.00 | 90.00 |
| 142.00 | 90.00 | 0.00 | 0.00 |
| 154.00 | 0.00 | 0.00 | 0.00 |
| 167.00 | 0.00 | 0.00 | 0.00 |
| 180.00 | 0.00 | 0.00 | 0.00 |
| 193.00 | 0.00 | 0.00 | 0.00 |
| 206.00 | 0.00 | 0.00 | 0.00 |

### 267. Garage Shift - Drive - Force Motor Pressure PSI - Trans Temp Vs RPM

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (RPM)
- Y-Axis: 8 points (DEG/C)
- Z-Axis (Data): 136 points (PSI)

**Statistics:**
- Min: 0.0000 PSI
- Max: 25.0000 PSI
- Avg: 8.6765 PSI
- Dimensions: 8 × 17

**Full Data Table** (8 rows × 17 cols):

| Y \ X | 0.00 | 128.00 | 256.00 | 384.00 | 512.00 | 640.00 | 768.00 | 896.00 | 1024.00 | 1152.00 | 1280.00 | 1408.00 | 1536.00 | 1664.00 | 1792.00 | 1920.00 | 2048.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| -40.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 |
| -20.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 |
| 0.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 |
| 20.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 |
| 40.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 |
| 60.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 |
| 80.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 |
| 100.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 |

### 268. Garage Shift - Reverse - Force Motor Pressure PSI - Trans Temp Vs RPM

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (RPM)
- Y-Axis: 8 points (DEG/C)
- Z-Axis (Data): 136 points (PSI)

**Statistics:**
- Min: 0.0000 PSI
- Max: 25.0000 PSI
- Avg: 9.0074 PSI
- Dimensions: 8 × 17

**Full Data Table** (8 rows × 17 cols):

| Y \ X | 0.00 | 128.00 | 256.00 | 384.00 | 512.00 | 640.00 | 768.00 | 896.00 | 1024.00 | 1152.00 | 1280.00 | 1408.00 | 1536.00 | 1664.00 | 1792.00 | 1920.00 | 2048.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| -40.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 | 25.00 |
| -20.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 20.00 | 20.00 | 20.00 | 20.00 | 20.00 | 20.00 | 20.00 | 20.00 | 20.00 |
| 0.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 8.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 |
| 20.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 |
| 40.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 |
| 60.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 |
| 80.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 |
| 100.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 |

### 269. Rolling Garage Shift - Force Motor Pressure PSI - MPH Vs TPS

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (%TPS)
- Y-Axis: 5 points (MPH)
- Z-Axis (Data): 85 points (PSI)

**Statistics:**
- Min: 0.0000 PSI
- Max: 0.0000 PSI
- Avg: 0.0000 PSI
- Dimensions: 5 × 17

**Full Data Table** (5 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 4.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 8.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 12.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 16.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 270. 4Th Gear High Speed Lube Pressure Limit Force Motor Pressure Vs Vehicle Speed

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (MPH)
- Y-Axis: 1 points (PSI)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 64.00 | 68.00 | 72.00 | 76.00 | 80.00 | 84.00 | 88.00 | 92.00 | 96.00 | 100.00 | 104.00 | 108.00 | 112.00 | 116.00 | 120.00 | 124.00 | 128.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 271. 5th Gear High Speed Lube Pressure Limit Force Motor Pressure Vs Vehicle Speed

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (MPH)
- Y-Axis: 1 points (PSI)
- Z-Axis (Data): 1 points (PSI)

**Statistics:**
- Min: 0.0000 PSI
- Max: 0.0000 PSI
- Avg: 0.0000 PSI
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 64.00 | 68.00 | 72.00 | 76.00 | 80.00 | 84.00 | 88.00 | 92.00 | 96.00 | 100.00 | 104.00 | 108.00 | 112.00 | 116.00 | 120.00 | 124.00 | 128.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 272. 2nd Gear Temp Pressure Adjust

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (DEG/C)
- Y-Axis: 4 points (%TPS)
- Z-Axis (Data): 68 points (PSI)

**Statistics:**
- Min: -3.0000 PSI
- Max: 11.0000 PSI
- Avg: 0.3824 PSI
- Dimensions: 4 × 17

**Full Data Table** (4 rows × 17 cols):

| Y \ X | -40.00 | -28.00 | -16.00 | -4.00 | 8.00 | 20.00 | 32.00 | 44.00 | 56.00 | 68.00 | 80.00 | 92.00 | 104.00 | 116.00 | 128.00 | 140.00 | 152.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | -3.00 | -3.00 | -3.00 | -3.00 | -3.00 | -3.00 | -2.00 | -1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 1 | -3.00 | -3.00 | -3.00 | -3.00 | -3.00 | -3.00 | -2.00 | -1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 2.00 | 8.00 | 8.00 | 11.00 |
| 2 | -2.00 | -2.00 | -2.00 | -2.00 | -2.00 | -2.00 | -1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 2.00 | 8.00 | 8.00 | 11.00 |
| 3 | -1.00 | -1.00 | -1.00 | -1.00 | -1.00 | -1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 2.00 | 8.00 | 8.00 | 11.00 |

### 273. 3rd Gear Temp Pressure Adjust

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (DEG/C)
- Y-Axis: 4 points (%TPS)
- Z-Axis (Data): 68 points (PSI)

**Statistics:**
- Min: -3.0000 PSI
- Max: 11.0000 PSI
- Avg: 0.2059 PSI
- Dimensions: 4 × 17

**Full Data Table** (4 rows × 17 cols):

| Y \ X | -40.00 | -28.00 | -16.00 | -4.00 | 8.00 | 20.00 | 32.00 | 44.00 | 56.00 | 68.00 | 80.00 | 92.00 | 104.00 | 116.00 | 128.00 | 140.00 | 152.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | -3.00 | -3.00 | -3.00 | -3.00 | -3.00 | -3.00 | -2.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 1 | -3.00 | -3.00 | -3.00 | -3.00 | -3.00 | -3.00 | -2.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 2.00 | 8.00 | 8.00 | 11.00 |
| 2 | -3.00 | -3.00 | -3.00 | -3.00 | -3.00 | -3.00 | -2.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 2.00 | 8.00 | 8.00 | 11.00 |
| 3 | -2.00 | -2.00 | -2.00 | -2.00 | -2.00 | -2.00 | -1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 2.00 | 8.00 | 8.00 | 11.00 |

### 274. 4th Gear Temp Pressure Adjust

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (DEG/C)
- Y-Axis: 4 points (%TPS)
- Z-Axis (Data): 68 points (PSI)

**Statistics:**
- Min: 0.0000 PSI
- Max: 11.0000 PSI
- Avg: 1.2794 PSI
- Dimensions: 4 × 17

**Full Data Table** (4 rows × 17 cols):

| Y \ X | -40.00 | -28.00 | -16.00 | -4.00 | 8.00 | 20.00 | 32.00 | 44.00 | 56.00 | 68.00 | 80.00 | 92.00 | 104.00 | 116.00 | 128.00 | 140.00 | 152.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 2.00 | 8.00 | 8.00 | 11.00 |
| 2 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 2.00 | 8.00 | 8.00 | 11.00 |
| 3 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 2.00 | 8.00 | 8.00 | 11.00 |

### 275. Load-Based Force Motor Pressure - TPS% Vs Speed 0-103 KPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 17 points (KPH)
- Z-Axis (Data): 289 points (PSI)

**Statistics:**
- Min: 0.0000 PSI
- Max: 90.0000 PSI
- Avg: 48.3253 PSI
- Dimensions: 17 × 17

**Full Data Table** (17 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 6.40 | 5.00 | 3.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 12.90 | 10.00 | 5.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 |
| 19.30 | 15.00 | 12.00 | 8.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 |
| 25.70 | 25.00 | 20.00 | 16.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 32.20 | 35.00 | 30.00 | 25.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 |
| 38.60 | 50.00 | 45.00 | 40.00 | 37.00 | 37.00 | 37.00 | 37.00 | 37.00 | 35.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 |
| 45.10 | 60.00 | 50.00 | 47.00 | 44.00 | 44.00 | 44.00 | 44.00 | 44.00 | 42.00 | 40.00 | 40.00 | 40.00 | 40.00 | 40.00 | 40.00 | 40.00 | 40.00 |
| 51.50 | 70.00 | 65.00 | 56.00 | 56.00 | 56.00 | 56.00 | 56.00 | 56.00 | 56.00 | 56.00 | 54.00 | 52.00 | 52.00 | 52.00 | 52.00 | 52.00 | 52.00 |
| 57.90 | 80.00 | 75.00 | 70.00 | 68.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 |
| 64.40 | 90.00 | 85.00 | 80.00 | 78.00 | 73.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 |
| 70.80 | 90.00 | 90.00 | 85.00 | 85.00 | 80.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 |
| 77.20 | 90.00 | 90.00 | 90.00 | 85.00 | 80.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 |
| 83.70 | 90.00 | 90.00 | 90.00 | 90.00 | 85.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 |
| 90.10 | 90.00 | 90.00 | 90.00 | 90.00 | 85.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 |
| 96.60 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 |
| 103.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 |

### 276. Load-Based Force Motor Pressure - TPS% Vs Speed 103-206 KPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 17 points (KPH)
- Z-Axis (Data): 289 points (PSI)

**Statistics:**
- Min: 0.0000 PSI
- Max: 90.0000 PSI
- Avg: 46.2941 PSI
- Dimensions: 17 × 17

**Full Data Table** (17 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 103.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 109.40 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 115.90 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 |
| 122.30 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 | 4.00 |
| 128.70 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 135.20 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 | 23.00 |
| 141.60 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 |
| 148.10 | 40.00 | 40.00 | 40.00 | 40.00 | 40.00 | 40.00 | 40.00 | 40.00 | 40.00 | 40.00 | 40.00 | 40.00 | 40.00 | 40.00 | 40.00 | 40.00 | 40.00 |
| 154.50 | 52.00 | 52.00 | 52.00 | 52.00 | 52.00 | 52.00 | 52.00 | 52.00 | 52.00 | 52.00 | 52.00 | 52.00 | 52.00 | 52.00 | 52.00 | 52.00 | 52.00 |
| 160.90 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 | 64.00 |
| 167.40 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 | 69.00 |
| 173.80 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 | 74.00 |
| 180.20 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 |
| 186.70 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 |
| 193.10 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 | 83.00 |
| 199.60 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 | 85.00 |
| 206.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 |

### 277. Normal Mode 2-3-4 Gear Pressure Offset - Force Motor Pressure Vs TPS

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 3 points (GEAR)
- Z-Axis (Data): 51 points (PSI)

**Statistics:**
- Min: -5.0000 PSI
- Max: 10.0000 PSI
- Avg: 2.0588 PSI
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.25 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | -3.00 | 0.00 | 0.00 | 5.00 | 10.00 | 9.00 | 4.00 | 7.00 | 5.00 | 6.00 | 6.00 | 5.00 | 5.00 | 5.00 | 4.00 | 3.00 | -1.00 |
| 1 | -3.00 | 0.00 | -2.00 | 0.00 | 1.00 | 2.00 | 3.00 | 3.00 | 1.00 | -5.00 | -3.00 | -3.00 | -3.00 | -3.00 | -3.00 | -1.00 | -5.00 |
| 2 | 0.00 | 0.00 | 3.00 | 4.00 | 4.00 | 6.00 | 3.00 | 2.00 | 2.00 | 3.00 | 4.00 | 5.00 | 5.00 | 5.00 | 5.00 | 5.00 | 0.00 |

### 278. Performance Mode 2-3-4 Gear Pressure Offset - Force Motor Pressure Vs TPS

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (TPS%)
- Y-Axis: 3 points (GEAR)
- Z-Axis (Data): 51 points (PSI)

**Statistics:**
- Min: -3.0000 PSI
- Max: 15.0000 PSI
- Avg: 5.8824 PSI
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.25 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | -3.00 | 1.00 | 3.00 | 9.00 | 15.00 | 15.00 | 10.00 | 12.00 | 10.00 | 12.00 | 13.00 | 14.00 | 12.00 | 10.00 | 7.00 | 5.00 | 0.00 |
| 1 | -3.00 | 0.00 | -1.00 | 2.00 | 4.00 | 5.00 | 7.00 | 9.00 | 9.00 | 3.00 | 4.00 | 4.00 | 5.00 | 5.00 | 4.00 | 5.00 | 0.00 |
| 2 | 0.00 | 0.00 | 5.00 | 7.00 | 8.00 | 10.00 | 6.00 | 6.00 | 6.00 | 6.00 | 6.00 | 7.00 | 7.00 | 7.00 | 7.00 | 5.00 | 0.00 |

### 279. 4-3-2-1 Downshift Pressure Mod Normal Mode Force Motor Pressure Vs Vehicle Speed

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (MPH)
- Y-Axis: 3 points (GEAR CHANGE)
- Z-Axis (Data): 51 points (PSI)

**Statistics:**
- Min: -128.0000 PSI
- Max: 0.0000 PSI
- Avg: -11.4510 PSI
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 4.00 | 8.00 | 12.00 | 16.00 | 20.00 | 24.00 | 28.00 | 32.00 | 36.00 | 40.00 | 44.00 | 48.00 | 52.00 | 56.00 | 60.00 | 64.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | -128.00 | 0.00 | -96.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 1 | 0.00 | 0.00 | 0.00 | -100.00 | 0.00 | -96.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 2 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | -68.00 | 0.00 | -96.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 280. 2-3-4 Pressure Offset PSI Vs TPS

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (%TPS)
- Y-Axis: 3 points (GEAR)
- Z-Axis (Data): 51 points (PSI)

**Statistics:**
- Min: 0.0000 PSI
- Max: 0.0000 PSI
- Avg: 0.0000 PSI
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.25 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 2 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 281. 1-2-3-4 Pressure Ramp Delay Time (Normal Mode) Ramp Delay Time Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (%TPS)
- Y-Axis: 3 points (GEAR - SEC)
- Z-Axis (Data): 51 points

**Statistics:**
- Min: 0.0000 
- Max: 0.5000 
- Avg: 0.2667 
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 |
| 1 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 |
| 2 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 282. 1-2-3-4 Pressure Ramp Delay Time (Performance Mode) Ramp Delay Time Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (%TPS)
- Y-Axis: 3 points (GEAR - SEC)
- Z-Axis (Data): 51 points

**Statistics:**
- Min: 0.0000 
- Max: 0.5000 
- Avg: 0.2667 
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 |
| 1 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 |
| 2 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 283. 1-2-3-4 Ramp 1 Pressure Delta (Normal Mode) Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (%TPS)
- Y-Axis: 3 points (GEAR-PSI/SEC)
- Z-Axis (Data): 51 points

**Statistics:**
- Min: 32.0000 
- Max: 38.2500 
- Avg: 32.2451 
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 |
| 1 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 38.25 | 38.25 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 |
| 2 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 |

### 284. 1-2-3-4 Ramp 1 Pressure Delta (Performance Mode) Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (%TPS)
- Y-Axis: 3 points (GEAR-PSI/SEC)
- Z-Axis (Data): 51 points

**Statistics:**
- Min: 32.0000 
- Max: 52.0000 
- Avg: 33.2745 
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 44.50 | 52.00 | 52.00 | 44.50 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 |
| 1 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 |
| 2 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 |

### 285. 1-2-3-4 Ramp 2 Pressure Delta (Normal Mode) Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (%TPS)
- Y-Axis: 3 points (GEAR PSI/SEC)
- Z-Axis (Data): 51 points

**Statistics:**
- Min: 32.0000 
- Max: 42.0000 
- Avg: 33.2255 
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 |
| 1 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 38.25 | 38.25 | 42.00 | 42.00 | 42.00 | 42.00 | 42.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 |
| 2 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 |

### 286. 1-2-3-4 Ramp 2 Pressure Delta (Performance Mode) Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (%TPS)
- Y-Axis: 3 points (GEAR PSI/SEC)
- Z-Axis (Data): 51 points

**Statistics:**
- Min: 32.0000 
- Max: 44.5000 
- Avg: 33.5196 
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 |
| 1 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 38.25 | 44.50 | 44.50 | 42.00 | 42.00 | 42.00 | 42.00 | 38.25 | 32.00 | 32.00 | 32.00 | 32.00 |
| 2 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 | 32.00 |

### 287. Power Enrichment Modification Force Motor Pressure Vs Engine Speed

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (RPM)
- Y-Axis: 1 points (PSI)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 512.00 | 1024.00 | 1536.00 | 2048.00 | 2560.00 | 3072.00 | 3584.00 | 4096.00 | 4608.00 | 5120.00 | 5632.00 | 6144.00 | 6656.00 | 7168.00 | 7680.00 | 8192.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 288. 1-2-3-4 Pressure Ramp 2 Time Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (%TPS)
- Y-Axis: 3 points (GEAR CHANGE SEC)
- Z-Axis (Data): 51 points

**Statistics:**
- Min: 0.0000 
- Max: 0.7500 
- Avg: 0.2216 
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 |
| 1 | 0.00 | 0.00 | 0.00 | 0.75 | 0.75 | 0.75 | 0.75 | 0.50 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 | 0.30 |
| 2 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 289. 1-2-3-4 Pressure Ramp 1 Extention Time (Delay Time For Ramp 2) (Normal Mode) Delay Time Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (%TPS)
- Y-Axis: 3 points (GEAR CHANGE SEC)
- Z-Axis (Data): 51 points

**Statistics:**
- Min: 0.0000 
- Max: 0.2500 
- Avg: 0.0490 
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 |
| 1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 2 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 290. 1-2-3-4 Pressure Ramp 1 Extention Time (Delay Time Of Ramp 2) (Performance Mode) Ramp Delay Time Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (%TPS)
- Y-Axis: 3 points (GEAR CHANGE SEC)
- Z-Axis (Data): 51 points

**Statistics:**
- Min: 0.0000 
- Max: 0.2500 
- Avg: 0.0490 
- Dimensions: 3 × 17

**Full Data Table** (3 rows × 17 cols):

| Y \ X | 0.00 | 6.25 | 12.50 | 18.75 | 25.00 | 31.25 | 37.50 | 43.75 | 50.00 | 56.25 | 62.50 | 68.75 | 75.00 | 81.25 | 87.50 | 93.75 | 100.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 |
| 1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 2 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 291. Altitude Compensation Factor Used For Modified Base Pressure. Factor Vs Baro & Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (DEG)
- Y-Axis: 17 points (KPA)
- Z-Axis (Data): 289 points (FACTOR)

**Statistics:**
- Min: 0.6562 FACTOR
- Max: 1.0000 FACTOR
- Avg: 0.9327 FACTOR
- Dimensions: 17 × 17

**Full Data Table** (17 rows × 17 cols):

| Row | C0 | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 | C13 | C14 | C15 | C16 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 50.00 | 0.66 | 0.66 | 0.66 | 0.70 | 0.80 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 |
| 54.00 | 0.66 | 0.66 | 0.66 | 0.70 | 0.80 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 |
| 58.00 | 0.66 | 0.66 | 0.66 | 0.70 | 0.80 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 | 0.92 |
| 62.00 | 0.66 | 0.66 | 0.66 | 0.70 | 0.80 | 0.92 | 0.93 | 0.93 | 0.93 | 0.93 | 0.93 | 0.93 | 0.93 | 0.93 | 0.93 | 0.93 | 0.93 |
| 66.00 | 0.66 | 0.66 | 0.66 | 0.70 | 0.80 | 0.92 | 0.93 | 0.94 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 |
| 70.00 | 0.70 | 0.70 | 0.70 | 0.98 | 0.82 | 0.94 | 0.94 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 |
| 74.00 | 0.74 | 0.74 | 0.74 | 0.77 | 0.85 | 0.95 | 0.95 | 0.95 | 0.96 | 0.96 | 0.96 | 0.96 | 0.96 | 0.96 | 0.96 | 0.96 | 0.96 |
| 78.00 | 0.78 | 0.76 | 0.76 | 0.81 | 0.88 | 0.95 | 0.96 | 0.96 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 |
| 82.00 | 0.83 | 0.83 | 0.83 | 0.85 | 0.90 | 0.96 | 0.97 | 0.97 | 0.98 | 0.98 | 0.98 | 0.98 | 0.98 | 0.98 | 0.98 | 0.98 | 0.98 |
| 86.00 | 0.87 | 0.87 | 0.87 | 0.88 | 0.92 | 0.97 | 0.98 | 0.98 | 0.98 | 0.98 | 0.98 | 0.98 | 0.98 | 0.98 | 0.98 | 0.98 | 0.98 |
| 90.00 | 0.91 | 0.91 | 0.91 | 0.92 | 0.95 | 0.98 | 0.98 | 0.98 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 |
| 94.00 | 0.95 | 0.95 | 0.95 | 0.96 | 0.98 | 0.99 | 0.99 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 98.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 102.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 106.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 110.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| 114.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

### 292. Barometric Pressure Vs AD Counts Lookup Table

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (A/D COUNTS)
- Y-Axis: 1 points (KPA)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 21.8750 
- Max: 104.6875 
- Avg: 67.5551 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 16.00 | 32.00 | 48.00 | 64.00 | 80.00 | 96.00 | 112.00 | 128.00 | 144.00 | 160.00 | 176.00 | 192.00 | 208.00 | 224.00 | 240.00 | 255.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 100.00 | 100.00 | 21.88 | 27.34 | 33.59 | 39.84 | 45.31 | 51.56 | 57.03 | 63.28 | 69.53 | 75.00 | 81.25 | 86.72 | 92.97 | 98.44 | 104.69 |

### 293. 3-2 Downshift Base Pressure @ Low Vehicle Speed Vs Gearbox Torque Or Throttle Mod & D32 Vehicle Speed Or Throttle Mod

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (MPH)
- Y-Axis: 9 points (FT.LBS OR %)
- Z-Axis (Data): 153 points (PSI)

**Statistics:**
- Min: 0.0000 PSI
- Max: 70.0000 PSI
- Avg: 42.7255 PSI
- Dimensions: 9 × 17

**Full Data Table** (9 rows × 17 cols):

| Y \ X | 6.00 | 9.00 | 12.00 | 15.00 | 18.00 | 21.00 | 24.00 | 27.00 | 30.00 | 33.00 | 36.00 | 39.00 | 42.00 | 45.00 | 48.00 | 51.00 | 54.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 1 | 50.00 | 50.00 | 50.00 | 60.00 | 55.00 | 55.00 | 55.00 | 50.00 | 46.00 | 42.00 | 37.00 | 33.00 | 33.00 | 33.00 | 33.00 | 33.00 | 33.00 |
| 2 | 50.00 | 50.00 | 50.00 | 60.00 | 55.00 | 55.00 | 55.00 | 50.00 | 46.00 | 42.00 | 37.00 | 33.00 | 33.00 | 33.00 | 33.00 | 33.00 | 33.00 |
| 3 | 60.00 | 60.00 | 60.00 | 70.00 | 55.00 | 55.00 | 55.00 | 50.00 | 46.00 | 42.00 | 37.00 | 33.00 | 33.00 | 33.00 | 33.00 | 33.00 | 33.00 |
| 4 | 60.00 | 60.00 | 60.00 | 70.00 | 65.00 | 65.00 | 65.00 | 60.00 | 50.00 | 42.00 | 39.00 | 33.00 | 33.00 | 33.00 | 33.00 | 33.00 | 33.00 |
| 5 | 60.00 | 60.00 | 60.00 | 70.00 | 70.00 | 70.00 | 65.00 | 60.00 | 50.00 | 46.00 | 39.00 | 33.00 | 33.00 | 33.00 | 33.00 | 33.00 | 33.00 |
| 6 | 60.00 | 60.00 | 60.00 | 70.00 | 70.00 | 70.00 | 65.00 | 60.00 | 50.00 | 46.00 | 39.00 | 33.00 | 33.00 | 33.00 | 33.00 | 33.00 | 33.00 |
| 7 | 60.00 | 60.00 | 60.00 | 70.00 | 70.00 | 70.00 | 70.00 | 60.00 | 50.00 | 46.00 | 39.00 | 33.00 | 33.00 | 33.00 | 33.00 | 33.00 | 33.00 |
| 8 | 60.00 | 60.00 | 60.00 | 70.00 | 70.00 | 70.00 | 70.00 | 60.00 | 50.00 | 50.00 | 46.00 | 39.00 | 33.00 | 33.00 | 33.00 | 33.00 | 33.00 |

### 294. 3-2 Downshift Base Pressure @ High Vehicle Speed Vs Gearbox Torque Or Throttle Mod & D32 Vehicle Speed Or Throttle Mod

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (MPH)
- Y-Axis: 9 points (FT.LBS OR %)
- Z-Axis (Data): 153 points (PSI)

**Statistics:**
- Min: 50.0000 PSI
- Max: 86.0000 PSI
- Avg: 66.9346 PSI
- Dimensions: 9 × 17

**Full Data Table** (9 rows × 17 cols):

| Y \ X | 32.00 | 35.00 | 38.00 | 41.00 | 44.00 | 47.00 | 50.00 | 53.00 | 56.00 | 59.00 | 62.00 | 65.00 | 68.00 | 71.00 | 74.00 | 77.00 | 80.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0 | 86.00 | 86.00 | 86.00 | 86.00 | 86.00 | 86.00 | 82.00 | 77.00 | 70.00 | 65.00 | 60.00 | 60.00 | 60.00 | 60.00 | 60.00 | 60.00 | 60.00 |
| 1 | 86.00 | 86.00 | 86.00 | 86.00 | 86.00 | 86.00 | 82.00 | 77.00 | 70.00 | 65.00 | 60.00 | 60.00 | 60.00 | 60.00 | 60.00 | 60.00 | 60.00 |
| 2 | 86.00 | 86.00 | 86.00 | 86.00 | 86.00 | 86.00 | 82.00 | 77.00 | 70.00 | 65.00 | 60.00 | 60.00 | 60.00 | 60.00 | 60.00 | 60.00 | 60.00 |
| 3 | 82.00 | 82.00 | 82.00 | 82.00 | 82.00 | 82.00 | 77.00 | 70.00 | 65.00 | 60.00 | 55.00 | 55.00 | 55.00 | 55.00 | 55.00 | 55.00 | 55.00 |
| 4 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 70.00 | 65.00 | 60.00 | 60.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 |
| 5 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 70.00 | 65.00 | 60.00 | 55.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 |
| 6 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 70.00 | 65.00 | 60.00 | 55.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 |
| 7 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 77.00 | 70.00 | 65.00 | 60.00 | 60.00 | 60.00 | 55.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 |
| 8 | 82.00 | 82.00 | 82.00 | 82.00 | 82.00 | 82.00 | 77.00 | 70.00 | 65.00 | 60.00 | 60.00 | 55.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 |

### 295. First Pressure Control Solenoid Closed Loop Gain Table

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 8 points (DEG/C)
- Y-Axis: 1 points (DC/AMP)
- Z-Axis (Data): 1 points (DC/AMP)

**Statistics:**
- Min: 18.4375 DC/AMP
- Max: 25.0000 DC/AMP
- Avg: 20.5078 DC/AMP
- Dimensions: 1 × 8

**Full Data Table** (1 rows × 8 cols):

| Y \ X | -40.00 | -16.00 | 8.00 | 32.00 | 56.00 | 80.00 | 104.00 | 128.00 |
|-----|------|------|------|------|------|------|------|------|
| 0.00 | 25.00 | 22.81 | 21.25 | 20.62 | 19.06 | 18.44 | 18.44 | 18.44 |

### 296. Second Pressure Control Solenoid Closed Loop Gain Table

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 8 points (DEG/C)
- Y-Axis: 1 points (DC/AMP)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 5.9375 
- Max: 14.6875 
- Avg: 9.6094 
- Dimensions: 1 × 8

**Full Data Table** (1 rows × 8 cols):

| Y \ X | -40.00 | -16.00 | 8.00 | 32.00 | 56.00 | 80.00 | 104.00 | 128.00 |
|-----|------|------|------|------|------|------|------|------|
| 0.00 | 14.69 | 12.50 | 10.94 | 10.00 | 8.44 | 7.50 | 6.88 | 5.94 |

### 297. Pressure Control Solenoid - AMPS Vs Positive Pressure & Trans Temp

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (PSI)
- Y-Axis: 17 points (DEG/C)
- Z-Axis (Data): 289 points (AMPS)

**Statistics:**
- Min: 0.1225 AMPS
- Max: 1.0833 AMPS
- Avg: 0.6326 AMPS
- Dimensions: 17 × 17

**Full Data Table** (17 rows × 17 cols):

| Y \ X | 0.00 | 6.00 | 12.00 | 18.00 | 24.00 | 30.00 | 36.00 | 42.00 | 48.00 | 54.00 | 60.00 | 66.00 | 72.00 | 78.00 | 84.00 | 90.00 | 96.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| -40.00 | 1.08 | 0.88 | 0.88 | 0.88 | 0.84 | 0.80 | 0.76 | 0.72 | 0.71 | 0.63 | 0.60 | 0.55 | 0.48 | 0.41 | 0.33 | 0.22 | 0.22 |
| -28.00 | 1.08 | 0.92 | 0.90 | 0.88 | 0.84 | 0.80 | 0.76 | 0.72 | 0.68 | 0.64 | 0.59 | 0.55 | 0.47 | 0.41 | 0.33 | 0.22 | 0.22 |
| -16.00 | 1.08 | 0.92 | 0.90 | 0.88 | 0.84 | 0.80 | 0.78 | 0.75 | 0.71 | 0.64 | 0.60 | 0.55 | 0.48 | 0.43 | 0.36 | 0.25 | 0.25 |
| -4.00 | 1.08 | 0.92 | 0.90 | 0.88 | 0.84 | 0.80 | 0.78 | 0.75 | 0.71 | 0.64 | 0.60 | 0.55 | 0.48 | 0.43 | 0.36 | 0.24 | 0.24 |
| 8.00 | 1.08 | 0.94 | 0.90 | 0.88 | 0.84 | 0.80 | 0.76 | 0.72 | 0.68 | 0.64 | 0.59 | 0.55 | 0.47 | 0.41 | 0.33 | 0.22 | 0.22 |
| 20.00 | 1.08 | 0.94 | 0.90 | 0.88 | 0.84 | 0.80 | 0.76 | 0.72 | 0.68 | 0.63 | 0.59 | 0.52 | 0.47 | 0.40 | 0.32 | 0.20 | 0.20 |
| 32.00 | 1.08 | 0.94 | 0.90 | 0.86 | 0.82 | 0.80 | 0.76 | 0.72 | 0.68 | 0.63 | 0.59 | 0.52 | 0.44 | 0.40 | 0.29 | 0.18 | 0.18 |
| 44.00 | 1.08 | 0.92 | 0.90 | 0.86 | 0.82 | 0.78 | 0.76 | 0.71 | 0.67 | 0.63 | 0.56 | 0.51 | 0.44 | 0.37 | 0.29 | 0.16 | 0.16 |
| 56.00 | 1.08 | 0.92 | 0.90 | 0.86 | 0.82 | 0.78 | 0.75 | 0.71 | 0.67 | 0.63 | 0.56 | 0.51 | 0.44 | 0.37 | 0.29 | 0.14 | 0.14 |
| 68.00 | 1.08 | 0.92 | 0.90 | 0.86 | 0.82 | 0.78 | 0.75 | 0.71 | 0.67 | 0.63 | 0.56 | 0.51 | 0.44 | 0.37 | 0.29 | 0.14 | 0.14 |
| 80.00 | 1.08 | 0.92 | 0.90 | 0.86 | 0.82 | 0.78 | 0.75 | 0.71 | 0.67 | 0.63 | 0.56 | 0.51 | 0.44 | 0.37 | 0.28 | 0.14 | 0.14 |
| 92.00 | 1.08 | 0.92 | 0.88 | 0.86 | 0.82 | 0.78 | 0.75 | 0.71 | 0.67 | 0.63 | 0.56 | 0.51 | 0.44 | 0.37 | 0.28 | 0.14 | 0.14 |
| 104.00 | 1.08 | 0.92 | 0.88 | 0.86 | 0.82 | 0.78 | 0.75 | 0.71 | 0.67 | 0.63 | 0.56 | 0.51 | 0.44 | 0.37 | 0.28 | 0.14 | 0.14 |
| 116.00 | 1.08 | 0.92 | 0.88 | 0.86 | 0.82 | 0.78 | 0.75 | 0.71 | 0.67 | 0.63 | 0.56 | 0.51 | 0.44 | 0.37 | 0.28 | 0.14 | 0.14 |
| 128.00 | 1.08 | 0.92 | 0.88 | 0.86 | 0.82 | 0.78 | 0.75 | 0.71 | 0.67 | 0.63 | 0.56 | 0.51 | 0.44 | 0.37 | 0.28 | 0.14 | 0.14 |
| 140.00 | 1.08 | 0.92 | 0.88 | 0.84 | 0.82 | 0.78 | 0.75 | 0.71 | 0.67 | 0.60 | 0.56 | 0.51 | 0.44 | 0.37 | 0.28 | 0.14 | 0.14 |
| 152.00 | 1.08 | 0.92 | 0.88 | 0.84 | 0.82 | 0.78 | 0.75 | 0.71 | 0.67 | 0.60 | 0.56 | 0.51 | 0.44 | 0.37 | 0.28 | 0.12 | 0.12 |

### 298. Pressure Control Solenoid - AMPS Vs Negative Pressure & Trans Temp

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (PSI)
- Y-Axis: 17 points (DEG/C)
- Z-Axis (Data): 289 points (AMPS)

**Statistics:**
- Min: 0.1225 AMPS
- Max: 1.0833 AMPS
- Avg: 0.6326 AMPS
- Dimensions: 17 × 17

**Full Data Table** (17 rows × 17 cols):

| Y \ X | 0.00 | 6.00 | 12.00 | 18.00 | 24.00 | 30.00 | 36.00 | 42.00 | 48.00 | 54.00 | 60.00 | 66.00 | 72.00 | 78.00 | 84.00 | 90.00 | 96.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| -40.00 | 1.08 | 0.88 | 0.88 | 0.88 | 0.84 | 0.80 | 0.76 | 0.72 | 0.71 | 0.63 | 0.60 | 0.55 | 0.48 | 0.41 | 0.33 | 0.22 | 0.22 |
| -28.00 | 1.08 | 0.92 | 0.90 | 0.88 | 0.84 | 0.80 | 0.76 | 0.72 | 0.68 | 0.64 | 0.59 | 0.55 | 0.47 | 0.41 | 0.33 | 0.22 | 0.22 |
| -16.00 | 1.08 | 0.92 | 0.90 | 0.88 | 0.84 | 0.80 | 0.78 | 0.75 | 0.71 | 0.64 | 0.60 | 0.55 | 0.48 | 0.43 | 0.36 | 0.25 | 0.25 |
| -4.00 | 1.08 | 0.92 | 0.90 | 0.88 | 0.84 | 0.80 | 0.78 | 0.75 | 0.71 | 0.64 | 0.60 | 0.55 | 0.48 | 0.43 | 0.36 | 0.24 | 0.24 |
| 8.00 | 1.08 | 0.94 | 0.90 | 0.88 | 0.84 | 0.80 | 0.76 | 0.72 | 0.68 | 0.64 | 0.59 | 0.55 | 0.47 | 0.41 | 0.33 | 0.22 | 0.22 |
| 20.00 | 1.08 | 0.94 | 0.90 | 0.88 | 0.84 | 0.80 | 0.76 | 0.72 | 0.68 | 0.63 | 0.59 | 0.52 | 0.47 | 0.40 | 0.32 | 0.20 | 0.20 |
| 32.00 | 1.08 | 0.94 | 0.90 | 0.86 | 0.82 | 0.80 | 0.76 | 0.72 | 0.68 | 0.63 | 0.59 | 0.52 | 0.44 | 0.40 | 0.29 | 0.18 | 0.18 |
| 44.00 | 1.08 | 0.92 | 0.90 | 0.86 | 0.82 | 0.78 | 0.76 | 0.71 | 0.67 | 0.63 | 0.56 | 0.51 | 0.44 | 0.37 | 0.29 | 0.16 | 0.16 |
| 56.00 | 1.08 | 0.92 | 0.90 | 0.86 | 0.82 | 0.78 | 0.75 | 0.71 | 0.67 | 0.63 | 0.56 | 0.51 | 0.44 | 0.37 | 0.29 | 0.14 | 0.14 |
| 68.00 | 1.08 | 0.92 | 0.90 | 0.86 | 0.82 | 0.78 | 0.75 | 0.71 | 0.67 | 0.63 | 0.56 | 0.51 | 0.44 | 0.37 | 0.29 | 0.14 | 0.14 |
| 80.00 | 1.08 | 0.92 | 0.90 | 0.86 | 0.82 | 0.78 | 0.75 | 0.71 | 0.67 | 0.63 | 0.56 | 0.51 | 0.44 | 0.37 | 0.28 | 0.14 | 0.14 |
| 92.00 | 1.08 | 0.92 | 0.88 | 0.86 | 0.82 | 0.78 | 0.75 | 0.71 | 0.67 | 0.63 | 0.56 | 0.51 | 0.44 | 0.37 | 0.28 | 0.14 | 0.14 |
| 104.00 | 1.08 | 0.92 | 0.88 | 0.86 | 0.82 | 0.78 | 0.75 | 0.71 | 0.67 | 0.63 | 0.56 | 0.51 | 0.44 | 0.37 | 0.28 | 0.14 | 0.14 |
| 116.00 | 1.08 | 0.92 | 0.88 | 0.86 | 0.82 | 0.78 | 0.75 | 0.71 | 0.67 | 0.63 | 0.56 | 0.51 | 0.44 | 0.37 | 0.28 | 0.14 | 0.14 |
| 128.00 | 1.08 | 0.92 | 0.88 | 0.86 | 0.82 | 0.78 | 0.75 | 0.71 | 0.67 | 0.63 | 0.56 | 0.51 | 0.44 | 0.37 | 0.28 | 0.14 | 0.14 |
| 140.00 | 1.08 | 0.92 | 0.88 | 0.84 | 0.82 | 0.78 | 0.75 | 0.71 | 0.67 | 0.60 | 0.56 | 0.51 | 0.44 | 0.37 | 0.28 | 0.14 | 0.14 |
| 152.00 | 1.08 | 0.92 | 0.88 | 0.84 | 0.82 | 0.78 | 0.75 | 0.71 | 0.67 | 0.60 | 0.56 | 0.51 | 0.44 | 0.37 | 0.28 | 0.12 | 0.12 |

### 299. Delta Pressure Vs Transmission Temperature

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 17 points (DEG/C)
- Y-Axis: 1 points (PSI)
- Z-Axis (Data): 1 points (PSI)

**Statistics:**
- Min: 1.0000 PSI
- Max: 1.0000 PSI
- Avg: 1.0000 PSI
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | -40.00 | -36.00 | -32.00 | -28.00 | -24.00 | -20.00 | -16.00 | -12.00 | -8.00 | -4.00 | 0.00 | 4.00 | 8.00 | 12.00 | 16.00 | 20.00 | 24.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

### 300. Interactive Heavy Purge - Maximum Duty Cycle Vs Airflow Or Cylair

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (DC%)
- Y-Axis: 17 points (G/S)
- Z-Axis (Data): 17 points (DC%)

**Statistics:**
- Min: 0.0000 DC%
- Max: 99.6094 DC%
- Avg: 43.9108 DC%
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 0.00 |
| 2.00 | 0.00 |
| 4.00 | 9.38 |
| 6.00 | 16.41 |
| 8.00 | 17.97 |
| 10.00 | 22.66 |
| 12.00 | 27.34 |
| 14.00 | 33.59 |
| 16.00 | 39.06 |
| 18.00 | 44.92 |
| 20.00 | 52.73 |
| 22.00 | 61.33 |
| 24.00 | 68.75 |
| 26.00 | 76.95 |
| 28.00 | 83.98 |
| 30.00 | 91.80 |
| 32.00 | 99.61 |

### 301. Interactive Heavy Purge - Minimum Duty Cycle Vs Airflow Or Cylair

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (DC%)
- Y-Axis: 17 points (G/S)
- Z-Axis (Data): 17 points (DC%)

**Statistics:**
- Min: 0.0000 DC%
- Max: 87.1094 DC%
- Avg: 33.4099 DC%
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 0.00 |
| 2.00 | 0.00 |
| 4.00 | 2.34 |
| 6.00 | 5.47 |
| 8.00 | 7.42 |
| 10.00 | 10.16 |
| 12.00 | 14.84 |
| 14.00 | 21.09 |
| 16.00 | 26.56 |
| 18.00 | 32.42 |
| 20.00 | 40.23 |
| 22.00 | 48.83 |
| 24.00 | 56.25 |
| 26.00 | 64.45 |
| 28.00 | 71.48 |
| 30.00 | 79.30 |
| 32.00 | 87.11 |

### 302. Default Coolant Adjustment Vs Runtime

**Category:** Transmission Calibration

**Axes:**
- X-Axis: 17 points (TIME IN SEC)
- Y-Axis: 1 points (DEG/C)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 20.2500 
- Max: 159.7500 
- Avg: 67.6324 
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 32.00 | 64.00 | 96.00 | 128.00 | 160.00 | 192.00 | 224.00 | 256.00 | 288.00 | 320.00 | 352.00 | 384.00 | 416.00 | 448.00 | 480.00 | 512.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 20.25 | 22.50 | 29.25 | 36.00 | 42.00 | 48.00 | 52.50 | 57.00 | 62.25 | 69.00 | 75.75 | 79.50 | 84.00 | 89.25 | 94.50 | 128.25 | 159.75 |

### 303. TPS Stuck Threshold Vs RPM

**Category:** Transmission Calibration

**Axes:**
- X-Axis: 10 points (RPM)
- Y-Axis: 1 points (TPS%)
- Z-Axis (Data): 1 points (%)

**Statistics:**
- Min: 19.9219 %
- Max: 44.1406 %
- Avg: 33.1641 %
- Dimensions: 1 × 10

**Full Data Table** (1 rows × 10 cols):

| Y \ X | 800.00 | 1200.00 | 1600.00 | 2000.00 | 2400.00 | 2800.00 | 3200.00 | 3600.00 | 4000.00 | 4400.00 |
|-----|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 19.92 | 21.88 | 26.95 | 28.91 | 32.81 | 37.11 | 39.06 | 39.84 | 41.02 | 44.14 |

### 304. Default Airflow Vs RPM & TPS %

**Category:** Transmission Calibration

**Axes:**
- X-Axis: 5 points (TPS %)
- Y-Axis: 7 points (RPM)
- Z-Axis (Data): 35 points (G/S)

**Statistics:**
- Min: 0.0000 G/S
- Max: 140.0000 G/S
- Avg: 32.2286 G/S
- Dimensions: 7 × 5

**Full Data Table** (7 rows × 5 cols):

| Y \ X | 0.00 | 12.50 | 25.00 | 37.50 | 50.00 |
|-----|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 800.00 | 0.00 | 8.00 | 18.00 | 20.00 | 20.00 |
| 1600.00 | 0.00 | 10.00 | 30.00 | 46.00 | 46.00 |
| 2400.00 | 0.00 | 10.00 | 36.00 | 60.00 | 64.00 |
| 3200.00 | 0.00 | 10.00 | 40.00 | 80.00 | 92.00 |
| 4000.00 | 0.00 | 10.00 | 40.00 | 96.00 | 104.00 |
| 4800.00 | 0.00 | 12.00 | 42.00 | 94.00 | 140.00 |

### 305. Default TPS Vs Modified Airflow

**Category:** Transmission Calibration

**Axes:**
- X-Axis: 17 points (GM/SEC MODIFIED AIRFLOW)
- Y-Axis: 1 points (TPS)
- Z-Axis (Data): 1 points (TPS%)

**Statistics:**
- Min: 0.0000 TPS%
- Max: 50.3906 TPS%
- Avg: 35.2482 TPS%
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 8.00 | 16.00 | 24.00 | 32.00 | 40.00 | 48.00 | 56.00 | 64.00 | 72.00 | 80.00 | 88.00 | 96.00 | 104.00 | 112.00 | 120.00 | 128.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 16.41 | 19.92 | 25.00 | 27.34 | 30.86 | 34.38 | 36.72 | 39.06 | 41.02 | 42.19 | 44.53 | 46.09 | 46.88 | 48.83 | 49.61 | 50.39 |

### 306. Catalyst Protection Mode Modifier Of Cat Air Fuel Ratio Vs Airflow

**Category:** Engine/Transmission Diagnostics

**Axes:**
- X-Axis: 33 points (GRAMS/SEC)
- Y-Axis: 1 points (MULT)
- Z-Axis (Data): 1 points

**Statistics:**
- Min: 1.0000 
- Max: 1.4688 
- Avg: 1.1132 
- Dimensions: 1 × 33

**Full Data Table** (1 rows × 33 cols):

| Y \ X | 0.00 | 4.00 | 8.00 | 12.00 | 16.00 | 20.00 | 24.00 | 28.00 | 32.00 | 36.00 | 40.00 | 44.00 | 48.00 | 52.00 | 56.00 | 60.00 | 64.00 | 68.00 | 72.00 | 76.00 | 80.00 | 84.00 | 88.00 | 92.00 | 96.00 | 100.00 | 104.00 | 108.00 | 112.00 | 116.00 | 120.00 | 124.00 | 128.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.04 | 1.08 | 1.11 | 1.13 | 1.16 | 1.19 | 1.21 | 1.24 | 1.27 | 1.30 | 1.34 | 1.37 | 1.40 | 1.43 | 1.47 |

### 307. Abuse Mode Deactivated While In Reverse And Garage Shift Timer Has Exceeded Lookup Value Based On Coolant Temp

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (%)
- Y-Axis: 17 points (DEG/C)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 4.6750 
- Max: 4.6750 
- Avg: 4.6750 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| -40.00 | 4.67 |
| -28.00 | 4.67 |
| -16.00 | 4.67 |
| -4.00 | 4.67 |
| 8.00 | 4.67 |
| 20.00 | 4.67 |
| 32.00 | 4.67 |
| 44.00 | 4.67 |
| 56.00 | 4.67 |
| 68.00 | 4.67 |
| 80.00 | 4.67 |
| 92.00 | 4.67 |
| 104.00 | 4.67 |
| 116.00 | 4.67 |
| 128.00 | 4.67 |
| 140.00 | 4.67 |
| 152.00 | 4.67 |

### 308. Abuse Mode Deactivated While In Drive And Garage Shift Timer Has Exceeded Lookup Value Based On Coolant Temp

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (%)
- Y-Axis: 17 points (DEG/C)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 4.6750 
- Max: 4.6750 
- Avg: 4.6750 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| -40.00 | 4.67 |
| -28.00 | 4.67 |
| -16.00 | 4.67 |
| -4.00 | 4.67 |
| 8.00 | 4.67 |
| 20.00 | 4.67 |
| 32.00 | 4.67 |
| 44.00 | 4.67 |
| 56.00 | 4.67 |
| 68.00 | 4.67 |
| 80.00 | 4.67 |
| 92.00 | 4.67 |
| 104.00 | 4.67 |
| 116.00 | 4.67 |
| 128.00 | 4.67 |
| 140.00 | 4.67 |
| 152.00 | 4.67 |

### 309. Enabling Engine Acceleration Threshold Vs Modified Throttle During 1-2-3-4 Upshift

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 3 points (GEAR CHANGE)
- Y-Axis: 17 points (%TPS)
- Z-Axis (Data): 51 points (DELTA RPM)

**Statistics:**
- Min: -128.0000 DELTA RPM
- Max: -128.0000 DELTA RPM
- Avg: -128.0000 DELTA RPM
- Dimensions: 17 × 3

**Full Data Table** (17 rows × 3 cols):

| Row | C0 | C1 | C2 |
|-----|------|------|------|
| 0.00 | -128.00 | -128.00 | -128.00 |
| 6.00 | -128.00 | -128.00 | -128.00 |
| 12.00 | -128.00 | -128.00 | -128.00 |
| 18.00 | -128.00 | -128.00 | -128.00 |
| 25.00 | -128.00 | -128.00 | -128.00 |
| 31.00 | -128.00 | -128.00 | -128.00 |
| 37.00 | -128.00 | -128.00 | -128.00 |
| 43.00 | -128.00 | -128.00 | -128.00 |
| 50.00 | -128.00 | -128.00 | -128.00 |
| 56.00 | -128.00 | -128.00 | -128.00 |
| 62.00 | -128.00 | -128.00 | -128.00 |
| 68.00 | -128.00 | -128.00 | -128.00 |
| 75.00 | -128.00 | -128.00 | -128.00 |
| 81.00 | -128.00 | -128.00 | -128.00 |
| 87.00 | -128.00 | -128.00 | -128.00 |
| 93.00 | -128.00 | -128.00 | -128.00 |
| 100.00 | -128.00 | -128.00 | -128.00 |

### 310. Disabling Engine Acceleration Threshold Vs Modified Throttle During 1-2-3-4 Upshift

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 3 points (GEAR CHANGE)
- Y-Axis: 17 points (%TPS)
- Z-Axis (Data): 51 points (DELTA RPM)

**Statistics:**
- Min: -128.0000 DELTA RPM
- Max: -128.0000 DELTA RPM
- Avg: -128.0000 DELTA RPM
- Dimensions: 17 × 3

**Full Data Table** (17 rows × 3 cols):

| Row | C0 | C1 | C2 |
|-----|------|------|------|
| 0.00 | -128.00 | -128.00 | -128.00 |
| 6.00 | -128.00 | -128.00 | -128.00 |
| 12.00 | -128.00 | -128.00 | -128.00 |
| 18.00 | -128.00 | -128.00 | -128.00 |
| 25.00 | -128.00 | -128.00 | -128.00 |
| 31.00 | -128.00 | -128.00 | -128.00 |
| 37.00 | -128.00 | -128.00 | -128.00 |
| 43.00 | -128.00 | -128.00 | -128.00 |
| 50.00 | -128.00 | -128.00 | -128.00 |
| 56.00 | -128.00 | -128.00 | -128.00 |
| 62.00 | -128.00 | -128.00 | -128.00 |
| 68.00 | -128.00 | -128.00 | -128.00 |
| 75.00 | -128.00 | -128.00 | -128.00 |
| 81.00 | -128.00 | -128.00 | -128.00 |
| 87.00 | -128.00 | -128.00 | -128.00 |
| 93.00 | -128.00 | -128.00 | -128.00 |
| 100.00 | -128.00 | -128.00 | -128.00 |

### 311. Time Of The Phase 'A' Of A Torque Reduction During 1-2 Upshift Time Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (SEC)
- Y-Axis: 17 points (%TPS)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 0.00 |
| 6.00 | 0.00 |
| 12.00 | 0.00 |
| 18.00 | 0.00 |
| 25.00 | 0.00 |
| 31.00 | 0.00 |
| 37.00 | 0.00 |
| 43.00 | 0.00 |
| 50.00 | 0.00 |
| 56.00 | 0.00 |
| 62.00 | 0.00 |
| 68.00 | 0.00 |
| 75.00 | 0.00 |
| 81.00 | 0.00 |
| 87.00 | 0.00 |
| 93.00 | 0.00 |
| 100.00 | 0.00 |

### 312. Time Of The Phase 'B' Of A Torque Reduction During 1-2 Upshift Time Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (SEC)
- Y-Axis: 17 points (%TPS)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 0.00 |
| 6.00 | 0.00 |
| 12.00 | 0.00 |
| 18.00 | 0.00 |
| 25.00 | 0.00 |
| 31.00 | 0.00 |
| 37.00 | 0.00 |
| 43.00 | 0.00 |
| 50.00 | 0.00 |
| 56.00 | 0.00 |
| 62.00 | 0.00 |
| 68.00 | 0.00 |
| 75.00 | 0.00 |
| 81.00 | 0.00 |
| 87.00 | 0.00 |
| 93.00 | 0.00 |
| 100.00 | 0.00 |

### 313. Time Of The Phase 'C' Of A Torque Reduction During 1-2 Upshift Time Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (SEC)
- Y-Axis: 17 points (%TPS)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 0.00 |
| 6.00 | 0.00 |
| 12.00 | 0.00 |
| 18.00 | 0.00 |
| 25.00 | 0.00 |
| 31.00 | 0.00 |
| 37.00 | 0.00 |
| 43.00 | 0.00 |
| 50.00 | 0.00 |
| 56.00 | 0.00 |
| 62.00 | 0.00 |
| 68.00 | 0.00 |
| 75.00 | 0.00 |
| 81.00 | 0.00 |
| 87.00 | 0.00 |
| 93.00 | 0.00 |
| 100.00 | 0.00 |

### 314. Time Of The Phase 'D' Of A Torque Reduction During 1-2 Upshift Time Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (SEC)
- Y-Axis: 17 points (%TPS)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 0.00 |
| 6.00 | 0.00 |
| 12.00 | 0.00 |
| 18.00 | 0.00 |
| 25.00 | 0.00 |
| 31.00 | 0.00 |
| 37.00 | 0.00 |
| 43.00 | 0.00 |
| 50.00 | 0.00 |
| 56.00 | 0.00 |
| 62.00 | 0.00 |
| 68.00 | 0.00 |
| 75.00 | 0.00 |
| 81.00 | 0.00 |
| 87.00 | 0.00 |
| 93.00 | 0.00 |
| 100.00 | 0.00 |

### 315. Time Of The Phase 'A' Of A Torque Reduction During 2-3 Upshift Time Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (SEC)
- Y-Axis: 17 points (%TPS)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 0.00 |
| 6.00 | 0.00 |
| 12.00 | 0.00 |
| 18.00 | 0.00 |
| 25.00 | 0.00 |
| 31.00 | 0.00 |
| 37.00 | 0.00 |
| 43.00 | 0.00 |
| 50.00 | 0.00 |
| 56.00 | 0.00 |
| 62.00 | 0.00 |
| 68.00 | 0.00 |
| 75.00 | 0.00 |
| 81.00 | 0.00 |
| 87.00 | 0.00 |
| 93.00 | 0.00 |
| 100.00 | 0.00 |

### 316. Time Of The Phase 'B' Of A Torque Reduction During 2-3 Upshift Time Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (SEC)
- Y-Axis: 17 points (%TPS)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 0.00 |
| 6.00 | 0.00 |
| 12.00 | 0.00 |
| 18.00 | 0.00 |
| 25.00 | 0.00 |
| 31.00 | 0.00 |
| 37.00 | 0.00 |
| 43.00 | 0.00 |
| 50.00 | 0.00 |
| 56.00 | 0.00 |
| 62.00 | 0.00 |
| 68.00 | 0.00 |
| 75.00 | 0.00 |
| 81.00 | 0.00 |
| 87.00 | 0.00 |
| 93.00 | 0.00 |
| 100.00 | 0.00 |

### 317. Time Of The Phase 'C' Of A Torque Reduction During 2-3 Upshift Time Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (SEC)
- Y-Axis: 17 points (%TPS)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 0.00 |
| 6.00 | 0.00 |
| 12.00 | 0.00 |
| 18.00 | 0.00 |
| 25.00 | 0.00 |
| 31.00 | 0.00 |
| 37.00 | 0.00 |
| 43.00 | 0.00 |
| 50.00 | 0.00 |
| 56.00 | 0.00 |
| 62.00 | 0.00 |
| 68.00 | 0.00 |
| 75.00 | 0.00 |
| 81.00 | 0.00 |
| 87.00 | 0.00 |
| 93.00 | 0.00 |
| 100.00 | 0.00 |

### 318. Time Of The Phase 'D' Of A Torque Reduction During 2-3 Upshift Time Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (SEC)
- Y-Axis: 17 points (%TPS)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 0.00 |
| 6.00 | 0.00 |
| 12.00 | 0.00 |
| 18.00 | 0.00 |
| 25.00 | 0.00 |
| 31.00 | 0.00 |
| 37.00 | 0.00 |
| 43.00 | 0.00 |
| 50.00 | 0.00 |
| 56.00 | 0.00 |
| 62.00 | 0.00 |
| 68.00 | 0.00 |
| 75.00 | 0.00 |
| 81.00 | 0.00 |
| 87.00 | 0.00 |
| 93.00 | 0.00 |
| 100.00 | 0.00 |

### 319. Time Of The Phase 'A' Of A Torque Reduction During 3-4 Upshift Time Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (SEC)
- Y-Axis: 17 points (%TPS)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 0.00 |
| 6.00 | 0.00 |
| 12.00 | 0.00 |
| 18.00 | 0.00 |
| 25.00 | 0.00 |
| 31.00 | 0.00 |
| 37.00 | 0.00 |
| 43.00 | 0.00 |
| 50.00 | 0.00 |
| 56.00 | 0.00 |
| 62.00 | 0.00 |
| 68.00 | 0.00 |
| 75.00 | 0.00 |
| 81.00 | 0.00 |
| 87.00 | 0.00 |
| 93.00 | 0.00 |
| 100.00 | 0.00 |

### 320. Time Of The Phase 'B' Of A Torque Reduction During 3-4 Upshift Time Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (SEC)
- Y-Axis: 17 points (%TPS)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 0.00 |
| 6.00 | 0.00 |
| 12.00 | 0.00 |
| 18.00 | 0.00 |
| 25.00 | 0.00 |
| 31.00 | 0.00 |
| 37.00 | 0.00 |
| 43.00 | 0.00 |
| 50.00 | 0.00 |
| 56.00 | 0.00 |
| 62.00 | 0.00 |
| 68.00 | 0.00 |
| 75.00 | 0.00 |
| 81.00 | 0.00 |
| 87.00 | 0.00 |
| 93.00 | 0.00 |
| 100.00 | 0.00 |

### 321. Time Of The Phase 'C' Of A Torque Reduction During 3-4 Upshift Time Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (SEC)
- Y-Axis: 17 points (%TPS)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 0.00 |
| 6.00 | 0.00 |
| 12.00 | 0.00 |
| 18.00 | 0.00 |
| 25.00 | 0.00 |
| 31.00 | 0.00 |
| 37.00 | 0.00 |
| 43.00 | 0.00 |
| 50.00 | 0.00 |
| 56.00 | 0.00 |
| 62.00 | 0.00 |
| 68.00 | 0.00 |
| 75.00 | 0.00 |
| 81.00 | 0.00 |
| 87.00 | 0.00 |
| 93.00 | 0.00 |
| 100.00 | 0.00 |

### 322. Time Of The Phase 'D' Of A Torque Reduction During 3-4 Upshift Time Vs Modified Throttle

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (SEC)
- Y-Axis: 17 points (%TPS)
- Z-Axis (Data): 17 points

**Statistics:**
- Min: 0.0000 
- Max: 0.0000 
- Avg: 0.0000 
- Dimensions: 17 × 1

**Full Data Table** (17 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 0.00 | 0.00 |
| 6.00 | 0.00 |
| 12.00 | 0.00 |
| 18.00 | 0.00 |
| 25.00 | 0.00 |
| 31.00 | 0.00 |
| 37.00 | 0.00 |
| 43.00 | 0.00 |
| 50.00 | 0.00 |
| 56.00 | 0.00 |
| 62.00 | 0.00 |
| 68.00 | 0.00 |
| 75.00 | 0.00 |
| 81.00 | 0.00 |
| 87.00 | 0.00 |
| 93.00 | 0.00 |
| 100.00 | 0.00 |

### 323. Higher Vehicle Speed Engine Acceleration Threshold For Flare Detection Vs MPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (RPM/SC)
- Y-Axis: 6 points (MPH)
- Z-Axis (Data): 6 points

**Statistics:**
- Min: -28914.0000 
- Max: -24620.0000 
- Avg: -27501.9167 
- Dimensions: 6 × 1

**Full Data Table** (6 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 44.00 | -24620.00 |
| 78.50 | -27628.00 |
| 113.00 | -27628.00 |
| 147.50 | -27885.75 |
| 182.00 | -28335.75 |
| 216.50 | -28914.00 |

### 324. Lower Vehicle Speed Engine Acceleration Threshold For Flare Detection Vs MPH

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (RPM/SC)
- Y-Axis: 6 points (MPH)
- Z-Axis (Data): 6 points

**Statistics:**
- Min: -29555.5000 
- Max: -27628.0000 
- Avg: -28570.5833 
- Dimensions: 6 × 1

**Full Data Table** (6 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 32.50 | -29427.50 |
| 62.50 | -29555.50 |
| 92.50 | -29555.50 |
| 122.50 | -27628.00 |
| 152.50 | -27628.00 |
| 182.50 | -27629.00 |

### 325. 3-2 Downshift Pressure Mod Vs Transmission Temperature

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (PSI)
- Y-Axis: 9 points (DEG/C)
- Z-Axis (Data): 9 points

**Statistics:**
- Min: 0.0000 
- Max: 20.0000 
- Avg: 7.3333 
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| -34.00 | 20.00 |
| -12.00 | 15.00 |
| 10.00 | 10.00 |
| 32.00 | 5.00 |
| 54.00 | 0.00 |
| 76.00 | 0.00 |
| 98.00 | 0.00 |
| 120.00 | 6.00 |
| 142.00 | 10.00 |

### 326. 3-2 Downshift Gain Vs Lower Vehicle Speed

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (GAIN)
- Y-Axis: 9 points (MPH)
- Z-Axis (Data): 9 points

**Statistics:**
- Min: 1.0000 
- Max: 1.0000 
- Avg: 1.0000 
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 6.00 | 1.00 |
| 12.00 | 1.00 |
| 18.00 | 1.00 |
| 24.00 | 1.00 |
| 30.00 | 1.00 |
| 36.00 | 1.00 |
| 42.00 | 1.00 |
| 48.00 | 1.00 |
| 54.00 | 1.00 |

### 327. 3-2 Downshift Gain Vs Higher Vehicle Speed

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 1 points (GAIN)
- Y-Axis: 9 points (MPH)
- Z-Axis (Data): 9 points

**Statistics:**
- Min: 1.0000 
- Max: 1.0000 
- Avg: 1.0000 
- Dimensions: 9 × 1

**Full Data Table** (9 rows × 1 cols):

| Y \ X | 0.00 |
|-----|------|
| 32.00 | 1.00 |
| 38.00 | 1.00 |
| 44.00 | 1.00 |
| 50.00 | 1.00 |
| 56.00 | 1.00 |
| 62.00 | 1.00 |
| 68.00 | 1.00 |
| 74.00 | 1.00 |
| 80.00 | 1.00 |

### 328. 3-2 Engine Speed Modifier (Added To 3-2 Downshift Pressure At Lower Vehicle Speeds) Vs D32NE & D32VSPD

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 7 points (MPH)
- Y-Axis: 10 points (RPM)
- Z-Axis (Data): 70 points (PSI)

**Statistics:**
- Min: -128.0000 PSI
- Max: 6.0000 PSI
- Avg: -3.9000 PSI
- Dimensions: 10 × 7

**Full Data Table** (10 rows × 7 cols):

| Y \ X | 6.00 | 14.00 | 22.00 | 30.00 | 38.00 | 46.00 | 54.00 |
|-----|------|------|------|------|------|------|------|
| 500.00 | -128.00 | -116.00 | -121.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 756.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 1012.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 4.00 |
| 1268.00 | 4.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 6.00 |
| 1524.00 | 6.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 1780.00 | 6.00 | 6.00 | 6.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 2036.00 | 6.00 | 6.00 | 6.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 2292.00 | 6.00 | 6.00 | 6.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 2548.00 | 6.00 | 6.00 | 6.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 2804.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 329. 3-2 Engine Speed Modifier (Added To 3-2 Downshift Pressure At Lower Vehicle Speeds) Vs D32NE & D32VSPD

**Category:** Transmission Diagnostics

**Axes:**
- X-Axis: 7 points (MPH)
- Y-Axis: 10 points (RPM)
- Z-Axis (Data): 70 points (PSI)

**Statistics:**
- Min: -128.0000 PSI
- Max: 8.0000 PSI
- Avg: -2.3857 PSI
- Dimensions: 10 × 7

**Full Data Table** (10 rows × 7 cols):

| Y \ X | 32.00 | 40.00 | 48.00 | 56.00 | 64.00 | 72.00 | 80.00 |
|-----|------|------|------|------|------|------|------|
| 1000.00 | -128.00 | -64.00 | -121.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 1256.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 4.00 | 4.00 |
| 1512.00 | 6.00 | 0.00 | 0.00 | 0.00 | 0.00 | 4.00 | 4.00 |
| 1768.00 | 6.00 | 6.00 | 8.00 | 0.00 | 0.00 | 4.00 | 4.00 |
| 2024.00 | 6.00 | 8.00 | 8.00 | 0.00 | 0.00 | 4.00 | 4.00 |
| 2280.00 | 6.00 | 6.00 | 8.00 | 0.00 | 0.00 | 4.00 | 4.00 |
| 2536.00 | 6.00 | 6.00 | 8.00 | 0.00 | 0.00 | 0.00 | 4.00 |
| 2792.00 | 4.00 | 4.00 | 6.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 3048.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 3304.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### 330. A/C Pressure Transducer Table A/D Input Voltage Vs A/C Pressure

**Category:** Speedometer

**Axes:**
- X-Axis: 17 points (KPA)
- Y-Axis: 1 points
- Z-Axis (Data): 1 points (KPA)

**Statistics:**
- Min: 0.0000 KPA
- Max: 3168.0000 KPA
- Avg: 1376.9412 KPA
- Dimensions: 1 × 17

**Full Data Table** (1 rows × 17 cols):

| Y \ X | 0.00 | 0.00 | 0.00 | 176.00 | 400.00 | 624.00 | 864.00 | 1088.00 | 1328.00 | 1552.00 | 1792.00 | 2016.00 | 2256.00 | 2480.00 | 2720.00 | 2944.00 | 3168.00 |
|-----|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 0.00 | 0.00 | 0.00 | 0.00 | 176.00 | 400.00 | 624.00 | 864.00 | 1088.00 | 1328.00 | 1552.00 | 1792.00 | 2016.00 | 2256.00 | 2480.00 | 2720.00 | 2944.00 | 3168.00 |


---

## Patches (Community Patchlist)

**Total Patches:** 3
- ✅ Applied: 0
- ❌ Not Applied: 2

### ❌ Not Applied Patches

- **TractionControlFuelPWBugFix**: This fixes the factory software bug that affects any cylinder resuming operation after a torque management fuel cut.
- **InjectorModelBugFix**: This fixes (some of) the factory injector model bugs.

---

*Generated by KingAI TunerPro Exporter v3.3.0*
*Author: kingaustraliagg (Jason King)*
