import os
import re
import shutil

def install(options,buildout):
    """Installs only the python site-packages."""
    cwd = os.getcwd()
    #os.system("""
    #          cd %s
    #          cd python
    #          make install""" % options['compile-directory'])

    for d in 'include', 'man', 'lib', 'share', 'bin':
        if os.path.exists(
            os.path.join(options['location'], d)):
            shutil.rmtree(
                os.path.join(options['location'], d))
    os.chdir(cwd)

def libxml(options, buildout, version):
    """Patch Makefile to point to our site packages."""
    MAKEFILE = os.path.join(
        options['compile-directory'],
        'python',
        'Makefile'
    )
    file=open(MAKEFILE)
    lines=file.readlines()
    for i,line in enumerate(lines):
        for word in 'pythondir', 'PYTHON_SITE_PACKAGES':
            if line.startswith(word):
                lines[i] = re.sub(
                    '%s.*' % word,
                    '%s = %s' % (
                        word,
                        os.path.join(
                            buildout['buildout']['directory'],
                            'parts',
                            'site-packages-%s' % version)
                    ),
                    line
                )
    file = open(MAKEFILE,'w+')
    file.writelines(lines)
    file.close()

def libxml2_24(options,buildout):
    """Patch Makefile to point to our site packages."""
    libxml(options, buildout, '2.4')

def libxml2_25(options,buildout):
    """Patch Makefile to point to our site packages."""
    libxml(options, buildout, '2.5')
def libxml2_26(options,buildout):
    """Patch Makefile to point to our site packages."""
    libxml(options, buildout, '2.6')
# vim:set ts=4 sts=4 et  :
