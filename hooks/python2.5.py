import os
import re
myos=os.uname()[0]

def libxml2(options,buildout):
    # patch Makefile
    pwd=options['compile-directory']
    file=open('/'.join((pwd,'python','Makefile')))
    import pdb;pdb.set_trace()  ## Breakpoint ##
    lines=file.readlines()
    for i,line in enumerate(lines):
        if line[:9] == 'LDFLAGS =' or line[:20] == 'PYTHON_SITE_PACKAGES':
            lines[i]=re.sub('2.4','2.5',line)
    file=open(os.path.join(pwd, 'python', 'Makefile'),'w+')
    file.writelines(lines)
    file.close()
    return None 

# vim:set ts=4 sts=4 et  :
