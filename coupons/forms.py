from django import forms
from django.utils.translation import gettext_lazy as _


class CouponApplyForm(forms.Form):

    code = forms.CharField(label=_("Coupon"))

    def clean_code(self):
        data = self.cleaned_data["code"]
        if "FRED" not in data:
            raise forms.ValidationError("You have forgotten about Fred!")

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data