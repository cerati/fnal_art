# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from llnl.util import tty
import sys
import os
import spack.util.spack_json as sjson

def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)

class Larsim(CMakePackage):
    """Larsim"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larsim"
    git_base = 'https://github.com/LArSoft/larsim.git'
    url      = "https://github.com/LArSoft/larsim/archive/v01_02_03.tar.gz"
    list_url = 'https://api.github.com/repos/LArSoft/larsim/tags'

    version('09.30.00.rc1', sha256='8371ab32c43b702337d7022fee255eb2a86164a7ee8edc91781f4b0494890142')
    version('09.18.00',     sha256='3dd73c86c5c736838d7e54c39743d341e17413a1713b4214363c8d36d1c04032')
    version('09.17.00',     sha256='a82180a4d6ff1a37543cc55206c8f619c322e8552e9b5370cbed28e28b0e6d89')
    version('09.16.01',     sha256='7aa9adf76f98a2ffafeb3d3ab096304e4ccf25bd8f029c6d723a653e43b74923')
    version('09.16.00',     sha256='36bd983c175334efa0c9453019ef3821087a59b178f198c419dba15432fa034a')
    version('09.15.00',     sha256='3b4b403f75ccf56b9b0c257d8a9082a139b0e2ddec161c12c92951fbe16a9c73')
    version('09.14.09',     sha256='3f32a13a96379e440c3497b598cd493cca597e6fa295aeff22b0a2d3fff29413')
    version('09.14.08',     sha256='0dd3735cc5f8b0d4b30bb239e93efe8f8bc5995a53ae1b1b14532c31af6fafeb')
    version('09.14.07',     sha256='a0a235caf17b5d9d2b3959ed967a5cdb2cc1851d3d696976a656c2f48834cadc')
    version('09.14.06',     sha256='5d729da4515d0315d123724b411c4e81e191ea88ed37692b5a037b7b7d94fbfb')
    version('mwm1', tag='mwm1', git='https://github.com/marcmengel/larsim.git', get_full_repo=True)


    def url_for_version(self, version):
        url = 'https://github.com/LArSoft/{0}/archive/v{1}.tar.gz'
        return url.format(self.name, version.underscored)

    def fetch_remote_versions(self, concurrency=None):
        return dict(map(lambda v: (v.dotted, self.url_for_version(v)),
                        [ Version(d['name'][1:]) for d in
                          sjson.load(
                              spack.util.web.read_from_url(
                                  self.list_url,
                                  accept_content_type='application/json')[2])
                          if d['name'].startswith('v') ]))

    patch('v09_18_00.patch', when='@09.18.00')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')



    depends_on('larsoft-data')
    depends_on('larevt')
    depends_on('marley')
    depends_on('cry')
    depends_on('genie')
    depends_on('ifdhc')
    depends_on('xerces-c')
    depends_on('libxml2')
    depends_on('clhep')
    depends_on('nug4')
    depends_on('nugen')
    depends_on('nurandom')
    depends_on('sqlite')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
               '-DIFDH_INC={0}'.
                format(self.spec['ifdhc'].prefix.include),
               '-DIFDH_LIB={0}'.
                format(self.spec['ifdhc'].prefix),
               '-DGENIE_INC={0}'.
                format(self.spec['genie'].prefix.include),
                '-DGENIE_VERSION=v{0}'.
                format(self.spec['genie'].version.underscored),
                '-DLARSOFT_DATA_DIR=v{0}'.
                format(self.spec['larsoft-data'].prefix),
                '-DLARSOFT_DATA_VERSION=v{0}'.
                format(self.spec['larsoft-data'].version.underscored),
                '-DIGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES=1'
        ]
        return args

    def flag_handler(self, name, flags):
        if name == 'cxxflags' and  self.spec.compiler.name == 'gcc':
            flags.append('-Wno-error=deprecated-declarations')
            flags.append('-Wno-error=class-memaccess')
        return (flags, None, None)

    def setup_build_environment(self, spack_env):
        spack_env.prepend_path('LD_LIBRARY_PATH', str(self.spec['root'].prefix.lib))
        # Binaries.
        spack_env.prepend_path('PATH',
                               os.path.join(self.build_directory, 'bin'))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH',
                               os.path.join(self.build_directory, 'lib'))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(root=False, cover='nodes', order='post',
                                    deptype=('link'), direction='children'):
            spack_env.prepend_path('ROOT_INCLUDE_PATH',
                                   str(self.spec[d.name].prefix.include))
        # Perl modules.
        spack_env.prepend_path('PERL5LIB',
                               os.path.join(self.build_directory, 'perllib'))
        # Set path to find fhicl files
        spack_env.prepend_path('FHICL_INCLUDE_PATH',
                               os.path.join(self.build_directory, 'job'))
        # Set path to find gdml files
        spack_env.prepend_path('FW_SEARCH_PATH',
                               os.path.join(self.build_directory, 'job'))
        # Cleaup.
        sanitize_environments(spack_env)

        # ups env vars used in build...
        spack_env.set('LIBXML2_FQ_DIR', self.spec['libxml2'].prefix)
        spack_env.set('GEANT4_FQ_DIR', self.spec['geant4'].prefix)
        spack_env.set('XERCES_C_INC', self.spec['xerces-c'].prefix.include)
        spack_env.set('GENIE_FQ_DIR', self.spec['genie'].prefix)
        spack_env.set('GENIE_INC', self.spec['genie'].prefix.include)
        spack_env.set('CRYHOME', self.spec['cry'].prefix)

    def setup_run_environment(self, run_env):
        # Ensure we can find plugin libraries.
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(root=False, cover='nodes', order='post',
                                    deptype=('link'), direction='children'):
            run_env.prepend_path('ROOT_INCLUDE_PATH',
                                 str(self.spec[d.name].prefix.include))
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Perl modules.
        run_env.prepend_path('PERL5LIB', os.path.join(self.prefix, 'perllib'))
        # Set path to find fhicl files
        run_env.prepend_path('FHICL_INCLUDE_PATH', os.path.join(self.prefix, 'job'))
        # Set path to find gdml files
        run_env.prepend_path('FW_SEARCH_PATH', os.path.join(self.prefix, 'job'))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        spack_env.append_path('FHICL_FILE_PATH','{0}/job'.format(self.prefix))
        spack_env.append_path('FW_SEARCH_PATH','{0}/gdml'.format(self.prefix))
        spack_env.append_path('FW_SEARCH_PATH','{0}/fw'.format(self.prefix))

    def setup_dependent_run_environment(self, run_env, dspec):
        # Ensure we can find plugin libraries.
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.append_path('FHICL_FILE_PATH','{0}/job'.format(self.prefix))
        run_env.append_path('FW_SEARCH_PATH','{0}/gdml'.format(self.prefix))
        run_env.append_path('FW_SEARCH_PATH','{0}/fw'.format(self.prefix))
