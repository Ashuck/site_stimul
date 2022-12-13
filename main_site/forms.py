from django.forms import ModelForm
from main_site.models import FeedbackContact


class FeedBackForm(ModelForm):
    class Meta:
        model = FeedbackContact
        fields = [
            "fio",
            "firm_name",
            "phone",
            "email"
        ]