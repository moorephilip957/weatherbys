from django import forms
from .models import KYCVerification
from PIL import Image

MAX_KYC_FILE_SIZE = 2 * 1024 * 1024  # 2MB


def validate_kyc_image(upload):
    if not upload:
        return upload

    # 1. File size
    if upload.size > MAX_KYC_FILE_SIZE:
        raise forms.ValidationError(
            "Image must be smaller than 2MB."
        )

    # 2. Content type
    allowed_types = {
        "image/jpeg",
        "image/jpg",
        "image/png",
    }

    if upload.content_type not in allowed_types:
        raise forms.ValidationError(
            "Only JPG, JPEG, and PNG images are allowed."
        )

    # 3. Verify that the file is actually an image
    try:
        image = Image.open(upload)
        image.verify()
    except Exception:
        raise forms.ValidationError(
            "The uploaded file is not a valid image."
        )

    # Reset file pointer after verify()
    upload.seek(0)

    return upload

class KYCVerificationForm(forms.ModelForm):

    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                "id":"dob",
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = KYCVerification

        # fields = '__all__'
        exclude = ['user', 'status']

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
                'id': 'name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com',
                'id': 'email'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 (555) 123-4567',
                'id': 'phone'
            }),

            'title': forms.Select(attrs={
                'class': 'form-select',
                'id': 'title'
            }),

            'gender': forms.Select(attrs={
                'class': 'form-select',
                'id': 'gender',
            }),

            'zipcode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '123456',
                'id': 'zipcode'
            }),

            'ssn': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'statenumber',
                'placeholder': 'XXX-XX-XXXX',
            }),

            'account_type': forms.Select(attrs={
                'class': 'form-select',
                'id': 'accounttype'
            }),

            'employment_type': forms.Select(attrs={
                'class': 'form-select',
                'id': 'employer'
            }),

            'annual_income_range': forms.Select(attrs={
                'class': 'form-select',
                'id': 'income'
            }),

            'address_line': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'id': 'address',
                'placeholder': '123 Main Street, Apt 4B'
            }),

            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'city',
                'placeholder': 'Enter Your City'
            }),

            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'state',
                'placeholder': 'Enter Your State'
            }),

            'nationality': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'country',
                'placeholder': 'Enter Your Country'
            }),

            'beneficiary_legal_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'kinname',
                'placeholder': 'Full name of beneficiary'
            }),

            'next_of_kin_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 1,
                'id': 'kinaddress',
                'placeholder': 'Beneficiary address'
            }),

            'relationship': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'relationship',
                'placeholder': 'e.g., Spouse, Parent, Sibling'
            }),

            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'age',
                'placeholder': 'Age in years'
            }),


            # 'document_type': forms.HiddenInput(),

            # ✅ CHANGED: Make document_type a visible Select with choices
            'document_type': forms.Select(attrs={
                'class': 'form-select',
                'id': 'document_type'
            }, choices=[
                ('passport', 'Passport'),
                ('drivers_license', "Driver's License"),
                ('national_id', 'National ID Card'),
                ('state_id', 'State ID'),
                ('military_id', 'Military ID'),
                ('other', 'Other Government ID'),
            ]),

            "upload_front_side": forms.ClearableFileInput(
                attrs={
                    "class": "form-control d-none",
                    "id": "frontimg",
                    "accept": "image/jpeg,image/png",
                }
            ),

            "upload_back_side": forms.ClearableFileInput(
                attrs={
                    "class": "form-control d-none",
                    "id": "backimg",
                    "accept": "image/jpeg,image/png,image/jpg",
                }
            ),

            "passport_photograph": forms.ClearableFileInput(
                attrs={
                    "class": "form-control d-none",
                    "id": "photo",
                    "accept": "image/jpeg,image/png",
                }
            ),
        }

    def clean_upload_front_side(self):
        upload = self.cleaned_data.get("upload_front_side")
        return validate_kyc_image(upload)

    def clean_upload_back_side(self):
        upload = self.cleaned_data.get("upload_back_side")
        return validate_kyc_image(upload)

    def clean_passport_photograph(self):
        upload = self.cleaned_data.get("passport_photograph")
        return validate_kyc_image(upload)


class PassportPhotoForm(forms.ModelForm):

    class Meta:
        model = KYCVerification
        fields = ["passport_photograph"]

        widgets = {
            "passport_photograph": forms.ClearableFileInput(
                attrs={
                    "id": "id_passport_photograph",
                    "accept": "image/jpeg,image/jpg,image/png",
                    "style": "display: none;",
                }
            )
        }

    def clean_passport_photograph(self):

        photo = self.cleaned_data.get("passport_photograph")

        if photo:
            # Validate file size (5MB max)
            if photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    "File size must be under 5MB."
                )

            # Validate file type
            allowed_types = ["image/jpeg", "image/jpg", "image/png"]
            if photo.content_type not in allowed_types:
                raise forms.ValidationError(
                    "Only JPG, JPEG, and PNG files are allowed."
                )

        return photo