# DIETERpy is electricity market model developed by the research group
# Transformation of the Energy Economy at DIW Berlin (German Institute of Economic Research)
# copyright 2021, Carlos Gaete-Morales, Martin Kittel, Alexander Roth,
# Wolf-Peter Schill, Alexander Zerrahn
"""

"""
import os
import glob
import json
import wget
import sys
import time
import shutil
from zipfile import ZipFile

from ..config import settings

def create_project(project_name, template, location=None):
    copy_to_user_data_dir(location=location)
    settings.PROJECT_NAME = project_name
    user_dir = location or settings.USER_PATH or settings.DEFAULT_DATA_DIR
    template_info_file = os.path.join(settings.MODULE_TEMPLATES_PATH,settings.TEMPLATES_INFO_FILE)

    with open(template_info_file) as info_file:
        info_dict = json.load(info_file)

    template_check = list(info_dict.keys())
    if template in template_check:
        pass
    else:
        raise Exception(f'--template argument "{template}" not in {template_check}')

    LOCAL_TPL = os.path.join(user_dir,template)
    PROJECT_DESTINATION = os.path.join(settings.CWD, settings.PROJECT_NAME)
    os.makedirs(PROJECT_DESTINATION, exist_ok=False)

    if info_dict[template]['download']:
        if info_dict[template]['access_method'] in ['zenodo','url']:
            if not os.path.exists(LOCAL_TPL):
                zipfilelocation = download_templates(DOI_OR_URL=info_dict[template]['location'], method=info_dict[template]['access_method'], template_name=template, location=location)
                unzip(zipfilelocation, user_dir)
                if not os.path.exists(LOCAL_TPL):
                    print(f"Warning: Destination of unzipped file {zipfilelocation} does not coincide with template name folder {LOCAL_TPL}. You can change template folder name manually.")
        elif info_dict[template]['access_method'] in ['local']:
            if os.path.exists(LOCAL_TPL):
                shutil.rmtree(LOCAL_TPL)
                time.sleep(1)
            HOST_TPL_FILES = glob.glob(os.path.join(info_dict[template]['location'], "**/*.*"), recursive=True)
            for file in HOST_TPL_FILES:
                rest = file.rsplit(info_dict[template]['location'])[-1][1:]
                destpath = os.path.join(LOCAL_TPL, rest)
                os.makedirs(os.path.split(destpath)[0], exist_ok=True)
                shutil.copyfile(file, destpath)
        else:
            raise Exception(f"access_method should be {', '.join(['zenodo','url','local'])}, while key 'download' is set as True. See this file '{template_info_file}'")
    else:
        pass

    SELECTED_TPL_FILES = glob.glob(os.path.join(LOCAL_TPL, "**/*.*"), recursive=True)

    for file in SELECTED_TPL_FILES:
        rest = file.rsplit(LOCAL_TPL)[-1][1:]
        destpath = os.path.join(PROJECT_DESTINATION, rest)
        os.makedirs(os.path.split(destpath)[0], exist_ok=True)
        shutil.copyfile(file, destpath)

    info = info_dict[template]['info']
    url = info_dict[template]['location']
    version = info_dict[template]['version']
    if url is None:
        url = ''
    print(f'''Project folder created! \n   Template name: {template} \n     Description: {info} \n         version: {version} \n            From: {url}''')
    return None

def template_list(location=None):
    user_dir = location or settings.USER_PATH or settings.DEFAULT_DATA_DIR
    copy_to_user_data_dir(location=location)

    with open(os.path.join(user_dir, settings.TEMPLATES_INFO_FILE)) as info_file:
        info_dict = json.load(info_file)
    for k, v in info_dict.items():
        print(f'''{k}: {v['info']}''')

def download_templates(DOI_OR_URL=None, method='url', template_name=None, location=None):
    """
    Download templates data from zenodo or an url.

    Args:
        location (str, optional): Path to user path. Defaults to None.

    Returns:
        list: list of downloaded files.
    """
    methods = ['zenodo', 'url']
    if method in methods:
        pass
    else:
        raise Exception(f'''Method selected should be one of the following "{'", "'.join(methods)}" ''')

    user_dir = location or settings.USER_PATH or settings.DEFAULT_DATA_DIR
    os.makedirs(user_dir, exist_ok=True)

    if method == 'zenodo':
        try:
            import zenodo_get
            os.chdir(user_dir)
            zenodo_get.zenodo_get([DOI_OR_URL, "-wurls.txt"])
            os.chdir(settings.CWD)
            time.sleep(1)
            fh = open(os.path.join(user_dir, "urls.txt"))
            text_list = []
            for line in fh:
                text_list.append(line.rstrip('\n'))
            fh.close()

            actual_url = None
            if template_name is None:
                actual_url = text_list[0]
            else:
                for url in text_list:
                    if template_name in url:
                        actual_url = url
                        break
                if actual_url is None:
                    raise Exception(f"Template name '{template_name}' is not part of any of urls in file {os.path.join(user_dir, 'urls.txt')}")
        except ImportError as error:
            # Output expected ImportErrors.
            print(error.__class__.__name__ + ": " + error.message)
        except Exception as exception:
            # Output unexpected Exceptions.
            print(exception, False)
            print(exception.__class__.__name__ + ": " + exception.message)
            
    elif method == 'url':
        actual_url = DOI_OR_URL

    filename = os.path.join(user_dir, os.path.split(actual_url)[-1])
    # print(f'filename: {filename}')
    if os.path.exists(filename):
        dest = filename
    else:
        print('')
        print(f"Internet connection is required as the selected project template will be first downloaded here: \n '{user_dir}'")
        time.sleep(3)
        print(f"Downloading file... {actual_url.strip()}")
        os.chdir(user_dir)
        dest_file = wget.download(actual_url.strip(), out=None, bar=bar_progress)
        os.chdir(settings.CWD)
        dest = os.path.join(user_dir, dest_file)
        print("")
        print("Zip file downloaded!")
    return dest

def unzip(path, folder='temp'):
    with ZipFile(path, 'r') as zipObj:
        zipObj.extractall(folder)

def bar_progress(*args):
    """
    Prints actual progress in format: "Downloading: 80% [8 / 10] kilobyte"
    Args:
        current (int): Current download.
        total (int): Total number of downloads.
    """
    current = args[0]
    total = args[1]
    progress_message = "Downloading: %d%% [%d / %d] kilobyte" % (
        current / total * 100,
        current / 1024,
        total / 1024,
    )
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()


def copy_to_user_data_dir(location=None):
    """
    Copies files to user data directory.

    Args:
        location (str, optional): Location to which files should be copied. Defaults to None.
    """
    flag = False
    user_dir = location or settings.USER_PATH or settings.DEFAULT_DATA_DIR
    os.makedirs(user_dir, exist_ok=True)
    PKG_DATA_FILES = glob.glob(os.path.join(settings.MODULE_TEMPLATES_PATH, "**/*.*"), recursive=True)
    for file in PKG_DATA_FILES:
        rest = file.rsplit(settings.MODULE_TEMPLATES_PATH)[-1][1:]
        destpath = os.path.join(user_dir, rest)
        if not os.path.exists(destpath):
            if not flag:
                print("Moving template files to the local directory")
                flag = True
            print('   ', destpath)
            os.makedirs(os.path.split(destpath)[0], exist_ok=True)
            shutil.copyfile(file, destpath)
    if flag:
        print("Template files moved successfully!")
