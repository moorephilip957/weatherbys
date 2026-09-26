from django import forms
from .models import LoanApplication
from customer.models import UserBankAccount
from django.contrib.auth.hashers import check_password

class LoanApplicationForm(forms.ModelForm):

    transaction_pin = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": "Enter your 6-digit PIN",
                "autocomplete": "off",
                "maxlength": "6",
                "inputmode": "numeric",
                "pattern": "[0-9]*",
            }
        ),
        required=True,
        label="Transaction PIN"
    )

    class Meta:
        model = LoanApplication

        fields = [
            'loan_type',
            'amount',
            'duration_months',
            'purpose',
            'monthly_net_income',
        ]

        widgets = {

            'loan_type': forms.Select(attrs={
                'class': 'form-select',
            }),

            'amount': forms.NumberInput(attrs={
                'class': 'form-input amount-input',
                'placeholder': '0.00',
                'min': '500',
                'max': '50000',
                'step': '100',
                'inputmode': 'decimal',
            }),

            'duration_months': forms.Select(
                choices=[
                    (3, '3 Months'),
                    (6, '6 Months'),
                    (12, '12 Months'),
                    (24, '24 Months'),
                    (36, '36 Months'),
                    (48, '48 Months'),
                    (60, '60 Months'),
                    (84, '84 Months'),
                ],
                attrs={
                    'class': 'form-select',
                }
            ),

            'purpose': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Please describe the purpose of this loan...',
                'rows': 4,
                'maxlength': '500',
            }),

            'monthly_net_income': forms.Select(attrs={
                'class': 'form-select',
            }),
        }

        labels = {
            'amount': 'Loan Amount',
            'duration_months': 'Duration (Months)',
            'loan_type': 'Credit Facility',
            'purpose': 'Purpose of Loan',
            'monthly_net_income': 'Monthly Net Income',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get("transaction_pin")
        amount = cleaned_data.get("amount")

        if not self.user:
            raise forms.ValidationError("User not authenticated.")

        # Validate PIN
        if pin:
            try:
                account = UserBankAccount.objects.get(user=self.user)
                if not check_password(str(pin), account.transaction_pin):
                    raise forms.ValidationError("Invalid transaction PIN.")
            except UserBankAccount.DoesNotExist:
                raise forms.ValidationError("Bank account not found.")

        # Validate amount range
        if amount:
            if amount < 500:
                raise forms.ValidationError("Minimum loan amount is $500.")
            if amount > 50000:
                raise forms.ValidationError("Maximum loan amount is $50,000.")

        return cleaned_data