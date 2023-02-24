import os
import zipfile
import tempfile
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import FormView
from datetime import date, timedelta
from .forms import ZipForm
from django.http import HttpResponse, HttpResponseBadRequest
import pandas as pd

# Create your views here.

class UnzipAndConcatenateView(FormView):
    form_class = ZipForm
    template_name = 'form.html'
    success_url = '/'

    def form_valid(self, form):
        # Save the uploaded ZIP file to a temporary file
        with tempfile.TemporaryFile() as tmp_file:
            for chunk in form.cleaned_data['zip_file'].chunks():
                tmp_file.write(chunk)
            tmp_file.seek(0)

            # Unzip the files and create a DataFrame from them
            with zipfile.ZipFile(tmp_file, 'r') as zipf:
                file_list = zipf.namelist()
                dfs = []
                for file in file_list:
                    with zipf.open(file) as f:
                        df = pd.read_excel(f)
                        dfs.append(df)
                if form.cleaned_data['option'] == 'sheet':
                    print("Concatenating dataframes")
                    df_concat = pd.concat(dfs)
                    print("Writing to Excel")
                    output_filename = 'concatenated_to_sheet.xlsx'
                    df_concat.to_excel(output_filename, index=False)
                    print("Done")
                elif form.cleaned_data['option'] == 'workbook':
                    output_filename = 'concatenated_to_workbook.xlsx'
                    with pd.ExcelWriter(output_filename) as writer:
                        for i, df in enumerate(dfs):
                            sheet_name = os.path.splitext(file_list[i])[0]
                            df.to_excel(writer, sheet_name=sheet_name)
                else:
                    return HttpResponseBadRequest("Invalid option selected.")

            # Send the file as a download
            with open(output_filename, "rb") as f:
                response = HttpResponse(f.read(), content_type="application/vnd.ms-excel")
                response["Content-Disposition"] = f"attachment; filename={output_filename}"
                return response

    def form_invalid(self, form):
        return HttpResponseBadRequest("Invalid form data.")
