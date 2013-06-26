import sys
import os
import hashlib
import shutil

def withAuthor(fname):
    with open(fname, "r") as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

def withoutAuthor(fname):
    with open(fname, "r") as fh:
        m = hashlib.md5()
        data = fh.read()
        dash = data.replace('/', '(', 2).find('/')
        data = data[dash:]
        m.update(data)
    return m.hexdigest()

def withoutAuthorProcessed(fname):
    with open(fname, "r") as fh:
        m = hashlib.md5()
        data = fh.read()
        dash = data.replace('/', '(', 2).find('/')
        data = ''.join(data[dash:].lower().split())
        m.update(data)
    return m.hexdigest()
    
def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk

def check_for_duplicates(paths, hash=hashlib.sha1):
    nrunique = 0
    nrdup = 0
    nrfiles = 0
    nrnonhtmlfiles = 0
    hashes = {}
    print len(hashes)
    for path in paths:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                nrfiles += 1
                notUsed, fileExtension = os.path.splitext(filename)
                if fileExtension == '.html':
                    full_path = os.path.join(dirpath, filename)
                    hashobj = hash()
                    for chunk in chunk_reader(open(full_path, 'rb')):
                        hashobj.update(chunk)
                    file_id = withoutAuthorProcessed(full_path)
                    duplicate = hashes.get(file_id, None)
                    if duplicate:
                        nrdup +=1
                        #print "Duplicate found: %s and %s" % (full_path, duplicate)
                    else:
                        nrunique += 1
                        hashes[file_id] = full_path
                        shutil.copy2(full_path, '/home/Johan/results')
                else:
                    nrnonhtmlfiles += 1
                    if fileExtension != '.txt':
                        print "NOT TXT BUT " + fileExtension

    print "Computation complete"
    print "Number of files processed: " + str(nrfiles)
    print "Size of hash table: " + str(len(hashes))
    print "Number of duplicate files was: " + str(nrdup)
    print "Number of unique files was: " + str(nrunique)
    print "Number of non HTML files was: " + str(nrnonhtmlfiles)
    print "Which sums up to: " + str(nrdup + nrunique + nrnonhtmlfiles)

if sys.argv[1:]:
    check_for_duplicates(sys.argv[1:])
else:
    print "Please pass the paths to check as parameters to the script"

    
