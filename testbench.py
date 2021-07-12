import ecc_template as ecc
import random

try:
    curve = ecc.Curve(0xA9FB57DBA1EEA9BC3E660A909D838D726E3BF623D52620282013481D1F6E5377,
                      0x7D5A0975FC2C3057EEF67530417AFFE7FB8055C126DC5C6CE94A4B44F330B5D9,
                      0x26DC5C6CE94A4B44F330B5D9BBD77CBF958416295CF7E1CE6BCCDC18FF8C07B6,
                      0x8BD2AEB9CB7E57CB2C4B482FFC81B7AFB9DE27E1E3BD23C23A4453BD9ACE3262,
                      0x547EF835C3DAC4FD97F8461A14611DC9C27745132DED8E545C1D54C72F046997,
                      0xA9FB57DBA1EEA9BC3E660A909D838D718C397AA3B561A6F7901E0E82974856A7)
except Exception as e:
    print(f"[-]EC konnte nicht erstellt werden {e}")
    exit(-1)

try:
    point = ecc.Point(0x8BD2AEB9CB7E57CB2C4B482FFC81B7AFB9DE27E1E3BD23C23A4453BD9ACE3262,
                      0x547EF835C3DAC4FD97F8461A14611DC9C27745132DED8E545C1D54C72F046997, curve)
except Exception as e:
    print(f"[-]Punkt konnte nicht erstellt werden {e}")
    exit(-1)

compare_val = ecc.Point(0x609638E7A3679D04AD149F698E58731598C14EA6F84631427346F912D7EFEE97,
                        0x4AF0802EAE475811C3686A89694D1631E14F375E811EE1C70A5D5DF647E5D31F, curve)
compare_value_1_naf = [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
compare_value_2_naf = [-1, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, -1, 0,
                       -1, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0,
                       -1, 0, -1, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0,
                       0, 0, -1, 0, -1, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 1]

err = 0
try:
    naf = ecc.calc_naf_representation(0b1111111111111111111111111111111111111111111111)
    err |= not (naf == compare_value_1_naf)
    naf = ecc.calc_naf_representation(0xFAFAFAFAFAFAFAFAFAFAFAFAFAF)
    err |= not (naf == compare_value_2_naf)
except Exception as e:
    print(e)

if err:
    print("[-]Fehler in NAF")
    exit(-1)
else:
    print("[+] NAF")

try:
    p_test = ecc.naf(point, 0xFAFAFAFAFAFAFAFAFAFAFAFAFAF)
    err |= not (p_test == compare_val)
    p_test = ecc.double_and_add(point, 0xFAFAFAFAFAFAFAFAFAFAFAFAFAF)
    err |= not (p_test == compare_val)
except Exception as e:
    print(e)

if err:
    print("[-]Fehler in Punktmultiplikation DAA oder NAF")
    exit(-1)
else:
    print("[+] NAF/Double and Add")

random.seed(1)
for i in range(0, 100):
    factor = random.randint(0, 2 ** 255)
    if (ecc.naf(point, factor) != ecc.double_and_add(point, factor)):
        print("[-]Error DAA und NAF verhalten sich unterschiedlich")
        exit(-1)

print("[+]success")
