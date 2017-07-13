import csv
import multiprocessing
import os
import time
from xml.etree import ElementTree as ET
import zipfile


def read_from_archive(archives_queue, levels_queue, objects_queue):
    while True:
        archive = archives_queue.get()
        if archive is None:
            break
        zf = zipfile.ZipFile(archive, 'r')
        for name in zf.namelist():
            f = zf.open(name)
            e = ET.parse(f).getroot()
            id = e[0].attrib['value']
            levels_queue.put([id, e[1].attrib['value']])
            for ob in e[2]:
                objects_queue.put([id, ob.attrib['name']])
    levels_queue.put(None)
    objects_queue.put(None)


def write_to_csv_file(output_file, workers, queue):
    processes = workers
    with open(output_file, 'w') as output_file:
        csv_levels = csv.writer(output_file, delimiter=',')
        while processes:
            try:
                record = queue.get()
                if record is None:
                    processes -= 1
                else:
                    csv_levels.writerow(record)
            except Exception as e:
                print e.message


def main():
    workers = 8
    path = os.path.join(os.path.dirname(__file__), 'archives')
    file_levels = os.path.join(os.path.dirname(__file__), 'levels.csv')
    file_objects = os.path.join(os.path.dirname(__file__), 'objects.csv')
    archives = os.listdir(path)

    archives_queue = multiprocessing.Queue()
    levels_queue = multiprocessing.Queue()
    objects_queue = multiprocessing.Queue()
    processes = []

    t1 = time.time()

    for archive in archives:
        archives_queue.put(os.path.join(path, archive))

    for w in xrange(workers):
        p = multiprocessing.Process(target=read_from_archive,
                                    args=(archives_queue, levels_queue, objects_queue))
        p.start()
        processes.append(p)
        archives_queue.put(None)

    write_levels = multiprocessing.Process(target=write_to_csv_file,
                                           args=(file_levels, workers, levels_queue))
    write_levels.start()

    write_objects = multiprocessing.Process(target=write_to_csv_file,
                                            args=(file_objects, workers, objects_queue))
    write_objects.start()

    for p1 in processes:
        p1.join()
    write_levels.join()
    write_objects.join()

    t2 = time.time()
    print t2 - t1


if __name__ == "__main__":
    main()
