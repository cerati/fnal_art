# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import sys

class Larbatch(Package):
    """package for batch job submission featuring project.py """

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larbatch-web-client/wiki"
    url      = "https://github.com/LArSoft/larbatch/archive/refs/tags/v01_51_15.tar.gz"

    version('01_51_15', sha256='609c85155d4368fd82f21cbb1b68b4f56556c4580e9ab6f36efa3f29ece02d0a')
    version('01.51.12', sha256='5ab54efd1897eeab66663a7029a9b0781b691051d0a47998b5989acbeb5117c3')
    version('01.51.11', sha256='e2336eb76b63e6aa95dc24d86ec6b777b31d7ed08cd45e331bcbee050e9e1018')
    version('01.51.10', sha256='da3c92246716484ba563147deefc4da878824d8109a8dd22d8877ed7926733ef')


    depends_on('sam-web-client', type=('run'))
    depends_on('python',         type=('run'))

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)

    def setup_run_environment(self, run_env):
        run_env.prepend_path('PYTHONPATH', self.prefix.bin)
        run_env.prepend_path('PYTHONPATH', self.prefix + '/python')

