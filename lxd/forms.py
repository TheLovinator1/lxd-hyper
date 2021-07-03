from django import forms

# TODO: Make this find containers automatically
# TODO: Add arm64, armhf, armel, i386, ppc64el and s390x
# TODO: Add default image
IMAGES_amd64 = (
    ("almalinux/8/cloud", "almalinux/8/cloud - Almalinux 8"),
    ("alpine/3.11", "alpine/3.11 - Alpine 3.11"),
    ("alpine/3.12", "alpine/3.12 - Alpine 3.12"),
    ("alpine/3.13/cloud", "alpine/3.13/cloud - Alpine 3.13"),
    ("alpine/3.14/cloud", "alpine/3.14/cloud - Alpine 3.14"),
    ("alpine/edge/cloud", "alpine/edge/cloud - Latest version of Alpine"),
    ("archlinux/cloud", "archlinux/cloud - Latest version of Arch"),
    ("centos/7/cloud", "centos/7/cloud - CentOS 7"),
    ("centos/8-Stream/cloud", "centos/8-Stream/cloud - Centos 8-Stream"),
    ("centos/8/cloud", "centos/8/cloud - CentOS 8"),
    ("debian/9/cloud", "debian/9/cloud - Debian 9 stretch"),
    ("debian/10/cloud", "debian/10/cloud - Debian 10 buster"),
    ("debian/11/cloud", "debian/11/cloud - Debian 11 bullseye"),
    ("debian/sid/cloud", "debian/sid/cloud - Debian sid"),
    ("devuan/ascii/cloud", "devuan/ascii/cloud - Devuan ascii"),
    ("devuan/beowulf/cloud", "devuan/beowulf/cloud - Devuan beowulf"),
    ("fedora/33/cloud", "fedora/33/cloud - Fedora 33"),
    ("fedora/34/cloud", "fedora/34/cloud - Fedora 34"),
    ("funtoo/1.4", "funtoo/1.4 - Funtoo 1.4"),
    ("gentoo/cloud", "gentoo/cloud - Latest version of Gentoo"),
    ("kali/cloud", "kali/cloud - Latest version of Kali"),
    ("mint/sarah/cloud", "mint/sarah/cloud - Mint sarah"),
    ("mint/serena/cloud", "mint/serena/cloud - Mint serena"),
    ("mint/sonya/cloud", "mint/sonya/cloud - Mint sonya"),
    ("mint/sylvia/cloud", "mint/sylvia/cloud - Mint sylvia"),
    ("mint/tara/cloud", "mint/tara/cloud - Mint tara"),
    ("mint/tessa/cloud", "mint/tessa/cloud - Mint tessa"),
    ("mint/tina/cloud", "mint/tina/cloud - Mint tina"),
    ("mint/tricia/cloud", "mint/tricia/cloud - Mint tricia"),
    ("mint/ulyana/cloud", "mint/ulyana/cloud - Mint ulyana"),
    ("mint/ulyssa/cloud", "mint/ulyssa/cloud - Mint ulyssa"),
    ("opensuse/15.2/cloud", "opensuse/15.2/cloud - Opensuse 15.2"),
    ("opensuse/15.3/cloud", "opensuse/15.3/cloud - Opensuse 15.3"),
    ("opensuse/tumbleweed/cloud", "opensuse/tumbleweed/cloud - Opensuse tumbleweed"),
    ("oracle/7/cloud", "oracle/7/cloud - Oracle 7"),
    ("oracle/8/cloud", "oracle/8/cloud - Oracle 8"),
    ("plamo/6.x", "plamo/6.x - Plamo 6.x"),
    ("plamo/7.x", "plamo/7.x - Plamo 7.x"),
    ("pld", "pld - PLD Linux"),
    ("rockylinux/8/cloud", "rockylinux/8/cloud - Rockylinux 8"),
    ("sabayon/cloud", "sabayon/cloud - Sabayon current"),
    ("springdalelinux/7/cloud", "springdalelinux/7/cloud - Springdale Linux (SDL) 7"),
    ("springdalelinux/8/cloud", "springdalelinux/8/cloud - Springdale Linux (SDL) 8"),
    ("ubuntu/16.04/cloud", "ubuntu/16.04/cloud - Ubuntu xenial"),
    ("ubuntu/18.04/cloud", "ubuntu/18.04/cloud - Ubuntu bionic"),
    ("ubuntu/20.10/cloud", "ubuntu/20.10/cloud - Ubuntu groovy"),
    ("ubuntu/21.04/cloud", "ubuntu/21.04/cloud - Ubuntu hirsute"),
    ("ubuntu/focal/cloud", "ubuntu/focal/cloud - Ubuntu focal"),
    ("ubuntu/impish/cloud", "ubuntu/impish/cloud - Ubuntu impish"),
    ("voidlinux", "voidlinux - Latest version of Voidlinux"),
    ("voidlinux/musl", "voidlinux/musl - Latest version of Voidlinux with musl"),
)


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
