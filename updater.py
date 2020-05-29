from halo import Halo


def init_update():
    print("Get the latest version from https://github.com/dhtdht020/osc-dl/")

    with Halo(text="Checking for updates..", color="white"):
        check_update()


def check_update():
    print("Automatic updater is not yet implemented.")
