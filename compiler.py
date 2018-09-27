import os, io
import py_compile 
import zipfile

pyc = 'mod_recent_stat'
path = '/1.1.0.1/'

class WotModZip(object):
    
    def __init__(self):
        self.compile(['res/scripts/client/gui/mods'])
        
    def dirs_inv(self, path):
        while path:
            path = os.path.dirname(path)
            yield path + '/'
            
    def parent_dirs(self, path):    
        return reversed(tuple(self.dirs_inv(path + '/'))[:-1])
           
    def compile(self, dirname):
        with io.BytesIO() as dst_bin:
            with zipfile.ZipFile(pyc.replace('mod_', '') + '.wotmod', 'w') as dst_zip: 
                for dirs_name in dirname:
                    namelist = dst_zip.namelist()
                    for parent_dir in self.parent_dirs(dirs_name):
                        if parent_dir not in namelist:
                            dst_zip.writestr(parent_dir, '')
                dst_zip.write('%s.pyc' % pyc, 'res/scripts/client/gui/mods/%s.pyc' % pyc)                        
                dst_zip.close()
            dst_bin_data = dst_bin.getvalue()
        return dst_bin_data


wotModZip = WotModZip()

fZip = zipfile.ZipFile(pyc.replace('mod_', '') + '.rar', 'w')
fZip.write(pyc.replace('mod_', '') + '.wotmod', path + pyc.replace('mod_', '') + '.wotmod')
fZip.close()
os.remove(pyc.replace('mod_', '') + '.wotmod')
