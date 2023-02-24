import pandas as pd
import os
from os.path import basename
import pendulum
from zipfile import ZipFile
from dataclasses import dataclass

@dataclass
class ExcelSplitter:
    dataframe: pd.DataFrame
    column: str
    keys: str = ""
    groups: pd.Grouper = ""

    def create_dir(self) -> None:
        directory = os.path.join(f"{self.column}-{pendulum.now().to_datetime_string()}")
        os.makedirs(directory, exist_ok=True)
        self.directory = directory
         
    def group_by_column(self) -> None:
        self.keys = pd.unique(self.dataframe[f'{self.column}'])
        self.groups = self.dataframe.groupby(f'{self.column}')
        
    def write_to_dir(self) -> None:
        try:
            for key in self.keys:
                group = self.groups.get_group(f"{key}")
                group.to_excel(f"{self.directory}/{key}.xlsx", index=False)
        except KeyError as error:
            pass

    def zip_dir(self):
        output_filename = 'Archive.zip'
        with ZipFile(output_filename, 'w') as zip_obj:
            for folderName, _, filenames in os.walk(self.directory):
                for filename in filenames:
                    #create complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)
                    # Add file to zip
                    zip_obj.write(filePath, basename(filePath))
        
        return output_filename
    

    # def run(self):
    #     self.folder_name = self.create_dir()
    #     self.group_by_column()
    #     self.write_to_dir()
    #     self.zip_dir()


