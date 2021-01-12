# dataWrangler.py - Antonio J. Leal
# Last review: 10/01/2021

class DataWrangler:
    import pandas as pd
    
    # This list will be used by several methods
    common_countries = []

    def clean_temp_data(self, start_date, end_date, data):
        """ Cleans and prepares tempearture raw data for analysis

        Args: 
            "start_date" / "end_date" [(str)] - Start and end dates (self explanatory)
            "data" [(dataframe)] - Raw temperature dataframe 

        Returns:
            The cleaned dataframe
        """
        #Remove non-common countries and undesired columns
        data = data.loc[data["Country"].isin(self.common_countries)]
        data = data.drop(columns=["AverageTemperatureUncertainty"])

        #Change 'Year' column type to datetime and filtering dates
        data["dt"] = self.pd.to_datetime(data["dt"])
        data = data.loc[(data["dt"] >= start_date) & (data["dt"] <= end_date)]

        #Reformat temperature data
        aux = data.loc[data["Country"] == self.common_countries[0]]
        aux.rename(columns={"dt":"Date","AverageTemperature":self.common_countries[0]}, inplace=True)
        aux.drop(columns="Country", inplace = True)

        #Add all countries
        for i in range(len(self.common_countries)):
            aux[self.common_countries[i]] = list(data.loc[data["Country"] == self.common_countries[i]]["AverageTemperature"])
        
        #Reset dataframe indexes
        aux.set_index("Date", inplace=True)

        #Check message
        print(">> Temperature data is cleaned and ready.")

        #Return cleaned dataframe
        return aux

    def common_countries_check(self, CO2_data, temp_data):
        """ Generates a list with the countrys that are in both dataframes

        Args: 
            "temp_data" [(dataframe)] - Temperature data
            "CO2_data" [(dataframe)] - CO2 emission data

        Returns:
            None
        """
        CO2_country_list = list(CO2_data["Country Name"])
        temp_country_list = list(temp_data["Country"].unique())

        for country in CO2_country_list:
            if country in temp_country_list:
                self.common_countries.append(country)

        print(">> The list with common countries has been generated with", len(self.common_countries), "elements.")

    def clean_CO2_data(self, data):
        """ Cleans and prepares CO2 raw data for analysis

        Args: 
            "data" [(dataframe)] - Raw CO2 dataframe 

        Returns:
            The cleaned dataframe
        """
        #Delete undesired columns from CO2_data_raw
        CO2 = data.drop(columns=["Country Code", "Indicator Name", "Indicator Code"]).iloc[:,:-5]

        #Delete rows with NaN values from CO2_data
        CO2.dropna(axis=0, how="any", inplace=True)
        CO2.reset_index(inplace=True, drop=True)

        #Transpose data and setting Country names as column label
        columns = list(CO2["Country Name"])
        CO2 = CO2.transpose()
        CO2.columns = columns
        CO2.drop(index="Country Name", inplace = True)
        CO2["Year"] = CO2.index

        #Reorder columns
        CO2 = CO2[["Year"]+columns]

        #Change 'Year' column type to datetime
        CO2["Year"] = self.pd.to_datetime(CO2["Year"])

        #Reset and ordering dataframe indexes
        CO2.set_index("Year", inplace=True)
        CO2.sort_index(axis=1, inplace=True)

        #Drop columns with not common countries
        CO2 = CO2.loc[:, CO2.columns.isin(self.common_countries)]

        #Drop non-country column
        CO2.drop(columns=["North America"], inplace=True)

        #Change data type to float
        for column in list(CO2.columns):
            try:
                CO2[column] = self.pd.to_numeric(CO2[column])
            except:
                print(column)

        #Update common countries list
        self.common_countries = list(CO2.columns)

        #Check message
        print(">> CO2 data is cleaned and ready.")

        #Return cleaned dataframe
        return CO2

    def clean_coord_data(self, data):
        """ Cleans and prepares coordinates raw data for analysis

        Args: 
            "data" [(dataframe)] - Raw coordinates dataframe 

        Returns:
            The cleaned dataframe
        """
        #Drop and renaming columns
        data.drop(columns="country", inplace=True)
        data.rename(columns={"latitude":"Lat", "longitude":"Lon", "name":"Country"}, inplace=True)

        #Remove non-common countries
        data = data.loc[data["Country"].isin(self.common_countries)]

        #Reshapedataset
        data = data.set_index("Country")
        data = data.T
        data.sort_index(axis=1, inplace=True)

        #Check message
        print(">> Coordinate data is cleaned and ready.")

        #Return data
        return data