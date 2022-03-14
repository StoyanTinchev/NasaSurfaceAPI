import random


class SurfaceController:
    def __init__(self, longitude: str, latitude: str, redis):
        self.longitude = longitude
        self.latitude = latitude
        self.redis = redis

        self.__weather_temperature = {"low": -100, "high": -7}
        self.__weather_pressure = {"low": 650, "high": 800}
        self.__weather_wind = {"low": 5, "high": 25}

    def get_weather(self):
        if self.__position_check() and self.redis.contains(self.longitude + self.latitude):
            return self.redis.get(self.longitude + self.latitude)

        for m in range(5, 0, -1):
            try:
                for i in range(int(self.longitude) - m, int(self.longitude) + 5):
                    for j in range(int(self.latitude) - m, int(self.latitude) + 5):
                        if self.redis.contains(str(i) + str(j)):
                            print("found {} {}".format(i, j))
                            return self.__result_manage(self.redis.get(str(i) + str(j)))
            except Exception:
                pass

        return self.__result_manage()

    def __weather_generator(self, redis_result=None):
        result = dict()
        result["sol_keys"] = list()
        for i in range(6):
            if redis_result is None:
                sol_day = self.__generate_weather_info(self.__weather_temperature,
                                                       self.__weather_pressure, self.__weather_wind)
            else:
                temp_redis = redis_result["sol_keys"][i]["AT"]
                pressure_redis = redis_result["sol_keys"][i]["PRE"]
                wind_redis = redis_result["sol_keys"][i]["HWS"]
                print("temp redis: {};  pressure redis: {};  wind redis: {}"
                      .format(temp_redis, pressure_redis, wind_redis))

                weather_temp = {"low": temp_redis - 2, "high": temp_redis + 2}
                weather_pressure = {"low": pressure_redis - 2, "high": pressure_redis + 2}
                weather_wind = {"low": wind_redis - 1, "high": wind_redis + 1}

                sol_day = self.__generate_weather_info(weather_temp,
                                                       weather_pressure, weather_wind)

            result["sol_keys"].append(sol_day.__dict__)

        return result

    @staticmethod
    def __generate_weather_info(weather_temp, weather_pressure, weather_wind):
        weather_temp_sol = random.randint(weather_temp["low"], weather_temp["high"])
        weather_pressure_sol = random.randint(weather_pressure["low"], weather_pressure["high"])
        weather_wind_sol = random.randint(weather_wind["low"], weather_wind["high"])

        sol_day = SolDay([weather_temp_sol, weather_pressure_sol, weather_wind_sol])

        return sol_day

    def __result_manage(self, items=None):
        result = self.__weather_generator(items)
        if self.__position_check():
            self.redis.set(self.longitude + self.latitude, result)

        return result

    def __position_check(self):
        if self.longitude is None or self.latitude is None:
            return False
        return True
