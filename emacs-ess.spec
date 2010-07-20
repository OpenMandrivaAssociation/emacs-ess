%define	rname ess
%define xemacs_name xemacs-%{rname}

Summary:	Emacs Speaks Statistics package for Emacs
Name:		emacs-%{rname}
Version:	5.11
Release:	%mkrel 1
License:	GPLv2+
Group:		Editors
URL:		http://ess.r-project.org
Source0:	http://ess.r-project.org/downloads/ess/%{rname}-%{version}.tgz
BuildRequires:	emacs-X11
BuildRequires:	emacs-el
BuildRequires:	texinfo
BuildRequires:	R-base
Requires:	emacs
Requires:	emacs-el
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
This package provides Emacs Speaks Statistics (ESS), which provides
Emacs-based front ends for popular statistics packages.

ESS provides an intelligent, consistent interface between the user and
the software.  ESS interfaces with S-PLUS, R, SAS, BUGS and other
statistical analysis packages under the Unix, Microsoft Windows, and
Apple Mac OS operating systems.  ESS is a package for the GNU Emacs
and XEmacs text editors whose features ESS uses to streamline the
creation and use of statistical software.  ESS knows the syntax and
grammar of statistical analysis packages and provides consistent
display and editing features based on that knowledge.  ESS assists in
interactive and batch execution of statements written in these
statistical analysis languages.

%package doc
Summary:	Emacs Speaks Statistics Documentation
Group:		Editors

%description doc
This package provides documentation for Emacs Speaks Statistics (ESS).

ESS provides an intelligent, consistent interface between the user and
the software.  ESS interfaces with S-PLUS, R, SAS, BUGS and other
statistical analysis packages under the Unix, Microsoft Windows, and
Apple Mac OS operating systems.  ESS is a package for the GNU Emacs
and XEmacs text editors whose features ESS uses to streamline the
creation and use of statistical software.  ESS knows the syntax and
grammar of statistical analysis packages and provides consistent
display and editing features based on that knowledge.  ESS assists in
interactive and batch execution of statements written in these
statistical analysis languages.

%if %{mdkversion} >= 200800
%package -n %{xemacs_name}
Summary:	Emacs Speaks Statistics package for XEmacs
Group:		Editors
BuildRequires:	xemacs
BuildRequires:	xemacs-el
BuildRequires:	texinfo
BuildRequires:	R-base
Requires:	xemacs
Requires:	xemacs-el

%description -n %{xemacs_name}
This package provides Emacs Speaks Statistics (ESS) for XEmacs, which provides
XEmacs-based front ends for popular statistics packages.

ESS provides an intelligent, consistent interface between the user and
the software.  ESS interfaces with S-PLUS, R, SAS, BUGS and other
statistical analysis packages under the Unix, Microsoft Windows, and
Apple Mac OS operating systems.  ESS is a package for the GNU Emacs
and XEmacs text editors whose features ESS uses to streamline the
creation and use of statistical software.  ESS knows the syntax and
grammar of statistical analysis packages and provides consistent
display and editing features based on that knowledge.  ESS assists in
interactive and batch execution of statements written in these
statistical analysis languages.
%endif

%prep
%setup -q -n %{rname}-%{version}
chmod u+w doc/{html,info,refcard,dir.txt} # fix perms
%if %{mdkversion} >= 200800
cp -Rp lisp lisp-xemacs
%endif

%build
%make \
	PREFIX=%{_prefix} \
	LISPDIR=%{_datadir}/emacs/site-lisp/%{rname} \
	ETCDIR=%{_datadir}/emacs/site-lisp/%{rname}/etc \
	INFODIR=%{_infodir}

%if %{mdkversion} >= 200800
pushd lisp-xemacs
%make \
	EMACS=xemacs \
	PREFIX=%{_prefix} \
	LISPDIR=%{_datadir}/xemacs/site-lisp/%{rname} \
	ETCDIR=%{_datadir}/xemacs/site-lisp/%{rname}/etc \
	INFODIR=%{_infodir}
popd

# create an init file that is loaded when a user starts up emacs to
# tell emacs to autoload our package's Emacs code when needed

cat > %{name}.el <<"EOF"
;;; Set up %{rname} for Emacs.
;;;
;;; This file is automatically loaded by emacs's site-start.el
;;; when you start a new emacs session.
(if (not (string-match "XEmacs" emacs-version)) (require 'ess-site))
EOF

cat > %{xemacs_name}.el <<"EOF"
;;; Set up %{rname} for XEmacs.
;;;
;;; This file is automatically loaded by emacs's site-start.el
;;; when you start a new emacs session.
(if (string-match "XEmacs" emacs-version) (progn (add-path "/usr/share/xemacs/site-lisp/ess")
						(require 'ess-site)))
EOF

%else

cat > %{name}.el <<"EOF"
;;; Set up %{rname} for Emacs and XEmacs.
;;;
;;; This file is automatically loaded by emacs's site-start.el
;;; when you start a new emacs session.
(if (string-match "XEmacs" emacs-version) (add-path "/usr/share/emacs/site-lisp/ess"))
(require 'ess-site)
%endif

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/emacs/site-start.d
install -d %{buildroot}%{_infodir}
install -d %{buildroot}%{_datadir}/emacs/site-lisp/%{name}

%makeinstall_std \
	PREFIX=%{buildroot}%{_prefix} \
	LISPDIR=%{buildroot}%{_datadir}/emacs/site-lisp/%{rname} \
	ETCDIR=%{buildroot}%{_datadir}/emacs/site-lisp/%{rname}/etc \
	INFODIR=%{buildroot}%{_infodir} \
	DOCDIR=%{buildroot}%{_docdir}/%{name}-doc
install -m 0644 %{name}.el %{buildroot}%{_sysconfdir}/emacs/site-start.d/
rm -f %{buildroot}%{_datadir}/emacs/site-lisp/%{rname}/etc/*.BAT
rm -f %{buildroot}%{_datadir}/emacs/site-lisp/%{rname}/etc/*.sparc
rm -f %{buildroot}%{_docdir}/%{name}-doc/*.dvi
rm -f %{buildroot}%{_docdir}/%{name}-doc/*.html

%if %{mdkversion} >= 200800
install -d %{buildroot}%{_datadir}/xemacs/site-lisp/%{name}
for D in lisp-xemacs etc
do
	pushd $D
	%makeinstall_std \
		EMACS=xemacs \
		PREFIX=%{buildroot}%{_prefix} \
		LISPDIR=%{buildroot}%{_datadir}/xemacs/site-lisp/%{rname} \
		ETCDIR=%{buildroot}%{_datadir}/xemacs/site-lisp/%{rname}/etc \
		INFODIR=%{buildroot}%{_infodir}
	popd
done
install -m 0644 %{xemacs_name}.el %{buildroot}%{_sysconfdir}/emacs/site-start.d/
rm -f %{buildroot}%{_datadir}/xemacs/site-lisp/%{rname}/etc/*.BAT
rm -f %{buildroot}%{_datadir}/xemacs/site-lisp/%{rname}/etc/*.sparc
%endif

%post
%_install_info %{rname}

%preun
%_remove_install_info %{rname}

%if %{mdkversion} >= 200800
%post -n %{xemacs_name}
%_install_info %{rname}

%preun -n %{xemacs_name}
%_remove_install_info %{rname}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ANNOUNCE ChangeLog README VERSION
%dir %{_datadir}/emacs/site-lisp
%{_datadir}/emacs/site-lisp/%{rname}
%{_infodir}/*
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/%{name}.el

%files doc
%defattr(-,root,root)
%doc doc/ess-intro-graphs.pdf doc/readme.pdf doc/html

%if %{mdkversion} >= 200800
%files -n %{xemacs_name}
%defattr(-,root,root)
%doc ANNOUNCE ChangeLog README VERSION
%dir %{_datadir}/xemacs/site-lisp
%dir %{_datadir}/xemacs/site-lisp/%{rname}
%{_datadir}/xemacs/site-lisp/%{rname}
%{_infodir}/*
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/%{xemacs_name}.el
%endif

