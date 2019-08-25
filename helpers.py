

class Helpers:

    @staticmethod
    def free_space():
        """ Show free space of microcontroller """
        import os
        fs_stat = os.statvfs('/')
        fs_size = fs_stat[0] * fs_stat[2]
        fs_free = fs_stat[0] * fs_stat[3]
        print("File System Size {:,} - Free Space {:,}".format(fs_size, fs_free))
