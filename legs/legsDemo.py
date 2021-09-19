import time
import numpy as np
import legs
import path


def demoLoop ():
    while True:
        TURRET_DIRECTION = 1 #Change to 1 or -1 to flip all turret rotations during demo
        X_DIRECTION = 1 #Change to 1 or -1 to flip all X axis motion during demo
        Y_DIRECTION = 1 #Change to 1 or -1 to flip all Y axis motion during demo
        ROTATION_DIRECTION = (1 if X_DIRECTION == Y_DIRECTION else -1)

        guardian.zeta  = [0,0,0]; guardian.resetLegs()
        while True:
            guardian.setTurretThrottle(-0.7*TURRET_DIRECTION); time.sleep(2); guardian.setTurretThrottle(0)
            time.sleep(0.5)
            guardian.setTurretThrottle(0.7*TURRET_DIRECTION); time.sleep(3); guardian.setTurretThrottle(0)
            time.sleep(1)
            guardian.setTurretThrottle(-0.1*TURRET_DIRECTION); guardian.rotate(ROTATION_DIRECTION*60*np.pi/180, True); guardian.setTurretThrottle(0)
            guardian.moveTo(0, 0.25*Y_DIRECTION, False)
            guardian.setTurretThrottle(0.3*TURRET_DIRECTION); time.sleep(2); guardian.setTurretThrottle(0)
            guardian.moveTo(0.1*X_DIRECTION, -0.5*Y_DIRECTION, True)
            guardian.setTurretThrottle(-0.2*TURRET_DIRECTION); guardian.rotate(ROTATION_DIRECTION*90*np.pi/180, False); guardian.setTurretThrottle(0)
            time.sleep(2)
            guardian.moveTo(0, 0, True)
            time.sleep(1)
            guardian.setTurretThrottle(0.5*TURRET_DIRECTION); time.sleep(5); guardian.setTurretThrottle(0)
            print("Resuming demo loop in 6 seconds.")
            time.sleep(6)


if __name__ == "__main__":
    guardian = legs.guardian()
    print("Resetting legs")
    guardian.resetLegs()
    time.sleep(2)
    print("Guardian is ready:\n==================")
    while True:
        var1,var2,var3,var4 = None, None, None, None
        cmd = input(">> ")
        if cmd == "help":
            print("Working commands:\n"+
                  "\'help\'\n"+
                  "\'demo\'\n"+
                  "\'resetLegs\'\n"+
                  "\'zeroZeta\'\n"+
                  "\'moveTo <x>, <y>, [RESET_AFTER], [SIMULATE]\'\n"+
                  "\'rotate <phi>, [RESET_AFTER], [SIMULATE]\'\n"+
                  "\'moveTurret <speed>, [duration]\'\n"+
                  "\'exit\'\n" +
                  "\nExample: \'moveTo -1, 1, True\'\n")
        elif cmd == "demo":
            print("Entering demo mode. Use CTRL+C to abort.")
            try: demoLoop()
            except: print("Demo aborted.\n")
        elif cmd == "resetLegs":
            guardian.resetLegs()
            print("")
        elif cmd == "zeroZeta":
            guardian.zeta = [0,0,0]
            print("")
        elif "moveTo" in cmd:
            try:
                cmd = cmd[6:].split(',')
                var1 = float(cmd[0])
                var2 = float(cmd[1])
                var3 = False
                var4 = False
                if len(cmd) > 2: var3 = ("True" in cmd[2])
                if len(cmd) > 3: var4 = ("True" in cmd[3])
                print("Moving to (" + str(var1) + ", " + str(var2) + ") meters" + (", then resetting." if var3 else ".") + " Use CTRL+C to abort.\n")
            except:
                print("Invalid command arguments:\n\'moveTo <x>, <y>, [RESET_AFTER], [SIMULATION]\'.\n")
                continue
            try: 
                if var4: 
                    guardian.calculateMoveTrajectory(var1,var2,var3)
                    sim = path.simulation(guardian, 10, 50); sim.show(); del sim
                else: guardian.moveTo(var1,var2,var3)
            except: print("Movement aborted.\n")
        elif "rotate" in cmd:
            try:
                cmd = cmd[6:].split(',')
                var1 = float(cmd[0])
                var2 = False
                var3 = False
                if len(cmd) > 1: var2 = ("True" in cmd[1])
                if len(cmd) > 2: var3 = ("True" in cmd[2])
                print("Rotating by " + str(var1) + " degrees" + (", then resetting." if var2 else ".") + " Use CTRL+C to abort.\n") 
            except:
                print("Invalid command arguments:\n\'rotate <phi>, [RESET_AFTER], [SIMULATION]\'.\n")
                continue
            try: 
                if var3: 
                    guardian.calculateRotateTrajectory(var1*np.pi/180,var2)
                    sim = path.simulation(guardian, 10, 50); sim.show(); del sim
                else: guardian.rotate(var1*np.pi/180,var2)
            except: print("Rotation aborted.\n")
        elif "moveTurret" in cmd:
            try: 
                cmd = cmd[10:].split(',')
                var1 = float(cmd[0])
                if len(cmd) > 1: var2 = float(cmd[1])
            except:
                print("Invalid command arguments:\n\'moveTurret <speed>, [duration]\'\n")
                continue
            try: 
                if var2 is None: 
                    if guardian.setTurretThrottle(var1) == 1: 
                        print("Setting turret throttle to " + str(var1*100) + "%.\n")   
                    else:
                        print("Unable to set turret throttle.\n")
                elif var2 >= 0:
                    if guardian.setTurretThrottle(var1) == 1: 
                        print("Setting turret throttle to " + str(var1*100) + "% for " + str(var2) + " seconds.\n") 
                        time.sleep(var2)
                        guardian.setTurretThrottle(0)
                    else:
                        print("Unable to set turret throttle.\n")
                else:
                    print("Invalid value for duration.\n")
            except: print("Turret Rotation aborted.\n")
        elif "exit" in cmd:
            print("Goodbye.\n")
            exit(0)
        else:
            print("Invalid command. Try \'help\'.\n")