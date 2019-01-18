%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%if 0%{?fedora} >= 24 || 0%{?rhel} > 7
%global with_python3 1
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
Version:        XXX
Release:        XXX
Summary:        OpenStack Oslo Middleware library

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

%package -n python2-%{pkg_name}
Summary:        OpenStack Oslo Middleware library
%{?python_provide:%python_provide python2-%{pkg_name}}

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
# for docs build
BuildRequires:  git
BuildRequires:  python2-oslo-config
BuildRequires:  python2-oslo-context
BuildRequires:  python2-oslo-i18n
BuildRequires:  python2-oslo-utils
# Required for testing
BuildRequires:  python2-fixtures
BuildRequires:  python2-hacking
BuildRequires:  python2-jinja2
BuildRequires:  python2-mock
BuildRequires:  python2-oslotest
BuildRequires:  python2-oslo-serialization
BuildRequires:  python2-statsd
BuildRequires:  python2-testtools
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:  python2-webob
%else
BuildRequires:  python-webob
%endif
# Required to compile translation files
BuildRequires:  python2-babel

Requires:       python2-pbr
Requires:       python2-debtcollector >= 1.2.0
Requires:       python2-jinja2
Requires:       python2-oslo-config >= 2:5.2.0
Requires:       python2-oslo-context >= 2.19.2
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-utils >= 3.33.0
Requires:       python2-six
Requires:       python2-statsd
Requires:       python2-stevedore >= 1.20.0
%if 0%{?fedora} || 0%{?rhel} > 7
Requires:       python2-webob >= 1.7.1
%else
Requires:       python-webob >= 1.7.1
%endif
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python2-%{pkg_name}
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{pkg_name}
Summary:        OpenStack Oslo Middleware library
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
# for docs build
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-context
BuildRequires:  python3-oslo-i18n
# Required for testing
BuildRequires:  python3-fixtures
BuildRequires:  python3-hacking
BuildRequires:  python3-jinja2
BuildRequires:  python3-mock
BuildRequires:  python3-oslotest
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-statsd
BuildRequires:  python3-testtools
BuildRequires:  python3-webob

Requires:       python3-pbr
Requires:       python3-debtcollector >= 1.2.0
Requires:       python3-jinja2
Requires:       python3-oslo-config >= 2:5.2.0
Requires:       python3-oslo-context >= 2.19.2
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-six
Requires:       python3-statsd
Requires:       python3-stevedore >= 1.20.0
Requires:       python3-webob >= 1.7.1
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
%{common_desc}

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

%endif

%if 0%{?with_doc}
%package doc
Summary:    Documentation for the Oslo Middleware library
Group:      Documentation

BuildRequires:  python2-sphinx
BuildRequires:  python2-openstackdocstheme

%description doc
Documentation for the Oslo Middleware library.
%endif

%package -n python2-%{pkg_name}-tests
Summary:    Tests for the Oslo Middleware library

Requires:  python2-%{pkg_name} = %{version}-%{release}
Requires:  python2-fixtures
Requires:  python2-hacking
Requires:  python2-mock
Requires:  python2-oslotest
Requires:  python2-testtools

%description -n python2-%{pkg_name}-tests
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
%py2_build

%if 0%{?with_python3}
%py3_build
%endif

%if 0%{?with_doc}
# generate html docs
python setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif
# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/oslo_middleware/locale

%install
%py2_install

%if 0%{?with_python3}
%py3_install
%endif

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
%if 0%{?with_python3}
rm -rf %{buildroot}%{python2_sitelib}/oslo_middleware/locale
rm -f %{buildroot}%{python3_sitelib}/oslo_middleware/locale/*/LC_*/oslo_middleware*po
rm -f %{buildroot}%{python3_sitelib}/oslo_middleware/locale/*pot
mv %{buildroot}%{python3_sitelib}/oslo_middleware/locale %{buildroot}%{_datadir}/locale
%else
rm -rf %{buildroot}%{python3_sitelib}/oslo_middleware/locale
rm -f %{buildroot}%{python2_sitelib}/oslo_middleware/locale/*/LC_*/oslo_middleware*po
rm -f %{buildroot}%{python2_sitelib}/oslo_middleware/locale/*pot
mv %{buildroot}%{python2_sitelib}/oslo_middleware/locale %{buildroot}%{_datadir}/locale
%endif

# Find language files
%find_lang oslo_middleware --all-name

%check
%{__python2} setup.py test
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
%endif

%files -n python2-%{pkg_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/oslo_middleware
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/oslo_middleware/tests/

%if 0%{?with_python3}
%files -n python3-%{pkg_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/oslo_middleware
%{python3_sitelib}/*.egg-info

%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_middleware/tests/
%endif

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python2-%{pkg_name}-tests
%{python2_sitelib}/oslo_middleware/tests/

%files -n python-%{pkg_name}-lang -f oslo_middleware.lang
%license LICENSE

%changelog
