//
//	Settings
//	Choose sensor
//
//	#define BMP180
#ifndef BMP180
	#define BMP280
#ifndef BMP280
	#define BME280
#endif
#define BMP_I2C 1
#define BMP_SPI 0
#endif
#ifdef BMP180
#define BMP_I2C 1
#endif
