import math
import matplotlib.pyplot as plt
from GeneralDistributions import Distribution

class Gaussian(Distribution):
    
    """Gaussian class to calculate and visualize the gaussian distribution
    
    Attributes:
        mean(μ) => float, represents the mean of the distribution
        sd (σ)=> float, represents the standard deviation of the distribution
        data_list => list of floats, a data that extracted from the input file
    """

    def __init__(self, gaussian_mean=0 , gaussian_sd=1 ):
        
        super().__init__(gaussian_mean,gaussian_sd)



    def calculate_mean(self):
        
        """Calculates the mean of the data list set
        
        Args:
            none
        Return:
            mean of the data set
        """
        average = 1.0 * sum(self.data_list)/ len(self.data_list)

        self.mean = average

        return self.mean
    
    def calculate_standardDeviation(self, sample = True):

        """Calculates the standard deviation of the data list set
        
        Args:
            sample: boolean to classify the data as sample or population
        Return:
            returns a float of standard deviation
        
        """

        if sample:
            no_sample = len(self.data_list) -1
        else:
            no_sample = len(self.data_list)

        mean = self.mean

        variance = 0

        for x in self.data_list:
            variance += (x-mean) ** 2 
        
        sigma = math.sqrt(variance / no_sample)

        self.sd = sigma

        return self.sd
    
    def read_data_file(self,file_Name,sample=True):

        """It is prepared to read the data set in txt form from folder
        
            But in eachline of the txt file should held one value which is float
            After that it is going to calculate the mean and standard deviation

        """
        """with open(data_file_name) as file:
            
            data_file = []
            line = file.readline()

            while line:
                data_file.append(int(line))
                line = file.readline()
            file.close()

            self.data_list = data_file
            self.mean = self.calculate_mean()
            self.sd = self.calculate_standardDeviation(sample)"""
        
        data = Distribution.read_data_file(self,file_Name)
        self.data_list = data
        self.mean = self.calculate_mean()
        self.sd = self.calculate_standardDeviation(sample)


    def plot_histogram_gaussian(self):
        """Method to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """

        plt.hist(self.data_list)
        plt.title("Histogram of guassian data")
        plt.xlabel("Data")
        plt.ylabel("Count")
        plt.show()

    def Pdf_of_gaussian(self,X):
        """Probability density function calculator for the gaussian distribution.
        
        Args:
            x (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """

        pdf = (1.0/(self.sd*(math.sqrt(2*math.pi))))*(math.exp(-0.5*((X-self.mean)/self.sd)**2))

        return pdf
    

    def plot_histogram_pdf(self, n_sample=50):
        """Method to plot the normalized histogram of the data and a plot of the 
        probability density function along the same range
        
        Args:
            n_spaces (int): number of data points 
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
        mu = self.mean
        sigma = self.sd

        min_range = min(self.data_list)
        max_range = max(self.data_list)

        interval = 1.0* (max_range - min_range) / n_sample

        x = []
        y = []

        # calculate the x values to visualize
        for i in range(n_sample):
            tmp = min_range + interval*i
            x.append(tmp)
            y.append(self.Pdf_of_gaussian(tmp))



        # make the plots
        fig, axes = plt.subplots(2,sharex=True)
        fig.subplots_adjust(hspace=.5)
        axes[0].hist(self.data_list, density=True)
        axes[0].set_title('Normed Histogram of Data')
        axes[0].set_ylabel('Density')

        axes[1].plot(x, y)
        axes[1].set_title('Normal Distribution for \n Sample Mean and Sample Standard Deviation')
        axes[0].set_ylabel('Density')
    

        return x, y
    

    def __add__(self,other):

        """Magic method to add together two Gaussian distributions
        
        Args:
            other (Gaussian): Gaussian instance
            
        Returns:
            Gaussian: Gaussian distribution
        """

        result = Gaussian()

        result.mean = self.mean + other.mean
        result.sd = math.sqrt((self.sd)**2 + (other.sd)**2)

        return result

    def __repr__(self):
        """Magic method to output the characteristics of the Gaussian instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Gaussian
        
        """

        print('Mean :{}, standard deviation : {} \n'.format(self.mean, self.sd))

