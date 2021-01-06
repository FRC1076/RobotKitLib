import checksumdir
import logging

def checksum(path, hashfunc="md5"):
    """Return checksum of files given by path.

    Wildcards can be used in check sum. Function is strongly dependent on checksumdir package by 'cakepietoast'.

    :param path: path of files to get hash from
    :param hashfunc: function used to get hash, default 'md5'
    :return: (str) hash of the file/files given by path
    """
    import checksumdir

    hash_func = checksumdir.HASH_FUNCS.get(hashfunc)
    if not hash_func:
        raise NotImplementedError("{} not implemented.".format(hashfunc))

    if os.path.isdir(path):
        return checksumdir.dirhash(path, hashfunc=hashfunc)

    hashvalues = []
    path_list = list(sorted(glob.glob(path)))
    logger.debug("path_list: len: %i", len(path_list))
    if len(path_list) > 0:
        logger.debug("first ... last: %s ... %s", str(path_list[0]), str(path_list[-1]))

    for path in path_list:
        if os.path.isfile(path):
            hashvalues.append(checksumdir._filehash(path, hashfunc=hash_func))
    logger.debug("one hash per file: len: %i", len(hashvalues))
    if len(path_list) > 0:
        logger.debug("first ... last: %s ... %s", str(hashvalues[0]), str(hashvalues[-1]))
    checksum_hash = checksumdir._reduce_hash(hashvalues, hashfunc=hash_func)
    logger.debug("total hash: {}".format(str(checksum_hash)))
    return checksum_hash

checksum('~/Robotics/RobotKitLib/RobotKitLib/RobotCode/robot.py')
