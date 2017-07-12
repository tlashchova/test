import os
import random
import string
from xml.etree import ElementTree as ET
from xml.dom import minidom
import zipfile


def random_string(length):
    return ''.join([random.choice(string.lowercase) for i in xrange(length)])


def create_archives(path, archives_count, xml_count):
    for i in xrange(archives_count):
        filename = os.path.join(path, '{0}.zip'.format(i + 1))
        with zipfile.ZipFile(filename, 'w') as zipped_f:
            for j in xrange(xml_count):
                filename = "test{0}.xml".format(j + 1)
                zipped_f.writestr(filename, create_xml())


def create_xml():
    root = ET.Element('root')
    var_id = ET.SubElement(root, 'var')
    var_id.set('name', 'id')
    var_id.set('value', random_string(10))
    var_level = ET.SubElement(root, 'var')
    var_level.set('name', 'level')
    var_level.set('value', str(random.randint(1, 100)))
    objects = ET.SubElement(root, 'objects')
    object_count = random.randint(1, 10)
    for i in xrange(object_count):
        object = ET.SubElement(objects, 'object')
        object.set('name', random_string(30))
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    return xmlstr


path = os.path.join(os.path.dirname(__file__), 'archives')
if not os.path.exists(path):
    os.makedirs(path)

create_archives(path, 50, 100)
