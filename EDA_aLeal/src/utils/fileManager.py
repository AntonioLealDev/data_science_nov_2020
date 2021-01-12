# plotMaker.py - Antonio J. Leal
# Last review: 10/01/2021

class FileManager:
    import pandas as pd

    def file_to_df(self, file_path):
        """ Reads a csv file and generates a dataframe.

        Args: 
            "file_path" [(str)] - Relative path where the file is stored

        Returns:
            The generated dataframe
        """
        try:
            df = self.pd.read_csv(file_path)
            print(">> Dataframe succesfully generated from:", file_path)
            return df
        except FileNotFoundError:
            print("File not Found.")


    def df_to_file(self, data, file_path):
        """ Saves df to csv file

            Args:
                "data" [(pandas.dataframe)] - Dataframe to be saved
                "file_path" [(str)] - Relative path where the data is saved

            Returns:
                None
        """
        try:
            print(">> Dataframe succesfully saved at:", file_path)
            data.to_csv(path_or_buf=file_path, mode="w")
        except:
            print("The data could not be saved to file.")