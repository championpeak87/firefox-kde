#
# spec file
#
# Copyright (c) 2023 SUSE LLC
# Copyright (c) 2006-2022 Wolfgang Rosenauer <wr@rosenauer.org>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%define _dwz_low_mem_die_limit  40000000
%define _dwz_max_die_limit     200000000

# changed with every update
# orig_version vs. mainver: To have beta-builds
# FF70beta3 would be released as FF69.99
# orig_version would be the upstream tar ball
# orig_version 70.0
# orig_suffix b3
# major 69
# mainver %major.99
%define major          108
%define mainver        %major.0.2
%define orig_version   108.0.2
%define orig_suffix    %{nil}
%define update_channel release
%define branding       1
%define devpkg         1

# PGO builds do not work in TW currently (bmo#1680306)
%define do_profiling   0

# upstream default is clang (to use gcc for large parts set to 0)
%define clang_build    0

%bcond_with only_print_mozconfig

# define if ccache should be used or not
%define useccache     0

# SLE-12 doesn't have this macro
%{!?_rpmmacrodir: %global _rpmmacrodir %{_rpmconfigdir}/macros.d}

# Firefox only supports i686
%ifarch %ix86
ExclusiveArch:  i586 i686
BuildArch:      i686
%{expand:%%global optflags %(echo "%optflags"|sed -e s/i586/i686/) -march=i686 -mtune=generic -msse2}
%endif
%{expand:%%global optflags %(echo "%optflags"|sed -e s/-Werror=return-type//) }
%{expand:%%global optflags %(echo "%optflags"|sed -e s/-flto=auto//) }

# general build definitions
%define progname firefox
%define appname  Firefox
%define pkgname  MozillaFirefox
%define srcname  firefox
%define progdir %{_prefix}/%_lib/%{progname}
%define gnome_dir     %{_prefix}
%define desktop_file_name %{progname}
%define firefox_appid \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
%define __provides_exclude ^lib.*\\.so.*$
%define __requires_exclude ^(libmoz.*|liblgpllibs.*|libxul.*)$
%define localize 1
%ifarch %ix86 x86_64
%define crashreporter 1
%else
%define crashreporter 0
%endif
%define with_pipewire0_3  1
%define wayland_supported 1
%if 0%{?sle_version} > 0 && 0%{?sle_version} < 150200
# pipewire is too old on Leap <=15.1
%define with_pipewire0_3 0
# Wayland is too old on Leap <=15.1 as well
%define wayland_supported 0
%endif

Name:           %{pkgname}
BuildRequires:  Mesa-devel
BuildRequires:  alsa-devel
BuildRequires:  autoconf213
BuildRequires:  dbus-1-glib-devel
BuildRequires:  dejavu-fonts
BuildRequires:  fdupes
BuildRequires:  memory-constraints
%if 0%{?suse_version} < 1550 && 0%{?sle_version} <= 150400
BuildRequires:  gcc11-c++
%else
BuildRequires:  gcc-c++
%endif
%if 0%{?suse_version} < 1550 && 0%{?sle_version} < 150300
BuildRequires:  cargo >= 1.63
BuildRequires:  rust >= 1.63
%else
# Newer sle/leap/tw use parallel versioned rust releases which have
# a different method for provides that we can use to request a
# specific version
# minimal requirement:
BuildRequires:  rust+cargo >= 1.63
# actually used upstream:
BuildRequires:  cargo1.65
BuildRequires:  rust1.65
%endif
%if 0%{useccache} != 0
BuildRequires:  ccache
%endif
BuildRequires:  libXcomposite-devel
BuildRequires:  libcurl-devel
BuildRequires:  libiw-devel
BuildRequires:  libproxy-devel
BuildRequires:  makeinfo
BuildRequires:  mozilla-nspr-devel >= 4.35
BuildRequires:  mozilla-nss-devel >= 3.85
BuildRequires:  nasm >= 2.14
BuildRequires:  nodejs >= 10.22.1
%if 0%{?sle_version} >= 120000 && 0%{?sle_version} < 150000
BuildRequires:  python-libxml2
BuildRequires:  python36
%else
BuildRequires:  python3 >= 3.5
BuildRequires:  python3-curses
BuildRequires:  python3-devel
%endif
BuildRequires:  rust-cbindgen >= 0.24.3
BuildRequires:  unzip
BuildRequires:  update-desktop-files
BuildRequires:  xorg-x11-libXt-devel
%if 0%{?do_profiling}
BuildRequires:  xvfb-run
%endif
BuildRequires:  yasm
BuildRequires:  zip
%if 0%{?suse_version} < 1550
BuildRequires:  pkgconfig(gconf-2.0) >= 1.2.1
%endif
%if (0%{?sle_version} >= 120000 && 0%{?sle_version} < 150000)
BuildRequires:  clang6-devel
%else
BuildRequires:  clang-devel >= 5
%endif
BuildRequires:  pkgconfig(glib-2.0) >= 2.22
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.14.0
BuildRequires:  pkgconfig(gtk+-unix-print-3.0)
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(libpulse)
%if %{with_pipewire0_3}
BuildRequires:  pkgconfig(libpipewire-0.3)
%endif
# libavcodec is required for H.264 support but the
# openSUSE version is currently not able to play H.264
# therefore the Packman version is required
# minimum version of libavcodec is 53
Recommends:     libavcodec-full >= 0.10.16
Version:        %{mainver}
Release:        0
%if "%{name}" == "MozillaFirefox"
Provides:       firefox = %{mainver}
Provides:       firefox = %{version}-%{release}
%endif
Provides:       web_browser
Provides:       appdata()
Provides:       appdata(firefox.appdata.xml)
# this is needed to match this package with the kde4 helper package without the main package
# having a hard requirement on the kde4 package
%define kde_helper_version 6
Provides:       mozilla-kde4-version = %{kde_helper_version}
Summary:        Mozilla %{appname} Web Browser
License:        MPL-2.0
Group:          Productivity/Networking/Web/Browsers
URL:            http://www.mozilla.org/
%if !%{with only_print_mozconfig}
Source:         https://ftp.mozilla.org/pub/%{srcname}/releases/%{version}%{orig_suffix}/source/%{srcname}-%{orig_version}%{orig_suffix}.source.tar.xz
Source1:        MozillaFirefox.desktop
Source2:        MozillaFirefox-rpmlintrc
Source3:        mozilla.sh.in
Source4:        tar_stamps
%if %{localize}
Source7:        l10n-%{orig_version}%{orig_suffix}.tar.xz
%endif
Source8:        firefox-mimeinfo.xml
Source9:        firefox.js
Source11:       firefox.1
Source12:       mozilla-get-app-id
Source13:       spellcheck.js
Source14:       https://github.com/openSUSE/firefox-scripts/raw/4503820/create-tar.sh
Source15:       firefox-appdata.xml
Source16:       %{name}.changes
Source17:       firefox-search-provider.ini
# Set up API keys, see http://www.chromium.org/developers/how-tos/api-keys
# Note: these are for the openSUSE Firefox builds ONLY. For your own distribution,
# please get your own set of keys.
Source18:       mozilla-api-key
Source19:       google-api-key
Source20:       https://ftp.mozilla.org/pub/%{srcname}/releases/%{version}%{orig_suffix}/source/%{srcname}-%{orig_version}%{orig_suffix}.source.tar.xz.asc
Source21:       https://ftp.mozilla.org/pub/%{srcname}/releases/%{version}%{orig_suffix}/KEY#/mozilla.keyring
# Gecko/Toolkit
Patch1:         mozilla-nongnome-proxies.patch
Patch2:         mozilla-kde.patch
Patch3:         mozilla-ntlm-full-path.patch
Patch4:         mozilla-aarch64-startup-crash.patch
Patch5:         mozilla-fix-aarch64-libopus.patch
Patch6:         mozilla-s390-context.patch
Patch7:         mozilla-pgo.patch
Patch8:         mozilla-reduce-rust-debuginfo.patch
Patch9:         mozilla-bmo1005535.patch
Patch10:        mozilla-bmo1568145.patch
Patch11:        mozilla-bmo1504834-part1.patch
Patch13:        mozilla-bmo1504834-part3.patch
Patch14:        mozilla-bmo1512162.patch
Patch15:        mozilla-fix-top-level-asm.patch
Patch17:        mozilla-bmo849632.patch
Patch18:        mozilla-bmo998749.patch
Patch20:        mozilla-s390x-skia-gradient.patch
Patch21:        mozilla-libavcodec58_91.patch
Patch22:        mozilla-silence-no-return-type.patch
Patch23:        mozilla-bmo531915.patch
Patch25:        one_swizzle_to_rule_them_all.patch
Patch27:        mozilla-buildfixes.patch
# Firefox/browser
Patch101:       firefox-kde.patch
Patch102:       firefox-branded-icons.patch
Patch103:       unity-menubar.patch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires(post): coreutils shared-mime-info desktop-file-utils
Requires(postun):shared-mime-info desktop-file-utils
Requires:       %{name}-branding >= 68
#%requires_ge    mozilla-nspr
#%requires_ge    mozilla-nss
#%requires_ge    libfreetype6
Recommends:     libcanberra0
Recommends:     libpulse0
# addon leads to startup crash (bnc#908892)
Obsoletes:      tracker-miner-firefox < 0.15
%if 0%{?devpkg} == 0
Obsoletes:      %{name}-devel < %{version}
%endif
# libproxy's mozjs pacrunner crashes FF (bnc#759123)
%if 0%{?suse_version} < 1220
Obsoletes:      libproxy1-pacrunner-mozjs <= 0.4.7
%endif
ExcludeArch:    armv6l armv6hl ppc ppc64 ppc64le

%description
Mozilla Firefox is a standalone web browser, designed for standards
compliance and performance.  Its functionality can be enhanced via a
plethora of extensions.

%if 0%{?devpkg}
%package devel
Summary:        Devel package for %{appname}
Group:          Development/Tools/Other
Provides:       firefox-devel = %{version}-%{release}
Requires:       %{name} = %{version}
Requires:       perl(Archive::Zip)
Requires:       perl(XML::Simple)

%description devel
Development files for %{appname} to make packaging of addons easier.
%endif

%if %localize
%package translations-common
Summary:        Common translations for %{appname}
Group:          System/Localization
Provides:       locale(%{name}:ar;ca;cs;da;de;el;en_GB;es_AR;es_CL;es_ES;fi;fr;hu;it;ja;ko;nb_NO;nl;pl;pt_BR;pt_PT;ru;sv_SE;zh_CN;zh_TW)
# This is there for updates from Firefox before the translations-package was split up into 2 packages
Provides:       %{name}-translations
Requires:       %{name} = %{version}
Obsoletes:      %{name}-translations < %{version}-%{release}

%description translations-common
This package contains several common languages for the user interface
of %{appname}.

%package translations-other
Summary:        Extra translations for %{appname}
Group:          System/Localization
Provides:       locale(%{name}:ach;af;an;ast;az;be;bg;bn;br;bs;cak;cy;dsb;en_CA;eo;es_MX;et;eu;fa;ff;fy_NL;ga_IE;gd;gl;gn;gu_IN;he;hi_IN;hr;hsb;hy_AM;ia;id;is;ka;kab;kk;km;kn;lij;lt;lv;mk;mr;ms;my;ne_NP;nn_NO;oc;pa_IN;rm;ro;si;sk;sl;son;sq;sr;ta;te;th;tr;uk;ur;uz;vi;xh)
Requires:       %{name} = %{version}
Obsoletes:      %{name}-translations < %{version}-%{release}

%description translations-other
This package contains rarely used languages for the user interface
of %{appname}.
%endif

%package branding-upstream
Summary:        Upstream branding for %{appname}
Group:          Productivity/Networking/Web/Browsers
Provides:       %{name}-branding = %{version}
Conflicts:      otherproviders(%{name}-branding)
Supplements:    packageand(%{name}:branding-upstream)
#BRAND: Provide three files -
#BRAND: /usr/lib/firefox/browserconfig.properties that contains the
#BRAND: default homepage and some other default configuration options
#BRAND: /usr/lib/firefox/defaults/profile/bookmarks.html that contains
#BRAND: the list of default bookmarks
#BRAND: It's also possible to create a file
#BRAND: /usr/lib/firefox/defaults/preferences/firefox-$vendor.js to set
#BRAND: custom preference overrides.
#BRAND: It's also possible to drop files in /usr/lib/firefox/distribution/searchplugins/common/

%description branding-upstream
This package provides upstream look and feel for %{appname}.

%if !%{with only_print_mozconfig}
%prep
%if %localize

# If generated incorrectly, the tarball will be ~270B in
# size, so 1MB seems like good enough limit to check.
MINSIZE=1048576
if (( $(stat -Lc%s "%{SOURCE7}") < MINSIZE)); then
    echo "Translations tarball %{SOURCE7} not generated properly."
    exit 1
fi

%setup -q -n %{srcname}-%{orig_version} -b 7
%else
%setup -q -n %{srcname}-%{orig_version}
%endif
cd $RPM_BUILD_DIR/%{srcname}-%{orig_version}
%autopatch -p1
%endif

%build
%if !%{with only_print_mozconfig}
# no need to add build time to binaries
modified="$(sed -n '/^----/n;s/ - .*$//;p;q' "%{_sourcedir}/%{pkgname}.changes")"
DATE="\"$(date -d "${modified}" "+%%b %%e %%Y")\""
TIME="\"$(date -d "${modified}" "+%%R")\""
find . -regex ".*\.c\|.*\.cpp\|.*\.h" -exec sed -i "s/__DATE__/${DATE}/g;s/__TIME__/${TIME}/g" {} +

# SLE-12 provides python36, but that package does not provide a python3 binary
%if 0%{?sle_version} >= 120000 && 0%{?sle_version} < 150000
sed -i "s/python3/python36/g" configure.in
sed -i "s/python3/python36/g" mach
export PYTHON3=/usr/bin/python36
%endif

#
kdehelperversion=$(cat toolkit/xre/nsKDEUtils.cpp | grep '#define KMOZILLAHELPER_VERSION' | cut -d ' ' -f 3)
if test "$kdehelperversion" != %{kde_helper_version}; then
  echo fix kde helper version in the .spec file
  exit 1
fi
# When doing only_print_mozconfig, this file isn't necessarily available, so skip it
cp %{SOURCE4} .obsenv.sh
%else
# We need to make sure its empty
echo "" > .obsenv.sh
%endif

cat >> .obsenv.sh <<EOF
export CARGO_HOME=${RPM_BUILD_DIR}/%{srcname}-%{orig_version}/.cargo
export MOZ_SOURCE_CHANGESET=\$RELEASE_TAG
export SOURCE_REPO=\$RELEASE_REPO
export source_repo=\$RELEASE_REPO
export MOZ_SOURCE_REPO=\$RELEASE_REPO
export MOZ_BUILD_DATE=\$RELEASE_TIMESTAMP
export MOZILLA_OFFICIAL=1
export BUILD_OFFICIAL=1
export MOZ_TELEMETRY_REPORTING=1
export MACH_BUILD_PYTHON_NATIVE_PACKAGE_SOURCE=system
export CFLAGS="%{optflags}"
%if 0%{?suse_version} < 1550 && 0%{?sle_version} <= 150400
export CC=gcc-11
%else
%if 0%{?clang_build} == 0
export CC=gcc
export CXX=g++
%if 0%{?gcc_version:%{gcc_version}} >= 12
export CFLAGS="\$CFLAGS -fimplicit-constexpr"
%endif
%endif
%endif
%ifarch %arm %ix86
# Limit RAM usage during link
export LDFLAGS="\$LDFLAGS -Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
# A lie to prevent -Wl,--gc-sections being set which requires more memory than 32bit can offer
export GC_SECTIONS_BREAKS_DEBUG_RANGES=yes
%endif
export LDFLAGS="\$LDFLAGS -fPIC -Wl,-z,relro,-z,now"
%ifarch ppc64 ppc64le
%if 0%{?clang_build} == 0
export CFLAGS="\$CFLAGS -mminimal-toc"
%endif
%endif
export CXXFLAGS="\$CFLAGS"
export MOZCONFIG=$RPM_BUILD_DIR/mozconfig
EOF
# Done with env-variables.
source ./.obsenv.sh

%ifarch aarch64 %arm ppc64 ppc64le
%limit_build -m 2500
%endif

# Generating mozconfig
cat << EOF > $MOZCONFIG
mk_add_options MOZILLA_OFFICIAL=1
mk_add_options BUILD_OFFICIAL=1
mk_add_options MOZ_MAKE_FLAGS=%{?jobs:-j%jobs}
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/../obj
. \$topsrcdir/browser/config/mozconfig
ac_add_options --disable-bootstrap
ac_add_options --prefix=%{_prefix}
ac_add_options --libdir=%{_libdir}
ac_add_options --includedir=%{_includedir}
ac_add_options --enable-release
%if 0%{wayland_supported}
ac_add_options --enable-default-toolkit=cairo-gtk3-wayland
%else
ac_add_options --enable-default-toolkit=cairo-gtk3
%endif
# bmo#1441155 - Disable the generation of Rust debug symbols on Linux32
%ifarch %ix86 %arm
ac_add_options --disable-debug-symbols
%else
ac_add_options --enable-debug-symbols=-g1
%endif
ac_add_options --disable-install-strip
# building with elf-hack started to fail everywhere with FF73
#%if 0%{?suse_version} > 1549
%ifarch %arm %ix86 x86_64
ac_add_options --disable-elf-hack
%endif
#%endif
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
%if 0%{useccache} != 0
ac_add_options --with-ccache
%endif
%if %{localize}
ac_add_options --with-l10n-base=$RPM_BUILD_DIR/l10n
%endif
#ac_add_options --with-system-jpeg    # libjpeg-turbo is used internally
#ac_add_options --with-system-png     # doesn't work because of missing APNG support
ac_add_options --with-system-zlib
ac_add_options --disable-updater
ac_add_options --disable-tests
ac_add_options --enable-alsa
ac_add_options --disable-debug
ac_add_options --enable-update-channel=%{update_channel}
ac_add_options --with-mozilla-api-keyfile=%{SOURCE18}
# Google-service currently not available for free anymore
#ac_add_options --with-google-location-service-api-keyfile=%{SOURCE19}
ac_add_options --with-google-safebrowsing-api-keyfile=%{SOURCE19}
ac_add_options --with-unsigned-addon-scopes=app
ac_add_options --allow-addon-sideload
# at least temporary until the "wasi-sysroot" issue is solved
ac_add_options --without-wasm-sandboxed-libraries
%ifarch x86_64 aarch64
ac_add_options --enable-rust-simd
%endif
%if %branding
ac_add_options --enable-official-branding
%endif
ac_add_options --enable-libproxy
%if ! %crashreporter
ac_add_options --disable-crashreporter
%endif
%ifarch %arm
ac_add_options --with-fpu=vfpv3-d16
ac_add_options --with-float-abi=hard
%ifarch armv6l armv6hl
ac_add_options --with-arch=armv6
%else
ac_add_options --with-arch=armv7-a
%endif
%endif
# mitigation/workaround for bmo#1512162
%ifarch s390x
ac_add_options --enable-optimize="-O1"
%endif
%ifarch x86_64
# LTO needs newer toolchain stack only (at least GCC 8.2.1 (r268506)
%if 0%{?suse_version} > 1500
ac_add_options --enable-lto
%if 0%{?do_profiling}
ac_add_options MOZ_PGO=1
%endif
%endif
%endif
EOF

%if %{with only_print_mozconfig}
cat ./.obsenv.sh
cat $MOZCONFIG
%else

%if 0%{useccache} != 0
ccache -s
%endif
%if 0%{?do_profiling}
xvfb-run --server-args="-screen 0 1920x1080x24" \
%endif
./mach build -v

# build additional locales
%if %localize
truncate -s 0 %{_tmppath}/translations.{common,other}
# langpack-build can not be done in parallel easily (see https://bugzilla.mozilla.org/show_bug.cgi?id=1660943)
# Therefore, we have to have a separate obj-dir for each language
# We do this, by creating a mozconfig-template with the necessary switches
# and a placeholder obj-dir, which gets copied and modified for each language

# Create mozconfig-template for langbuild
cat << EOF > ${MOZCONFIG}_LANG
mk_add_options MOZILLA_OFFICIAL=1
mk_add_options BUILD_OFFICIAL=1
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/../obj_LANG
. \$topsrcdir/browser/config/mozconfig
ac_add_options --prefix=%{_prefix}
ac_add_options --with-l10n-base=$RPM_BUILD_DIR/l10n
ac_add_options --disable-updater
ac_add_options --without-wasm-sandboxed-libraries
%if %branding
ac_add_options --enable-official-branding
%endif
EOF

%ifarch %ix86
%define njobs 1
%else
%define njobs 0%{?jobs:%jobs}
%endif
mkdir -p $RPM_BUILD_DIR/langpacks_artifacts/
sed -r '/^(ja-JP-mac|ga-IE|en-US|)$/d;s/ .*$//' $RPM_BUILD_DIR/%{srcname}-%{orig_version}/browser/locales/shipped-locales \
    | xargs -n 1 %{?njobs:-P %njobs} -I {} /bin/sh -c '
        locale=$1
        cp ${MOZCONFIG}_LANG ${MOZCONFIG}_$locale
        sed -i "s|obj_LANG|obj_$locale|" ${MOZCONFIG}_$locale
        export MOZCONFIG=${MOZCONFIG}_$locale
        # nsinstall is needed for langpack-build. It is already built by `./mach build`, but building it again is very fast
        ./mach build config/nsinstall langpack-$locale
        cp -L ../obj_$locale/dist/linux-*/xpi/firefox-%{orig_version}.$locale.langpack.xpi \
            $RPM_BUILD_DIR/langpacks_artifacts/langpack-$locale@firefox.mozilla.org.xpi
        # check against the fixed common list and sort into the right filelist
        _matched=0
        for _match in ar ca cs da de el en-GB es-AR es-CL es-ES fi fr hu it ja ko nb-NO nl pl pt-BR pt-PT ru sv-SE zh-CN zh-TW; do
            [ "$_match" = "$locale" ] && _matched=1
        done
        [ $_matched -eq 1 ] && _l10ntarget=common || _l10ntarget=other
        echo %{progdir}/browser/extensions/langpack-$locale@firefox.mozilla.org.xpi \
            >> %{_tmppath}/translations.$_l10ntarget
' -- {}
%endif

%if 0%{useccache} != 0
ccache -s
%endif
%endif

%install
cd $RPM_BUILD_DIR/obj
source %{SOURCE4}
export MOZ_SOURCE_STAMP=$RELEASE_TAG
export MOZ_SOURCE_REPO=$RELEASE_REPO
# need to remove default en-US firefox-l10n.js before it gets
# populated into browser's omni.ja; it only contains general.useragent.locale
# which should be loaded from each language pack (set in firefox.js)
rm dist/bin/browser/defaults/preferences/firefox-l10n.js
make -C browser/installer STRIP=/bin/true MOZ_PKG_FATAL_WARNINGS=0
#DEBUG (break the build if searchplugins are missing / temporary)
grep amazondotcom dist/firefox/browser/omni.ja
# copy tree into RPM_BUILD_ROOT
mkdir -p %{buildroot}%{progdir}
cp -rf $RPM_BUILD_DIR/obj/dist/%{srcname}/* %{buildroot}%{progdir}
mkdir -p %{buildroot}%{progdir}/browser/extensions
cp -rf $RPM_BUILD_DIR/langpacks_artifacts/* %{buildroot}%{progdir}/browser/extensions/
mkdir -p %{buildroot}%{progdir}/distribution/extensions
mkdir -p %{buildroot}%{progdir}/browser/defaults/preferences/
# renaming executables (for regular vs. ESR)
%if "%{srcname}" != "%{progname}"
mv %{buildroot}%{progdir}/%{srcname} %{buildroot}%{progdir}/%{progname}
mv %{buildroot}%{progdir}/%{srcname}-bin %{buildroot}%{progdir}/%{progname}-bin
%endif
# install gre prefs
install -m 644 %{SOURCE13} %{buildroot}%{progdir}/defaults/pref/
# install browser prefs
install -m 644 %{SOURCE9} %{buildroot}%{progdir}/browser/defaults/preferences/firefox.js

# remove some executable permissions
find %{buildroot}%{progdir} \
     -name "*.js" -o \
     -name "*.jsm" -o \
     -name "*.rdf" -o \
     -name "*.properties" -o \
     -name "*.dtd" -o \
     -name "*.txt" -o \
     -name "*.xml" -o \
     -name "*.css" \
     -exec chmod a-x {} +
# remove mkdir.done files from installed base
find %{buildroot}%{progdir} -type f -name ".mkdir.done" -delete
# overwrite the mozilla start-script and link it to /usr/bin
mkdir --parents %{buildroot}/usr/bin
sed "s:%%PREFIX:%{_prefix}:g
s:%%PROGDIR:%{progdir}:g
s:%%APPNAME:%{progname}:g
s:%%WAYLAND_SUPPORTED:%{wayland_supported}:g
s:%%PROFILE:.mozilla/firefox:g" \
  %{SOURCE3} > %{buildroot}%{progdir}/%{progname}.sh
chmod 755 %{buildroot}%{progdir}/%{progname}.sh
ln -sf ../..%{progdir}/%{progname}.sh %{buildroot}%{_bindir}/%{progname}
# desktop file
mkdir -p %{buildroot}%{_datadir}/applications
sed "s:%%NAME:%{appname}:g
s:%%EXEC:%{progname}:g
s:%%ICON:%{progname}:g" \
  %{SOURCE1} > %{buildroot}%{_datadir}/applications/%{desktop_file_name}.desktop
%suse_update_desktop_file %{desktop_file_name} Network WebBrowser GTK
# additional mime-types
mkdir -p %{buildroot}%{_datadir}/mime/packages
cp %{SOURCE8} %{buildroot}%{_datadir}/mime/packages/%{progname}.xml
# appdata
mkdir -p %{buildroot}%{_datadir}/metainfo
sed "s:firefox.desktop:%{desktop_file_name}:g" \
  %{SOURCE15} > %{buildroot}%{_datadir}/metainfo/%{desktop_file_name}.appdata.xml
# install man-page
mkdir -p %{buildroot}%{_mandir}/man1/
cp %{SOURCE11} %{buildroot}%{_mandir}/man1/%{progname}.1
# install GNOME Shell search provider
mkdir -p %{buildroot}%{_datadir}/gnome-shell/search-providers
cp %{SOURCE17} %{buildroot}%{_datadir}/gnome-shell/search-providers
##########
# ADDONS
#
mkdir -p %{buildroot}%{_datadir}/mozilla/extensions/%{firefox_appid}
mkdir -p %{buildroot}%{_libdir}/mozilla/extensions/%{firefox_appid}
# Install symbolic icon for GNOME
%if %branding
for size in 16 22 24 32 48 64 128 256; do
%else
for size in 16 32 48; do
%endif
  mkdir -p %{buildroot}%{gnome_dir}/share/icons/hicolor/${size}x${size}/apps/
  cp %{buildroot}%{progdir}/browser/chrome/icons/default/default$size.png \
         %{buildroot}%{gnome_dir}/share/icons/hicolor/${size}x${size}/apps/%{progname}.png
done
# excludes
rm -f %{buildroot}%{progdir}/updater.ini
rm -f %{buildroot}%{progdir}/removed-files
rm -f %{buildroot}%{progdir}/README.txt
rm -f %{buildroot}%{progdir}/old-homepage-default.properties
rm -f %{buildroot}%{progdir}/run-mozilla.sh
rm -f %{buildroot}%{progdir}/LICENSE
rm -f %{buildroot}%{progdir}/precomplete
rm -f %{buildroot}%{progdir}/update-settings.ini
%if 0%{?devpkg}
# devel
mkdir -p %{buildroot}%{_bindir}
install -m 755 %SOURCE12 %{buildroot}%{_bindir}
# inspired by mandriva
mkdir -p %{buildroot}%{_rpmmacrodir}
cat <<'FIN' >%{buildroot}%{_rpmmacrodir}/macros.%{progname}
# Macros from %{name} package
%%firefox_major              %{major}
%%firefox_version            %{version}
%%firefox_mainver            %{mainver}
%%firefox_mozillapath        %%{_libdir}/%{progname}
%%firefox_pluginsdir         %%{_libdir}/mozilla/plugins
%%firefox_appid              \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
%%firefox_extdir             %%(if [ "%%_target_cpu" = "noarch" ]; then echo %%{_datadir}/mozilla/extensions/%%{firefox_appid}; else echo %%{_libdir}/mozilla/extensions/%%{firefox_appid}; fi)

%%firefox_ext_install() \
   extdir="%%{buildroot}%%{firefox_extdir}/`mozilla-get-app-id '%%1'`" \
   mkdir -p "$extdir" \
   %%{__unzip} -q -d "$extdir" "%%1" \
   %%{nil}
FIN
%endif
# fdupes
%fdupes %{buildroot}%{progdir}
%fdupes %{buildroot}%{_datadir}

%post
# update mime and desktop database
%mime_database_post
%desktop_database_post
%icon_theme_cache_post
exit 0

%postun
%icon_theme_cache_postun
%desktop_database_postun
%mime_database_postun
exit 0

%files
%defattr(-,root,root)
%dir %{progdir}
%dir %{progdir}/browser/
%dir %{progdir}/browser/chrome/
%{progdir}/browser/defaults
%{progdir}/browser/features/
%{progdir}/browser/chrome/icons
%{progdir}/browser/omni.ja
%dir %{progdir}/distribution/
%{progdir}/distribution/extensions/
%{progdir}/defaults/
%{progdir}/gmp-clearkey/
%attr(755,root,root) %{progdir}/%{progname}.sh
%{progdir}/%{progname}
%{progdir}/%{progname}-bin
%{progdir}/application.ini
%{progdir}/dependentlibs.list
%{progdir}/*.so
%{progdir}/omni.ja
%{progdir}/fonts/
%{progdir}/pingsender
%{progdir}/platform.ini
%{progdir}/plugin-container
%if %crashreporter
%{progdir}/crashreporter
%{progdir}/crashreporter.ini
%{progdir}/Throbber-small.gif
%{progdir}/minidump-analyzer
%{progdir}/browser/crashreporter-override.ini
%endif
%{_datadir}/applications/%{desktop_file_name}.desktop
%{_datadir}/mime/packages/%{progname}.xml
%dir %{_datadir}/gnome-shell
%dir %{_datadir}/gnome-shell/search-providers
%{_datadir}/gnome-shell/search-providers/*.ini
%dir %{_datadir}/mozilla
%dir %{_datadir}/mozilla/extensions
%dir %{_datadir}/mozilla/extensions/%{firefox_appid}
%dir %{_libdir}/mozilla
%dir %{_libdir}/mozilla/extensions
%dir %{_libdir}/mozilla/extensions/%{firefox_appid}
%{gnome_dir}/share/icons/hicolor/
%{_bindir}/%{progname}
%doc %{_mandir}/man1/%{progname}.1.gz
%{_datadir}/metainfo/

%if 0%{?devpkg}
%files devel
%defattr(-,root,root)
%{_bindir}/mozilla-get-app-id
%{_rpmmacrodir}/macros.%{progname}
%endif

%if %localize
%files translations-common -f %{_tmppath}/translations.common
%defattr(-,root,root)
%dir %{progdir}
%dir %{progdir}/browser/extensions/

%files translations-other -f %{_tmppath}/translations.other
%defattr(-,root,root)
%dir %{progdir}
%dir %{progdir}/browser/extensions/
%endif

# this package does not need to provide files but is needed to fulfill
# requirements if no other branding package is to be installed
%files branding-upstream
%defattr(-,root,root)
%dir %{progdir}

%changelog
* Mon Jan 09 2023 Kalev Lember <klember@redhat.com> - 108.0.1-4
- Drop conditionals for F35

* Wed Dec 21 2022 Martin Stransky <stransky@redhat.com>- 108.0.1-3
- Added second arch build fix

* Wed Dec 21 2022 Martin Stransky <stransky@redhat.com>- 108.0.1-2
- Added mozbz#1795851 [wayland] Crash buffer size (170x113)
  is not divisible by scale (2)

* Mon Dec 19 2022 Martin Stransky <stransky@redhat.com>- 108.0.1-1
- Update to 108.0.1

* Wed Dec 14 2022 Martin Stransky <stransky@redhat.com>- 108.0-2
- Update to 108.0 Build 2
- Added fix for rhbz#2149821

* Tue Dec 6 2022 Martin Stransky <stransky@redhat.com>- 108.0-1
- Update to 108.0

* Tue Dec 6 2022 Martin Stransky <stransky@redhat.com>- 107.0.1-1
- Update to 107.0.1

* Thu Nov 24 2022 Martin Stransky <stransky@redhat.com>- 107.0-4
- Added fix for mozbz#1779186 - fix VA-API playback artifacts

* Mon Nov 21 2022 Martin Stransky <stransky@redhat.com>- 107.0-3
- Disabled crashreporter

* Mon Nov 21 2022 Jan Horak <jhorak@redhat.com> - 107.0-2
- Enabled mozilla crashreporter again

* Mon Nov 14 2022 Martin Stransky <stransky@redhat.com>- 107.0-1
- Update to 107.0

* Fri Nov 04 2022 Martin Stransky <stransky@redhat.com>- 106.0.4-1
- Update to 106.0.4

* Mon Oct 31 2022 Martin Stransky <stransky@redhat.com>- 106.0.3-1
- Update to 106.0.3

* Sun Oct 23 2022 Martin Stransky <stransky@redhat.com>- 106.0.1-1
- Update to 106.0.1
- Require xdg-desktop-portal when file dialog portal is used.
- Disabled file dialog portals on F37+

* Thu Oct 20 2022 Jan Grulich <jgrulich@redhat.com> - 106.0-2
- Enable upstream WebRTC code for screensharing on Wayland

* Fri Oct 14 2022 Martin Stransky <stransky@redhat.com>- 106.0-1
- Updated to 106.0
- Disabled PGO build due to rhbz#2136401

* Fri Oct 14 2022 Martin Stransky <stransky@redhat.com>- 105.0.2-2
- Fixed crashes on multi-monitor systems (mzbz#1793922)

* Wed Oct 5 2022 Martin Stransky <stransky@redhat.com>- 105.0.2-1
- Updated to 105.0.2

* Fri Sep 30 2022 Martin Stransky <stransky@redhat.com>- 105.0.1-2
- Added fix for mozilla#1791856 / rhbz#2130087

* Thu Sep 22 2022 Martin Stransky <stransky@redhat.com>- 105.0.1-1
- Updated to 105.0.1
- Excluded i686 due to https://bugzilla.mozilla.org/show_bug.cgi?id=1792159,
  https://bugzilla.redhat.com/show_bug.cgi?id=2129720

* Tue Sep 20 2022 Martin Stransky <stransky@redhat.com>- 105.0-1
- Updated to 105.0

* Tue Sep 6 2022 Martin Stransky <stransky@redhat.com>- 104.0.2-1
- Updated to 104.0.2

* Tue Aug 30 2022 Martin Stransky <stransky@redhat.com>- 104.0.1-1
- Updated to 104.0.1

* Tue Aug 23 2022 Kalev Lember <klember@redhat.com> - 104.0-5
- Use constrain_build macro to simplify parallel make handling
- Drop obsolete build conditionals
- Drop unused patches
- Use build_ldflags
- Drop hardened_build option
- Re-enable s390x builds

* Tue Aug 23 2022 Jan Horak <jhorak@redhat.com> - 104.0-4
- Rebuild due to ppc64le fixes

* Mon Aug 22 2022 Eike Rathke <erack@redhat.com> - 104.0-3
- Update to 104.0 respin

* Wed Aug 17 2022 Martin Stransky <stransky@redhat.com>- 104.0-2
- Added build fixes

* Tue Aug 16 2022 Martin Stransky <stransky@redhat.com>- 104.0-1
- Updated to 104.0

* Fri Aug 12 2022 Martin Stransky <stransky@redhat.com>- 103.0.2-1
- Updated to 103.0.2

* Thu Aug 4 2022 Martin Stransky <stransky@redhat.com>- 103.0.1-2
- Added arm build fixes by Gabriel Hojda
- Enable VA-API (rhbz#2115253)

* Tue Aug 2 2022 Martin Stransky <stransky@redhat.com>- 103.0.1-1
- Update to 103.0.1

* Tue Jul 26 2022 Martin Stransky <stransky@redhat.com>- 103.0-1
- Update to 103.0
- Disabled ppc64le due to webrtc build failures (rhbz#2113850)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 102.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Martin Stransky <stransky@redhat.com>- 102.0-3
- Update preference logging.
- Added ARM fixes by Gabriel Hojda.

* Mon Jul 11 2022 Jan Grulich <jgrulich@redhat.com> - 102.0-2
- Backport upstream fixes to WebRTC for screensharing on Wayland

* Tue Jun 28 2022 Martin Stransky <stransky@redhat.com>- 102.0-1
- Updated to 102.0
- Applied patch from https://src.fedoraproject.org/rpms/firefox/pull-request/43

* Mon Jun 27 2022 Martin Stransky <stransky@redhat.com>- 101.0.1-7
- Rebuild

* Fri Jun 17 2022 Martin Stransky <stransky@redhat.com>- 101.0.1-6
- Added fix for mozbz#1774271 - Intel/dmabuf export issues.

* Wed Jun 15 2022 Martin Stransky <stransky@redhat.com>- 101.0.1-5
- Added fix for mozbz#1758948 (AV1 VA-API playback shuttering)

* Tue Jun 14 2022 Martin Stransky <stransky@redhat.com>- 101.0.1-3
- Added fixes for mozbz#1773377 and mozbz#1774075

* Mon Jun 13 2022 Martin Stransky <stransky@redhat.com>- 101.0.1-2
- Fix WebGL mem leaks (mzbz#1773968)

* Thu Jun 9 2022 Martin Stransky <stransky@redhat.com>- 101.0.1-1
- Updated to 101.0.1
- More VA-API sandbox fixes (mzbz#1769182)
- Fixed OpenH264 decode (rhbz#2094319)

* Tue Jun 7 2022 Martin Stransky <stransky@redhat.com>- 101.0-2
- Enabled VA-API by default (+ added VA-API fixes from upstream)
- Fixed WebGL performance on NVIDIA drivers (mzbz#1735929)

* Mon May 30 2022 Martin Stransky <stransky@redhat.com>- 101.0-1
- Updated to 101.0

* Wed May 25 2022 Martin Stransky <stransky@redhat.com>- 100.0.2-2
- Added fix for mzbz#1771104

* Fri May 20 2022 Martin Stransky <stransky@redhat.com>- 100.0.2-1
- Updated to 100.0.2

* Wed May 18 2022 Martin Stransky <stransky@redhat.com>- 100.0.1-1
- Updated to 100.0.1

* Mon May 16 2022 Jan Horak <jhorak@redhat.com> - 100.0-6
- Fix spellchecker.dictionary_path of F36+

* Tue May 10 2022 Jan Horak <jhorak@redhat.com> - 100.0-5
- Fix crashes on f36 multimonitor setup and too big profile manager

* Mon May 9 2022 Martin Stransky <stransky@redhat.com>- 100.0-4
- Added fix for mozbz#1767916.

* Thu May 5 2022 Martin Stransky <stransky@redhat.com>- 100.0-3
- Removed Fedora user agent patch (rhbz#2081791).

* Tue May 3 2022 Martin Stransky <stransky@redhat.com>- 100.0-2
- Added fix for mozbz#1759137

* Mon May 2 2022 Martin Stransky <stransky@redhat.com>- 100.0-1
- Updated to 100.0

* Thu Apr 28 2022 Jan Horak <jhorak@redhat.com> - 99.0.1-2
- Fixing bookmark install location - rhbz#2054953

* Wed Apr 13 2022 Martin Stransky <stransky@redhat.com> - 99.0.1-1
- Updated to 99.0.1

* Wed Apr 6 2022 Martin Stransky <stransky@redhat.com> - 99.0-1
- Updated to 99.0

* Thu Mar 31 2022 Martin Stransky <stransky@redhat.com> - 98.0.2-1
- Updated to 98.0.2

* Wed Mar 30 2022 Jan Grulich <jgrulich@redhat.com> - 98.0-4
- Wayland screensharing: avoid potential crash when cursor metadata are not set

* Wed Mar 16 2022 Martin Stransky <stransky@redhat.com> - 98.0-3
- Added a workaround for rhbz#2063961

* Wed Mar 2 2022 Martin Stransky <stransky@redhat.com> - 98.0-2
- Added support for ffmpeg 5.0
- Spec tweaks
- Updated to Build 3

* Tue Mar 1 2022 Martin Stransky <stransky@redhat.com> - 98.0-1
- Updated to 98.0

* Mon Feb 21 2022 Jan Grulich <jgrulich@redhat.com> - 97.0.1-2
- Backport WebRTC changes to PipeWire/Wayland screen sharing support

* Fri Feb 18 2022 Martin Stransky <stransky@redhat.com> - 97.0.1-1
- Updated to 97.0.1
- GCC 12 build fixes

* Tue Feb 8 2022 Martin Stransky <stransky@redhat.com> - 97.0-1
- Updated to 97.0

* Mon Jan 31 2022 Martin Stransky <stransky@redhat.com> - 96.0.3-1
- Updated to 96.0.3

* Tue Jan 25 2022 Parag Nemade <pnemade AT redhat DOT com> - 96.0.1-3
- Update hunspell-dir path
  F36 Change https://fedoraproject.org/wiki/Changes/Hunspell_dictionary_dir_change

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 96.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 18 2022 Martin Stransky <stransky@redhat.com> - 96.0.1-1
- Updated to 96.0.1

* Tue Jan 11 2022 Martin Stransky <stransky@redhat.com> - 96.0-1
- Updated to 96.0

* Sat Jan 08 2022 Miro Hrončok <mhroncok@redhat.com> - 95.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/LIBFFI34

* Thu Dec 23 2021 Martin Stransky <stransky@redhat.com> - 95.0.2-4
- Added fix fox mozbz#1744896 (VSync)

* Wed Dec 22 2021 Martin Stransky <stransky@redhat.com> - 95.0.2-3
- Added Fedora 36 build fix (mzbz#1745560)

* Mon Dec 20 2021 Martin Stransky <stransky@redhat.com> - 95.0.2-1
- Updated to 95.0.2
- Enabled Wayland on KDE by default

* Thu Dec 9 2021 Martin Stransky <stransky@redhat.com> - 95.0-2
- Updated symbolic icon (rhbz#2028939)

* Fri Dec 3 2021 Martin Stransky <stransky@redhat.com> - 95.0-1
- Updated to 95.0

* Fri Nov 19 2021 Martin Stransky <stransky@redhat.com> - 94.0-2
- Added fix for mozbz#1739924 / rhbz#2020981.

* Mon Nov 1 2021 Martin Stransky <stransky@redhat.com> - 94.0-1
- Updated to 94.0

* Thu Oct 07 2021 Martin Stransky <stransky@redhat.com> - 93.0-2
- Require NSS 3.70

* Wed Sep 29 2021 Martin Stransky <stransky@redhat.com> - 93.0-1
- Updated to 93.0

* Mon Sep 27 2021 Martin Stransky <stransky@redhat.com> - 92.0.1-1
- Updated to 92.0.1

* Mon Sep 13 2021 Martin Stransky <stransky@redhat.com> - 92.0-3
- Added fix for mozbz#1725828

* Thu Sep 9 2021 Martin Stransky <stransky@redhat.com> - 92.0-2
- Disable test

* Fri Sep 3 2021 Martin Stransky <stransky@redhat.com> - 92.0-1
- Updated to 92.0
- Added fix for mozbz#1728749
- Added fix for mozbz#1708709

* Thu Aug 26 2021 Martin Stransky <stransky@redhat.com> - 91.0.2-1
- Updated to 91.0.2

* Mon Aug 23 2021 Martin Stransky <stransky@redhat.com> - 91.0.1-2
- Set %%build_with_clang automatically based on %%toolchain
  by Timm Bäder <tbaeder@redhat.com>
- Updated Fedora UA patch by Eric Engestrom
  (https://src.fedoraproject.org/rpms/firefox/pull-request/21)
- Added fix for mozbz#1726515

* Mon Aug 23 2021 Martin Stransky <stransky@redhat.com> - 91.0.1-1
- Updated to 91.0.1

* Tue Aug 10 2021 Martin Stransky <stransky@redhat.com> - 91.0-1
- Updated to 91.0

* Wed Aug 04 2021 Martin Stransky <stransky@redhat.com> - 90.0.2-2
- Added fix for rhbz#1988841 - Allow unsigned extensions when installed
  under non-user-writable dirs.

* Thu Jul 22 2021 Martin Stransky <stransky@redhat.com> - 90.0.2-1
- Updated to 90.0.2

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 90.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Martin Stransky <stransky@redhat.com> - 90.0.1-1
- Updated to 90.0.1
- Added fixes to build on rawhide

* Thu Jul 15 2021 Martin Stransky <stransky@redhat.com> - 90.0-3
- Disabled Wayland backend on KDE due to
  https://bugzilla.mozilla.org/show_bug.cgi?id=1714132

* Tue Jul 13 2021 Martin Stransky <stransky@redhat.com> - 90.0-2
- Added xorg-x11-server-Xwayland dependency for Mutter

* Mon Jul 12 2021 Martin Stransky <stransky@redhat.com> - 90.0-1
- Updated to 90.0

* Mon Jul 12 2021 Daiki Ueno <dueno@redhat.com> - 89.0.2-3
- flatpak: Enable loading system trust store on the host (rhbz#1766340)

* Wed Jun 30 2021 Martin Stransky <stransky@redhat.com> - 89.0.2-2
- Added fix for mozbz#1715254 (rhbz#1976892).

* Thu Jun 24 2021 Martin Stransky <stransky@redhat.com> - 89.0.2-1
- Updated to latest upstream (89.0.2)

* Mon Jun 14 2021 Martin Stransky <stransky@redhat.com> - 89.0-2
- Added fix for mozbz#1646135

* Tue Jun 1 2021 Martin Stransky <stransky@redhat.com> - 89.0-1
- Updated to latest upstream (89.0)

* Mon May 10 2021 Martin Stransky <stransky@redhat.com> - 88.0.1-1
- Updated to latest upstream (88.0.1)

* Tue May 4 2021 Martin Stransky <stransky@redhat.com> - 88.0-8
- Added fix for mozbz#1705048.

* Fri Apr 30 2021 Martin Stransky <stransky@redhat.com> - 88.0-7
- Added pciutils-libs req (rhbz#1955338)
- Enabled Wayland on KDE (rhbz#1922608)

* Tue Apr 27 2021 Martin Stransky <stransky@redhat.com> - 88.0-6
- Test fix.

* Fri Apr 23 2021 Martin Stransky <stransky@redhat.com> - 88.0-5
- Added fix for mozbz#1580595 - mouse pointer lock.
- Another test update.

* Thu Apr 22 2021 Martin Stransky <stransky@redhat.com> - 88.0-4
- Run with mochitest test suite.

* Thu Apr 22 2021 Martin Stransky <stransky@redhat.com> - 88.0-3
- Build with crashreporter enabled.

* Wed Apr 21 2021 Martin Stransky <stransky@redhat.com> - 88.0-2
- Added clipboard fix mzbz#1703763.

* Mon Apr 19 2021 Martin Stransky <stransky@redhat.com> - 88.0-1
- Update to 88.0

* Mon Apr 12 2021 Martin Stransky <stransky@redhat.com> - 87.0-12
- Added fix for mozbz#1701089 (Widevine playback issues).

* Tue Apr 6 2021 Martin Stransky <stransky@redhat.com> - 87.0-11
- Enabled xpcshell/crashtests on Wayland.

* Sat Apr 3 2021 Martin Stransky <stransky@redhat.com> - 87.0-10
- Wayland testing again.

* Thu Apr 1 2021 Martin Stransky <stransky@redhat.com> - 87.0-9
- Added fix for mozbz#1702606 / rhbz#1936071
- Switched tests back to X11 due to massive failures.

* Thu Apr 1 2021 Martin Stransky <stransky@redhat.com> - 87.0-8
- Run testsuite on Wayland on Fedora 33+
- Spec cleanup

* Wed Mar 31 2021 Martin Stransky <stransky@redhat.com> - 87.0-7
- Added fix for mozbz#1693472 - Wayland/KDE rendering issues.

* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 87.0-6
- Rebuilt for removed libstdc++ symbol (#1937698)

* Tue Mar 30 2021 Martin Stransky <stransky@redhat.com> - 87.0-5
- Reftest fix

* Fri Mar 26 2021 Martin Stransky <stransky@redhat.com> - 87.0-4
- More test fixes
- Enabled ppc64le
- Disabled crashreporter on Fedora 34+

* Wed Mar 24 2021 Martin Stransky <stransky@redhat.com> - 87.0-2
- More test fixes

* Tue Mar 23 2021 Martin Stransky <stransky@redhat.com> - 87.0-1
- Disabled ARM due to build failures
- Updated to 87.0

* Sat Mar 13 2021 Martin Stransky <stransky@redhat.com> - 86.0.1-2
- Enabled ARM

* Fri Mar 12 2021 Martin Stransky <stransky@redhat.com> - 86.0.1-1
- Update to latest upstream (86.0.1)

* Wed Mar 10 2021 Martin Stransky <stransky@redhat.com> - 86.0-8
- Temporary disable ppc64le/Fedora 35 due to
  https://bugzilla.redhat.com/show_bug.cgi?id=1933742

* Wed Mar 3 2021 Martin Stransky <stransky@redhat.com> - 86.0-7
- Added fix for mozbz#1694670

* Mon Mar 1 2021 Martin Stransky <stransky@redhat.com> - 86.0-6
- Run xpcshell tests sequential
- Test fixes

* Mon Mar 1 2021 Martin Stransky <stransky@redhat.com> - 86.0-4
- Enable Wayland backend only when Wayland display is set.

* Mon Mar 1 2021 Martin Stransky <stransky@redhat.com> - 86.0-3
- Added icecat-78.7.1-fix_error_template_with_C_linkage.patch to
  build on F34+

* Fri Feb 26 2021 Martin Stransky <stransky@redhat.com> - 86.0-2
- Built with system nss

* Tue Feb 23 2021 Martin Stransky <stransky@redhat.com> - 86.0-1
- Update to 86.0
- Disabled Wayland backend on KDE/Plasma

* Tue Feb 23 2021 Martin Stransky <stransky@redhat.com> - 85.0.1-2
- Fixed some reftest run in Mock

* Mon Feb 08 2021 Martin Stransky <stransky@redhat.com> - 85.0.1-1
- Updated to 85.0.1

* Wed Feb 03 2021 Dan Horák <dan[at]danny.cz> - 85.0-11
- Fix parameter passing on ppc64le (mozb#1690152)

* Tue Feb 02 2021 Kalev Lember <klember@redhat.com> - 85.0-10
- Remove gtk2 support as flash plugin is no longer supported

* Sat Jan 30 2021 Martin Stransky <stransky@redhat.com> - 85.0-9
- Enable WebRender on KDE/Wayland and AMD/Intel drivers.

* Sat Jan 30 2021 Martin Stransky <stransky@redhat.com> - 85.0-8
- Enable Wayland backend on Fedora 34/KDE/Plasma (and other compositors)
  by default (https://bugzilla.redhat.com/show_bug.cgi?id=1922608).

* Fri Jan 29 2021 Martin Stransky <stransky@redhat.com> - 85.0-7
- Added clipboard fix mozbz#1631061.

* Thu Jan 28 2021 Kalev Lember <klember@redhat.com> - 85.0-6
- Make provides/requires filtering smarter/automatic (rhbz#1582116)
- Drop dbus-glib requires that are now automatically generated again

* Thu Jan 28 2021 Martin Stransky <stransky@redhat.com> - 85.0-5
- Add dbus-glib requires.

* Tue Jan 26 2021 Martin Stransky <stransky@redhat.com> - 85.0-4
- Added fix for mozbz#1679933 - startup crash

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 85.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 Martin Stransky <stransky@redhat.com> - 85.0-2
- Update to 85.0.

* Wed Jan 20 2021 Jan Horak <jhorak@redhat.com> - 84.0.2-8
- Fixing package requires/provides

* Tue Jan 19 2021 Martin Stransky <stransky@redhat.com> - 84.0.2-7
- Fixed mzbz#164294 regression.

* Fri Jan 15 2021 Martin Stransky <stransky@redhat.com> - 84.0.2-6
- Added WebRender fix (mozbz#1681107).

* Thu Jan 14 2021 Martin Stransky <stransky@redhat.com> - 84.0.2-5
- Removed some failing tests.
- Spec file tweaks.

* Tue Jan 12 2021 Martin Stransky <stransky@redhat.com> - 84.0.2-4
- Enabled LTO in Firefox build system.

* Tue Jan 12 2021 Martin Stransky <stransky@redhat.com> - 84.0.2-3
- Removed failing xpcshell/reftests, test tweaks.

* Mon Jan 11 2021 Martin Stransky <stransky@redhat.com> - 84.0.2-2
- Added a workaround for rhbz#1908018

* Wed Jan 6 2021 Martin Stransky <stransky@redhat.com> - 84.0.2-1
- Updated to 84.0.2

* Tue Jan 05 2021 Jan Horak <jhorak@redhat.com> - 84.0.1-5
- Removing requires/provides of the bundled libraries

* Mon Jan 4 2021 Martin Stransky <stransky@redhat.com> - 84.0.1-4
- Enabled tests

* Mon Jan 4 2021 Martin Stransky <stransky@redhat.com> - 84.0.1-3
- Enabled armv7hl arch on rawhide

* Wed Dec 23 2020 Martin Stransky <stransky@redhat.com> - 84.0.1-2
- Reverted mzbz#1631061 due to clipboard regressions
- Disabled armv7hl build on rawhide due to rhbz#1910277
- Build with system nss on rawhide (rhbz#1908791).

* Tue Dec 22 2020 Martin Stransky <stransky@redhat.com> - 84.0.1-1
- Updated to 84.0.1

* Sun Dec 20 2020 Miro Hrončok <mhroncok@redhat.com> - 84.0-7
- Filter out private libraries provides
- Fixes: rhbz#1908791

* Thu Dec 17 2020 Martin Stransky <stransky@redhat.com> - 84.0-6
- Disable PGO on Rawhide due to build issues
- Disable system nss on Rawhide due to rhbz#1908018
- Enabled system nss on Fedora 33/32

* Wed Dec 16 2020 Martin Stransky <stransky@redhat.com> - 84.0-5
- Build with tests enabled

* Wed Dec 16 2020 Martin Stransky <stransky@redhat.com> - 84.0-4
- Disabled LTO due to massive test failures

* Wed Dec 16 2020 Martin Stransky <stransky@redhat.com> - 84.0-3
- Updated to Firefox 84 Build 3
- Disabled system nss due to addon breakage (rhbz#1908018).

* Wed Dec 9 2020 Martin Stransky <stransky@redhat.com> - 83.0-15
- Enabled tests everywhere
- Enabled crash reporter

* Tue Dec 1 2020 Martin Stransky <stransky@redhat.com> - 83.0-14
- Enabled LTO

* Tue Dec 1 2020 Martin Stransky <stransky@redhat.com> - 83.0-13
- Added fix for mozbz#1672139

* Tue Dec 1 2020 Martin Stransky <stransky@redhat.com> - 83.0-12
- More mochitest fixes

* Mon Nov 30 2020 Martin Stransky <stransky@redhat.com> - 83.0-11
- Mochitest tweaking

* Sat Nov 28 2020 Martin Stransky <stransky@redhat.com> - 83.0-10
- Added fix for mzbz#1678680

* Wed Nov 25 2020 Martin Stransky <stransky@redhat.com> - 83.0-9
- Added mochitest test files

* Wed Nov 25 2020 Martin Stransky <stransky@redhat.com> - 83.0-8
- Added fix for rhbz#1900542

* Wed Nov 25 2020 Martin Stransky <stransky@redhat.com> - 83.0-7
- Export MOZ_GMP_PATH from /usr/bin/firefox script
  (https://pagure.io/fedora-workstation/issue/126)

* Tue Nov 24 2020 Martin Stransky <stransky@redhat.com> - 83.0-6
- Fix mochitest

* Wed Nov 18 2020 Martin Stransky <stransky@redhat.com> - 83.0-5
- Build with tests enabled

* Wed Nov 18 2020 Martin Stransky <stransky@redhat.com> - 83.0-4
- Enable all arches

* Fri Nov 13 2020 Martin Stransky <stransky@redhat.com> - 83.0-3
- Updated to 83.0 Build 2

* Thu Nov 12 2020 Martin Stransky <stransky@redhat.com> - 83.0-1
- Updated to 83.0
- Updated PipeWire patches from mozbz#1672944

* Tue Nov 10 2020 Martin Stransky <stransky@redhat.com> - 82.0.3-2
- Added fix for mozbz#1885133

* Mon Nov 9 2020 Martin Stransky <stransky@redhat.com> - 82.0.3-1
- Updated to 82.0.3

* Mon Nov 9 2020 Kalev Lember <klember@redhat.com> - 82.0.2-7
- Include date in appdata release tags

* Fri Nov 6 2020 Tomas Popela <tpopela@redhat.com> - 82.0.2-6
- Re-enable s390x buils by backporting a change from Thunderbird
  https://src.fedoraproject.org/rpms/thunderbird/c/5f0bec1b5b79e117cc469710afbfa4d008af9c29?branch=master

* Tue Nov 3 2020 Martin Stransky <stransky@redhat.com> - 82.0.2-5
- Added mozilla-openh264 dependency to play H264 clips out of the box
- Updated Firefox tests

* Tue Nov 3 2020 Martin Stransky <stransky@redhat.com> - 82.0.2-3
- Disabled LTO again.

* Tue Nov 3 2020 Martin Stransky <stransky@redhat.com> - 82.0.2-2
- NSS debug build

* Thu Oct 29 2020 Martin Stransky <stransky@redhat.com> - 82.0.2-1
- Updated to 82.0.2
- Removed mzbz#1668771 due to rhbz#1888920

* Wed Oct 28 2020 Martin Stransky <stransky@redhat.com> - 82.0.1-1
- Updated to 82.0.1

* Tue Oct 27 2020 Martin Stransky <stransky@redhat.com> - 82.0-8
- Added fix for mozbz#1673313

* Tue Oct 27 2020 Martin Stransky <stransky@redhat.com> - 82.0-7
- Added fix for rawhide crashes (rhbz#1891234)

* Sat Oct 24 2020 Martin Stransky <stransky@redhat.com> - 82.0-6
- Enable LTO

* Tue Oct 20 2020 Martin Stransky <stransky@redhat.com> - 82.0-5
- Added fix for rhbz#1889742 - Typo in /usr/bin/firefox

* Mon Oct 19 2020 Martin Stransky <stransky@redhat.com> - 82.0-4
- Updated openh264 patch to use keyframes from contained
  for openh264 only.

* Mon Oct 19 2020 Martin Stransky <stransky@redhat.com> - 82.0-3
- Added ELN build fixes

* Thu Oct 15 2020 Martin Stransky <stransky@redhat.com> - 82.0-2
- Updated SELinux relabel setup (rhbz#1731371)

* Thu Oct 15 2020 Martin Stransky <stransky@redhat.com> - 82.0-1
- Updated to 82.0 Build 2

* Thu Oct 15 2020 Martin Stransky <stransky@redhat.com> - 81.0.2-3
- Added experimental openh264 seek patch (mzbz#1670333)

* Mon Oct 12 2020 Martin Stransky <stransky@redhat.com> - 81.0.2-2
- Added a partial fox for rhbz#1886722

* Mon Oct 12 2020 Martin Stransky <stransky@redhat.com> - 81.0.2-1
- Updated to latest upstream - 81.0.2

* Thu Oct 8 2020 Martin Stransky <stransky@redhat.com> - 81.0.1-9
- Added an updated fix for mozbz#1656727

* Thu Oct 8 2020 Martin Stransky <stransky@redhat.com> - 81.0.1-8
- Added fixes for mozbz#1634404, mozbz#1669495

* Thu Oct 8 2020 Martin Stransky <stransky@redhat.com> - 81.0.1-7
- Removed mozbz#1656727 as it causes a regression rhbz#1886243

* Wed Oct 7 2020 Martin Stransky <stransky@redhat.com> - 81.0.1-6
- PGO patch update
- Added fix for mzbz#1669442 (LTO builds)

* Mon Oct 5 2020 Martin Stransky <stransky@redhat.com> - 81.0.1-5
- Added fix for mozbz#1656727

* Fri Oct 2 2020 Martin Stransky <stransky@redhat.com> - 81.0.1-4
- Added fix for mozbz#1668771

* Thu Oct 1 2020 Martin Stransky <stransky@redhat.com> - 81.0.1-3
- Added fix for mozbz#1661192

* Thu Oct 1 2020 Martin Stransky <stransky@redhat.com> - 81.0.1-2
- Added fix for mozbz#1640567
- Enable PGO

* Wed Sep 30 2020 Martin Stransky <stransky@redhat.com> - 81.0.1-1
- Updated to 81.0.1

* Wed Sep 30 2020 Martin Stransky <stransky@redhat.com> - 81.0-9
- Disabled openh264 download
- Removed fdk-aac-free dependency (rhbz#1883672)
- Enabled LTO

* Sat Sep 26 2020 Dan Horák <dan[at]danny.cz> - 81.0-8
- Re-enable builds for ppc64le

* Fri Sep 25 2020 Martin Stransky <stransky@redhat.com> - 81.0-7
- Added openh264 fixes

* Wed Sep 23 2020 Martin Stransky <stransky@redhat.com> - 81.0-6
- Added fix for rhbz#1731371

* Tue Sep 22 2020 Kalev Lember <klember@redhat.com> - 81.0-5
- Re-enable builds for armv7hl and aarch64 architectures

* Tue Sep 22 2020 Kalev Lember <klember@redhat.com> - 81.0-4
- Disable LTO to work around firefox build failing in F33+

* Mon Sep 21 2020 Martin Stransky <stransky@redhat.com> - 81.0-3
- Updated to 81.0 Build 2
- Updated firefox-disable-ffvpx-with-vapi patch
- Deleted old changelog entries

* Thu Sep 17 2020 Martin Stransky <stransky@redhat.com> - 81.0-2
- Added upstream patches mzbz#1665324 mozbz#1665329
- Updated requested nss version to 3.56

* Tue Sep 15 2020 Martin Stransky <stransky@redhat.com> - 81.0-1
- Updated to 81.0

* Thu Sep 10 2020 Martin Stransky <stransky@redhat.com> - 80.0.1-3
- Test build for all arches.

* Fri Sep 4 2020 Martin Stransky <stransky@redhat.com> - 80.0.1-2
- Added patch for mozbz#1875469

* Tue Sep 1 2020 Martin Stransky <stransky@redhat.com> - 80.0.1-1
- Updated to 80.0.1

* Tue Aug 18 2020 Martin Stransky <stransky@redhat.com> - 80.0-1
- Updated to 80.0 Build 2
- Go back to gcc
- Disabled WebGL dmabuf backend due to reported errors
  (mzbz#1655323, mozbz#1656505).

* Tue Aug 18 2020 Martin Stransky <stransky@redhat.com> - 79.0-6
- Enabled pgo
- Build with clang

* Tue Aug 4 2020 Martin Stransky <stransky@redhat.com> - 79.0-5
- Added upstream fix for mozbz#1656436.

* Mon Aug 3 2020 Martin Stransky <stransky@redhat.com> - 79.0-4
- Updated fix for mozbz#1645671

* Thu Jul 30 2020 Martin Stransky <stransky@redhat.com> - 79.0-3
- Added VA-API fix for mozbz#1645671

* Wed Jul 29 2020 Martin Stransky <stransky@redhat.com> - 79.0-2
- Try to enable armv7hl again.
- Disabled ppc64le due to cargo crash (rhbz#1862012).

* Mon Jul 27 2020 Martin Stransky <stransky@redhat.com> - 79.0-1
- Update to 79.0
- Disabled PGO due to rhbz#1849165 (gcc internal error).

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 78.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 78.0-4
- Use python3 instead of python2 for build

* Tue Jul 21 2020 Martin Stransky <stransky@redhat.com> - 78.0-3
- Added fix for mozbz#1651701/rhbz#1855730

* Fri Jul 10 2020 Jan Horak <jhorak@redhat.com> - 78.0.2-2
- Fixing clang build - linker setup

* Thu Jul 09 2020 Jan Horak <jhorak@redhat.com> - 78.0.2-1
- Update to 78.0.2 build2

* Wed Jul 01 2020 Jan Horak <jhorak@redhat.com> - 78.0.1-1
- Update to 78.0.1 build1

* Wed Jul 1 2020 Martin Stransky <stransky@redhat.com> - 78.0-2
- Add 'Open the Profile Manager' desktop file entry

* Mon Jun 29 2020 Jan Horak <jhorak@redhat.com> - 78.0-1
- Update to 78.0 build2

* Tue Jun 23 2020 Martin Stransky <stransky@redhat.com> - 77.0.1-3
- Build with PGO/LTO again.

* Wed Jun 03 2020 Jan Horak <jhorak@redhat.com> - 77.0.1-2
- Update to 77.0.1 build1

* Wed Jun 03 2020 Jan Horak <jhorak@redhat.com> - 77.0.1-1
- Fixing pipewire patch
- New upstream version (77.0.1)

* Tue Jun 2 2020 Martin Stransky <stransky@redhat.com> - 77.0-2
- Rebuild with updated langpacks (rhbz#1843028).

* Fri May 29 2020 Martin Stransky <stransky@redhat.com> - 77.0-1
- Updated to Firefox 77.0

* Mon May 25 2020 Martin Stransky <stransky@redhat.com> - 76.0.1-7
- Added fix for mozbz#1632456

* Mon May 25 2020 Martin Stransky <stransky@redhat.com> - 76.0.1-6
- Added fix for mozbz#1634213

* Mon May 25 2020 Martin Stransky <stransky@redhat.com> - 76.0.1-5
- Added fix for mozbz#1619882 - video flickering when va-api is used.

* Thu May 21 2020 Jan Grulich <jgrulich@redhat.com> - 76.0.1-4
- Add support for PipeWire 0.3

* Wed May 20 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 76.0.1-3
- Build aarch64 again so aarch64 users get updates

* Wed May 13 2020 Martin Stransky <stransky@redhat.com> - 76.0.1-2
- Added extra va-api frames to vp8/9 decoder.

* Fri May 8 2020 Martin Stransky <stransky@redhat.com> - 76.0.1-1
- Updated to 76.0.1

* Thu May 7 2020 Martin Stransky <stransky@redhat.com> - 76.0-3
- Disable ffvpx when va-api is enabled.

* Tue May 05 2020 Jan Horak <jhorak@redhat.com> - 76.0-2
- Don't use google safe browsing api key for the geolocation

* Sun May 3 2020 Martin Stransky <stransky@redhat.com> - 76.0-1
- Updated to 76.0

* Thu Apr 23 2020 Martin Stransky <stransky@redhat.com> - 75.0-3
- Added fix for mozilla bug #1527976 (browser D&D)

* Tue Apr 14 2020 Jan Horak <jhorak@redhat.com> - 75.0-2
- Removed gconf-2.0 build requirement

* Mon Apr 06 2020 Martin Stransky <stransky@redhat.com> - 75.0-1
- Updated to 75.0

* Mon Apr 06 2020 Martin Stransky <stransky@redhat.com> - 74.0.1-3
- Added fix for mozbz#1627469

* Mon Apr 06 2020 Jan Horak <jhorak@redhat.com> - 74.0.1-2
- Fixing pipewire patch

* Sat Apr 4 2020 Martin Stransky <stransky@redhat.com> - 74.0.1-1
- Updated to latest upstream
- Added fix for mozbz#1624745

* Wed Apr 1 2020 Martin Stransky <stransky@redhat.com> - 74.0-14
- Added fixes to gnome shell search provider

* Tue Mar 31 2020 Jan Horak <jhorak@redhat.com> - 74.0-13
- Allow addons sideload to fix missing langpacks issues

* Thu Mar 19 2020 Martin Stransky <stransky@redhat.com> - 74.0-12
- Added fix for rhbz#1814850 by Daniel Rusek

* Tue Mar 17 2020 Martin Stransky <stransky@redhat.com> - 74.0-11
- Added fix for mozbz#1623106

* Tue Mar 17 2020 Martin Stransky <stransky@redhat.com> - 74.0-9
- Added fix for mozbz#1623060

* Tue Mar 17 2020 Jan Grulich <jgrulich@redhat.com> - 74-0-8
- Add support for window sharing

* Mon Mar 16 2020 Martin Stransky <stransky@redhat.com> - 74.0-7
- Use D-Bus remote exclusively for both X11 and Wayland backends
  when WAYLAND_DISPLAY is present.

* Fri Mar 13 2020 Martin Stransky <stransky@redhat.com> - 74.0-6
- Added fix for mozbz#1615098

* Thu Mar 12 2020 Martin Stransky <stransky@redhat.com> - 74.0-5
- Added fix for mozbz#1196777

* Tue Mar 10 2020 Kalev Lember <klember@redhat.com> - 74.0-4
- Remove unused libIDL build dep
- Disabled arm due to build failures

* Tue Mar 10 2020 Martin Stransky <stransky@redhat.com> - 74.0-3
- Update to 74.0 Build 3

* Mon Mar 09 2020 Martin Stransky <stransky@redhat.com> - 74.0-2
- Update to 74.0 Build 2

* Tue Mar 03 2020 Martin Stransky <stransky@redhat.com> - 74.0-1
- Update to 74.0 Build 1
- Added mozbz#1609538

* Mon Feb 24 2020 Martin Stransky <stransky@redhat.com> - 73.0.1-4
- Using pipewire-0.2 as buildrequire
- Added armv7hl fixes by Gabriel Hojda

* Mon Feb 24 2020 Martin Stransky <stransky@redhat.com> - 73.0.1-2
- Fixed Bug 1804787 - Some .desktop menu entries unlocalized

* Thu Feb 20 2020 Martin Stransky <stransky@redhat.com> - 73.0.1-1
- Update to 73.0.1

* Tue Feb 11 2020 Jan Horak <jhorak@redhat.com> - 73.0-1
- Update to 73.0 build3

* Tue Feb 04 2020 Kalev Lember <klember@redhat.com> - 72.0.2-3
- Fix various issues with appdata, making the validation pass again
- Validate appdata during the build
- Make sure the release tag in appdata is in sync with the package version

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 72.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Jan Horak <jhorak@redhat.com> - 72.0.2-1
- Update to 72.0.2 build1

* Wed Jan 15 2020 Jan Horak <jhorak@redhat.com> - 72.0.1-2
- Added fix for wrong cursor offset of popup windows and bumped required nss
  version

* Wed Jan 08 2020 Jan Horak <jhorak@redhat.com> - 72.0.1-1
- Update to 72.0.1 build1

* Mon Jan 06 2020 Jan Horak <jhorak@redhat.com> - 72.0-2
- Update to 72.0 build4

* Fri Jan 03 2020 Jan Horak <jhorak@redhat.com> - 72.0-1
- Update to 72.0 build3

* Wed Dec 18 2019 Jan Horak <jhorak@redhat.com> - 71.0-17
- Fix for wrong intl.accept_lang when using non en-us langpack

* Mon Dec 9 2019 Martin Stransky <stransky@redhat.com> - 71.0-16
- Build with asan

* Mon Dec 9 2019 Martin Stransky <stransky@redhat.com> - 71.0-15
- Enabled Mozilla crash reporter
- Enabled PGO builds

* Mon Dec 9 2019 Martin Stransky <stransky@redhat.com> - 71.0-14
- Updated workaround for mzbz#1601707

* Sat Dec 7 2019 Martin Stransky <stransky@redhat.com> - 71.0-13
- Built with -fno-lifetime-dse

* Fri Dec 6 2019 Martin Stransky <stransky@redhat.com> - 71.0-12
- Clang test build, should fix extension breakage

* Fri Dec 6 2019 Martin Stransky <stransky@redhat.com> - 71.0-11
- Added workaround for:
  https://bugzilla.mozilla.org/show_bug.cgi?id=1601707
  http://gcc.gnu.org/PR92831

* Fri Dec 6 2019 Martin Stransky <stransky@redhat.com> - 71.0-10
- Remove appdata and ship metainfo only

* Wed Dec 4 2019 Martin Stransky <stransky@redhat.com> - 71.0-9
- Included kiosk mode workaround (mozbz#1594738)

* Tue Dec 3 2019 Martin Stransky <stransky@redhat.com> - 71.0-8
- Disabled PGO due to startup crash

* Mon Dec 2 2019 Martin Stransky <stransky@redhat.com> - 71.0-7
- Updated to 71.0 Build 5
- Updated Gnome search provider

* Wed Nov 27 2019 Martin Stransky <stransky@redhat.com> - 71.0-6
- Enable Gnome search provider

* Wed Nov 27 2019 Martin Stransky <stransky@redhat.com> - 71.0-5
- Added fix for mozbz#1593408
- Temporary disable Gnome search provider

* Tue Nov 26 2019 Martin Stransky <stransky@redhat.com> - 71.0-2
- Enable Gnome search provider

* Tue Nov 26 2019 Martin Stransky <stransky@redhat.com> - 71.0-1
- Updated to 71.0 Build 2

* Tue Nov 19 2019 Jan Horak <jhorak@redhat.com> - 70.0.1-5
- Added fixes for missing popup and overflow widget glitches

* Mon Nov 04 2019 Jan Horak <jhorak@redhat.com> - 70.0.1-4
- Added fix for non-scrollable popups

* Fri Nov 1 2019 Martin Stransky <stransky@redhat.com> - 70.0.1-1
- Updated to 70.0.1
- Built with system-nss (reverted 70.0-2 change).

* Thu Oct 31 2019 Martin Stransky <stransky@redhat.com> - 70.0-2
- Switched to in-tree nss due to rhbz#1752303

* Tue Oct 15 2019 Martin Stransky <stransky@redhat.com> - 70.0-1
- Updated to 70.0
