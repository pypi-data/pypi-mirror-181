#!/bin/zsh

typeset -A opt_args

_virt_linked_clone() {
    local -a connection_uris=(
        'qemu:///session'
        'qemu:///system'
    )
    local -a domains=($(virsh -c qemu:///session list --all --name))
    local -a virt_linked_clone_opts=(
        {-h,--help}'[show help]'
        '--version[show version]'
        {-c,--connection}'=[libvirt connection uri]:connection:($connection_uris)'
        "1::source:($domains)"
        "2::target:($domains)"
    )
    _arguments -C -s $virt_linked_clone_opts
}

compdef _virt_linked_clone virt-linked-clone
