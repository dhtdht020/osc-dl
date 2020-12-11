import psutil


class SDManagement:
    disks = []

    def get_disks(self):
        for disk in psutil.disk_partitions():
            if disk.opts == "rw,removable":
                self.disks.append(disk)
        return self.disks
