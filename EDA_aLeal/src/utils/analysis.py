# analysis.py - Antonio J. Leal
# Last review: 10/01/2021

class Analysis:
    import pandas as pd
    import sklearn.linear_model as lm
    import sklearn.metrics as metrics

    def get_correlations(self, temp_data, CO2_data):
        """ Generates a data frame with correlation info. between temperature and CO2 database for each country

        Args: 
            "temp_data" [(dataframe)] - Temperature data
            "CO2_data" [(dataframe)] - CO2 emission data

        Returns:
            The generated dataframe
        """
        # Get start and end dates
        min = CO2_data.index.min().strftime(r"%Y-%m-%d")
        max = temp_data.index.max().strftime(r"%Y-%m-%d")

        # Prepare dataframes for correlations
        CO2_data = CO2_data.loc[CO2_data.index <= max]
        temp_data = temp_data.loc[(temp_data.index >= min)]
        temp_data = temp_data.resample("AS").mean()

        # Calculate correlations
        corr = []
        for column in CO2_data.columns:
            corr.append(CO2_data[column].corr(temp_data[column], method="pearson"))

        # Generate and return dataframe
        r = range(len(CO2_data.columns))
        index = [i for i in r]

        return self.generate_dataframe(["Country", "index", "corr"], [list(CO2_data.columns), index, corr])

    def get_regression_data(self, temp_by_year, CO2_data):
        """ Generates a data frame with temperature regression and CO2 data for each country

        Args: 
            "temp_by_year" [(dataframe)] - Temperature data resampled by year
            "CO2_data" [(dataframe)] - CO2 emission data

        Returns:
            The generated dataframe
        """
        # Fill dict_list with desired data
        dict_list = []
        columns = list(temp_by_year.columns)
        for column in columns:
            dict_list.append({"Slope": self.linear_regression_slope(self.series_to_2D_array(temp_by_year.index.year), self.series_to_2D_array(temp_by_year[column])),\
                              "CO2_Mean":CO2_data[column].mean(), \
                              "R2":self.get_r2_score(self.series_to_2D_array(temp_by_year.index.year), self.series_to_2D_array(temp_by_year[column])), \
                              "Country":column})

        # Return dataframe created from dickt_list
        return self.pd.DataFrame(dict_list)

    def generate_dataframe(self, columns, data):
        """ Generates a Dataframe with given columns / data

        Args: 
            "columns" [(list)] - List of strings with the names of the column
            "data" [(list)] - List of lists with each row info

        Returns:
            The generated dataframe
        """
        # Construct a dictionary
        dictionary = {}
        for i in range(len(columns)):
            dictionary[columns[i]] = data[i]

        # Return dataframe
        return self.pd.DataFrame(dictionary)

    def get_r2_score(self, x, y):
        """ Gets linear regression R2 score

        Args: 
            "x" [(2D array)] - X axis data
            "y" [(2D array)] - Y axis data

        Returns:
            R2 score
        """
        # Calculates linear regression
        regression = self.lm.LinearRegression()
        regression.fit(x, y)
        y_predict = regression.predict(x)

        # Returns R2 score
        return self.metrics.r2_score(y, y_predict)

    def linear_regression_slope(self, x, y):
        """ Gets linear regression slope value

        Args: 
            "x" [(2D array)] - X axis data
            "y" [(2D array)] - Y axis data

        Returns:
            Value for the linear regression slope
        """
        # Calculates linear regression
        regression = self.lm.LinearRegression()
        regression.fit(x, y)
        
        # Return slope
        return regression.coef_[0,0]

    def get_prediction(self, x, y):
        """ Gets predicted 'y' values for linear regression

        Args: 
            "x" [(2D array)] - X axis data
            "y" [(2D array)] - Y axis data

        Returns:
            Value for the linear regression slope
        """
        # Calculates linear regression
        regression = self.lm.LinearRegression()
        regression.fit(x, y)

        # Return prediction
        return regression.predict(x)

    def regression_data(self, x, y):
        """ Gets required regression data (prediction, slope, r2 score)

        Args: 
            "x" [(2D array)] - X axis data
            "y" [(2D array)] - Y axis data

        Returns:
            List with the above mentioned values
        """
        # Transforms lists into 2dArrays
        x = self.series_to_2D_array(x)
        y = self.series_to_2D_array(y)

        # Calculate regression and values
        regression = self.lm.LinearRegression()
        regression.fit(x, y)
        y_predict = regression.predict(x)
        r2_score = self.metrics.r2_score(y, y_predict)
        slope = regression.coef_[0,0]

        return [y_predict, r2_score, slope]
        
    def bound_data(self, temp_data, co2_data):
        """ Generates a data frame with temperature and CO2 emission minimum and maximum values for each country

        Args: 
            "temp_data" [(dataframe)] - Temperature data
            "CO2_data" [(dataframe)] - CO2 emission data

        Returns:
            The generated dataframe
        """
        # Initializing list
        rows = []

        # Getting bounds from data
        columns = list(temp_data.columns)
        for column in columns:
            rows.append({"T_Min":temp_data[column].min(), "T_Max":temp_data[column].max(), "CO2_Min":co2_data[column].min(), "CO2_Max":co2_data[column].max(), "Country":column})

        # Returning dataframe
        return self.pd.DataFrame(rows)

    def mean_by_year(self, data, start_date="1000-01-01", end_date="3000-01-01"):
        """ Resamples monthly sampled dataframe into yearly basis within selected dates

        Args: 
            "data" [(dataframe)] - Monthly sampled dataframe
            "start_date" / "end_date" [(str)] - Start and end dates (self explanatory)

        Returns:
            The resampled dataframe
        """
        # Select date range
        data = data.loc[(data.index >= start_date) & (data.index <= end_date)]

        # Return resampled dataframe 
        return data.resample("AS").mean()

    def series_to_2D_array(self, x):
        """ Transform a Series object into 2D array

        Args: 
            "x" [(Series)] - The Series to be transformed

        Returns:
            The generated 2D array
        """
        # Transform series into list
        x = list(x)

        # Generate 2D Array
        array_2D= []
        for item in x:
            array_2D.append([item])

        return array_2D

