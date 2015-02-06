%define upstream_name ess

Summary:	Emacs Speaks Statistics package for Emacs
Name:		emacs-%{upstream_name}
Version:	13.09
Release:	2
License:	GPLv2+
Group:		Editors
Url:		http://ess.r-project.org
Source0:	http://ess.r-project.org/downloads/ess/%{upstream_name}-%{version}.tgz
BuildRequires:	emacs
BuildRequires:	emacs-el
BuildRequires:	R-base
BuildRequires:	texinfo
Requires:	emacs
Requires:	emacs-el
BuildArch:	noarch

%description
This package provides Emacs Speaks Statistics (ESS), which provides
Emacs-based front ends for popular statistics packages.

ESS provides an intelligent, consistent interface between the user and
the software.  ESS interfaces with S-PLUS, R, SAS, BUGS and other
statistical analysis packages under the Unix, Microsoft Windows, and
Apple Mac OS operating systems.  ESS is a package for the GNU Emacs
text editor whose features ESS uses to streamline the creation and use
of statistical software. ESS knows the syntax and grammar of statistical
analysis packages and provides consistent display and editing features
based on that knowledge. ESS assists in interactive and batch execution
of statements written in these statistical analysis languages.

%files
%doc ANNOUNCE ChangeLog README VERSION
%dir %{_datadir}/emacs/site-lisp
%{_datadir}/emacs/site-lisp/%{upstream_name}
%{_infodir}/%{upstream_name}.info.xz
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/%{name}.el

#----------------------------------------------------------------------------

%package doc
Summary:	Emacs Speaks Statistics Documentation
Group:		Editors

%description doc
This package provides documentation for Emacs Speaks Statistics (ESS).

%prep
%setup -q -n %{upstream_name}-%{version}
chmod u+w doc/{html,info,refcard,dir.txt} # fix perms

%files doc
%doc doc/ess-intro-graphs.pdf doc/readme.pdf doc/html

#----------------------------------------------------------------------------

%build
%make \
	PREFIX=%{_prefix} \
	LISPDIR=%{_datadir}/emacs/site-lisp/%{upstream_name} \
	ETCDIR=%{_datadir}/emacs/site-lisp/%{upstream_name}/etc \
	INFODIR=%{_infodir}

cat > %{name}.el <<"EOF"
;;; Set up %{upstream_name} for Emacs.
;;;
;;; This file is automatically loaded by emacs's site-start.el
;;; when you start a new emacs session.
(if (not (string-match "XEmacs" emacs-version)) (require 'ess-site))
EOF

%install
install -d %{buildroot}%{_sysconfdir}/emacs/site-start.d
install -d %{buildroot}%{_infodir}

%makeinstall_std \
	PREFIX=%{buildroot}%{_prefix} \
	LISPDIR=%{buildroot}%{_datadir}/emacs/site-lisp/%{upstream_name} \
	ETCDIR=%{buildroot}%{_datadir}/emacs/site-lisp/%{upstream_name}/etc \
	INFODIR=%{buildroot}%{_infodir} \
	DOCDIR=%{buildroot}%{_docdir}/%{name}-doc
install -m 0644 %{name}.el %{buildroot}%{_sysconfdir}/emacs/site-start.d/
rm -f %{buildroot}%{_datadir}/emacs/site-lisp/%{upstream_name}/etc/*.BAT
rm -f %{buildroot}%{_datadir}/emacs/site-lisp/%{upstream_name}/etc/*.sparc
rm -f %{buildroot}%{_docdir}/%{name}-doc/*.dvi
rm -f %{buildroot}%{_docdir}/%{name}-doc/*.html

