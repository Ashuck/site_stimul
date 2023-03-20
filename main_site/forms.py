from django.forms import ModelForm
from main_site.models import FeedbackContact, FileForSearch


class FeedBackForm(ModelForm):
    class Meta:
        model = FeedbackContact
        fields = [
            "fio",
            "firm_name",
            "phone",
            "email"
        ]


class SearchFromFileForm(ModelForm):
    class Meta:
        model = FileForSearch
        fields = [
            "search_file"
        ]