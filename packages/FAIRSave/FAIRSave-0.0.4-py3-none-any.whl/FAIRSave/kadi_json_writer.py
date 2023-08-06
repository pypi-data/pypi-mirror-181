import ast


# Create_list_from_dict is a function that converts a json to the Kadi4Mat json style
# which doesn't consist of key-value pairs rather than of lists with three to four
# dict items with keys: key, type, value and sometimes unit.
# Example:
# {"Name": "Max Mustermann"} converts to {"key":"Name","type":"string","value":"Max Mustermann"}

# Function to create a list from a dict. The functions calls others
# functions to convert the items in the dict by their type
def create_list_from_dict(key, value):
    """Create a list of dicts from a dict

    :param key: Key of a dict item.
    :param value: Value of a dict item.
    :return: dict_for_list
    :rtype: dict
    """
    dict_for_list = {'key':key, 'type':type(value).__name__, 'value':[]}
    for j in value.keys():
        # Float with unit is a dict that needs to be a dict with the unit as string in it
        if isinstance(value.get(j), dict) and word_in_list('@unit',list(value.get(j).keys())):
            attr = {'unit':value.get(j).get('@unit')}
            dict_for_list['value'].append(create_dict_from_element(j,value.get(j).get('#text'),attr))
            if dict_for_list['value'][-1] == None:
                dict_for_list['value'].pop(-1)
        elif isinstance(value.get(j), dict) and word_in_list('@id',list(value.get(j).keys())):
            dict_for_list['value'].append(create_list_from_list(j,value.get(j)))
        elif isinstance(value.get(j), dict):
            dict_for_list['value'].append(create_list_from_dict(j,value.get(j)))
        elif isinstance(value.get(j), list):
            dict_for_list['value'].append(create_list_from_list(j,value.get(j)))
        else:
            if type(value.get(j)).__name__ == 'NoneType':
                continue
            else:
                dict_for_list['value'].append(create_dict_from_element(j,value.get(j),{}))
    return dict_for_list

# Function to determine if @unit is an attribute of an json string
def word_in_list(word, list):
    """Looks for word in list
    :param word: Word that should be in list.
    :param list: List to look for the word.
    :return: True
    :rtype: bool
    """
    if word in list:
        return True

# Function to create a dict out of strings, integers and floats
def create_dict_from_element(key,value,attr):
    """ Create dict from element

    Kadi4Mat needs
    {'dict_key': 'dict_value'} to be in the following from:
    {'key':'dict_key', 'type': 'type_of_dict_value', 'value': 'dict_value'}

    :param key: dict_key from example. The key of the dict to be converted
    :param value: dict_value from example. The value of the dict to be converted
    :param attr: info about the attribute 'unit'
    :return: dict_of_element
    :rtype: dict
    """
    if bool(list(attr.keys())) is True:
        if  isinstance(ast.literal_eval(value), int):
            if value == '0' and (key == 'Relative_Starting_Position_Setpoint' or key == 'Targeted_Normal_Load'):
                pass
            else:
                dict_of_element = {'key':key, 'type':type(ast.literal_eval(value)).__name__, list(attr.keys())[0]: attr.get('unit'),'value':int(value)}
                return dict_of_element
        else:
            dict_of_element = {'key':key, 'type':type(ast.literal_eval(value)).__name__, list(attr.keys())[0]: attr.get('unit'),'value':float(value)}
            return dict_of_element
    elif key == 'Setup_Starting_Time' or key == 'Experiment_Starting_Time' or key == 'Experiment_Ending_Time':
        dict_of_element = {'key':key, 'type':'date','value':value}
        return dict_of_element
    else:
        # Floor and Room need to be str
        if key == 'Room' or key == 'Floor':
            value = str(value)
        elif key == 'Targeted Normal Load':
            value = round(float(value),5)
        # Only the ID is interesting
        elif key == 'Specimen_ID':
            value = value.split().pop(-1)
        elif key == 'Starting Position' or key == 'Relative Transverse Position' or key == 'Target Controlled Humidity':
            value = round(float(value),5)
        elif value.isdigit() == True and isinstance(ast.literal_eval(value), int):
            value = int(value)
        elif value.isdigit() == True and isinstance(ast.literal_eval(value), float):
            value = float(value)
        dict_of_element = {'key':key, 'type':type(value).__name__,'value':value}
        return dict_of_element

# Function to create a list out of a list
def create_list_from_list(key,value):
    """Create a dict from a list with a list in it

    :param key: 
    :param value: List to look for the word.
    :return: dict_for_list
    :rtype: dict
    """
    if isinstance(value, list):
        dict_for_list = {'key':key, 'type':type(value).__name__,'value':[]}
        for k in value:
            k.pop('@id')
            dict_list = []
            for m in k.keys():
                if type(k.get(m)).__name__ =='dict' and word_in_list('@unit',list(k.get(m).keys())):
                    attr = {'unit':k.get(m).get('@unit')}
                    dict_list.append(create_dict_from_element(m,k.get(m).get('#text'),attr))
                elif type(k.get(m)).__name__ =='dict':
                    dict_list.append(create_list_from_dict(m,k.get(m).get('#text')))
                elif isinstance(k.get(m), list):
                    dict_list.append(create_list_from_list(m,k.get(m)))
                else:
                    if type(k.get(m)).__name__ == 'NoneType':
                        continue
                    else:
                        dict_list.append(create_dict_from_element(m,k.get(m),{}))
            dict_for_list['value'].append({'type':'dict', 'value':dict_list})
    # List with only one element is not detected as list
    else:
        dict_for_list = {'key':key, 'type':'list', 'value':[]}
        id = value.pop('@id')
        dict_list = []
        for m in value.keys():
            if type(value.get(m)).__name__ == 'dict' and word_in_list('@unit',list(value.get(m).keys())):
                attr = {'unit':value.get(m).get('@unit')}
                dict_list.append(create_dict_from_element(m,value.get(m).get('#text'),attr))
            elif type(value.get(m)).__name__ =='dict':
                dict_list.append(create_list_from_dict(m,value.get(m).get('#text')))
            elif isinstance(value.get(m), list):
                dict_list.append(create_list_from_list(m,value.get(m)))
            else:
                if type(value.get(m)).__name__ == 'NoneType':
                    continue
                else:
                    dict_list.append(create_dict_from_element(m,value.get(m),{}))
        dict_for_list['value'].append({'type':'dict', 'value':dict_list})

    return dict_for_list