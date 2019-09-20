# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

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
Version:        XXX
Release:        XXX
Summary:        OpenStack Oslo Middleware library

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

%package -n python%{pyver}-%{pkg_name}
Summary:        OpenStack Oslo Middleware library
%{?python_provide:%python_provide python%{pyver}-%{pkg_name}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
# for docs build
BuildRequires:  git
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-oslo-context
BuildRequires:  python%{pyver}-oslo-i18n
BuildRequires:  python%{pyver}-oslo-utils
# Required for testing
BuildRequires:  python%{pyver}-fixtures
BuildRequires:  python%{pyver}-hacking
BuildRequires:  python%{pyver}-jinja2
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-oslo-serialization
BuildRequires:  python%{pyver}-statsd
BuildRequires:  python%{pyver}-testtools
%if %{pyver} == 2
BuildRequires:  python-webob
%else
BuildRequires:  python%{pyver}-webob
%endif
# Required to compile translation files
BuildRequires:  python%{pyver}-babel

Requires:       python%{pyver}-pbr
Requires:       python%{pyver}-debtcollector >= 1.2.0
Requires:       python%{pyver}-jinja2
Requires:       python%{pyver}-oslo-config >= 2:5.2.0
Requires:       python%{pyver}-oslo-context >= 2.19.2
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-six
Requires:       python%{pyver}-statsd
Requires:       python%{pyver}-stevedore >= 1.20.0
%if 0%{?fedora} || 0%{?rhel} > 7
Requires:       python%{pyver}-webob >= 1.8.0
%else
Requires:       python-webob >= 1.8.0
%endif
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python%{pyver}-%{pkg_name}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:    Documentation for the Oslo Middleware library
Group:      Documentation

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme

%description doc
Documentation for the Oslo Middleware library.
%endif

%package -n python%{pyver}-%{pkg_name}-tests
Summary:    Tests for the Oslo Middleware library

Requires:  python%{pyver}-%{pkg_name} = %{version}-%{release}
Requires:  python%{pyver}-fixtures
Requires:  python%{pyver}-hacking
Requires:  python%{pyver}-mock
Requires:  python%{pyver}-oslotest
Requires:  python%{pyver}-testtools

%description -n python%{pyver}-%{pkg_name}-tests
%{common_desc2}

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo middleware library

%description -n python-%{pkg_name}-lang
Translation files for Oslo middleware library

%description
%{common_desc}

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the dependencies
rm -rf {test-,}requirements.txt

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif
# Generate i18n files
%{pyver_bin} setup.py compile_catalog -d build/lib/oslo_middleware/locale

%install
%{pyver_install}

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{pyver_sitelib}/oslo_middleware/locale/*/LC_*/oslo_middleware*po
rm -f %{buildroot}%{pyver_sitelib}/oslo_middleware/locale/*pot
mv %{buildroot}%{pyver_sitelib}/oslo_middleware/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang oslo_middleware --all-name

%check
%{pyver_bin} setup.py test
rm -rf .testrepository

%files -n python%{pyver}-%{pkg_name}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/oslo_middleware
%{pyver_sitelib}/*.egg-info
%exclude %{pyver_sitelib}/oslo_middleware/tests/

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python%{pyver}-%{pkg_name}-tests
%{pyver_sitelib}/oslo_middleware/tests/

%files -n python-%{pkg_name}-lang -f oslo_middleware.lang
%license LICENSE

%changelog
