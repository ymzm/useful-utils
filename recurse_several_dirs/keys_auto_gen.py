#!/usr/bin/python
import os
import sys
import re
import getopt

param_config = {
"NoLog":0,
"Directory":'',
}

# should be provided by operating system
white_list_paths = [
"/usr/bin",
"/bin",
"/usr/lib",
"/lib",
"/lib64",
"/usr/sbin",
]

ignore_path_table = [
"/dev",
#"/usr/src",
]

ignore_suffix_table = [
"\.c",
#"\.h",
"\.txt",
]

exec_table = []
script_table = []
lib_table = []
unknown_table = []

elfmsgstr = ['\x7f', '\x45', '\x4c', '\x46', '\x01', '\x01','\x01','\x00','\x00','\x00','\x00','\x00','\x00','\x00','\x00','\x00','\x00']
# assume that file is exec or library
def elf_type_get_append(file):
    elf_f = open(file, 'r')
    content = elf_f.read(100)
    if content is None:
        return
    else:
        if (len(content) <= 17):    
            unknown_table.append(file)
            return
        for i in range(4):
            if content[i] != elfmsgstr[i]:
                #print (content[i] + '!=' + elfmsgstr[i])
                #print ("Unknown "+ file)
                unknown_table.append(file)
                return
	if content[16] == '\x02':
            exec_table.append(file)
	elif (content[16]) > '\x00' and (content[16]) < '\x05':
            lib_table.append(file)
	else:
            for i in range(17):
                #print("unknown ELF" + file)
                unknown_table.append(file)
    return


def recurse_dir (path, f):
    files = os.listdir(path)
    for file in files:
        file = os.path.realpath(os.path.join(path, file))
#        print(type(i))
        if file == os.path.realpath(path):
            continue
        continue_flag = 0
        for ignore_path in ignore_path_table:
            if continue_flag == 1:
                break
            if not re.match("^" + ignore_path + ".*", file) is None:
                continue_flag = 1
                continue
        if continue_flag == 1:
            continue
#        if not re.match("^/usr/src.*", file) is None:
#            continue
        if os.path.isdir(file):
            recurse_dir(file, f)
        if os.path.isfile(file):
            continue_flag = 0
            for ignore_suffix in ignore_suffix_table:
                if continue_flag == 1:
                    break
                if not re.match(".*" + ignore_suffix + "$", file) is None:
                    continue_flag = 1
                    continue
            if continue_flag == 1:
                continue

            
            if not re.match(".*\.py$", file) is None:
                script_table.append(re.match(".*\.py$", "".join(file)).group())
            elif not re.match(".*\.sh$", file) is None:
                script_table.append(re.match(".*\.sh$", "".join(file)).group())
            else:
                elf_type_get_append(file)         
#f.write(i + '\n')
            
def list_files(paths, f):
    for i in paths:
        recurse_dir(i, f)

optlist, args = getopt.getopt(sys.argv[1:],'ld:')
for option, value in optlist:
    if option in ["-l", "--nolog"]:
        param_config["NoLog"] = 1
    elif option in ["-d", "--Directory"]:
        param_config["Directory"] = value

#print ("nolog = %d path = %s", param_config["NoLog"], param_config["Directory"])

if param_config["Directory"] != '':
    white_list_paths.append(param_config["Directory"])

keys_filename = os.path.split(sys.path[0])[0] + "/keys"


keys_f = open(keys_filename, 'w+')

white_list_paths.sort();

list_files(white_list_paths, keys_f)

keys_f.write("[excutable]\n")
for i in exec_table:
    keys_f.write(i+"\n")

keys_f.write("[library]\n")
for i in lib_table:
    keys_f.write(i+"\n")

keys_f.write("[script]\n")
for i in script_table:
    keys_f.write(i+"\n")

keys_f.write("[unknown]\n")
for i in unknown_table:
    keys_f.write(i+"\n")



#print(elfmsgstr)
#for i in script_table:
#    print (i)

keys_f.close()
