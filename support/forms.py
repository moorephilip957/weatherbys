from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "subject",
            "priority",
            "category",
            "message",
            "attachment",
        ]

        widgets = {
            "subject": forms.TextInput(attrs={
                "class": "form-input",
                "id": "subject",
                "placeholder": "Briefly describe your issue",
                "autocomplete": "off",
                "maxlength": "255",
            }),

            "priority": forms.Select(attrs={
                "class": "form-select",
                "id": "selectPriority",
            }),

            "category": forms.Select(attrs={
                "class": "form-select",
                "id": "selectCategory",
            }),

            "message": forms.Textarea(attrs={
                "class": "form-textarea",
                "id": "message",
                "placeholder": "Please provide all relevant details about your issue so we can help you better",
                "autocomplete": "off",
                "rows": 6,
                "maxlength": "2000",
            }),

            "attachment": forms.ClearableFileInput(attrs={
                "class": "form-input",
                "id": "attachment",
                "accept": ".png,.jpg,.jpeg,.pdf,.doc,.docx",
            }),
        }

        labels = {
            "subject": "Subject",
            "priority": "Priority",
            "category": "Category",
            "message": "Description",
            "attachment": "Attachments",
        }