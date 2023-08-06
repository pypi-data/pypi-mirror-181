
class Distribution:


    """Gaussian class to calculate and visualize the gaussian distribution
    
    Attributes:
        mean(μ) => float, represents the mean of the distribution
        sd (σ)=> float, represents the standard deviation of the distribution
        data_list => list of floats, a data that extracted from the input file
    """

    def __init__(self, gaussian_mean=0 , gaussian_sd=1 ):
        
        self.mean = gaussian_mean
        self.sd = gaussian_sd
        self.data_list = []

    


    def read_data_file(self, data_file_name):

        """It is prepared to read the data set in txt form from folder
        
            But in eachline of the txt file should held one value which is float
            After that it is going to calculate the mean and standard deviation

        """
        with open(data_file_name) as file:
            
            data_file = []
            line = file.readline()

            while line:
                data_file.append(int(line))
                line = file.readline()
            file.close()

            self.data_list = data_file
        return self.data_list



    
    
