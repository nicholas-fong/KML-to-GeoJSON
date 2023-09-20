import math

#python code in java class-method style

class HaversineCalculator:
    EARTH_RADIUS = 6371000.0  # Earth's radius

    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)

        a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            math.sin(d_lon / 2) * math.sin(d_lon / 2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return HaversineCalculator.EARTH_RADIUS * c  # unit in meters

def main():
    print("Calculate distance between 2 points on earth using haversine distance formula")
    in_str1 = input("Enter first latitude and longitude separated by a comma: ")
    print("You entered GPS", in_str1)
    in_str2 = input("Enter second latitude and longitude separated by a comma: ")
    print("You entered GPS", in_str2)

    latlon1 = in_str1.strip().split(",")
    lat1 = float(latlon1[0])
    lon1 = float(latlon1[1])

    latlon2 = in_str2.strip().split(",")
    lat2 = float(latlon2[0])
    lon2 = float(latlon2[1])

    distance = HaversineCalculator.haversine_distance(lat1, lon1, lat2, lon2)

    if distance < 1000:
        print(f"Distance between two points = {distance:.1f} meters")
    else:
        print(f"Distance between two points = {distance / 1000:.1f} kilometers")

if __name__ == "__main__":
    main()
