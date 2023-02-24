from django.shortcuts import render
from io import BytesIO
# Create your views here.
from .splitter import ExcelSplitter
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import FormView
from datetime import date, timedelta
from .forms import SplitForm
from django.http import HttpResponse, HttpResponseBadRequest
import pandas as pd

# Create your views here.

class SplitAndZipView(FormView):
    form_class = SplitForm
    template_name = 'split.html'
    success_url = '/'

    def form_valid(self, form):
        uploaded_file = form.cleaned_data['file']
        buffer = BytesIO(uploaded_file.read())
        # Use pandas to read the contents of the file into a DataFrame
        if uploaded_file.name.endswith('.csv'):
            # If the file is a CSV, use read_csv() method
            df = pd.read_csv(buffer)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            # If the file is an Excel file, use read_excel() method
            df = pd.read_excel(buffer)
        else:
            # Handle unsupported file types
            raise ValueError("Unsupported file type")

        column = form.cleaned_data['column_name']

        splitter = ExcelSplitter(df, column)
        splitter.create_dir()
        splitter.group_by_column()
        splitter.write_to_dir()
        output_filename = splitter.zip_dir()

        with open(output_filename, "rb") as f:
            response = HttpResponse(f.read(), content_type="application/zip")
            response["Content-Disposition"] = f"attachment; filename={output_filename}"
            return response

    def form_invalid(self, form):
        print(form.data)
        return HttpResponseBadRequest("Invalid form data.")
