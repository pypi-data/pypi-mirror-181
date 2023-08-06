import gzip
import os
import tarfile
import zipfile

import pyproj


class FileIO:
    @staticmethod
    def mkdirs(file_path: str):
        dir_name = os.path.dirname(file_path) if os.path.isfile(file_path) else file_path
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    @staticmethod
    def extract_zip_file(input_file, output_folder=None):
        """
        This function extract the zip files

        Keyword Arguments:
        output_file -- name, name of the file that must be unzipped
        output_folder -- Dir, directory where the unzipped data must be
                               stored
        """
        # extract the data
        if not output_folder:
            output_folder = input_file[:-4]
        z = zipfile.ZipFile(input_file, 'r')
        z.extractall(output_folder)
        z.close()
        return output_folder

    @staticmethod
    def extract_data_gz(zip_filename, outfilename):
        """
        This function extract the zip files

        Keyword Arguments:
        zip_filename -- name, name of the file that must be unzipped
        outfilename -- Dir, directory where the unzipped data must be
                               stored
        """

        with gzip.GzipFile(zip_filename, 'rb') as zf:
            file_content = zf.read()
            save_file_content = open(outfilename, 'wb')
            save_file_content.write(file_content)
        save_file_content.close()
        zf.close()
        os.remove(zip_filename)

    @staticmethod
    def extract_data_tar_gz(zip_filename, output_folder):
        """
        This function extract the tar.gz files

        Keyword Arguments:
        zip_filename -- name, name of the file that must be unzipped
        output_folder -- Dir, directory where the unzipped data must be
                               stored
        """

        os.chdir(output_folder)
        tar = tarfile.open(zip_filename, "r:gz")
        tar.extractall()
        tar.close()

    @staticmethod
    def extract_data_tar(zip_filename, output_folder):
        """
        This function extract the tar files

        Keyword Arguments:
        zip_filename -- name, name of the file that must be unzipped
        output_folder -- Dir, directory where the unzipped data must be
                               stored
        """

        os.chdir(output_folder)
        tar = tarfile.open(zip_filename, "r")
        tar.extractall()
        tar.close()

    @staticmethod
    def get_file_name_ext(fp):
        base_name = os.path.basename(fp)
        sfp = base_name.split(".")
        return ",".join(sfp[:-1]), sfp[-1]

    @classmethod
    def read_prj_file(cls, prj_path) -> pyproj.CRS:
        name, ext = cls.get_file_name_ext(prj_path)
        if ext == "prj":
            with open(prj_path) as f:
                wkt = f.read()
                crs = pyproj.CRS.from_wkt(wkt)
                return crs
        return None

    @classmethod
    def get_files_list_in_folder(cls, dir_path, ext=None):
        only_files = []
        for f in os.listdir(dir_path):
            fp = os.path.join(dir_path, f)
            if os.path.isfile(fp):
                if ext is not None:
                    if cls.get_file_name_ext(fp)[1] == ext:
                        only_files.append(fp)
                else:
                    only_files.append(fp)
        return only_files

    @classmethod
    def write_file(cls, file_path, content):
        with open(file_path, "wb") as file:
            file.write(content)

