import yaml
import json
import glob


def convert_type_string(string_in):
    if string_in == 'string':
        return 'str'
    # ???? Do we need that ????
    elif string_in == 'integer':
        return 'int'
    elif string_in == 'float':
        return 'flt'


def get_global_attribute_and_type(ipath, status):
    # Load types
    ifile_global_attr_type = glob.glob(ipath+'*types*')[0]
    with open(ifile_global_attr_type, 'rb') as json_file:
        types = json.load(json_file)['attribute_types']

    # Load global attributes bu status
    ifile_global_attr = glob.glob(ipath+'*'+status+'*')[0]
    with open(ifile_global_attr, 'rb') as json_file:
        attr_list = json.load(json_file)[status+'_global_attributes']
    attr_name_type = {}
    for attr in attr_list:
        attr_name_type[attr] = types[attr]
    return attr_name_type


def global_attribute_type_check(ipath, status):
    attr_and_type = get_global_attribute_and_type(ipath, status)
    # Write global attribute checks into a list
    check_list = []
    for attr in attr_and_type.keys():
        check = {'check_name': 'atmodat_checklib.register.GlobalAttrTypeCheck',
                 'check_id': attr.lower() + '_attribute_type_check',
                 'parameters': {'attribute': attr, 'type': convert_type_string(attr_and_type[attr]),
                                'status': 'mandatory'}}
        check_list.append(check)
    return check_list


def global_attribute_cv_check(ipath, status):
    attr_and_type = get_global_attribute_and_type(ipath, status)
    json_list = glob.glob(ipath+'*.json')
    check_list = []
    for attr in attr_and_type.keys():
        if attr+'.json' in str(json_list):
            check = {'check_name': 'atmodat_checklib.register.GlobalAttrVocabCheckByStatus',
                     'check_id': attr.lower() + '_attribute_CV_check',
                     'parameters': {'attribute': attr, 'vocab_lookup': 'label', 'vocabulary_ref': 'atmodat:atmodat',
                                    'status': 'required'}}
            check_list.append(check)
    return check_list


def create_yaml_checksuit(ipath, status=None, version=None):
    # Global attribute type checks
    check_list_type_check = global_attribute_type_check(ipath, status)
    check_list_cv_check = global_attribute_cv_check(ipath, status)
    check_list = check_list_type_check + check_list_cv_check
    # Write checks to yaml
    suite_string = 'atmodat_standard_checker_'+status
    with open(suite_string+'.yml', 'w') as ofile:
        yaml.dump(dict(suite_name=suite_string+':'+version), ofile)
        yaml.dump(dict(checks=check_list), ofile, default_flow_style=False)


json_path = 'AtMoDat_CV_json/'
create_yaml_checksuit(json_path, status='mandatory', version='1.0')
create_yaml_checksuit(json_path, status='recommended', version='1.0')

exit()
