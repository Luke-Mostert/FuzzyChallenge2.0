import numpy as np
import math
import matplotlib.pyplot as plt


class FuzzySet:
    def __init__(self, name):
        self.name = name
        self.min = 0
        self.max = 0

    def calcMembership(self, x):
        pass
    #
    #def draw(self):
    #    pass


class Triangle(FuzzySet):
    def __init__(self, name, a, b, c):
        self.name = name
        self.a = a
        self.b = b
        self.c = c
        self.min = a
        self.max = c
        self.domain = c - a

    def calcMembership(self, x):
        if self.b == x:
            return 1
        elif self.a <= x < self.b:
            return (x - self.a) / (self.b - self.a)
        elif self.b < x <= self.c:
            return (self.c - x) / (self.c - self.b)
        else:
            return 0

    def draw(self):
        plt.figure()
        points = np.array([self.a, self.b], )
        tri = plt.Polygon()


class Trapezoid(FuzzySet):
    def __init__(self, name, a, b, c, d):
        self.name = name
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.min = a
        self.max = d
        self.domain = d - a

    def calcMembership(self, x):
        if x < self.a:
            return 0
        elif self.a <= x < self.b:
            return (x - self.a) / (self.b - self.a)
        elif self.b <= x <= self.c:
            return 1
        elif self.c < x <= self.d:
            return (self.d - x) / (self.d - self.c)
        elif self.d < x:
            return 0


class Gaussian(FuzzySet):
    def __init__(self, name, mean, std):
        self.name = name
        self.mean = mean
        self.std = std
        #min and max

    def calcMembership(self, x):
        return pow(math.e, -pow(2, (x - self.mean)) / 2 * pow(2, self.std)) #change


class Singleton(FuzzySet):
    def __init__(self, name, a):
        self.name = name
        self.a = a
        self.min = a
        self.max = a

    def calcMembership(self, x):
        if x == self.a:
            return x
        else:
            return 0



  # def Union(self, USet):
  #     pass

  # def Intersection(self, ISet):
  #     pass

  # def Complement(self):
  #     pass
