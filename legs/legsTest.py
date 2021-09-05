import legs
import time

if __name__ == "__main__":
    guardian = legs.guardian()
    print("Resetting legs")
    guardian.resetLegs()
    time.sleep(2)
    while True:
        X = float(input("\nEnter target x position [m]: "))
        Y = float(input("Enter target y position [m]: "))
        print("Moving to (" + str(X) + ", " + str(Y) + ")")
        guardian.moveTo(X, Y)