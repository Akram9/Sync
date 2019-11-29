import hashlib

def hash_file(file):
      sha256hash = hashlib.sha256()
      with open(file, 'rb') as f:
          for block in iter(lambda: f.read(4096), b''):
              sha256hash.update(block)
      return(sha256hash.hexdigest())

def sha_check(file1, file2):
    hash1 = hash_file(file1)
    hash2 = hash_file(file2)
    if (hash1 == hash2):
        return(True)
    else:
        return(False)
