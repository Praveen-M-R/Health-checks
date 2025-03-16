from django import forms
from .models import Check

class CheckForm(forms.ModelForm):
    class Meta:
        model = Check
        fields = [
            "name", "duration_days", "duration_hours", "duration_minutes", 
            "grace_days","grace_hours", "grace_minutes", "channel", "recipient"
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Check Name"}),
            "duration_days": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Days"}),
            "duration_hours": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Hours"}),
            "duration_minutes": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Minutes"}),
            "grace_days": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Grace Days"}),
            "grace_hours": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Grace Hours"}),
            "grace_minutes": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Grace Minutes"}),
            "channel": forms.TextInput(attrs={"class": "form-control", "placeholder": "Notification Channel"}),
            "recipient": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Recipient Email"}),
        }
