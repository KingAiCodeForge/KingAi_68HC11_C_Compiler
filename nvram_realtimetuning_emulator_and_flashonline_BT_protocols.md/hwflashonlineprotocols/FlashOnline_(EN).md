<!-- Converted from: FlashOnline_(EN).pdf -->
<!-- Converted at: 2026-01-12T13:05:57.908171 -->
<!-- Method: markitdown -->
<!-- Words: 3190 | Chars: 20258 | Lines: 650 -->

www.cobrartp.com

FlashOnline

User Manual

 Document revision 2.1

www.cobrartp.com

FlashOnline user manual

1

WARNING

1. Connect (disconnect) the device to the ECU only in a de-energized
state.  Connecting  during  operation  (switched  on)  may  damage  the
device or the vehicle's ECU!

2. Be careful when handling the device even when it is switched off
due  to the presence  of a battery (cell CR2032). Short-circuiting the
battery for a long time may cause an explosion or fire!

3. Be extremely careful when working with high temperatures!

4. When disconnecting (removing) the cable from the emulator and
the SOP44 adapter, pull strictly perpendicularly, in no case do not pull
it to the side, you will damage the connector!

5. Carefully study this manual to avoid unwanted consequences! The
operation of this device requires certain skills.

www.cobrartp.com

FlashOnline user manual

2

GETTING STARTED

USB - connection

  FlashOnline is connected to a PC using a Mini-USB cable.
  FlashOnline can only be connected to a PC, i.e. there is no need to install

(connect) the emulator in the ECU, or connect a separate power source.

Install USB Driver for Rev 3.x boards version
After connecting, you should have a new device in the Device manager.

After that, you need to install the USB driver.

can

Drivers

website:
downloaded
https://cobrartp.com/en/downloads, by selecting an item for the appropriate
version of Windows.

our

on

be

After downloading the driver archive, you must also select the appropriate
installer, depending on the bit depth of your operating system x86 (x32) or x64.
Drivers tested on Windoes XP, Windows 7, Windows 10. Official website of the
https://www.silabs.com/products/development-
driver
tools/software/usb-to-uart-bridge-vcp-drivers.

provider:

Type of driver distribution.

The installation process is standard.

If there is no installer in the folder (Windows 10/11), the driver must be
installed through the Device Manager: By device (FlashOnline), right-click -
Properties - Driver - Update driver. Next, select the folder with the
downloaded drivers.

www.cobrartp.com

FlashOnline user manual

3

 After the driver installation is successfully completed, a virtual COM port

should appear in the device manager, if there is a connected emulator:

View of the device in the device manager upon successful driver installation.

  After installing the drivers, you can use the emulator with the
configuration software, and also check it in the CobraRTP Utility.

Install USB Driver for Rev 4.x boards version
    For  revisions  R4.x  and  later,  the  driver  is  not  required  in  the  case  of
Windows  10/11.  If  you  have  Windows  XP,  Vista,  7,  8.x  driver  installation  is
from  our  website:
required.  The  driver  can  also  be  downloaded
https://cobrartp.com/en/downloads.

To install the driver, use the installer for the appropriate version of Windows

(W):

After the driver installation is successfully completed, a virtual COM port

will appear in the device manager, if there is a connected emulator:

After installing the drivers, you can use the emulator with the configuration

software, and also check it in the CobraRTP Utility.

www.cobrartp.com

FlashOnline user manual

4

Bluetooth (wireless) connection (versions with Bluetooth only)

Wireless  connection  on  your  PC  requires  Bluetooth  v2.0  (hereinafter

referred to as BT) or higher. Connection is made in the following sequence:

1. Connect the emulator to the ECU or via USB. At the same time, the red

indicator of the BT module should blink quickly (about 3 times / sec)

2. Turn on the BT module of the PC and pair with a new device (the name

is usually “FlashOnline BT”). Password 1234 or 0000 (Necessarily).

3. After successful pairing, 2 virtual COM ports should appear (see Device
Manager), one of which will be used for data exchange. How correctly programs
(TunerPRO RT, CobraRTP Utility) find the right port automatically if the device
is turned on and ready to pair.

Attention! When working via BT, the emulator must not be connected

via USB, otherwise a conflict is possible!

Notes:

1.  After  each disconnection of  the  emulator  (for  example,  when  the  ignition is
turned off), in order to continue working in the software, it is necessary to reconnect
(in the program).

2. Many ECUs do not de-energize immediately after the ignition is turned off, and
continue to work for some time (20-60 seconds), keep this in mind, although on the
other hand this is an advantage, given p1.

You  can  check  the  device  using  our  software  -  CobraRTP  Utility

(https://cobrartp.com/en/cobrartp-utility):

www.cobrartp.com

FlashOnline user manual

5

1.  – emulator firmware version.
2.   - the number of the used COM port on which the device is operating at a

given time (may differ in your case).

Note: read the utility manual in the archive with the program (pdf).

To check and work with the emulator on a PC, there is no need to connect to
an  ECU!  The  device  can  be  powered  both  from  the  ECU  and  from  the  USB
connector.

Attention! If the emulator is not recognized in TunerPRO RT, CobraRTP
Utility or other software, check if the emulator is currently connected in
another  program!  The  emulator  port  can  only  be  connected  in  one
program at a time, so before connecting, make sure that the device is not
currently connected in another program (process).

www.cobrartp.com

FlashOnline user manual

6

INSTALLATION AND CONNECTION TO ECU

The FlashOnline board is connected to the ECU using a proprietary adapter

(SOP44 adapter) using a special cable from the kit:

Before installation, pay attention to the correct connection of the adapter

(the locks must be on one side):

www.cobrartp.com

FlashOnline user manual

7

Since the device is an emulator of a memory chip, for correct operation it
is required to dismantle or disconnect the standard flash memory chip from the
ECU board.

1) Removing the flash memory chip from the ECU board

With this method, the flash memory chip must be removed from the ECU
board. For this we recommend using hot air, i.e. hot air soldering station with
high  quality  neutral  flux  gel.  We  also  recommend  using  a  board  preheater
whenever possible.

The air temperature at the outlet of the nozzle and the distance should be
selected in such a way that the temperature of the computer board eventually
reaches a temperature of 210-220°C and no more than 240°C.

After removing the chip, prepare the pads:

www.cobrartp.com

FlashOnline user manual

8

After you remove the chip, the board surface should look like this:

ATTENTION:  be  careful  when  removing  the  chip,  since  there  is  a  high
probability of touching and moving or completely losing other elements
on the board when the melting temperature of the solder of the elements
of the ECU board is reached! You should also pay special attention to the
elements  on  the  back  of  the  board!  Therefore,  for  these  works,  we
strongly recommend using a special holder or a preheater of the boards.

2) Mounting the adapter

Remember to apply flux to the pads before installing the adapter:

www.cobrartp.com

FlashOnline user manual

9

Next, you can and mount it on the ECU board.

Installation can be done in two ways - using hot air or using a soldering

iron:

The first method is faster, but each heating of the ECU board and adapter
negatively  affects  the  printed  circuit  boards  and  their  elements,  so  we
recommend the second method, the essence of which is to solder each contact
with a soldering iron.

In both cases, you should get the following:

ATTENTION: be extremely careful when installing the adapter in the
first way, since the solder on all contacts of the adapter board also reaches
the melting temperature and, accordingly, you can accidentally move or
completely  separate  the  connector  (cable  connection  socket)  of  the
adapter from the board! Also note that the maximum temperature of the
adapter connector material is 240°C, exceeding which the connector may
be irreversibly damaged! Check, if possible, the actual outlet temperature
of your hot air station. Leave the heated elements at rest until they cool
completely!

After  you  have  done  these  steps,  check  all  connections  and  contacts,
connect the emulator using a flat cable. When the computer is turned on (the
emulator  should  not  be  connected  via  USB),  the  “Status”  indicator  on  the
emulator  board  should  light  up,  if  this  does  not  happen  -  check  the  correct
connection and contacts. If the indicator lights up - get to work!

www.cobrartp.com

FlashOnline user manual

10

Removing the adapter

The adapter is dismantled at the installation temperature, otherwise the
same  rules  are  followed  as  when  dismantling  the  chip,  but  you  should  pay
attention to the adapter connector, the maximum temperature of the material
of which is 240°C, as well as the fact that the solder holding the connector also
melts and it can be easy to move.

Never pull on the connector when removing the adapter! It is allowed
to hold the adapter during instsall / deinstal only for a fee (base)! Heating
of each side separately is also not allowed! Heat both sides of the adapter
evenly!

www.cobrartp.com

FlashOnline user manual

11

CONFIGURATION JUMPERS OF THE SOP44 ADAPTER

On the SOP44 adapter board, you can see jumpers (J1, J2) that are designed
to  eliminate  conflict  situations when working with  some  ECUs with  28F200,
29F200, 29F400 chips. The fact is that for these chips, some address lines are
not used in the ECU, and can be either disabled or connected in an unintended
way, for example, to Vcc (+ 5V) or to GND. For FlashOnline to work properly,
these  lines  must  be  free  when  emulating  the  above  chips.  This  affects  the
selection of the correct memory block and, accordingly, the correct operation
of the Dual-Mod mode.

At the time of writing this version of the document, this must be done for

the following ECUs: Bosch ME3.8.3

If your FlashOnline does not work properly with your ECU, then you must

configure using these jumpers (X – remove, ν - soldered):

Type

28f200, 29f200

29F400

29F800

J1

X

X

ν

J2

X

ν

ν

www.cobrartp.com

FlashOnline user manual

12

USE WITH PC SOFTWARE

TunerPRO RT

To  work  with  TunerPRO  RT,  make  sure  you  have  build  version

5.00.9332.00 or higher (Help -> About…):

We recommend downloading the program from the official website: www.tunerpro.net

Further, if this condition is met, the device is connected, and the drivers
are installed correctly, then at startup the program will automatically detect the
device:

After that the program is ready to work.

We  recommend  that  you  study  our  article  on  using  TunerPRO  RT:

https://cobrartp.com/en/online_tuning

Attention! If the emulator is not recognized in TunerPRO RT, check if
the emulator is currently connected in another program! The emulator
port can only be connected in one program at a time, so before
connecting, make sure that the device is not currently connected in
another program (process).

www.cobrartp.com

FlashOnline user manual

13

Address (tables) hit tracking

Hardware  tracing  is  a  feature  that  allows  you  to  track  which  areas  of
memory  the  ECU  processor  is  accessing  without  using  any  third-party
hardware.  In  other  words,  you  can  observe  the  coordinates  in  the  maps  of
interest, according to which the ECU is working at a particular moment in time.
To accomplish this,  this  function  is  supported in  TunerPRO  RT,  as  well  as  in
CobraRTP Utility with v2.8 (Address watch function).

To enable this function in TunerPRO RT, use the corresponding button on

the toolbar of the table of interest:

Note: you may not see the pointer (yellow cell) on certain maps at a
certain point in time. This does not mean that this function is not working
correctly,  it  means  that  the  ECU  processor  does  not  access  this  card
(address range) at the expected time. It is also possible that the card is not
used at all during normal engine operation, such as cranking cards.

Call Address watch, i.e. tracing the addresses by which the ECU processor
accesses a given address range (memory area). It works on the principle of the
table  trace  function  in  TunerPRO  RT  (for  more  details,  see  the  manual  for
CobraRTP Utility):

www.cobrartp.com

FlashOnline user manual

14

CobraRTP Utility

This  is  a  proprietary  utility  for  working  with  CobraRTP  emulators,  incl.
and with FlashOnline since version 2.7. Allows you to load (read) firmware into
the  emulator,  check  and  download  firmware  updates,  configure  the  device,
check the operability.

A detailed manual is contained in the archive with the program.

More information, as well as download the latest version of the program:

https://cobrartp.com/en/cobrartp-utility/

Other software

You can use other firmware editors, for example WinOLS, RomRaider, ECM
Titanium, etc., which save the firmware in binary format (.bin), and then upload
the firmware via CobraRTP Utility. With the powerful "Autoupload" function,
the firmware will be  automatically loaded  online  when  its file is changed, ie.
after  saving  (overwriting)  the  file  to  disk.  (more  in  the  CobraRTP  Utility
manual).

www.cobrartp.com

FlashOnline user manual

15

General note on used firmware

1.

 For  the  emulator  to  work,  you  need  to  download  the  full  ECU
firmware (256-1024kb) at least once for a specific ECU, then you can change
(upload)  only  individual  maps,  tables,  parameters  (calibrations)  of  the
firmware  online  in TunerPRO  RT, WinOLS,  RomRaider,  etc.  and,  accordingly,
there is no need to download the firmware completely every time, for this there
is a " Autoupload " function in our utility, or, if you use TunerPRO RT, the maps
are loaded from the program itself online (See. нашу статью о TunerPRO).

2.

Check if you need to correct the checksum for a specific firmware
(ECU),  as  well  as  when  editing  the  firmware  for  writing  to  flash  memory!
FlashOnline does not correct the checksum! In TunerPRO, you can check this in
the XDF edit section:

3.

Use firmware 100% compatible with your ECU and only complete,
not  calibrations  (the  emulator  performs  the  same  role  as  the  chip  that  was
uploaded - it will work!). Ideally, the firmware can be downloaded via the OBD
connector from the ECU with which you will use FlashOnline.

4.

 After  downloading  the  full  firmware,  many  ECUs  require  a
complete restart, at least by turning off the ignition. In this case, the emulator
does not need to be restarted, turned off, etc.

www.cobrartp.com

FlashOnline user manual

16

DUAL-MOD feature

Dual-mod  is  an  additional  function  that  allows  you  to  upload  several

independent complete firmwares to the emulator, then switch online.

For this purpose, the FlashOnline board has corresponding contacts, upon
closing or opening of which the corresponding memory block of the emulator
is selected (firmware):

Dual-mod  works  only  in  emulation  mode  28F200,  28F400,  29F200,
29F400, i.e. with firmware 256-512kB, tk. FlashOnline total memory 1024kB
(100000h) or 2 conventional blocks of 512kB each. When emulating 29F800,
this function does not work.!

To select a memory block into which the firmware will be loaded, you must

install in the utility:

Selecting memory blocks (switching) on the FlashOnline board:

Block 0 - contacts open

Block 1 - contacts closed (jumper installed)

Note: In TunerPRO, only memory block 0 is used by default. Therefore, for
full use of the dual-mod with TunerPRO, save the firmware (bin) and load them
through the CobraRTP Utility already with the ability to select memory blocks.

www.cobrartp.com

FlashOnline user manual

17

ECU COMPATIBILITY OPTIONS

These  options  are  intended  to  make  the  emulator  compatible  with
different  ECUs.  These  options  are  responsible  for  representing  data  in  the
emulator's memory chip:

1.            Encoding - decides the compatibility with the ECU, where the flash
memory data bus is connected non-standard. As a rule, this is a Siemens ECU.
This option must be enabled if your ECU is on the list.

2.

Target CPU - responsible for the data byte order system. To date,
there  are  several  byte  endianness  systems  for  16  or  more  bit  CPUs:  Little-
endian and Big-endian. In most cases, Little-endian is used, but Big-endian is
also found in the ECU when Motorola processors are used, such as Siemens
MSS52-54.  The  option  is  available  starting  with  firmware  version  1.30  and
CobraRTP Utulity v3.10.

If these options are  selected incorrectly, then, accordingly, the ECU

will not work with FlashOnline.

www.cobrartp.com

FlashOnline user manual

18

FLASHONLINE RESTRICTIONS

1. FlashOnline can only work in read mode, i.e. there is no hardware ability
to program the emulator via the ECU as well as the chip (for example, via the
OBD2 connector)! Data can only be recorded via the USB interface of the device.
In  this  regard,  for  ECUs  that  use  flash  memory  to  record  calibrations
(adaptations) in normal ECU operation, data will not be written to FlashOnline
as well as to a flash memory chip.

2. FlashOnline can be installed and used instead of the memory chip on a
permanent basis, but it should be borne in mind that the CR2032 3V battery
installed on the device board serves to power the volatile memory, which stores
the firmware (s) when the device is turned off. Accordingly, the charge of this
element is sufficient for 1.5-2 years. After the cell is discharged below 1.5V, the
data in the memory will be corrupted after each power outage.

3.  Dual-mod  function  only  works  in  emulation  mode  29f200  /  28f200,

29f400 / 28f400 (256-512kB), and is not supported for 29f800 (1024kB).

www.cobrartp.com

FlashOnline user manual

19

TROUBLESHOOTING

The engine will not start and the ECU does not go to diagnostics

  Сheck if the firmware is compatible with your ECU

  Сheck if the checksum is correct


It  may be  necessary  to  perform  actions  according  to  paragraph  "CONFIGURATION
JUMPERS"

  The wrong memory block of the emulator (DualMod) may be selected
•  Сheck if you need to apply encoding for your ECU in CobraRTP Utility options (see

utility manual)

  Check if the target CPU type matches your ECU CPU in the CobraRTP utility options
  When  loading  the  firmware  via  CobraRTP  Utility,  the  wrong  type  of  emulated

memory was selected

  Check all contacts and connections of the device with the computer.

Tracing does not work in TunerPRO RT

1. Perhaps you have selected an inactive map (see the paragraph on tracing, note)
2. Check if Memory Block 0 is selected in DualMod
3. Make sure the XDF file matches your firmware (bin).
4. Make sure your FlashOnline firmware version is v1.20 or later.

An error appears when loading data into the emulator

1. If an error occurs during the download/read process - replace the USB cable.
2. If the error occurs only in TunerPRO RT, and in CobraRTP Utrility the data exchange
with the emulator is in order, check if the bin file parameters are specified correctly in the
XDF settings - Bin size (HEX) and offset, It’s must be equal to the size of the bin file and
divided by 2. For example: if file size is 512kB, then it should be 80000.
3. If you use Bluetooth pairing, do not forget to connect again in the program after turning
off the emulator (ignition).
4. If the problem persists, contact technical support.

     After  turning  off  the  emulator  for  a  while,  the  car  stops  starting,
although it did start before turning off

Check the backup battery (CR2032), the voltage in the disconnected state should not be
lower than 2.5V. Replace the element.

www.cobrartp.com

FlashOnline user manual

20

Specifications

Supply voltage
Supply current
Ambient temperature
Maximum Bluetooth Range
Weight

4.7 - 5.5V
70mA
0 - 50°С
10m
80g

CobraRTP Team 2018-2023

cobrartp.com/en

www.cobrartp.com

FlashOnline user manual

21

