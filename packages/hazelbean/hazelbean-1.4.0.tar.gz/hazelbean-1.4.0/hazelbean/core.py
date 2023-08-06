import os, logging, datetime, errno, time
import hazelbean as hb
from hazelbean import os_utils

hb.LAST_TIME_CHECK = 0

def timer(msg=None, silent=False, suppress=False):
    if suppress:
        return
    
    if hb.LAST_TIME_CHECK == 0.0:
        hb.LAST_TIME_CHECK = time.time()
    else:
        if not msg:
            msg = 'Elapsed'
        if not silent:
            print(str(msg) + ': ' + str(time.time() - hb.LAST_TIME_CHECK) + '.')
            
    hb.LAST_TIME_CHECK = time.time()

from hazelbean.config import logging_levels

def get_logger(logger_name=None, logging_level='info', format='full'):
    """Used to get a custom logger specific to a file other than just susing the config defined one."""
    if not logger_name:
        try:
            logger_name = os.path.basename(main.__file__)
        except:
            logger_name = 'unnamed_logger'
    L = logging.getLogger(logger_name)
    L.setLevel(logging_levels[logging_level])
    CL = hb.config.CustomLogger(L, {'msg': 'Custom message: '})
    # FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    FORMAT = "%(message)s"
    formatter = logging.Formatter(FORMAT)

    # handler = logging.StreamHandler()
    # handler.setFormatter(formatter)
    # L.addHandler(handler)
    return CL

# def timer(msg=None, silent=False):
#     if hb.config.LAST_TIME_CHECK == 0.0:
#         hb.config.LAST_TIME_CHECK = time.time()
#     else:
#         if not msg:
#             msg = 'Elapsed'
#         if not silent:
#             print(str(msg) + ': ' + str(time.time() - hb.config.LAST_TIME_CHECK) + ' at time ' + str(hb.pretty_time()))
#         hb.config.LAST_TIME_CHECK = time.time()
        
def path_exists(path, minimum_size_check=0, verbose=False):
    # os.path.exists throws an exception rather than False if given None. This version resolves None as False.
    # set minimum_size_check to None if 0 size is okay.
    # if verbose:
    #     L.info('  Checking to see if ' + str(path) + ' exists.')
    
    # If verbose is a Logger object, use it. Otherwise create it.
    if verbose is not False:
        if verbose is not True:
            L = verbose
        else:
            L = get_logger('hb.core')
            
    if path is None:
        if verbose:
            L.critical('Path given to hazelbean.path_exists() was None.')
        return False
    if os.path.isdir(path):
        if verbose:
            L.info('Path exists: ' + str(path) + ' exists but it is a directory.')
        return True

    # if isinstance(path, hb.InputPath):
    #     path = path.get_path(hb.path_filename(path))
    if not path:
        if verbose:
            L.info('Path DOES NOT exist: ' + str(path) + ' DOES NOT EXIST, but it is a HB InputPath object.')
        return False
    else:
        if minimum_size_check is not None:
            try:
                if os.path.getsize(path) > minimum_size_check:
                    if verbose:
                        L.info('Path exists: ' + str(path) + ' exists and has a filesize above minimum.')
                    return True
                else:
                    if verbose:
                        L.info('Path DOES NOT exist: ' + str(path) + ' DOES NOT EXIST, at least not with a filesize above the minimum.')
                    return False
            except:
                if verbose:
                    L.info('Path DOES NOT exist: ' + str(path) + ' DOES NOT EXIST, because it wasnt able to run os.path.getsize.')
                return False
        else:
            try:
                if os.path.exists(path):
                    if verbose:
                        L.info('Path exists: ' + str(path) + ' exists, found via os.path.exists().')
                    return True
                else:
                    if verbose:
                        L.info('Path DOES NOT exist: ' + str(path) + ' DOES NOT EXIST, at least according to os.path.exists().')
                    return False
            except:
                if verbose:
                    L.info('Path DOES NOT exist: ' + str(path) + ' DOES NOT EXIST, because os.path.exists() failed to run.')
                return False


def path_file_root(input_path):
    # if isinstance(input_path, hb.InputPath):
    #     input_path = str(input_path)
    return os.path.splitext(os.path.split(input_path)[1])[0]

def file_root(input_path):
    return path_file_root(input_path)


def pretty_time(format=None):
    # Returns a nicely formated string of YEAR-MONTH-DAY_HOURS-MIN-SECONDS based on the the linux timestamp
    now = str(datetime.datetime.now())
    day, time = now.split(' ')
    day = day.replace('-', '')
    time = time.replace(':', '')
    if '.' in time:
        time, milliseconds = time.split('.')
        milliseconds = milliseconds[0:3]
    else:
        milliseconds = '000'

    if not format:
        return day + '_' + time
    elif format == 'full':
        return day + '_' + time + '_' + milliseconds
    elif format == 'day':
        return day
    elif format == 'day_hyphens':
        now = str(datetime.datetime.now())
        day, time = now.split(' ')
        return day
    elif format == 'year_month_day_hyphens':
        now = str(datetime.datetime.now())
        day, time = now.split(' ')
        return day



def create_directories(directory_list):
    """Make directories provided in list of path strings.

    This function will create any of the directories in the directory list
    if possible and raise exceptions if something exception other than
    the directory previously existing occurs.

    Args:
        directory_list (list/string): a list of string uri paths

    Returns:
        None
    """
    if isinstance(directory_list, str):
        directory_list = [directory_list]
    elif not isinstance(directory_list, list):
        raise TypeError('Must give create_directories either a string or a list.')

    for dir_name in directory_list:
        split_dir_name = None
        has_extension = os.path.splitext(dir_name)[1]
        if len(has_extension) > 0:
            split_dir_name = os.path.split(dir_name)[0]
        else:
            split_dir_name = dir_name
        # try:
        #     os.makedirs(dir_name)
        # except:
        #     split_dir_name = os.path.split(dir_name)[0]
        if split_dir_name is not None:
            try:
                os.makedirs(split_dir_name)
            except OSError as exception:
                #It's okay if the directory already exists, if it fails for
                #some other reason, raise that exception
                if (exception.errno != errno.EEXIST and
                        exception.errno != errno.ENOENT):
                    raise



