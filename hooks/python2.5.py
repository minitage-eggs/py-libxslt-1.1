import os
import re
import zc.buildout
myos=os.uname()[0]


def libxml2(options,buildout):
    # patch Makefile
    pwd=os.getcwd()
    file=open('/'.join((pwd,'python','Makefile')))
    #file=open('/home/kiorky/Makefile')
    lines=file.readlines()
    for i,line in enumerate(lines):
        if line[:8] == 'PYTHON =':
            lines[i]='PYTHON = %s/bin/python2.5\n' % buildout['python2.5']['location']
        if line[:17] == 'PYTHON_INCLUDES =':
            lines[i]='PYTHON_INCLUDES = %s/python2.5\n' % buildout['python2.5']['include']
        if line[:16] == 'PYTHON_VERSION =':
            lines[i]='PYTHON_VERSION = 2.5\n' 
        if line[:9] == 'LDFLAGS =' or line[:20] == 'PYTHON_SITE_PACKAGES':
            lines[i]=re.sub('2.4','2.5',line)
    file=open('/'.join((os.getcwd(),'python','Makefile')),'w+')
    file.writelines(lines)
    file.close()
    os.chdir('python')
    os.system('make clean')
    os.system('make')
    os.system('make install')
    os.chdir(pwd)
    return None 


# vim:set ts=4 sts=4 et  :
