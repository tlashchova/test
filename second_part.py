import csv
import os
from xml.etree import ElementTree as ET
import zipfile

path = os.path.join(os.path.dirname(__file__), 'archives')

file1 = os.path.join(os.path.dirname(__file__), 'file1.csv')
file2 = os.path.join(os.path.dirname(__file__), 'file2.csv')

archives = os.listdir(path)

with open(file1, 'w') as f1, open(file2, 'w') as f2:
    csv_writer1 = csv.writer(f1, delimiter=',')
    csv_writer2 = csv.writer(f2, delimiter=',')
    for archive in archives:
        zf = zipfile.ZipFile(os.path.join(path, archive), 'r')
        for name in zf.namelist():
            f = zf.open(name)
            e = ET.parse(f).getroot()
            id = e[0].attrib['value']
            csv_writer1.writerow([id, e[1].attrib['value']])
            for ob in e[2]:
                csv_writer2.writerow([id, ob.attrib['name']])
