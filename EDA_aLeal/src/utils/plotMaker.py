# plotMaker.py - Antonio J. Leal
# Last review: 10/01/2021

class PlotMaker:
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    from mpl_toolkits.basemap import Basemap
    
    def make_column_lineplot(self, data, data_name):
        """ Makes lineplots for each column to check tendencies. Saves the plots to "..\\reports\\plots\\lineplots\\"

        Args: 
            "data" [(DataFrame)] - DataFrame to be plotted
            "data_name" [(str)] - "T" for temperature and "CO2" for gas emission

        Returns:
            None
        """
        # Loop through column list
        columns = list(data.columns)
        for column in columns:
            # Set histogram
            plot = self.sns.lineplot(data= data, x=data.index, y=data[column])
            if data_name == "CO2":
                plot.set(xlabel= "Date", ylabel= "CO2 emission", title= column)
            else:
                plot.set(xlabel= "Date", ylabel= "Temperature", title= column)

            # Save plot to path
            self.plt.show()
            plot.figure.savefig("..\\reports\\plots\\lineplots\\" + data_name + "\\" + column + ".jpg")
    
    def make_column_histogram(self, data, data_name, period, bins=5):
        """ Makes histograms for each column as the task asks for. Saves the plots to "..\\reports\\plots\\histograms\\"
            The plots includes the width of the resulted bins.

        Args: 
            "data" [(DataFrame)] - DataFrame to be plotted
            "data_name" [(str)] - "T" for temperature and "CO2" for gas emission
            "period" [(str)] - "Year" if the data is yearly based. "Month" otherwise
            "bins" [(int)] - Number of desired bins

        Returns:
            None
        """
        # Loop through column list
        columns = list(data.columns)
        for column in columns:
            # Calculate bin width in order to show it in the plot
            bin_width = round((data[column].max() - data[column].min()) / bins, 2)

            # Set histogram
            histo = self.sns.displot(data[column], bins=5)
            if data_name == "CO2":
                histo.set(xlabel= "Tons/capita (bin size = " + str(bin_width) + ")", ylabel= period + " count", title= column)
            else:
                histo.set(xlabel= "Temperature (bin size = " + str(bin_width) + ")", ylabel= period + " count", title= column)

            # Save plot to path
            histo.savefig("..\\reports\\plots\\histograms\\" + data_name + "\\" + column + ".jpg")

    def make_correlation_line(self, dataframe, title, x_label, y_label, path, threshold = False, top = 0, bottom = 0):
        """ Makes a line plot with the correlations between CO2 and temperature dataframes. Saves it to file.

        Args: 
            "dataframe" [(DataFrame)] - DataFrame to be plotted
            "title" [(str)] - Plot title
            "x_label" [(str)] - Label for x axis
            "y_label" [(str)] - Label for y axis
            "path" [(str)] - Relative path to save the figure
            "threshold" [(bool)] - True to include thresholds. False otherwise (default)
            "top" / "bottom" [(float)] - Top and bottom thresholds values (0 default, not used if threshold == False)

        Returns:
            None
        """
        # Make line plot
        plot = self.sns.lineplot(x="index", y="corr", data=dataframe)

        # Include threshold lines or not
        if threshold:
            plot.axhline(top, ls="--", color="r")
            plot.axhline(bottom, ls="--", color="r")
        
        # Set y axis limits and other parameters
        plot.set(ylim=(-1,1), xlabel=x_label, ylabel=y_label, title=title)

        # Save plot to path
        plot.figure.savefig(path)

    def make_histogram(self, data, x, bins, x_label, y_label, title, path):
        """ Makes an histrogram from single dataframe column. Saves figure to file.

        Args: 
            "data" [(DataFrame)] - DataFrame to be plotted
            "x" [(str)] - Column name
            "x_label" [(str)] - Label for x axis
            "y_label" [(str)] - Label for y axis
            "title" [(str)] - Plot title
            "path" [(str)] - Relative path to save the figure

        Returns:
            None
        """
        # Make plot and set parameters
        histo = self.sns.displot(data=data, x=data[x], bins=bins)
        histo.set(xlabel=x_label, ylabel=y_label, title=title)

        # Includes top and right borders
        self.sns.despine(top=False, right=False)
        
        # Save plot to path
        histo.savefig(path)

    def make_scatter_plot(self, data, x, y, x_label, y_label, title, path):
        """ Makes an scatterplot from two dataframe columns. Saves figure to file.

        Args: 
            "data" [(DataFrame)] - DataFrame to be plotted
            "x" / "y" [(str)] - Columns names
            "x_label" [(str)] - Label for x axis
            "y_label" [(str)] - Label for y axis
            "title" [(str)] - Plot title
            "path" [(str)] - Relative path to save the figure

        Returns:
            None
        """
        # Make scatter plot and set parameters
        scatter = self.sns.scatterplot(data=data, x=x, y=y)
        scatter.set(xlabel=x_label, ylabel=y_label, title=title)
        scatter.figure.savefig(path)

    def plot_scatter_regression(self, x, y, x_label, y_label, title, path, y_predicted=None):
        """ Makes an scatterplot from two dataframe columns, includes linear regression prediction. Saves figure to file.

        Args: 
            "data" [(DataFrame)] - DataFrame to be plotted
            "x" / "y" [(str)] - Columns names
            "x_label" [(str)] - Label for x axis
            "y_label" [(str)] - Label for y axis
            "title" [(str)] - Plot title
            "path" [(str)] - Relative path to save the figure
            "y_predicted" [(Series)] - Linear regression prediction

        Returns:
            None
        """
        # Make plot and set parameters
        plot = self.plt.scatter(x, y)
        self.plt.xlabel(x_label)
        self.plt.ylabel(y_label)
        self.plt.title(title)

        # Linear regression included (or not)
        if y_predicted is not None:
            self.plt.plot(x, y_predicted, color="r")

        # Save plot to path
        self.plt.show()
        plot.figure.savefig(path)

    def make_bounds_plot(self, data, dataType, x_label, y_label, title, path):
        """ Combines two line plots for minimum and maximum data. Saves it to file

        Args: 
            "data" [(DataFrame)] - DataFrame to be plotted
            "dataType" [(str)] - "T" for Temperature, "CO2" otherwise
            "x_label" [(str)] - Label for x axis
            "y_label" [(str)] - Label for y axis
            "title" [(str)] - Plot title
            "path" [(str)] - Relative path to save the figure

        Returns:
            None
        """
        # Sort dataframe for correct visualization
        data = data.sort_values(by=dataType+"_Min")
        data = data.reset_index(drop=False)

        # Make upper/lower bound line plots and set parameters
        plot = self.sns.lineplot(x=data.index, y=data[dataType+"_Min"])
        self.sns.lineplot(x=data.index, y=data[dataType+"_Max"])
        plot.set(xlabel= x_label, ylabel= y_label, title=title)

        # For Temperature, find highest and lowest
        if (dataType == "T"):
            self.sns.scatterplot(x=[0, 30], y=[-37.177, 37.750])
            plot.text(2, -37.1, "Greenland")
            plot.text(32, 37.7, "UAE")

        # For CO2, find tops
        if (dataType == "CO2"):
            tops = data.loc[data["CO2_Max"] > 80]
            self.sns.scatterplot(x=tops.index, y=tops["CO2_Max"])
            plot.text(82, 360.853233, "Aruba")
            plot.text(17, 99.464612, "Qatar")
            plot.text(102, 100, "UAE")

        # Save plot to path
        self.plt.show()
        plot.figure.savefig(path)

    def plot_map(self, coord_data, CO2_data, scale, path):
        """ Plots map with CO2 emission data. Saves de figure to file

        Args: 
            "coord_data" [(DataFrame)] - DataFrame with latitude and longitude for each country
            "CO2_data" [(DataFrame)] - Cleaned CO2 emission dataframe
            "scale" [(float)] - Adjustment value for representation
            "path" [(str)] - Relative path to save the figure

        Returns:
            None
        """
        # Get country and year lists
        countries = list(coord_data.columns)
        
        # Extract longitude and latitude data
        lat = []
        lon = []
        for country in countries:
            lat.append(coord_data.iloc[0, coord_data.columns.get_loc(country)])
            lon.append(coord_data.iloc[1, coord_data.columns.get_loc(country)])

        # Extract CO2 data for size
        CO2 = []
        for country in countries:
            CO2.append(CO2_data.mean()[country])
        CO2 = [x*scale for x in CO2]

        # Make plot
        self.plt.figure(figsize=(24,12))
        map = self.Basemap()
        map.drawcoastlines()
        x, y = map(lon, lat)
        map.scatter(x, y, s=CO2, c='b')

        # Save figure
        self.plt.savefig(path)

    def pie_chart(self, path):
        """ Plots a pie chart

        Args: 
            "path" [(str)] - Relative path to save the figure

        Returns:
            None
        """
        # Generate data for pie chart
        data = {"Task":["Topic/data", "Clean data", "Plots/Analysis", "Documentation", "Learning"], "Time":[5,15,30,10,40]}
        data = self.pd.DataFrame(data)

        # Make pie chart
        fig, ax = self.plt.subplots()
        self.plt.pie(x=data["Time"], labels=data["Task"], autopct="%1.1f%%", shadow=True, startangle=90)
        ax.axis('equal')
        self.plt.tight_layout()

        # Save figure to file
        self.plt.savefig(path)