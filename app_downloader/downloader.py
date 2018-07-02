import time

import app_downloader.gplaycli.gplaycli as gplaycli
from constants import DOWNLOAD_FOLDER, DATABASE_FILE
import os
import logging
import pandas as pd

logging.basicConfig(format='%(asctime)s [%(name)-12.12s] %(levelname)-8s %(message)s',
                        level=logging.INFO)
logger = logging.getLogger(__name__)


class Downloader:
    """
    Downloads apks from the play store based on the options passed during initialization. This module is built on
    a slightly modified version of `Gplaycli <https://github.com/matlink/gplaycli>` (modified to work as a module).
    1. use_database (default=True): Use the provided database file to find the file name mappings for packages
    2. database_file: The file to search for mappings, by default it uses the file specified in the constants file
    3. download_folder: The folder to write the downloaded apps to, existing files with the same filename will **not** be
                        overwritten unless explicitly specified
    """
    def __init__(self,
            use_database=True,
            database_file=DATABASE_FILE,
            download_folder=DOWNLOAD_FOLDER):
        self.__download_folder = download_folder
        if not os.path.isdir(self.__download_folder):
            os.makedirs(self.__download_folder)

        self.__use_database = use_database
        if self.__use_database:
            self.__database_file = database_file
            self.__database_helper = dbhelper.DatabaseHelper(self.__database_file)

        # This config file is used by the GPlaycli module to determine the authentication token
        # By default, no account information is provided and a token is downloaded from developer's API
        self.__config_file = os.path.dirname(os.path.realpath(__file__)) + '/gplaycli.conf'

    def download(self, apps_list, force_download=False):
        """
        Downloads the apps passed in as parameters
        :param apps_list: A list of package names for the apps, or a list of [package names, file names]
        :param force_download: Overwrite an existing file with the same name. By default this is set to False.
        :return: A list of timestamps indicating the when the download was completed. If the download fails,
                 a None value is inserted instead.
        """
        if self.__use_database:
            apps_list = self.__database_helper.get_filename_mappings(apps_list)

        downloaded_apps = os.listdir(self.__download_folder)
        download_completion_time = []

        for index, app in enumerate(apps_list):
            print(app)
            if isinstance(app, str):
                app = [app, app + '.apk']

            if not force_download and app[1] in downloaded_apps:
                logger.info("App already downloaded - %s" % app[0])
                continue
            try:
                downloader = gplaycli.GPlaycli(config_file=self.__config_file)
                downloader.set_download_folder(self.__download_folder)
                logger.info("Downloading app - {} as {}".format(app[0], app[1]))
                return_value = downloader.download([app])
                download_completion_time.append(time.time() if return_value else None)
                del downloader
            except Exception as e:
                logger.error("Download failed - %s" % app[0])
                logger.error(e)
                download_completion_time.append(None)
        return download_completion_time

    def download_apps_from_file(self, filename):
        """
        Download apps with package names specified in the CSV file passed as a parameter
        :param filename: The filename (with path) for the CSV file.
                         The first line of the filename must be "package_name"
        :return: A list of timestamps indicating the when the download was completed. If the download fails,
                 a None value is inserted instead.
        """
        if not os.path.exists(filename):
            logger.error("File to download apps from, could not be found.")
            return
        # TODO Add feature to read file names with package names
        try:
            df = pd.read_csv(filename)
        except KeyError as e:
            logger.error("Incorrect keys in the file")
            logger.error(e)
            return [None]
        apps = df['package_name'].tolist()
        return self.download(apps)

    def get_doc_apk_details(self, packages):
        downloader = gplaycli.GPlaycli(config_file=self.__config_file)
        return downloader.get_doc_apk_details(packages)

def main():
    # TODO Add command line functionality to the module
    logging.info("Command line feature still in development")
    return


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s [%(name)-12.12s] %(levelname)-8s %(message)s',
                        level=logging.INFO)
    main()
