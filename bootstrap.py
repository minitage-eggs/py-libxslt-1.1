##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Bootstrap a buildout-based project

Simply run this script in a directory containing a buildout.cfg.
The script accepts buildout command-line options, so you can
use the -c option to specify an alternate configuration file.

$Id$
"""

import os, shutil, sys, tempfile, urllib2

tmpeggs = tempfile.mkdtemp()

try:
    import pkg_resources
except ImportError:
    ez = {}
    exec urllib2.urlopen('http://peak.telecommunity.com/dist/ez_setup.py'
                         ).read() in ez
    ez['use_setuptools'](to_dir=tmpeggs, download_delay=0)

    import pkg_resources

cmd = 'from setuptools.command.easy_install import main; main()'
if sys.platform == 'win32':
    cmd = '"%s"' % cmd # work around spawn lamosity on windows

ws = pkg_resources.working_set
assert os.spawnle(
    os.P_WAIT, sys.executable, sys.executable,
    '-c', cmd, '-mqNxd', tmpeggs, 'zc.buildout',
    dict(os.environ,
         PYTHONPATH=
         ws.find(pkg_resources.Requirement.parse('setuptools')).location
         ),
    ) == 0

ws.add_entry(tmpeggs)
ws.require('zc.buildout')
import zc.buildout.buildout
zc.buildout.buildout.main(sys.argv[1:] + ['bootstrap'])
shutil.rmtree(tmpeggs)


# ADD PKG_CONFIG_PATH and LD_LIBRARY_PATH in environnement
import os,sys
buildout=os.getcwd()+'/bin/buildout'
os.chdir(os.getcwd())
file=open(buildout).readlines()
newlines=[] 
for line in file:
    if line == '  ]\n':
        newlines.append("'%s/%s',\n"%(os.getcwd(),'hooks'))
        newlines.append(line)
        newlines.append('from setenv import getcairoenv;getcairoenv() #set PKG_CONFIG_PATH\n')
    else:
        newlines.append(line)

file = open(buildout,"w+")
file.writelines(newlines)

