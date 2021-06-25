from django import forms


class CreateInstanceForm(forms.Form):
    """Create container or VM"""

    name = forms.CharField(label="Name", max_length=100, strip=True)
    description = forms.CharField(widget=forms.Textarea, label="Description")
    is_vm = forms.BooleanField(
        label="Create virtual machine instead of container?", required=False
    )
