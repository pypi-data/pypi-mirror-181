from kadi_apy import KadiManager
import uuid


def Template_Create(data, title, instance=None,host=None, pat=None, group_id=None):
    template_name = []
    template_name_words = title.split(' ')[:2]
    template_name = '-'.join((template_name_word[:3] for template_name_word in template_name_words))
    template_name = template_name + '-'
    
    template = KadiManager(instance=instance, host=host, token=pat).template(title=title,identifier=(template_name+str(uuid.uuid4())),type='record', data=data, create=True)
    template.add_group_role(group_id=group_id, role_name='editor')