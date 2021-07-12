from fastecdsa.curve import Curve
from fastecdsa.point import Point
import fastecdsa

ka = 0x20A5B20E076E77984380CB49173F6ED7FDED87E645747133F63888907245E5D8
kb = 0x63690612179A5742A7DB7003F0545E866CAF9DE086BF272A0E1827165381B399
curve1 = fastecdsa.curve.brainpoolP256r1
# curve1= Curve("Test",19,3,6,17,3,17)
poi = point = Point(0x8BD2AEB9CB7E57CB2C4B482FFC81B7AFB9DE27E1E3BD23C23A4453BD9ACE3262,
                    0x547EF835C3DAC4FD97F8461A14611DC9C27745132DED8E545C1D54C72F046997, curve1)
poi = poi * 0x4862E61E2AC376CFAB9D61827E646421B28E9E0E2ACA462573
# poi = Point(3,17,curve1)
# t = poi*4
print(poi)

# sudo pip install fastecdsa zum installieren
