'''
delete_duplicated_wps_addons.py
删除wps过时的插件
对比版本号: https://geek-docs.com/python/python-ask-answer/96_python_how_do_i_compare_version_numbers_in_python.html
'''

import os
import sys

def get_newest_addon(filename_list):
    if len(filename_list)==0:
        raise Exception('get_newest_addon(filename_list): filename_list is empty')
    main_name = filename_list[0][:filename_list[0].rfind('_')]
    result = filename_list[0]
    try:
        for filename in filename_list:
            v1 = list(map(int, result[result.rfind('_')+1:].split(".")))
            v2 = list(map(int, filename[filename.rfind('_')+1:].split(".")))
            if v1>=v2:
                continue
            else:
                result = filename
    except Exception as e:
        print('------->' + result + '<------------')
        print(e)
    return result

if not sys.platform.startswith('win'):
    print('Only running on windows system')
    sys.exit(1)

path = os.path.join(os.environ.get('APPDATA'), 'kingsoft','wps','addons','pool','win-i386')
print('scanning path is:', path)
if not os.path.exists(path):
    print('path is not exist.')
    sys.exit(1)
filenames = os.listdir(path)
filenames = [ filename for filename in filenames if os.path.isdir(path+os.sep+filename) ]

main_names = list(set([ filename[:filename.rfind('_')] for filename in filenames]))

newest_addon_list = [ get_newest_addon([filename for filename in filenames if filename.startswith(main_name+'_')]) for main_name in main_names ]

for filename in filenames:
    #print(filename)
    main_name = filename[:filename.rfind('_')]
    if filename not in newest_addon_list:
        print('========================')
        print('非最新版本:', filename)
        print('其它版本文件包括：')
        print([ oth_file for oth_file in filenames if oth_file.startswith(main_name+'_')])
        print('其中最新版本为：', [ n_file for n_file in newest_addon_list if n_file.startswith(main_name+'_')])
        print('删除' + filename + '...')
        os.system('rd /s /q ' + path + os.sep + filename)
