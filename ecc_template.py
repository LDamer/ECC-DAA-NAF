ka = 0x20A5B20E076E77984380CB49173F6ED7FDED87E645747133F63888907245E5D8
kb = 0x63690612179A5742A7DB7003F0545E866CAF9DE086BF272A0E1827165381B399


class Curve(object):
    def __init__(self, p, a, b, x, y, q):
        super(Curve, self).__init__()
        self.p = p
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.q = q

    def oncurve(self, x1, y1):
        x2 = (x1 ** 3 + self.a * x1 + self.b) % self.p
        y2 = y1 ** 2 % self.p
        if x2 == y2:
            return True
        return False


class Point(object):
    def __init__(self, x, y, curve):
        super(Point, self).__init__()
        self.x = x
        self.y = y
        self.curve = curve

    def oncurve(self):
        return self.curve.oncurve(self.x, self.y)

    def pointdouble(self):
        if self.y == 0:
            return Point("O", "O", self.curve)
        s = (3 * self.x ** 2 + self.curve.a) % self.curve.p
        s = s * inv_euklid(self.y * 2, self.curve.p)
        x_new = (s ** 2 - 2 * self.x) % self.curve.p
        y_new = (s * (self.x - x_new) - self.y) % self.curve.p
        return Point(x_new, y_new, self.curve)

    def pointaddition(self, p2):
        if self.y == -p2.y % self.curve.p and self.x == p2.x:
            return Point("O", "O", self.curve)
        s = (p2.y - self.y) * inv_euklid(p2.x - self.x, self.curve.p) % self.curve.p
        x_new = (s ** 2 - self.x - p2.x) % self.curve.p
        y_new = (s * (self.x - x_new) - self.y) % self.curve.p
        return Point(x_new, y_new, self.curve)

    def return_coordinates(self):
        return self.x, self.y

    def return_inverse(self):
        return Point(self.x, -self.y, self.curve)

    def __add__(self, obj):
        if self.x == 'O':
            return obj
        if obj.x == 'O':
            return self
        if self == obj:
            ret = self.pointdouble()
        else:
            ret = self.pointaddition(obj)
        return ret

    def __str__(self):
        return "x: %s\ny: %s" % (hex(self.x), hex(self.y)) if type(self.x) is int else "x: O\ny: O"

    def __eq__(self, obj):
        return (self.x == obj.x % obj.curve.p and self.y == obj.y % obj.curve.p)

    def __sub__(self, obj):
        inv = Point(obj.x, -obj.y % obj.curve.p, obj.curve)
        return self.__add__(inv)

    def __mul__(self, a):
        return naf(self, a)

    def __rmul__(self, a):
        return self.__mul__(self, a)


def inv_euklid(a, b):
    x0, x1, y0, y1 = 0, 1, 1, 0
    a = a % b
    m = b
    while a != 0:
        q = b // a
        t = a
        a = b % a
        b = t

        t = y0
        y0 = y1
        y1 = t - q * y1

        t = x0
        x0 = x1
        x1 = t - q * x1
    return x0 % m


# to implement
def double_and_add(p: Point, a: int):
    l = len(bin(a)[2:])
    res = p
    for i in range(1, l):
        res += res
        if a & (1 << (l - i - 1)) == 1 << (l - i - 1):
            res += p
    return res


# to implement
def calc_naf_representation(exponent: int):
    x = exponent
    i = 0
    res = []
    while x >= 1:
        if x % 2 == 1:
            e = 2 - (x % 4)
            x = x - e
        else:
            e = 0
        x = x // 2
        i += 1
        res.append(e)
    return res


# to implement
def naf(p: Point, a: int):
    naf_array = calc_naf_representation(a)
    le = len(naf_array)
    res = p
    for i in range(le - 2, -1, -1):
        res += res
        if naf_array[i] == 1:
            res += p
        elif naf_array[i] == -1:
            res -= p
    return res


c = Curve(0xA9FB57DBA1EEA9BC3E660A909D838D726E3BF623D52620282013481D1F6E5377,
          0x7D5A0975FC2C3057EEF67530417AFFE7FB8055C126DC5C6CE94A4B44F330B5D9,
          0x26DC5C6CE94A4B44F330B5D9BBD77CBF958416295CF7E1CE6BCCDC18FF8C07B6,
          0x8BD2AEB9CB7E57CB2C4B482FFC81B7AFB9DE27E1E3BD23C23A4453BD9ACE3262,
          0x547EF835C3DAC4FD97F8461A14611DC9C27745132DED8E545C1D54C72F046997,
          0xA9FB57DBA1EEA9BC3E660A909D838D718C397AA3B561A6F7901E0E82974856A7)

Q = Point(0x8BD2AEB9CB7E57CB2C4B482FFC81B7AFB9DE27E1E3BD23C23A4453BD9ACE326,
          0x547EF835C3DAC4FD97F8461A14611DC9C27745132DED8E545C1D54C72F046997, c)
_a = 0xFAFAFAFAFAFAFAFAFAFAFAFAF

# Für Aufgabe d) : double_and_add(Q, pow(_a, -1, 0xA9FB57DBA1EEA9BC3E660A909D838D718C397AA3B561A6F7901E0E82974856A7))
#
#
# ----------------  LÖSUNGEN DER AUFGABEN -----------------------------
#
# Q * a^-1 = ( x: 0x4664a075aade0eb7bec6f5163e0bacc585bac514242acef6018c2248e79f253d
#              y: 0x8724441cc505b63d26adb77b533f9016d9d19ebda4c037159b8611c0162189ea )
#
#   --NAF--
#   254 doubles
#   38 adds (staring with res = p and not res = "O")
#   47 subs
#
# --noraml DAA--
#   254 doubles
#   133 adds (staring with res = p and not res = "O")
#
#
