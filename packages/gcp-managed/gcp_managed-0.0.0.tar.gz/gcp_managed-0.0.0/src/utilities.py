
def clear_rules(stream_obj):
    for rules_list in stream_obj:
        rule_ids = [rule.id for rule in rules_list]
        if rule_ids:
            stream_obj.delete_rules()
        break


def load_keys(path):
    keys_dict = {}
    with open(path, 'r') as keys:
        keys_lines = keys.readlines()
    for keys_line in keys_lines:
        lst = keys_line.split('=')
        keys_dict[lst[0].strip()] = lst[1].strip()
    return keys_dict
