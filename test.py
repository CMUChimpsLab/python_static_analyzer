from androguard.core.bytecodes import apk
import xmltodict
import collections
import pprint

pp = pprint.PrettyPrinter(indent=4, width = 1)
a = [1,2,3,4,5]
pp.pprint(a)

temp_apk = "/home/alexyu0/new_pipeline/temp/2cabd12eb48647fda748ca68117ccf79"
a = apk.APK(temp_apk, zipmodule=1)

print a.get_androidversion_code()
print a.get_androidversion_name()
print a.get_package()
print a.get_filename()
d = xmltodict.parse(a.get_AndroidManifest().toxml())

def convert_to_dict(ordered_dict):
    ordered_dict = dict(ordered_dict)
    for key in ordered_dict:
        if type(ordered_dict[key]) == collections.OrderedDict:
            ordered_dict[key] = convert_to_dict(ordered_dict[key])
        elif type(ordered_dict[key]) == list:
            dicts = []
            for item in ordered_dict[key]:
                if type(item) == collections.OrderedDict:
                    dicts.append(convert_to_dict(item))
            ordered_dict[key] = dicts
    return ordered_dict

pp.pprint(convert_to_dict(d))