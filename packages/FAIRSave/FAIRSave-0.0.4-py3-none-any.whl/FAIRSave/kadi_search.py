from kadi_apy import KadiManager
import re


def Search_Item_Titles(instance: str, item: str, keywords=None, title=None, tags=None,
                       description=None, record_type=None, collection_id=None, collection=None):
    """Search for Items.

    Args:
        instance (str): The name of the instance to use in combination with a config file.
        item (str): item: The resource type defined either as string or class.
        keywords (str, optional): Words in title or tags to search for. Defaults to None.
        title (str, optional): Words in title to search for. Defaults to None.
        tags (str, optional): Words in tags to search for. Defaults to None.
        description (str, optional): Words in description to search for. Defaults to None.
        record_type (str, optional): Type of record to search for. Defaults to None.
        colection_id (int, optional): ID of collection to search in. Defaults to None.
        collection (str, optional): Name of collection to search in. Defaults to None.

    Returns:
        list: List of items found in Kadi4Mat.
    """
    # Replace empty strings with None
    if keywords == "":
        keywords = None
    elif title =="":
        title = None
    elif tags =="":
        tags = None
    elif description == "":
        description = None
        
    if collection != None:
        collection_id = Search_Item_ID(instance, title=collection, item='collection')

    SR = KadiManager(instance=instance).search_resource()

    search_results = (SR.search_items(  item=item,
                                        type=record_type,
                                        collection=collection_id,
                                        per_page =100))
    pages = search_results.json()['_pagination'].get('total_pages')

    title_list = []
    for n in range(1,pages+1):
        var = SR.search_items(  item=item,
                                type=record_type,
                                collection=collection_id,
                                per_page =100, page=n).json().get('items')
        if keywords != None:
            title_list +=  [x['title']
                            for x in var
                            if keywords in x['title'] or any(keywords in s for s in x['tags']) or keywords in x['plain_description']]
        elif title != None:
            title_list +=  [x['title']
                            for x in var
                            if title in x['title']]
        elif tags != None:
            title_list +=  [x['title']
                            for x in var
                            if any(tags in s for s in x['tags'])]
        elif description != None:
            title_list +=  [x['title']
                            for x in var
                            if description in x['plain_description']]
        else: 
            title_list += [x['title'] for x in var]
    return title_list

def Search_Item_ID(instance:str, title:str, item:str, collection=None, collection_id=None, record_type=None):
    """Search for ID of item.

    Args:
        instance (str): The name of the instance to use in combination with a config file.
        title (str): Title of the record to get the ID from.
        item (str): The resource type defined as string. 
        collection (str): Title of collection to search in. Defaults to None.
        collection_id (int): ID of collection to search in. Defaults to None.
        record_type (str, optional): Type of record to search ID from. Defaults to None.

    Returns:
        int: Id of the record.
    """
    if collection != None:
        collection_id = Search_Item_ID(instance, title=collection, item='collection')
        
    SR = KadiManager(instance=instance).search_resource()
    search_results = (SR.search_items(  item=item,
                                        collection = collection_id,
                                        type=record_type,
                                        title=title,
                                        per_page =100))
    pages = search_results.json()['_pagination'].get('total_pages')
    for n in range(1, pages+1):
        var = SR.search_items(  item=item,
                                collection=collection_id,
                                type=record_type,
                                title=title,
                                per_page =100, page=n).json().get('items')
        title_id_tuple = [(x['title'], x['id'])
                          for x in var
                          if x['title']==title][0]
        return title_id_tuple[1]

def Search_Files(instance:str, record_id=None, record=None):
    """Searches for files attached to a record in Kadi4Mat.

    Args:
        instance (str): The name of the instance to use in combination with a config file.
        record_id (int): ID of the record in Kadi4Mat. Defaults to None.
        record (str): Name of the record in Kadi4Mat. Defaults to None.

    Returns:
        filelist (list): List of files attached to record.
    """
    if record is None and record_id is None:
        raise ValueError('Choose a record to get files from.')
    
    if record != None:
        record_id = Search_Item_ID(instance=instance, title=record, item='record')

    record = KadiManager(instance = instance).record(id = record_id)
    pages = record.get_filelist().json()['_pagination'].get('total_pages')
    filelist = []
    for n in range(1, pages+1):
        for x in range(len(record.get_filelist(per_page = 100, page=n).json().get('items'))):
            file_name = record.get_filelist(per_page = 100, page=n).json().get('items')[x]['name']
            filelist.append(file_name)
    return filelist

def Latest_Title(instance:str, record_type:str, collection=None, collection_id=None, keywords=None):
    # Suggests a title based on the latest title before
    if collection != None:
        collection_id = Search_Item_ID(instance=instance, title=collection, item='collection')
    
    record_list = Search_Item_Titles(instance=instance, item='record',collection_id=collection_id, record_type=record_type, keywords=keywords)
    record_numbers=[]
    for record in record_list:
        number = int(re.findall('#[0-9]{4}',record)[0].replace('#','').lstrip('0'))
        record_numbers.append(number)
    if record_numbers != []:
        record_max_number = str(max(record_numbers))
        for record in record_list:
            if record[-4:] == record_max_number.zfill(4):
                record_name = record
        
        return record_name

def Suggest_Title(instance:str, record_type:str, collection=None, collection_id=None, keywords=None):
    if collection != None:
        collection_id = Search_Item_ID(instance=instance, title=collection, item='collection')
        
    latest_title = Latest_Title(instance=instance, collection_id=collection_id, record_type=record_type)
    if latest_title != "":
        record_number = str(int(latest_title[-4:].strip('0'))+1).zfill(4)
        suggested_title = latest_title[:-4] + record_number
    
        return suggested_title