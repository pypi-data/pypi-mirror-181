from kadi_apy import KadiManager
import uuid
from datetime import datetime
import os
from genericpath import isdir, isfile
import shutil
from FAIRSave.kadi_search import *
import requests
import json
import rstr         ####### License: BSD License


def Record_Create(instance:str, record_name:str, top_level_term:str, Gitlab_PAT:str):
    """Create a record in Kadi4Mat.

    Args:
        instance (str): The name of the instance to use in combination with a config file.
        record_name (str): Name of the record.
        top_level_term (str): Top Level term of the vocabulary.
        GITLAB_PAT (str): Personal access token to Gitlab.
    """

    project_id = 41732562

    # Search in Gitlab for top-level term ID of vocabulary
    # private token or personal token authentication (GitLab.com)
    # issues_ep = "/projects/41732562/issues"

    issues_ep = f"projects/{project_id}/issues"
    params = {'private_token': Gitlab_PAT,
              'scope': 'all',
              'order_by': 'created_at',
              'sort': 'desc',
              'per_page': 100,
              'search': top_level_term}
    # get all repository issues
    issues_response = requests.get(f"https://gitlab.com/api/v4/{issues_ep}",
                                    params=params)
    issues_dict_list = issues_response.json()
    
    # handle pagination
    for page in range(2, 1 + int(issues_response.headers.get('X-Total-Pages',0))):
        params['page'] = page
        next_page = requests.get(f"https://gitlab.com/api/v4/{issues_ep}",
                                    params=params)
        issues_dict_list += next_page.json()

    for issue in issues_dict_list:
        title = issue['title']
        label = title.split(' | ')[0].split('] ')[1]
        if top_level_term == label:
            global_t_id = title.split(' | ')[1]
            break


    repo_tree_ep = f"projects/{project_id}/repository/tree"
    params = {'private_token': Gitlab_PAT,
              'path': 'approved_terms',
              'per_page': 100,
              'ref': 'main'}

    repo_files = []
    repo_files_response = requests.get(f"https://gitlab.com/api/v4/{repo_tree_ep}",
                                    params=params)

    repo_files += repo_files_response.json()

    # handle pagination
    if 'rel="next"' in repo_files_response.headers['Link']:
        more_pages_left = True
    else:
        more_pages_left = False

    while more_pages_left:
        # get all pagination links
        pagination_links = (repo_files_response.headers['Link']
                            .split(', '))
        # get the link to the next page
        next_page_link = [x
                          for x in pagination_links
                          if 'rel="next"' in x][0]
        # strip 'rel="next"'
        next_page_link = next_page_link.split(';')[0]
        # remove leading < and trailing >
        next_page_link = next_page_link[1:-1]
        repo_files_response = requests.get(next_page_link, params=params)
        repo_files += repo_files_response.json()

        # breaking condition
        if any([f'{global_t_id}.json' == x['name'] for x in repo_files]):
            more_pages_left = False
        elif 'rel="next"' in repo_files_response.headers['Link']:
            more_pages_left = True
        else:
            more_pages_left = False

    file_dict = [x for x in repo_files if x['name'] == f'{global_t_id}.json'][0]
    file_path = file_dict['path'].replace('approved_terms/', 'approved_terms%2F').replace('.json', '%2Ejson')
    file_ep = f"projects/{project_id}/repository/files/{file_path}/raw"
    params = {'private_token': Gitlab_PAT,
              'ref': 'main'}
    file = requests.get(f"https://gitlab.com/api/v4/{file_ep}",
                                    params=params)
    metadata = file.json().get('metadata')
    id_t_local = metadata.get('id_t_local')
        
    # Access Manager with Configuration Instance
    manager = KadiManager(instance = instance)

    ## Create a record for the processed data in Kadi4Mat

    # Basic info for the new record
    title = record_name
    
    # Create identifier from local_id and unique identifier for external applications
    unique_identifier = rstr.xeger(r'[a-z0-9]{5}')
    identifier = id_t_local + '-' + unique_identifier + '-kitmt'

    # Search identifiers in Kadi4Mat to check new identifiers uniqueness
    search_results = (manager.search_resource().search_items(item='record',
                                        identifier=identifier,
                                        per_page =100))
    pages = search_results.json()['_pagination'].get('total_pages')

    identifier_list = []
    for page in range(1,pages+1):
        results = manager.search_resource().search_items( item='record',
                                                    identifier=identifier,
                                                    per_page =100, page=page).json().get('items')
        for record in results:
            identifier_list.append(record.get('identifier'))
    
    #Check if identifier is unique
    identifier_uniqueness = False
    while identifier_uniqueness == False:
        for existing_identifier in identifier_list:
            if identifier[-11:] != existing_identifier[-11:]:
                identifier_uniqueness = True
            elif identifier[-11:] == existing_identifier[-11:]:
                print("not unique")
                unique_identifier = rstr.xeger(r'[a-z0-9]{5}')
                identifier = id_t_local + '-' + unique_identifier + '-kitmt'
                identifier_uniqueness = False
                break
        
    # This either gets an existing record or creates a new record if none with
    # the given identifier exists yet. If one exists, but we cannot access it,
    # an exception will be raised.
    record = manager.record(identifier=identifier, title=title, create=True)
    return record.id, identifier

def Record_Add_Links_and_Edit(instance:str, link_to, link_name:str, record_type=None, record=None, record_id=None, description=None):
    """Add links to a record and edit the metadata of the record.

    Args:
        instance (str): The name of the instance to use in combination with a config file.
        record_to_link (any): Name of the raw data record which the new record should be linked to.
        link_name (str): Name of the link.
        record(str, optional): Name of the record. Defaults to None.
        record_id (int, optional): ID of the record to edit. Defaults to None.
    """
    manager = KadiManager(instance=instance)
    # Get record ID if only name is given
    if record != None:
        record_id = Search_Item_ID(instance=instance, title=record, item='record')
    record = manager.record(id=record_id)
    
    # Get record ID from record to be linked
    if type(link_to) == 'int': 
        linked_record_id = link_to
    else:
        linked_record_id = Search_Item_ID(instance=instance, title=link_to, item='record')
    rd_record = manager.record(id=linked_record_id)

    # Add to collection
    collection_links = rd_record.get_collection_links().json()
    if collection_links.get('items') != []:
        for n in collection_links.get('items'):
            collection_id = n.get('id')
            record.add_collection_link(collection_id)
    # Add record link to experiment
    link_name = link_name
    record.link_record(linked_record_id, link_name)
    # Add the type of record
    record.edit(type=record_type)
    record.edit(visibilty=rd_record.meta.get('visibilty'))
    record.edit(license=rd_record.meta.get('license'))
    
    # Add description    #################################### TODO generalize ##############################################
    description_ontology= "TriboDataFAIR-Ontology"
    description_URL = "https://github.com/nick-garabedian/TriboDataFAIR-Ontology"
    description_commit = "ec2fb485b05d73013f8057f3853b4d92e42e2db3"
    description_class = "TribologicalExperiment"
    description_id = "TDO:0000001"
    description_onto_info = ("Record based on *" + description_ontology + 
                             "*\n\nURL: " + description_URL + 
                             " \n\nCommit: " + description_commit + 
                             " \n\nOntology Class Name: " + description_class + 
                             " \n\nOntology Persistent ID: " + description_id)
    if description != None:
        description_new = description + "\n\n" + description_onto_info
        record.edit(description=description_new)
    else:
        description_new = description_onto_info
        record.edit(description=description_new)
        
        
    # Add permissions to record
    for x in rd_record.get_groups().json().get('items'):
        group_id = x.get('group').get('id')
        group_role = x.get('role').get('name')
        record.add_group_role(group_id=group_id, role_name=group_role)
    
def Record_Add_Tags(instance:str, tags:str, record=None, record_id=None):
    """Add tags to a record.

    Args:
        instance (str): The name of the instance to use in combination with a config file.
        tags (str): Tags to add to a record.
        record(str, optional): Name of the record. Defaults to None.
        record_id (int, optional): ID of the record to edit. Defaults to None.
    """
    manager = KadiManager(instance = instance)
    if record != None:
        record_id = Search_Item_ID(instance=instance, title=record, item='record')
    record = manager.record(id=record_id)
    
    # Add tags to record
    tags = tags.replace(' ','').split(",")
    for tag in tags:
        record.add_tag(tag)

def Record_Add_Metadata(instance:str, record=None, record_id=None):
    """Add metadata to a record.

    Args:
        instance (str): The name of the instance to use in combination with a config file.
        record(str, optional): Name of the record. Defaults to None.
        record_id (int, optional): ID of the record to edit. Defaults to None.
    """
    manager = KadiManager(instance = instance)
    if record != None:
        record_id = Search_Item_ID(instance=instance, title=record, item='record')
    record = manager.record(id=record_id)
    
    # Read metadata from operator.txt file
    with open('FAIR_Save_helpers/operator.txt', 'r') as Record_info:
        """Reades info from file from LabView
        Line 1: Building
        Line 2: Floor
        Line 3: Room
        Line 4: Institution (Location)
        Line 5: Last Name
        Line 6: First Name
        Line 7: Institution
        Line 8: User Role
        Line 9: User Token
        Line 10: Matlab Version
        Line 11: Description
        Line 12: Tags for Kadi4Mat record
        """
        # Location
        building = Record_info.readline().replace('\n', '').replace('"','')
        floor = Record_info.readline().replace('\n', '').replace('"','')
        room = Record_info.readline().replace('\n', '').replace('"','')
        Institution_Location = Record_info.readline().replace('\n', '').replace('"','')
        # Operator
        last_name = Record_info.readline().replace('\n', '').replace('"','')
        first_name = Record_info.readline().replace('\n', '').replace('"','')
        institution = Record_info.readline().replace('\n', '').replace('"','')
        role = Record_info.readline().replace('\n', '').replace('"','')
        token = Record_info.readline().replace('\n', '').replace('"','')
        # Additional info
        version = Record_info.readline().replace('\n', '').replace('"','')
        
        
    # Add metadata to the record
    list_of_dict = [{'key': 'General Info', 'type': 'dict', 'value': [
                                {'key': 'Location', 'type': 'dict', 'value': [
                                    {'key': 'Building', 'type': 'str', 'value': building},
                                    {'key': 'Floor', 'type': 'str', 'value': floor},
                                    {'key': 'Room', 'type': 'str', 'value': room},
                                    {'key': 'Institution (Location)', 'type': 'str', 'value': Institution_Location}
                                    ]},
                                {'key': 'Operator(s) in Charge', 'type': 'dict', 'value': [
                                    {"key": "Last Name", "type": "str", "value": last_name},
                                    {"key": "First Name", "type": "str", "value": first_name},
                                    {'key': 'Institution Name', 'type': 'str', 'value': institution},
                                    {'key': 'User Role', 'type': 'str', 'value': role},
                                    {'key': 'User Token', 'type': 'str', 'value': token}]}, 
                                {'key': 'Timestamp', 'type': 'date', 'value': str(datetime.now()).replace(' ', 'T') + '+02:00'}
                                ]}, # TODO Software is not generalized
                            {'key': 'Array of Software Used', 'type': 'list', 'value': [
                                {'type': 'dict', 'value': [
                                    {'key': 'Software Name', 'type': 'str', 'value': 'MATLAB'},
                                    {'key': 'Software Version', 'type': 'str', 'value': version}
                                    ]}
                                ]}
                           ]
    record.add_metadata(list_of_dict, force=False)

def Record_Add_Files(instance:str, files_path:str, file_purpose:str, record=None, record_id=None):
    """Add Files to a record and add the metadata of the files to record extras.

    Args:
        instance (str): The name of the instance to use in combination with a config file.
        files_path (str): Path where the files to upload are stored.
        files_purpose (str): Purpose of the files that are uploaded.
        record(str, optional): Name of the record. Defaults to None.
        record_id (int, optional): ID of the record to edit. Defaults to None.
    """
    manager = KadiManager(instance = instance)
    if record != None:
        record_id = Search_Item_ID(instance=instance, title=record, item='record')
    record = manager.record(id=record_id)
    
    files_metadata = {'key': 'Array of Produced File Metadata', 'type': 'list',
            'value': []}
        
    file_id=[]
    if files_path != None:
        ## Add metadata from files
        for file in os.listdir(files_path):
            if isfile(files_path + '\\' + file):
                record.upload_file(files_path + '\\' + file, force=True)
                file_id = record.get_file_id(file)
                file_info = record.get_file_info(file_id).json()
                file_size = file_info.get('size')/1000 #size is given in bytes but displayed in kB
                file_MD = {'type': 'dict', 'value': [
                            {'key': 'File Persistent ID', 'type': 'str', 'value': file_id},
                            {'key': 'File Path', 'type': 'str', 'value': files_path + '/' + file},
                            {'key': 'File Name', 'type': 'str', 'value': file},
                            {'key': 'File Size', 'type': 'float', 'unit': 'kB', 'value': file_size},
                            {'key': 'File(s) Purpose', 'type': 'str', 'value': file_purpose}
                            ]}
                files_metadata['value'].append(file_MD)
            elif isdir(files_path + '\\' + file):
                zip_file = shutil.make_archive(files_path + '/' + file, 'zip', files_path + '/' + file, files_path)
                record.upload_file(zip_file, force=True)
                file_id = record.get_file_id(file + '.zip')
                file_info = record.get_file_info(file_id).json()
                file_MD = {'type': 'dict', 'value': [
                            {'key': 'File Persistent ID', 'type': 'str', 'value': file_id},
                            {'key': 'Number of Files', 'type': 'int', 'value': len(os.listdir(files_path + '\\' + file))},
                            {'key': 'File Path', 'type': 'str', 'value': str(zip_file)},
                            {'key': 'File Name', 'type': 'str', 'value': file + '.zip'},
                            {'key': 'File(s) Purpose', 'type': 'str', 'value': file_purpose}
                            ]}
                files_metadata['value'].append(file_MD)

    record.edit_file(file_id=file_id, description=files_metadata)
    
    
