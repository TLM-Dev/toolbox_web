import pandas as pd
import zipfile
from smtplib import SMTP
import tempfile
from io import BytesIO
import os
from django.views.generic.edit import FormView
from .forms import MassEmailForm
from .emailer import MassEmailer  # assuming this class is defined in another file

class MassEmailView(FormView):
    form_class = MassEmailForm
    template_name = 'mail.html'
    success_url = '/'

    def form_valid(self, form):
        sender = form.cleaned_data['sender']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        cc = form.cleaned_data['cc']
        recipients_file = form.cleaned_data['recipients']
        attachments = form.cleaned_data['attachments']
        server = SMTP(host='relay.p8mail.io', port=587, local_hostname='localhost')
        server.starttls()
        server.login(user='relay@masters.co.za', password='t5YHG78964')
    
        recipients = None
        # Read the recipients file
        with recipients_file.open(mode='rb') as f:
            buffer = BytesIO(f.read())
            if recipients_file.name.endswith('.csv'):
                recipients = pd.read_csv(buffer)
            elif recipients_file.name.endswith(('.xls', '.xlsx')):
                recipients = pd.read_excel(buffer)
            else:
                # Handle unsupported file types
                raise ValueError("Unsupported file type")

        if recipients is None:
            raise ValueError("Failed to read recipients file")

        with tempfile.TemporaryFile() as tmp_file:
            # Write the zip file to a temporary file
            for chunk in attachments.chunks():
                tmp_file.write(chunk)
            tmp_file.seek(0)

            # Unzip the files and create a DataFrame from them
            with zipfile.ZipFile(tmp_file, 'r') as zipf:
                file_list = zipf.namelist()
                file_names = [os.path.splitext(os.path.basename(name))[0].strip() for name in file_list]
                for file in file_list:
                    file_key = os.path.splitext(os.path.basename(file))[0].strip()
                    with zipf.open(file) as f:
                        email_addresses = list(recipients.loc[recipients['AccountCode'] == file_key, 'EmailAddress'].values)
                        mail = MassEmailer(
                            file_key,
                            sender,
                            email_addresses,
                            f"{file_key}: {subject}",
                            message,
                            server=server,  # assuming server is not defined in this scope
                            file=f,
                            cc=[cc],
                        )
                        mail.run()

        return super().form_valid(form)
