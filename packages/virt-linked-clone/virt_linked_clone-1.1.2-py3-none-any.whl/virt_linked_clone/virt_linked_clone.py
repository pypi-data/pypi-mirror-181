import contextlib
import copy
import pathlib
import subprocess
import time

import xml.etree.ElementTree as xml

import libvirt  # python package: libvirt-python


@contextlib.contextmanager
def libvirt_connection(name='qemu:///session'):
    """Libvirt connection context."""
    # libvirt-host: virConnectOpen(name)
    conn = libvirt.open(name)
    try:
        yield conn
    finally:
        # libvirt-host: virConnectClose()
        conn.close()


def get_domain(conn, name):
    """Return libvirt domain object or None if not defined."""
    # libvirt-domain: virConnectListDefinedDomains(connection)
    if name in conn.listDefinedDomains():
        # libvirt-domain: virDomainLookupByName(name)
        return conn.lookupByName(name)


def shutdown_domain(domain):
    """Shutdown the domain, trying several times before giving up."""
    # libvirt-domain: virDomainShutdown(domain)
    domain.shutdown()
    start = time.time()
    timeout = 3 * 60  # 3 minutes
    while (time.time() - start) < timeout:
        # libvirt-domain: virDomainGetState(domain)
        state, reason = domain.state()
        if state == libvirt.VIR_DOMAIN_SHUTOFF:
            break
        else:
            time.sleep(1)
    if state != libvirt.VIR_DOMAIN_SHUTOFF:
        raise RuntimeError(f'shutdown of {domain} unsuccessful, currently: {state}')


def ensure_shutdown(domain, shutdown=True):
    """Raise exception if domain is not or can not be shutdown."""
    # libvirt-domain: virDomainGetState(domain)
    state, reason = domain.state()
    if state == libvirt.VIR_DOMAIN_RUNNING:
        if shutdown:
            shutdown_domain(domain)
        else:
            raise RuntimeError(f'domain {source} must be shut down')
    # libvirt-domain: virDomainGetState(domain)
    state, reason = domain.state()
    if state != libvirt.VIR_DOMAIN_SHUTOFF:
        msg = f'domain {source} must be shut down, current state: {state}'
        raise RuntimeError(msg)


def list_cow_disks(domain):
    """Return a list of copy-on-write disks (qcow2) used by this domain."""
    result = []
    # libvirt-domain: virDomainGetXMLDesc(domain, flags)
    domain_xml = xml.fromstring(domain.XMLDesc(0))
    for disk in domain_xml.findall('devices/disk'):
        if disk.get('type') == 'file' and disk.get('device') == 'disk':
            driver = disk.find('driver')
            if driver.get('name') == 'qemu' and driver.get('type') == 'qcow2':
                source_file = pathlib.Path(disk.find('source').get('file'))
                target_dev = disk.find('target').get('dev')
                result.append((source_file, target_dev, disk))
    return result


def set_disk_readonly(domain, disk_xml, value=True):
    """Set/unset disk readonly attribute in the given domain."""
    readonly_tags = disk_xml.findall('readonly')
    if value and not readonly_tags:
        disk_xml.append(xml.Element('readonly'))
    elif not value and readonly_tags:
        for readonly_tag in readonly_tags:
            disk_xml.remove(readonly_tag)
    else:
        # no changes neccessary
        return
    disk_xml_str = xml.tostring(disk_xml, encoding='unicode')
    # libvirt-domain: virDomainUpdateDeviceFlags(domain, xml, flags)
    domain.updateDeviceFlags(disk_xml_str, 0)


def create_clone(source, target, skip_copy_devices):
    """Clone source to target, reusing the disks as-is (no copies)."""
    cmd = ['virt-clone', '--preserve-data', '--auto-clone']
    cmd += ['--original', source]
    cmd += ['--name', target]
    for disk_device in skip_copy_devices:
        cmd += ['--skip-copy', disk_device]
    subprocess.run(cmd, check=True)


def qemu_img_create(new_file, backing_file):
    """Create an overlay disk image based on another qcow2 image."""
    cmd = ['qemu-img', 'create', '-q', '-f', 'qcow2', '-F', 'qcow2']
    cmd += ['-o', f'backing_file={backing_file}']
    cmd += [new_file]
    subprocess.run(cmd, check=True)


def create_overlay_disks(domain, cow_disks):
    """Make existing disk in domain an overlay qcow2 image on the original."""
    # libvirt-domain: virDomainGetName(domain)
    domain_name = domain.name()
    for disk_file, disk_device, disk_xml in cow_disks:
        # make linked copy-on-write clone of the disk image file
        new_file = disk_file.parent / f'{domain_name}-{disk_device}.qcow2'
        qemu_img_create(new_file, backing_file=disk_file)

        # ensure the disk is marked read/write
        set_disk_readonly(domain, disk_xml, value=False)

        # set the new disk as the source file in the target domain
        # set the source file as the backing store, and append
        # source's backing store to the chain
        disk_source = disk_xml.find('source')
        source_file = disk_source.get('file')

        disk_source.set('file', str(new_file))
        backing_store = xml.Element('backingStore', {'type': 'file'})
        backing_store.append(xml.Element('format', {'type': 'qcow2'}))
        backing_store.append(xml.Element('source', {'file': source_file}))
        if source_chain := disk_xml.find('backingStore'):
            backing_store.append(copy.copy(source_chain))
            disk_xml.remove(source_chain)
        disk_xml.append(backing_store)

        disk_xml_str = xml.tostring(disk_xml, encoding='unicode')
        # libvirt-domain: virDomainUpdateDeviceFlags(domain, xml, flags)
        domain.updateDeviceFlags(disk_xml_str, 0)


def create_linked_clone(
    source, target, connection='qemu:///session', shutdown_source=True
):
    """Clone a libvirt domain, creating overlay images for all qcow2 disks."""
    with libvirt_connection(connection) as conn:
        source_domain = get_domain(conn, source)
        if source_domain is None:
            raise ValueError(f'source libvirt domain "{source}" not found')

        if get_domain(conn, target) is not None:
            raise ValueError(f'target libvirt domain "{target}" already exists')

        cow_disks = list_cow_disks(source_domain)
        if not cow_disks:
            msg = f'source libvirt domain "{source}" has no copy-on-write disks'
            raise ValueError(msg)

        ensure_shutdown(source_domain, shutdown_source)

        for _, _, disk_xml in cow_disks:
            set_disk_readonly(source_domain, disk_xml, value=True)

        cow_disks_dev = [dev for _, dev, _ in cow_disks]
        create_clone(source, target, cow_disks_dev)

        target_domain = get_domain(conn, target)
        try:
            create_overlay_disks(target_domain, cow_disks)
        except:
            # libvirt-domain: virDomainUndefine(domain)
            target_domain.undefine()
            raise
