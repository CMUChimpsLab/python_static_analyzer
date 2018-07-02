from unittest import TestCase
from app_downloader.downloader import Downloader
import os
import shutil


class TestDownloader(TestCase):
    def setUp(self):
        self.__download_folder = "test_download_folder"
        self.__test_app_name = 'com.facebook.katana'
        self.__downloader = Downloader(use_database=False, download_folder=self.__download_folder)
        self.__test_csv_file = 'test_file'

    def tearDown(self):
        shutil.rmtree(self.__download_folder)
        if os.path.exists(self.__test_csv_file):
            os.remove(self.__test_csv_file)

    def test_download_folder_creation(self):
        self.assertTrue(os.path.isdir(self.__download_folder))

    def test_download_without_filename(self):
        return_value = self.__downloader.download([self.__test_app_name])
        self.assertTrue(os.path.exists(self.__download_folder + '/com.facebook.katana.apk'))
        self.assertEqual(len(return_value), 1)

    def test_download_with_filename(self):
        return_value = self.__downloader.download([[self.__test_app_name, 'test.apk']])
        self.assertTrue(os.path.exists(self.__download_folder + '/test.apk'))
        self.assertEqual(len(return_value), 1)

    def test_download_apps_from_properly_formatted_file(self):
        lines = ['package_name\n', self.__test_app_name]
        with open(self.__test_csv_file, 'w+') as f:
            f.writelines(lines)

        self.__downloader.download_apps_from_file(self.__test_csv_file)
        self.assertTrue(os.path.exists(self.__download_folder + '/com.facebook.katana.apk'))

    def test_unknown_app_name(self):
        return_value = self.__downloader.download(['sdublsn'])
        self.assertEqual(return_value[0], None)
