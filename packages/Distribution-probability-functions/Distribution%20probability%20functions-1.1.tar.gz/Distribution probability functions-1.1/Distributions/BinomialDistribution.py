
import math

import matplotlib.pyplot as plt 
from GeneralDistributions import Distribution


class Binomial(Distribution):

    """ Binomial distribution class for calculating and 
    visualizing a Binomial distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
                
    """

    def __init__(self, p =0.5,s=20):

        self.prob = p
        self.size = s

        Distribution.__init__(self,self.calculate_mean(),self.calculate_stdev())

        
    

    def calculate_mean(self):
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """

        self.mean = self.prob * self.size

        return self.mean
    
    def calculate_stdev(self):
        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """
        self.sd = math.sqrt(self.size*self.prob*(1.0 - self.prob))

        return self.sd
    

    def replace_stats_with_data(self):

        """Function to calculate p and n from the data set
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """

        """total_positive_occ =0
        for d in self.data_list:
            if d == 1:
                total_positive_occ += 1
        
        self.size = sum(self.data_list)

        self.prob = 1.0 * total_positive_occ/self.size
        
        self.mean = self.calculate_mean(self)
        self.sd = self.calculate_stdev(self)"""

        self.size = len(self.data_list)
        self.prob = 1.0* sum(self.data_list)/len(self.data_list)
        self.mean = self.calculate_mean()
        self.sd = self.calculate_stdev()

        return self.prob , self.size


    def plot_bar(self):

        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
        """
        total_positive_value = 0
        total_negative_value = 0
        Y_count = []
        X_count = []

        for d in self.data_list:
            if d == 1:
                total_positive_value += 1
            else:
                total_negative_value += 1
        
        X_count.append(0)
        X_count.append(1)
        Y_count.append(total_negative_value * (1.0 - self.prob))
        Y_count.append(total_positive_value * self.prob)"""

        plt.bar(x=['0','1'],height=[(1.0 - self.prob)*self.size,self.prob*self.size])
        plt.title('Binomial distribution')
        plt.xlabel('Occurence of element')
        plt.ylabel('total occurence of element')
        

    def pdf(self,k):
        """Probability density function calculator for the gaussian distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """
        remaining_value = self.size - k
        probable = math.pow(self.prob,k)* math.pow(1-self.prob,remaining_value)
        pdf = math.factorial(self.size)/(math.factorial(k)* (math.factorial(remaining_value)))*probable
        return pdf

    def plot_bar_pdf(self):

        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
        x = []
        y = []
        
        # calculate the x values to visualize
        for i in range(self.size + 1):
            x.append(i)
            y.append(self.pdf(i))

        # make the plots
        plt.bar(x, y)
        plt.title('Distribution of Outcomes')
        plt.ylabel('Probability')
        plt.xlabel('Outcome')

        plt.show()

        return x, y

    def __add__(self, other):
        """Function to add together two Binomial distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """
        try:
            assert self.prob == other.prob, 'p values are not equal'
        except AssertionError as error:
            raise
        
        result = Binomial()
        result.size = self.size + other.size
        result.prob = self.prob + other.prob
        result.calculate_mean()
        result.calculate_stdev()

        return result
    
    def __repr__(self):
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Gaussian
        
        """
        return "mean {}, standard deviation {}, p {}, n {}".\
        format(self.mean, self.stdev, self.p, self.n)







    