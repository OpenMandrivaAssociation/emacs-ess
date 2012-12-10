%define	rname ess
%define xemacs_name xemacs-%{rname}

Summary:	Emacs Speaks Statistics package for Emacs
Name:		emacs-%{rname}
Version:	5.13
Release:	2
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

%install
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

%files
%defattr(-,root,root)
%doc ANNOUNCE ChangeLog README VERSION
%{_datadir}/emacs/site-lisp/%{rname}
%{_infodir}/*
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/%{name}.el

%files doc
%defattr(-,root,root)
%doc doc/ess-intro-graphs.pdf doc/readme.pdf doc/html

%files -n %{xemacs_name}
%defattr(-,root,root)
%doc ANNOUNCE ChangeLog README VERSION
%{_datadir}/xemacs/site-lisp/%{rname}
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/%{xemacs_name}.el



%changelog
* Fri Feb 11 2011 Luc Menut <lmenut@mandriva.org> 5.13-1mdv2011.0
+ Revision: 637342
- update to 5.13

* Wed Nov 10 2010 Luc Menut <lmenut@mandriva.org> 5.12-1mdv2011.0
+ Revision: 595641
- update to 5.12

* Tue Jul 20 2010 Luc Menut <lmenut@mandriva.org> 5.11-1mdv2011.0
+ Revision: 556285
- update to 5.11

* Sat Jul 10 2010 Luc Menut <lmenut@mandriva.org> 5.10-1mdv2011.0
+ Revision: 550511
- update to 5.10

* Sun Mar 21 2010 Luc Menut <lmenut@mandriva.org> 5.8-1mdv2010.1
+ Revision: 526161
- update to 5.8

* Tue Jan 05 2010 Luc Menut <lmenut@mandriva.org> 5.7.1-1mdv2010.1
+ Revision: 486509
- update to version 5.7.1

* Tue Sep 01 2009 Luc Menut <lmenut@mandriva.org> 5.4-1mdv2010.0
+ Revision: 424043
- update to new version 5.4

* Fri Mar 20 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 5.3.11-1mdv2009.1
+ Revision: 358221
- update to new version 5.3.11 (mdvbz #48435)
- fix docs installation (use Luc Menut's spec changes)

* Thu Nov 06 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 5.3.8-2mdv2009.1
+ Revision: 300329
- add requires on emacs-el and xemacs-el (#44842)

* Thu Aug 07 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 5.3.8-1mdv2009.0
+ Revision: 266245
- update to new version 5.3.8
- spec file clean

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 5.3.6-3mdv2009.0
+ Revision: 244700
- rebuild

* Sat Jan 26 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 5.3.6-1mdv2008.1
+ Revision: 158380
- some minor changes in a spec file
- import emacs-ess


* Fri Jan 18 2008 Luc Menut <Luc.Menut@supagro.inra.fr> 5.3.6-1mdv2008.1
- Release 5.3.6
- fix site-start file for XEmacs
- build emacs-ess and xemacs-ess for mdkversion >= 200800

* Fri Sep 14 2007 Luc Menut <Luc.Menut@supagro.inra.fr> 5.3.5-1mdv2007.1
- initial Mandriva package
- based on Tom Moertel's spec file included in the ess source
