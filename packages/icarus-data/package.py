
from spack import *
import os
import glob

class IcarusData(Package):
    """Bundle of data files for icarus"""

    homepage = "https://icarus.fnal.gov/"

    version('09.35.00', sha256='b7ac7cb3e1ccc64edd3be91392933b0d5c928701cdfd620a7fd453015b0c5312',
            url="https://scisoft.fnal.gov/scisoft/packages/icarus_data/v09_35_00/icarus_data-09.35.00-noarch.tar.bz2")
    version('09.28.01', sha256='e1c69a66d554ab6b6244656eac6b89fa0eb3cd372e12188a4d6df33846023053',
            url="https://scisoft.fnal.gov/scisoft/packages/icarus_data/v09_28_01/icarus_data-09.28.01-noarch.tar.bz2")
    version('09.26.00', sha256 = '42cc1b8d4a17ad7d1f1bd3e1a1446dfee953ec7109e11cf28f180ea69ca321ec',
            url="https://scisoft.fnal.gov/scisoft/packages/icarus_data/v09_26_00/icarus_data-09.26.00-noarch.tar.bz2")

    def url_for_version(self, version):
        url='https://scisoft.fnal.gov/scisoft/packages/icarus_data/v{0}/icarus_data-{1}-noarch.tar.bz2'
        return url.format(version.underscored, version.dotted)


    def install(self, spec, prefix):
        src = glob.glob("%s/v*[0-9]" % self.stage.source_path)[0]
        install_tree(src,prefix)

    def setup_run_environment(self, env):
        env.set('ICARUS_DATA_VERSION', 'v%s' % self.version.underscored )
        env.prepend_path('WIRECELL_PATH', '%s/icarus_data/WirecellData'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data/NoiseHistos'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data/Responses'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data/PhotonLibrary'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data/CRT'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data/PandoraMVAs'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data/database'  % self.prefix )
        env.prepend_path('CMAKE_PREFIX_PATH', '%s'  % self.prefix )
        env.prepend_path('PKG_CONFIG_PATH', '%s'  % self.prefix )

