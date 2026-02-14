/* Simple test - basic RPM threshold check */
volatile unsigned char *RPM = (volatile unsigned char *)0x00A2;
volatile unsigned char *FLAGS = (volatile unsigned char *)0x0046;

void check_rpm(void) {
    unsigned char rpm = *RPM;
    if (rpm >= 0xF0) {
        *FLAGS = *FLAGS | 0x80;
    }
    if (rpm < 0xEC) {
        *FLAGS = *FLAGS & 0x7F;
    }
}
