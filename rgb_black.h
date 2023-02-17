//Black - Not tested
// These are from https://github.com/FalconChristmas/fpp/blob/master/src/pru/PocketScrollerV1.hp
// _gpio tells which gpio port and _pin tells which bit in the port
// The first 1 in r11 is for the J1 connector
// See the githuub file for the other connectors

#define r11_gpio 2
#define r11_pin 11
#define g11_gpio 1
#define g11_pin 31
#define b11_gpio 2
#define b11_pin 10

#define r12_gpio 2
#define r12_pin 12
#define g12_gpio 1
#define g12_pin 30
#define b12_gpio 2
#define b12_pin 13

#define pru_latch 8	// These are the bit positions in R30
#define pru_oe 9    
#define pru_clock 10

// Control pins are all in GPIO2
// The pocket has these on R0, the code needs to be changed for this work work
#define gpio_sel0 0 /* must be sequential with sel1 and sel2 */
#define gpio_sel1 1
#define gpio_sel2 2
#define gpio_sel3 3
