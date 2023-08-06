from kadi_apy import KadiManager
import shutil
import pprint
from FAIRSave.kadi_search import Search_Item_ID


def Download_Files_from_Kadi(instance:str, files_path:str, file_list:list, unpack_zip:bool, collection=None, collection_id=None, record_id=None, record=None):
    """Download files from a record on Kadi4Mat

    Args:
        Instance (str): The name of the instance to use in combination with a config file.
        files_path (path): Path to store the downloaded files
        file_list (list): List of files to download from record
        unpack_zip (bool): Boolean to indicate whether the zip files should be unpacked or not.
        collection (str, opt): Title of collection to search the record in. Defaults to None.
        collection_id (int, opt): ID of collection to search the record in. Defaults to None.
        record_id (int, opt): ID of the record to download files from. Defaults to None.
        record (str, opt): Title of record to download files from. Defaults to None.
    """
    # Create Manager with configuration instance
    manager = KadiManager(instance = instance)
    
    if collection != None:
        collection_id = Search_Item_ID(instance=instance, title=record, item='record', collection=collection)
        
    if record != None:
        record_id = Search_Item_ID(instance=instance, title=record, item='record', collection=collection)
        
    record = manager.record(id=record_id)

    # Path to store the files for Matlab
    for file in file_list:
        file_id = record.get_file_id(file)
        record.download_file(file_id, files_path + '/' + file)

        # unzip the zip folder to acccess the position data files
        if unpack_zip == 'True': # True is not a boolean in this case, its a string from matlab
            if file.endswith('.zip'):
                shutil.unpack_archive(files_path + '/' + file,
                                    files_path + '/' + file.strip('.zip'),
                                    'zip')

def Kadi_Metadata(instance:str, file_path=None, save_as_txt=0, record_id=None, record=None, collection=None):
    """Prints the Metadata of a record to a text file.

    Args:
        Instance (str): The name of the instance to use in combination with a config file.
        file_path (str, optional): Path to store the metadata.txt. Defaults to None.
        save_as_txt (int): Is either 0 for not saving the metadata as txt file or 1 for saving.
        record_id (int, optional): ID of the record to get metadata from. Defaults to None.
        record_name (str, optional): Name of the record. Defaults to None.
        collection (str): Collection to the record in. Defaults to None.
    """
    # Create Manager with configuration of the host and personal access token (PAT)
    manager = KadiManager(instance = instance)
    
    if record != None:
        record_id = Search_Item_ID(instance=instance, title=record, item='record', collection=collection)
        
    metadata = manager.record(id=record_id).meta
    
    if save_as_txt == 1:
        with open(record_id + '.txt', 'w+') as f:
            pprint.pprint(metadata, indent=4, stream=f)
        
    return metadata
