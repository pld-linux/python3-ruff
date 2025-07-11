# TODO: vendor external crates
Summary:	An extremely fast Python linter and code formatter, written in Rust
Summary(pl.UTF-8):	Bardzo szybki linter i formater kodu dla Pythona, napisany w języku Rust
Name:		python3-ruff
Version:	0.12.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/ruff/
Source0:	https://files.pythonhosted.org/packages/source/r/ruff/ruff-%{version}.tar.gz
# Source0-md5:	6fc65b457fd73b373c9dfc1a4c9d3e23
URL:		https://pypi.org/project/ruff/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-maturin >= 1.0
BuildRequires:	python3-maturin < 2
BuildRequires:	python3-modules >= 1:3.7
# 1.86 for 0.12.2
BuildRequires:	rust >= 1.85
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An extremely fast Python linter and code formatter, written in Rust.

%description -l pl.UTF-8
Bardzo szybkie narzędzie do sprawdzania stylu i formatowania kodu w
Pythonie, napisane w języku Rust.

%prep
%setup -q -n ruff-%{version}

%build
%py3_build_pyproject

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/ruff
%dir %{py3_sitedir}/ruff
%{py3_sitedir}/ruff/*.py
%{py3_sitedir}/ruff/__pycache__
%{py3_sitedir}/ruff-%{version}.dist-info
