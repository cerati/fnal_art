# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install sbanaobj
#
# You can edit this file again by typing:
#
#     spack edit sbanaobj
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Sbnanaobj(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://www.example.com"
    url      = "https://github.com/SBNSoftware/sbnanaobj/archive/refs/tags/v09_17_04.tar.gz"

    version('09.17.04', sha256='06f4534f5b5022162fae07581a53d16ca3a7b3bd27e42738c8ce33558ca0b348')
    version('09.17.02', sha256='985796b3b49a2d3fc93984b65169593c1483e29df78c98ac6c215eae88b59b7e')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch('v09_17_04.patch', when='@09_17_04')
    patch('v09_17_02.patch', when='@09_17_02')

    depends_on('root')
    depends_on('cetmodules', type='build')

    def url_for_version(self, version):
        #url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        url = 'https://github.com/SBNSoftware/{0}/archive/v{1}.tar.gz'
        return url.format(self.name, version.underscored)

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)]
        return args
