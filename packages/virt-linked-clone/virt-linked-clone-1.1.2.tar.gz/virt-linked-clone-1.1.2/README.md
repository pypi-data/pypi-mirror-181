# Create a Shallow Clone of a QCOW2-Backed LibVirt Virtual Machine

```shell
pip install virt-linked-clone
```

```shell
usage: virt-linked-clone [-h] [--zsh-completion] [--version] [-c CONNECTION] source target

positional arguments:
  source                Virtual machine from which to create a clone where all writable
                        qcow2-backed drives are linked using copy-on-write. It must be defined
                        with libvirt and accessible via virsh commands.
  target                Name of the new virtual machine to define. Most of the settings of the
                        source image will be copied into the new libvirt domain. Defaults to
                        adding "-clone" to the source domain name.

options:
  -h, --help            show this help message and exit
  --zsh-completion      Print out the zsh autocompletion code for this utility and exit.
  --version             show program's version number and exit
  -c CONNECTION, --connection CONNECTION
                        LibVirt URI to use for connecting to the domain controller. Will honor the
                        value of the VIRSH_DEFAULT_CONNECT_URI environment variable. (default:
                        qemu:///session)
```
