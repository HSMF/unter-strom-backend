import accumulator
import uploader
import threading
import sys


"""
@about
[en] Script to download current power measurements and upload them to a mysql database
[de] Skript, welches Produktion der Solarzellen liest und auf eine Mysql Datenbank hochlädt

TODO: 
 - rewrite in C++ 
 - implement function 100
"""

DEVICES = {
    "10.41.100.121": "GesamtMessungKRW",
    # "10.41.100.122": "MessungKRW_Mensa",
    # "10.41.100.123": "MessungKRW_Aula",
    # "10.41.100.124": "MessungKRW_Sudtrakt",
    # "10.41.100.125": "MessungKRW_Hauptgebaude",
    # "10.41.100.126": "GesamtMessungPV_Rysolar",
    # "10.41.100.127": "MessungRysolarHauptgebaude",
    # "10.41.100.128": "MessungRysolarMensa",
    # "10.41.100.129": "MessungRysolarSudtrakt",
}


def thread_func(ip, name):
    index = 0
    while 1:
        index += 1
        try:
            acc = accumulator.Accumulator(
                f"THREAD({ip}-{index})", ip, lambda x: uploader.upload(name, x))
            acc.start()
            acc.join()
        except Exception as e:
            print(e)


def main():
    try:
        for device in DEVICES:
            thread = threading.Thread(
                target=lambda: thread_func(device, DEVICES[device]))
            thread.start()
        thread.join()
    except:
        sys.exit(1)


if __name__ == "__main__":
    main()