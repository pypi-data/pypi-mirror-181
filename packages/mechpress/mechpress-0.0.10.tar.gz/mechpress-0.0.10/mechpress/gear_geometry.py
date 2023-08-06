import math

class GearGeometry:
    """
    A class for calculating geometrical parameters of cylindrical gears

    ...

    Attributes
    ----------
    mn : float
        normal module
    z1: int
        number of teeth in gear 1
    z2: int
        number of teeth in gear 2
    alpn_deg: float (optional)
        normal pressure angle in deg
    x1: float (optional)
        correction factor in gear 1
    x2: float (optional)
        correction factor in gear 2
    beta_deg: float (optional)
        helix angle in deg

    Methods
    -------

    def getMt(self):
        Returns transverse module

    def getPcd1(self):
        return pcd in mm

    def getPcd2(self):
        return pcd in mm

    def getTipCirDia1_S0(self):
        return tip circle dia in mm

    def getTipCirDia2_S0(self):
        return tip circle dia in mm

    def norToothThkOnPcd(self):
        return normal tooth thk on pcd in mm

    def transToothThkOnPcd(self):
        return transverse tooth thk on pcd in mm

    def getRootCirDia1(self):
        return root circle dia in mm

    def getRootCirDia2(self):
        return root circle dia in mm

    def getAlpt(self):
        return transverse pressure angle in rad

    def getAlptW(self):
        return transverse working pressure angle in rad

    def getTipCirWotDia1_S(self):
        return tip circle dia without topping in mm

    def getTipCirWotDia2_S(self):
        return tip circle dia without topping in mm

    def getA_S(self):
        return actual center distance in mm

    def getTipCirWtDia1_S(self):
        return tip circle dia with topping in mm

    def getTipCirWtDia2_S(self):
        return tip circle dia with topping in mm

    def getYm(self):
        return topping in mm

    def getTopClearance(self):
        return top clearance in mm

    def workCirDia1(self):
        return working circle dia in mm

    def workCirDia2(self):
        return working circle dia in mm

    """

    def __init__(self, mn, z1, z2, alpn_deg = 20, x1 = 0, x2 = 0,  beta_deg = 0):
        """
        Constructs all the necessary attributes for the GearGeometry object
        
        Parameters
        ----------
        mn : float
            normal module
        z1: int
            number of teeth in gear 1
        z2: int
            number of teeth in gear 2
        alpn_deg: float (optional)
            normal pressure angle in deg
        x1: float (optional)
            correction factor in gear 1
        x2: float (optional)
            correction factor in gear 2
        beta_deg: float (optional)
            helix angle in deg

        """
        self.mn = mn
        self.z1 = int(z1)
        self.z2 = int(z2)
        self.alpn_deg = alpn_deg
        self.alpn = self.alpn_deg * math.pi / 180  # converting into radian
        self.beta_deg = beta_deg
        self.beta = self.beta_deg * math.pi / 180  # converting into radian
        self.x1 = x1
        self.x2 = x2

        self.mt = self.mn / math.cos(self.beta)  # transverse module
        self.pcd1 = self.z1 * self.mt  # pcd in mm
        self.pcd2 = self.z2 * self.mt  # pcd in mm
        self.a0 = (self.pcd1 + self.pcd2) / 2  # std center distance in mm

    def getMt(self):
        """
        Returns the transverse module

        Parameters
        ----------

        Returns
        -------
        float
        Returns the transverse module
        """
        return self.mt  # transverse module

    def getPcd1(self):
        """
        Returns the pcd of gear 1 in mm

        Parameters
        ----------

        Returns
        -------
        float
        Returns the pcd of gear 1 in mm
        """
        return self.pcd1  # pcd in mm

    def getPcd2(self):
        """
        Returns the pcd of gear 2 in mm

        Parameters
        ----------

        Returns
        -------
        float
        Returns the pcd of gear 2 in mm
        """
        return self.pcd2  # pcd in mm

    #  Formulas for S0 gearing

    def getTipCirDia1_S0(self):
        """
        Returns the tip circle dia of gear 1 in mm

        Parameters
        ----------

        Returns
        -------
        float
        Returns the tip circle dia of gear 1 in mm
        """
        return self.pcd1 + 2 * self.mn * (1 + self.x1)  # tip circle dia in mm

    def getTipCirDia2_S0(self):
        """
        Returns the tip circle dia of gear 2 in mm

        Parameters
        ----------

        Returns
        -------
        float
        Returns the tip circle dia of gear 2 in mm
        """
        return self.pcd2 + 2 * self.mn * (1 + self.x2)  # tip circle dia in mm

    # Formula common to both S and S0 gearing

    def norToothThkOnPcd(self):
        """
        Returns the normal tooth thk on pcd in mm

        Parameters
        ----------

        Returns
        -------
        float
        Returns the normal tooth thk on pcd in mm
        """
        return self.mn * (0.5 * math.pi + 2 * self.x1 * math.tan(self.alpn))  # normal tooth thk on pcd in mm

    def transToothThkOnPcd(self):
        """
        Returns the transverse tooth thk on pcd in mm

        Parameters
        ----------

        Returns
        -------
        float
        Returns the transverse tooth thk on pcd in mm
        """
        return self.mt * (0.5 * math.pi + 2 * self.x1 * math.tan(self.alpn))  # transverse tooth thk on pcd in mm

    def getRootCirDia1(self):
        """
        Returns the root circle dia of gear 1 in mm

        Parameters
        ----------

        Returns
        -------
        float
        Returns the root circle dia of gear 1 in mm
        """
        return self.pcd1 - 2 * 1.25 * self.mn + 2 * self.x1 * self.mn  # root circle dia in mm

    def getRootCirDia2(self):
        """
        Returns the root circle dia of gear 2 in mm

        Parameters
        ----------

        Returns
        -------
        float
        Returns the root circle dia of gear 2 in mm
        """
        return self.pcd2 - 2 * 1.25 * self.mn + 2 * self.x2 * self.mn  # root circle dia in mm

    #  Formulas for S gearing

    def getAlpt(self):
        """
        Returns the transverse pressure angle in rad

        Parameters
        ----------

        Returns
        -------
        float
        Returns the transverse pressure angle in rad
        """
        return math.atan(math.tan(self.alpn)/math.cos(self.beta))  # transverse pressure angle in rad

    def getAlptW(self):
        """
        Returns the transverse working pressure angle in rad

        Parameters
        ----------

        Returns
        -------
        float
        Returns the transverse working pressure angle in rad
        """
        inv_alptw = ((2 * (self.x1 + self.x2) * math.tan(self.alpn) / (self.z1 + self.z2)) +
                     (math.tan(GearGeometry.getAlpt(self)) - GearGeometry.getAlpt(self)))
        return inv(inv_alptw)  # transverse working pressure angle in rad

    def getTipCirWotDia1_S(self):
        """
        Returns the tip circle dia without topping of gear 1 in mm

        Parameters
        ----------

        Returns
        -------
        float
        Returns the tip circle dia without topping of gear 1 in mm
        """
        return self.pcd1 + 2 * self.mn + 2 * self.x1 * self.mn  # tip circle dia without topping in mm

    def getTipCirWotDia2_S(self):
        """
        Returns the tip circle dia without topping of gear 2 in mm

        Parameters
        ----------

        Returns
        -------
        float
        Returns the tip circle dia without topping of gear 2 in mm
        """
        return self.pcd2 + 2 * self.mn + 2 * self.x2 * self.mn  # tip circle dia without topping in mm

    def getA_S(self):
        """
        Returns the actual center distance in mm

        Parameters
        ----------

        Returns
        -------
        float
        Returns the actual center distance in mm
        """
        return self.a0 * math.cos(GearGeometry.getAlpt(self)) / math.cos(GearGeometry.getAlptW(self))  # actual center distance in mm

    def getTipCirWtDia1_S(self):
        """
        Returns the tip circle dia with topping of gear 1 in mm

        Parameters
        ----------

        Returns
        -------
        float
        Returns the tip circle dia with topping of gear 1 in mm
        """
        return 2 * (GearGeometry.getA_S(self) + self.mn - self.x2 * self.mn) - self.pcd2  # tip circle dia with topping in mm

    def getTipCirWtDia2_S(self):
        """
        Returns the tip circle dia with topping of gear 2 in mm

        Parameters
        ----------

        Returns
        -------
        float
        Returns the tip circle dia with topping of gear 2 in mm
        """
        return 2 * (GearGeometry.getA_S(self) + self.mn - self.x1 * self.mn) - self.pcd1  # tip circle dia with topping in mm

    def getYm(self):
        """
        Returns the topping in mm

        Parameters
        ----------

        Returns
        -------
        float
        Returns the topping in mm
        """
        return self.a0 + (self.x1 + self.x2) * self.mn - GearGeometry.getA_S(self)  # topping in mm

    def getTopClearance(self):
        """
        Returns the top clearance in mm

        Parameters
        ----------

        Returns
        -------
        float
        Returns the top clearance in mm
        """
        return GearGeometry.getA_S(self) - (GearGeometry.getTipCirWtDia1_S(self) + GearGeometry.getRootCirDia2(self)) / 2  # top clearance in mm

    def workCirDia1(self):
        """
        Returns the working circle dia of gear 1 in mm

        Parameters
        ----------

        Returns
        -------
        float
        Returns the working circle dia of gear 1 in mm
        """
        return self.pcd1 * math.cos(GearGeometry.getAlpt(self)) / math.cos(GearGeometry.getAlptW(self))  # working circle dia in mm

    def workCirDia2(self):
        """
        Returns the working circle dia of gear 2 in mm

        Parameters
        ----------

        Returns
        -------
        float
        Returns the working circle dia of gear 2 in mm
        """
        return self.pcd2 * math.cos(GearGeometry.getAlpt(self)) / math.cos(GearGeometry.getAlptW(self))  # working circle dia in mm



def inv(alp):
    inv_alp = alp
    guess = 0.35
    epsilon = 0.00000001
    while abs((math.tan(guess) - guess) - inv_alp) >= epsilon:
        guess = guess - ((math.tan(guess) - guess) - inv_alp) / ((1 / (math.cos(guess))**2) - 1)
        if(guess > 1 or guess < 0.001):
            return 0
            break
    if(guess < 1 and guess > 0.001):
        return guess


# a = GearGeometry(10, 17, 93)
# print("Transverse module")
# print(a.getMt())
# print("\n")
# print("pcd1")
# print(a.getPcd1())
# print("\n")
# print("pcd2")
# print(a.getPcd2())
# print("\n")
# print("tip circle1")
# print(a.getTipCirDia1_S0())
# print("\n")
# print("tip circle2")
# print(a.getTipCirDia2_S0())
# print("\n")
# print("Normal tooth thickness on pcd")
# print(a.norToothThkOnPcd())
# print("\n")
# print("Transverse tooth thickness on pcd")
# print(a.transToothThkOnPcd())
# print("\n")
# print("Root circle dia1")
# print(a.getRootCirDia1())
# print("\n")
# print("Root circle dia2")
# print(a.getRootCirDia2())
# print("\n")
# print("Transverse pressure angle")
# print(a.getAlpt())
# print("\n")
# print("Working pressure angle")
# print(a.getAlptW())
# print("\n")
# print("Tip circle dia1 without topping")
# print(a.getTipCirWotDia1_S())
# print("\n")
# print("Tip circle dia2 without topping")
# print(a.getTipCirWotDia2_S())
# print("\n")
# print("Actual center distance")
# print(a.getA_S())
# print("\n")
# print("Tip circle dia1 after topping")
# print(a.getTipCirWtDia1_S())
# print("\n")
# print("Tip circle dia2 after topping")
# print(a.getTipCirWtDia2_S())
# print("\n")
# print("Topping")
# print(a.getYm())
# print("\n")
# print("Top clearance")
# print(a.getTopClearance())
# print("\n")
# print("Working circle dia1")
# print(a.workCirDia1())
# print("\n")
# print("Working circle dia2")
# print(a.workCirDia2())