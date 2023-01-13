import numpy as np
import matplotlib.pyplot as plt
from Fuzzy_Variables import Fuzzy_Set
import random


class TSKLearning:

    def __init__(self, n):
        self.n = n

    def TSKLearn(self, epochs, compfunc):
        xk = []
        wk = []
        rules = []
        memFunctions = []
        error = []
        output = 0
        gradient = [0] * self.n
        outputX = [0] * self.n
        outputY = [0] * self.n
        for k in range(0, self.n + 2):
            xk.append(((2 * np.pi) / self.n) * (k - 1))
        for j in range(1, self.n + 1):
            memFunctions.append(Fuzzy_Set.Triangle("A" + str(j), xk[j - 1], xk[j], xk[j + 1]))
            #These two are for the initial weights. First one is for random between -1,1 and the second will be for pre determined weights
            wk.append(random.uniform(-1,1))
            #wk.append(compfunc(xk[j]))
        for i in range(epochs):
            x = np.random.rand() * (2 * np.pi)
            output = 0
            for k in range(len(wk)):
                output += wk[k] * memFunctions[k].calcMembership(x)
            for k in range(len(wk)):
                gradient[k] = (2 * (output - compfunc(x))) * memFunctions[k].calcMembership(x)
                wk[k] = wk[k] - (0.5 * gradient[k])
            error.append(TSKLearning.MSE(self,memFunctions,wk,xk,compfunc))
        for l in range(self.n):
            outputX[l] = l * ((2 * np.pi) / self.n)
            outputY[l] = wk[l] * memFunctions[l].calcMembership(l * ((2 * np.pi) / self.n))
        self.DrawError(epochs, error)
        self.DrawFunction(outputX, outputY)


    #MSE Needs work D:
    def MSE(self, memFunctions,wk,xk,compfunc):
        result = 0
        for i in range(len(xk)):
            for k in range(len(memFunctions)):
                coeff = (1/(2 * self.n))
                diff = (memFunctions[k].calcMembership(xk[i]) * wk[k]) - compfunc(xk[i])
                print(str((memFunctions[k].calcMembership(xk[i]) * wk[k])) + str(compfunc(xk[i])))
                result += coeff * (diff * diff)
        return result

    def DrawError(self, epochs, error):
        x = np.arange(0, epochs, 1)
        plt.plot(x, error)
        plt.title("Error")
        plt.show()

    def DrawFunction(self, outputX, outputY):
        x = np.arange(0, 2 * np.pi, 0.1)  # start,stop,step
        plt.plot(x, np.sin(x), label="Sin()")
        plt.plot(outputX, outputY, label="Approximation")
        plt.grid(color='k', linestyle='-', linewidth=.3)
        plt.legend(loc='upper right')
        plt.show()

