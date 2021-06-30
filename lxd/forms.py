from django import forms


class CreateInstanceForm(forms.Form):
    """Create container or VM"""

    name = forms.CharField(
        label="Name",
        max_length=100,
        strip=True,
        required=False,
        help_text="The name of the container or VM.",
    )
    description = forms.CharField(
        widget=forms.Textarea,
        label="Description",
        required=False,
        help_text="A description given to the container or VM",
    )
    is_vm = forms.BooleanField(
        label="VM?",
        required=False,
        help_text="Create a virtual machine instead of container?",
    )


NETWORK_TYPE_CHOICES = [
    ("bridge", "Bridge (Default)"),
    ("macvlan", "MACVLAN"),
    ("sriov", "SR-IOV"),
    ("ovn", "OVN (Open Virtual Network)"),
    ("physical", "Physical"),
]


class CreateNetworkForm(forms.Form):
    """Create new network"""

    name = forms.CharField(
        label="Name",
        max_length=100,
        strip=True,
        required=False,
        help_text="The name of the network.",
    )
    description = forms.CharField(
        widget=forms.Textarea,
        label="Description",
        required=False,
        help_text="Network description",
    )
    network_type = forms.CharField(
        label="Network type?",
        widget=forms.Select(choices=NETWORK_TYPE_CHOICES),
    )
