import math
from .Generaldistribution import Distribution


class Gaussian(Distribution):

    def __init__(self, mu=0, sigma=1):

        Distribution.__init__(self, mu, sigma)

    def calculate_mean(self):

        avg = 1.0 * sum(self.data) / len(self.data)

        self.mean = avg

        return self.mean

    def calculate_stdev(self, sample=True):

        """Function to calculate the standard deviation of the data set.

        Args:
            sample (bool): whether the data represents a sample or population

        Returns:
            float: standard deviation of the data set

        """

        if sample:
            n = len(self.data) - 1
        else:
            n = len(self.data)

        mean = self.calculate_mean()

        sigma = 0

        for d in self.data:
            sigma += (d - mean) ** 2

        sigma = math.sqrt(sigma / n)

        self.stdev = sigma

        return self.stdev

    def pdf(self, x):
        """Probability density function calculator for the gaussian distribution.

        Args:
            x (float): point for calculating the probability density function


        Returns:
            float: probability density function output
        """

        return (1.0 / (self.stdev * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - self.mean) / self.stdev) ** 2)

    def __add__(self, other):

        """Function to add together two Gaussian distributions

        Args:
            other (Gaussian): Gaussian instance

        Returns:
            Gaussian: Gaussian distribution

        """

        result = Gaussian()
        result.mean = self.mean + other.mean
        result.stdev = math.sqrt(self.stdev ** 2 + other.stdev ** 2)

        return result

    def __repr__(self):

        return "mean {}, standard deviation {}".format(self.mean, self.stdev)
