from kadi_apy.globals import CONFIG_PATH
import configparser
import os


def Show_Kadi_Instances():
    """_summary_

    Raises:
        KadiAPYConfigurationError: No config file was found.

    Returns:
        list: Instances saved in config file
    """
    # Config_path from https://gitlab.com/iam-cms/kadi-apy/-/blob/develop/kadi_apy/globals.py
    # CONFIG_PATH = Path.home().joinpath(".kadiconfig")        

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    instances = config.sections()
    instances.pop(0) # pop global instance
    instances.pop(0) # pop my_kadi_instance
    
    return instances

def Create_Kadi_Instance(instance:str, host:str, pat:str):
    """Creates a config file if not existing and creates an instance in the config file

    Args:
        instance (str): Name of the instance to be created
        host (str): fully qualified domain name of the Kadi4Mat instance
        pat (str): personal access token (PAT)
    """
    if not os.path.isfile(CONFIG_PATH):
        os.system('cmd /c "kadi-apy config create"')        

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    # config.remove_section("my_kadi_instance")
    # config.sections().remove('my_kadi_instance')
    config.add_section(instance)
    config.set(instance, 'host', host)
    config.set(instance, 'pat', pat)
    with open(CONFIG_PATH, 'w+') as configfile:
        config.write(configfile)
