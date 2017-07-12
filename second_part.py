import os
from xml.etree import ElementTree as ET
import zipfile

path = os.path.join(os.path.dirname(__file__), 'archives')

file1 = os.path.join(os.path.dirname(__file__), 'file1.csv')
file2 = os.path.join(os.path.dirname(__file__), 'file2.csv')

archives = os.listdir(path)

with open(file1, 'w') as f1, open(file2, 'w') as f2:
    for archive in archives:
        zf = zipfile.ZipFile(os.path.join(path, archive), 'r')
        for name in zf.namelist():
            if name.endswith('/'):
                continue
            f = zf.open(name)
            e = ET.parse(f).getroot()
            id = e[0].attrib['value']
            f1.write("{0} {1}\n".format(id, e[1].attrib['value']))
            for ob in e[2]:
                f2.write("{0} {1}\n".format(id, ob.attrib['name']))
