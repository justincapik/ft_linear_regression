import re
from train import normalize_data,unnormalize_data

def EstimatePrice(mileage, th0, th1):
    return (th0 + (th1 * mileage))

def predict():
    milage = float(input("Milage: "))

    th0 = 0
    th1 = 0

    try:
        with open('thetas.txt', 'r') as file:
            txt = file.read()

            ths = re.findall(r"-?\d+\.\d+", txt)
            th0 = float(ths[0])
            th1 = float(ths[1])
            bounds = re.findall(r"-?\d+", txt)
            min_km = float(bounds[4])
            min_price = float(bounds[5])
            max_km = float(bounds[6])
            max_price = float(bounds[7])

            milage = (milage - min_km) / max_km
            ep = EstimatePrice(milage, th0, th1)
            ep = ep * max_price + min_price

            print ("Estimated price is " + str(ep))

    except Exception as e:
        print ("No previous training")

        th0 = 0
        th1 = 0
        ep = EstimatePrice(milage, th0, th1)

        print ("Estimated price is " + str(ep))


if __name__ == '__main__':
    predict()