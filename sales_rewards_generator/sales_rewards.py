from .invoicegenerator import InvoiceGenerator 
import os 
from pathlib import Path 
import pandas as pd 
from pathlib import Path
from os import path
from zipfile import ZipFile

import pendulum
from dataclasses import dataclass


## Startup a Django APP
## Username Login
## Combine Products

@dataclass
class SalesRewards:
    dataframe: pd.DataFrame
    COMPANY_NAME: str = 'Catalytic Connections (Pty) Ltd'
    COMPANY_LOGO: str = "https://static.wixstatic.com/media/65a092_8ff816bb1012478d8f5273532e878327~mv2.png/v1/fill/w_324,h_146,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/Logo%20blue%20no%20slogan.png"
    GROUP_BY_KEY: str = 'Dealer Code'


    def create_dir(self) -> None:
        directory = os.path.join(f"Sales Rewards - {pendulum.now().to_datetime_string()}")
        os.makedirs(directory, exist_ok=True)
        self.directory = directory 

    def get_dealer_codes(self) -> None:
        self.dealer_codes = self.dataframe[self.GROUP_BY_KEY].drop_duplicates().reset_index(drop=True).to_list()

    def get_groups(self) -> None:
        self.groups = self.dataframe.groupby(self.GROUP_BY_KEY)

    def generate_pdf(self, dealer: str) -> None:
        reward_file = self.groups.get_group(dealer)
        products = reward_file[['Product Name', 'Quantity', 'Once Off Sales Reward Excl. VAT', 'Customer Code', 'Customer Name']].to_dict('records')
        dealer_name =  reward_file['Dealer Name'].values[0]
        vat = float(15) if reward_file['VAT Number'].values[0] > 1 else 0

        ## When the script loops, insert tax rate per dealer
        invoice = InvoiceGenerator(
            sender=self.COMPANY_NAME,
            to=f'{dealer}: {dealer_name}',
            logo=self.COMPANY_LOGO,
            tax=f'{vat}'
        )

        # Renaming normal invoice headers to Catalytic standard
        invoice.set_template_text("header", 'Sales Rewards')
        invoice.set_template_text('to_title', 'Rewarded to')
        invoice.set_template_text('item_header', 'Product')


        # Add a for-loop to loop through each product in the products list and add each product w/ descriptions
        for product in products:
            if product['Once Off Sales Reward Excl. VAT'] > 0:
                invoice.add_item(
                    name=product['Product Name'],
                    description=f"{ product['Customer Code'] } - {product['Customer Name']}",
                    quantity=product['Quantity'],
                    unit_cost=product['Once Off Sales Reward Excl. VAT'],
                )
            else:
                pass

        invoice.toggle_subtotal(shipping=False)

        invoice.download(f'{self.directory}/{dealer} rewards.pdf')
     
    def zip_dir(self):
        output_filename = 'Archive.zip'
        with ZipFile(output_filename, 'w') as zip_obj:
            for folderName, _, filenames in os.walk(self.directory):
                for filename in filenames:
                    #create complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)
                    # Add file to zip
                    zip_obj.write(filePath, os.path.basename(filePath))
        
        return output_filename

