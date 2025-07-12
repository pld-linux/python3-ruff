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
# cargo vendor-filterer --platform='*-unknown-linux-*' --tier=2
# tar cJf ruff-%{version}-vendor.tar.xz vendor Cargo.lock
Source1:	ruff-%{version}-vendor.tar.xz
# Source1-md5:	f3307c32dabcd6a6a8f43fcf14ec16e4
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
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	python3-modules >= 1:3.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An extremely fast Python linter and code formatter, written in Rust.

%description -l pl.UTF-8
Bardzo szybkie narzędzie do sprawdzania stylu i formatowania kodu w
Pythonie, napisane w języku Rust.

%prep
%setup -q -n ruff-%{version} -a1

# remove strip section from tool.maturin
%{__sed} -i -e '/strip = true/d' pyproject.toml

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config.toml <<EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "$PWD/vendor"

[source.git-lsp-types]
git = "https://github.com/astral-sh/lsp-types.git"
rev = "3512a9f"
replace-with = "vendored-sources"

[source.git-salsa]
git = "https://github.com/salsa-rs/salsa.git"
rev = "09627e450566f894956710a3fd923dc80462ae6d"
replace-with = "vendored-sources"
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"
export CARGO_OFFLINE=true
export RUSTFLAGS="%{rpmrustflags}"
export CARGO_TERM_VERBOSE=true
%ifarch x32
export CARGO_BUILD_TARGET=x86_64-unknown-linux-gnux32
export PKG_CONFIG_ALLOW_CROSS=1
export PYO3_CROSS_LIB_DIR=%{_libdir}
%endif

%py3_build_pyproject

%install
rm -rf $RPM_BUILD_ROOT

export CARGO_HOME="$(pwd)/.cargo"
export CARGO_OFFLINE=true
export RUSTFLAGS="%{rpmrustflags}"
export CARGO_TERM_VERBOSE=true
%ifarch x32
export CARGO_BUILD_TARGET=x86_64-unknown-linux-gnux32
export PKG_CONFIG_ALLOW_CROSS=1
%endif

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
