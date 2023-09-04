%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x815AFEC729392386480E076DCC0DFE2D21C023C9
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global with_doc 1

%global pypi_name oslo.middleware
%global pkg_name oslo-middleware
%global common_desc \
The OpenStack Oslo Middleware library. \
Oslo middleware library includes components that can be injected into wsgi \
pipelines to intercept request/response flows. The base class can be \
enhanced with functionality like add/delete/modification of http headers \
and support for limiting size/connection etc.

%global common_desc2 \
Tests for the Oslo Middleware library.

Name:           python-oslo-middleware
Version:        5.2.0
Release:        1%{?dist}
Summary:        OpenStack Oslo Middleware library

License:        Apache-2.0
URL:            https://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%package -n python3-%{pkg_name}
Summary:        OpenStack Oslo Middleware library

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  git-core
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo Middleware library
Group:      Documentation

%description -n python-%{pkg_name}-doc
Documentation for the Oslo Middleware library.
%endif

%package -n python3-%{pkg_name}-tests
Summary:    Tests for the Oslo Middleware library

Requires:  python3-%{pkg_name} = %{version}-%{release}
Requires:  python3-fixtures
Requires:  python3-hacking
Requires:  python3-mock
Requires:  python3-oslotest
Requires:  python3-testtools

%description -n python3-%{pkg_name}-tests
%{common_desc2}

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo middleware library

%description -n python-%{pkg_name}-lang
Translation files for Oslo middleware library

%description
%{common_desc}

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

# Generate i18n files
python3 setup.py compile_catalog -d %{buildroot}%{python3_sitelib}/oslo_middleware/locale --domain oslo_middleware


# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/oslo_middleware/locale/*/LC_*/oslo_middleware*po
rm -f %{buildroot}%{python3_sitelib}/oslo_middleware/locale/*pot
mv %{buildroot}%{python3_sitelib}/oslo_middleware/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_middleware --all-name

%check
%tox -e %{default_toxenv}

%files -n python3-%{pkg_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/oslo_middleware
%{python3_sitelib}/*.dist-info
%exclude %{python3_sitelib}/oslo_middleware/tests/

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_middleware/tests/

%files -n python-%{pkg_name}-lang -f oslo_middleware.lang
%license LICENSE

%changelog
* Mon Sep 04 2023 RDO <dev@lists.rdoproject.org> 5.2.0-1
- Update to 5.2.0

