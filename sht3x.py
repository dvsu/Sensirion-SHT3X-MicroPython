from ubinascii import hexlify
from time import sleep
from machine import I2C


class SHT3X:

    def __init__(self, bus_obj:I2C, address:int):
        self.address = address
        self.bus = bus_obj

    def get_temperature_in_celsius(self, data:int) -> float:
        #   Temperature conversion formula (Celsius)
        #   T[C] = -45 + (175 * (raw_temp_data / (2^16 - 1)))
        return round(-45 + (175 * (data / ((2**16) - 1))), 2)    

    def get_temperature_in_fahrenheit(self, data:int) -> float:
        #   Temperature conversion formula (Fahrenheit)
        #   T[F] = -49 + (315 * (raw_temp_data / (2^16 - 1)))
        return round(-49 + (315 * (data / ((2**16) - 1))), 2)

    def get_relative_humidity(self, data:int) -> float:
        #   Relative humidity conversion formula
        #   RH = 100 * (raw_humidity_data / (2^16 - 1))
        return round(100 * (data/ ((2**16) - 1)), 2)

    def get_measurement(self) -> dict:

        try:
            sleep(0.05)
            self.bus.writeto(self.address, b'\x2c\x06')
            sleep(0.05)
            data = hexlify(self.bus.readfrom(self.address, 6))
            temp_data = int(data[0:4], 16)
            humi_data = int(data[6:10], 16)
            sleep(0.05)

            return {
                "temp_celsius": self.get_temperature_in_celsius(temp_data),
                "temp_fahrenheit": self.get_temperature_in_fahrenheit(temp_data),
                "humidity": self.get_relative_humidity(humi_data)
            }
        
        except Exception as e:
            print("Failed to read temperature and humidity value")
            print(e)


class SHT31(SHT3X):

    def __init__(self, bus_obj:I2C):
        self.sensor_name = 'SHT31'
        super().__init__(bus_obj, address=68) # 0x44


class SHT35(SHT3X):

    def __init__(self, bus_obj:I2C):
        self.sensor_name = 'SHT35'
        super().__init__(bus_obj, address=69) # 0x45
