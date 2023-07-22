import re

def EstimatePrice(mileage, th0, th1):
    return (th0 + (th1 * mileage))

milage = float(input("Milage: "))

th0 = 0
th1 = 0

try:
    with open('thetas.txt', 'r') as file:
        txt = file.read()

        ths = re.findall("\d+\.\d+", txt)
        th0 = float(ths[0])
        th1 = float(ths[1])
except:
    print ("No previous training")

ep = EstimatePrice(milage, th0, th1)

print ("Estimated price is " + str())