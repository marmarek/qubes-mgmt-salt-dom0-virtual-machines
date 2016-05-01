%{!?version: %define version %(cat version)}

Name:      qubes-mgmt-salt-dom0-virtual-machines
Version:   %{version}
Release:   1%{?dist}
Summary:   Downloads, installs and configures template as well as creating and configuring virtual-machine AppVM's.
License:   GPL 2.0
URL:	   http://www.qubes-os.org/

Group:     System administration tools
BuildArch: noarch
Requires:  qubes-mgmt-salt
Requires:  qubes-mgmt-salt-dom0

%define _builddir %(pwd)

%description
Downloads, installs and configures template as well as creating and configuring virtual-machine AppVM's.
Uses pillar data to define default VM names and configuration details.

%prep
# we operate on the current directory, so no need to unpack anything
# symlink is to generate useful debuginfo packages
rm -f %{name}-%{version}
ln -sf . %{name}-%{version}
%setup -T -D

%build

%install
make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} BINDIR=%{_bindir} SBINDIR=%{_sbindir} SYSCONFDIR=%{_sysconfdir}

%post
# Update Salt Configuration
qubesctl state.sls config -l quiet --out quiet > /dev/null || true
qubesctl saltutil.clear_cache -l quiet --out quiet > /dev/null || true
qubesctl saltutil.sync_all refresh=true -l quiet --out quiet > /dev/null || true

# Enable States
#qubesctl top.enable qvm.sys-net -l quiet --out quiet > /dev/null || true
#qubesctl top.enable qvm.sys-firewall -l quiet --out quiet > /dev/null || true
#qubesctl top.enable qvm.sys-whonix -l quiet --out quiet > /dev/null || true
#qubesctl top.enable qvm.anon-whonix -l quiet --out quiet > /dev/null || true
#qubesctl top.enable qvm.personal -l quiet --out quiet > /dev/null || true
#qubesctl top.enable qvm.work -l quiet --out quiet > /dev/null || true
#qubesctl top.enable qvm.untrusted -l quiet --out quiet > /dev/null || true
#qubesctl top.enable qvm.vault -l quiet --out quiet > /dev/null || true

# Enable Pillar States
qubesctl top.enable qvm pillar=true -l quiet --out quiet > /dev/null || true

# Migrate enabled tops from dom0 to base environment
for top in sys-net sys-firewall sys-whonix anon-whonix personal work untrusted vault sys-net-with-usb; do
    if [ -r /srv/salt/_tops/dom0/qvm.$top.top ]; then
        rm -f /srv/salt/_tops/dom0/qvm.$top.top
        qubesctl top.enable qvm.$top -l quiet --out quiet > /dev/null || true
    fi
done

if [ -r /srv/pillar/_tops/dom0/qvm.top ]; then
    rm -f /srv/pillar/_tops/dom0/qvm.top
fi

%files
%defattr(-,root,root)
%doc LICENSE README.rst
%attr(750, root, root) %dir /srv/formulas/dom0/virtual-machines-formula
/srv/formulas/dom0/virtual-machines-formula/README.rst
/srv/formulas/dom0/virtual-machines-formula/LICENSE
/srv/formulas/dom0/virtual-machines-formula/qvm/anon-whonix.sls
/srv/formulas/dom0/virtual-machines-formula/qvm/anon-whonix.top
/srv/formulas/dom0/virtual-machines-formula/qvm/personal.sls
/srv/formulas/dom0/virtual-machines-formula/qvm/personal.top
/srv/formulas/dom0/virtual-machines-formula/qvm/sys-firewall.sls
/srv/formulas/dom0/virtual-machines-formula/qvm/sys-firewall.top
/srv/formulas/dom0/virtual-machines-formula/qvm/sys-net.sls
/srv/formulas/dom0/virtual-machines-formula/qvm/sys-net.top
/srv/formulas/dom0/virtual-machines-formula/qvm/sys-net-with-usb.sls
/srv/formulas/dom0/virtual-machines-formula/qvm/sys-net-with-usb.top
/srv/formulas/dom0/virtual-machines-formula/qvm/sys-usb.sls
/srv/formulas/dom0/virtual-machines-formula/qvm/sys-usb.top
/srv/formulas/dom0/virtual-machines-formula/qvm/sys-whonix.sls
/srv/formulas/dom0/virtual-machines-formula/qvm/sys-whonix.top
/srv/formulas/dom0/virtual-machines-formula/qvm/template-debian-7.sls
/srv/formulas/dom0/virtual-machines-formula/qvm/template-debian-8.sls
/srv/formulas/dom0/virtual-machines-formula/qvm/template-fedora-21-minimal.sls
/srv/formulas/dom0/virtual-machines-formula/qvm/template-fedora-21.sls
/srv/formulas/dom0/virtual-machines-formula/qvm/template.jinja
/srv/formulas/dom0/virtual-machines-formula/qvm/template-whonix-gw.sls
/srv/formulas/dom0/virtual-machines-formula/qvm/template-whonix-ws.sls
/srv/formulas/dom0/virtual-machines-formula/qvm/untrusted.sls
/srv/formulas/dom0/virtual-machines-formula/qvm/untrusted.top
/srv/formulas/dom0/virtual-machines-formula/qvm/vault.sls
/srv/formulas/dom0/virtual-machines-formula/qvm/vault.top
/srv/formulas/dom0/virtual-machines-formula/qvm/work.sls
/srv/formulas/dom0/virtual-machines-formula/qvm/work.top

%attr(750, root, root) %dir /srv/pillar/dom0/qvm
%config(noreplace) /srv/pillar/dom0/qvm/init.sls
/srv/pillar/dom0/qvm/init.top

%changelog
