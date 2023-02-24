from io import BytesIO
from .forms import SalesRewardsForm
from .sales_rewards import SalesRewards
from django.views.generic.edit import FormView
from django.http import HttpResponse, HttpResponseBadRequest

import pandas as pd

# Create your views here.

class GeneratePDFRewardView(FormView):
    form_class = SalesRewardsForm
    template_name = 'generator.html'
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

        generator = SalesRewards(df)
        generator.create_dir()
        generator.get_dealer_codes()
        generator.get_groups()

        for dealer in generator.dealer_codes:
            generator.generate_pdf(dealer)

        output_filename = generator.zip_dir()

        with open(output_filename, "rb") as f:
            response = HttpResponse(f.read(), content_type="application/zip")
            response["Content-Disposition"] = f"attachment; filename={output_filename}"
            return response

    def form_invalid(self, form):
        return HttpResponseBadRequest("Invalid form data.")
