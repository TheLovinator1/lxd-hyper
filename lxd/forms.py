from django import forms


class CreateInstanceForm(forms.Form):
    """Create container or VM"""

    name = forms.CharField(
        label="Name",
        max_length=100,
        strip=True,
        required=False,
        help_text="The name of the instance. This attribute serves as the primary identifier of an instance",
    )
    description = forms.CharField(
        widget=forms.Textarea,
        label="Description",
        required=False,
        help_text="A description given to the instance",
    )
    is_vm = forms.BooleanField(
        label="VM?",
        required=False,
        help_text="Create virtual machine instead of container?",
    )
