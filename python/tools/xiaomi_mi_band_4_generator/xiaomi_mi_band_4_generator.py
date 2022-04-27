"""
Założenia:
 - Rozpakowywanie WF (Na razie ręcznie)
 - Pakowanie WF (na razie ręcznie)
 - Łączenie jsonów (poprawić)
 - Generowanie jednego globalneggo jsona (poprawić)

  python scripy.py --json / --bin

    Do .bashrc należy dodać alias na xiaomi mi band 4 (un)packer : MiBandWFTool
    alias MiBandWFTool='wine /anubis/xiaomi_mi_band_4/PC/SOFTWARE/MiBandWFTool_1.4.2/PaletteImageMode/WatchFace.exe'
"""


import argparse
import glob
import json
import os

from jsonmerge import merge # jsonmerge==1.7.0

glob_data = []

WATCHFACES_DOWNLOAD_FOLDER_PATH = '/anubis/xiaomi_mi_band_4/PC/DOWNLOADED'
DESTINATION_JSON_PATH = '/anubis/repositories/github.com/8tm/scripts/python/tools/xiaomi_mi_band_4_generator/destination_json.json'

WATCHFACES_BINARY_DOWNLOAD_FOLDER_PATH = '/anubis/xiaomi_mi_band_4/PC/DOWNLOADED/ALL'

class WatchFace:

    _path = str

    def __init__(self):
        pass

    def set_path_to_watchface_folder(self, path_to_watchface_folder):
        self._path = path_to_watchface_folder

    def pack(self, path_to_watchface_json_file):
        pass

    def unpack(self, path_to_watchface_binary_file):
        pass


def merge_jsons(path_to_first_json_file, path_to_second_json_file, path_to_output_json_file):
    open(path_to_second_json_file, "w").writelines([l for l in open(path_to_output_json_file).readlines()])

    print(" - Converting:\n      a) {a}\n      b) {b}\n      c) {c}\n\n".format(a=path_to_first_json_file,
                                                                                b=path_to_second_json_file,
                                                                                c=path_to_output_json_file))
    try:
        a = json.loads(open(path_to_first_json_file).read())
        b = json.loads(open(path_to_second_json_file).read())
        result = merge(a, b)
        #print(result)
        with open(path_to_output_json_file, 'w') as f:
            json.dump(result, f, indent=4)
    except FileNotFoundError as error:
        print("File not found" + error)


def unpack_watchface(watchface_bin_path):
    pass


def pack_watchface(watchface_json_path):
    pass


def get_downloaded_watchfaces(download_folder_path):
    return glob.glob(f'{WATCHFACES_DOWNLOAD_FOLDER_PATH}/*')


def get_watchface_bin_file(watchface_path):
    bin_file = ''
    try:
        bin_file, *_ = glob.glob(f'{watchface_path}/*.bin')
    except IndexError as ie:
        pass
    except ValueError as ve:
        pass
    return bin_file if os.path.exists(bin_file) else ""


def get_watchface_json_file(watchface_path):
    json_file = ''
    try:
        json_file, *_ = glob.glob(f'{watchface_path}/*/*.json')
    except IndexError as ie:
        pass
    except ValueError as ve:
        pass
    return json_file if os.path.exists(json_file) else ""


def get_arguments():
    """ function for parsing arguments - returns arguments - object containing arguments """
    parser = argparse.ArgumentParser(description="Some description")

    parser.add_argument("--bin", required=False, help="Path to binary file")
    parser.add_argument("--downloads", required=False, help="Path to download folder with folders contains bin files")
    parser.add_argument("--json", required=False, help="Path to json file")
    parser.add_argument("--destination", required=False, help="Path to destination json file")

    return parser.parse_args()


if __name__ == "__main__":
    arguments = get_arguments()

    WATCHFACES_DOWNLOAD_FOLDER_PATH = arguments.downloads if arguments.downloads else WATCHFACES_DOWNLOAD_FOLDER_PATH
    DESTINATION_JSON_PATH = arguments.destination if arguments.destination else DESTINATION_JSON_PATH

    watchace = WatchFace()
    watchace.path = '/test/inny/folder'

    folders = get_downloaded_watchfaces(WATCHFACES_DOWNLOAD_FOLDER_PATH)
    for folder in folders:
        bin_path = get_watchface_bin_file(folder)
        json_path = get_watchface_json_file(folder)
        #print(bin_path) if bin_path else None
        #print(json_path) if json_path else None

        merge_jsons(json_path, '{file}.temp'.format(file=DESTINATION_JSON_PATH), DESTINATION_JSON_PATH)



    #json_files = list()

    #for folder_path in glob.glob(f'{WATCHFACES_DOWNLOAD_FOLDER_PATH}/*'):
    #    try:
    #        json_file, *_ = glob.glob(f'{folder_path}/*/*.json')
    #    except IndexError as ie:
    #        pass
    #    except ValueError as ve:
    #        pass
    #    json_files.append(json_file)
    #return json_files



    #for json_path in json_files:
    #    print(json_path)

    #with open(file) as json_file:
    #    data = json.load(json_file)
    #    i = 0
    #    while i < len(data):
    #        glob_data.append(data[i])
    #        i += 1

    #with open('../../finalFile.json', 'w') as f:
    #    json.dump(glob_data, f, indent=4)



