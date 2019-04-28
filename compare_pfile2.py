##from dictdiffer import diff, patch, swap, revert
#/Library/Frameworks/Python.framework/Versions/3.6/bin
u'''
 This is version python2 compatible explicitly formated for unicode
 utility to compare oracle pfiles source against a target and generate output in csv
 The first output is where the parameters are identical
 The second is where the parameters from source are not in the target so they are exceptions
'''
from io import open
#target_list=()
gold_dir = u"/Users/pmistry/PycharmProjects/test1/"
gold_file = u"initowb11g.ora"

target_dir = u"/Users/pmistry/PycharmProjects/test1/"
target_file = u"inittemplat1.ora"
target_list = (u'inittemplat1.ora',u'inittemplat1.ora')

exclusion_list = (u'audit_file_dest',u'control_files',u'db_create_file_dest',u'db_recovery_file_dest',
                  u'diagnostic_dest',u'dispatchers',u'local_listener',u'remote_login_passwordfile',
                  u'log_archive_format',u'db_domain')
inclusion_list = (u'db_name',u'db_unique_name',u'pga_aggregate_target')
source_dict = {}
target_dict = {}
output_list = []

u''' Extracts the contents of a file into a python dictionary '''
def extract_pfile(file_name):
    h_file = open(file_name, u"r")
    if h_file.readable():
        ln_counter = 0
        my_dict={}
        for rec in h_file:
            #print(rec)
            delme_key = rec.rsplit(u".", -1)[1].rsplit(u"=", -1)[0]
            if u"__" not in rec and u"control_files" not in rec and delme_key not in exclusion_list:
                #print(delme_key)
                # additionally removes new line character
                delme_value = rec.rsplit(u".", -1)[1].rsplit(u"=", -1)[1].rstrip().strip(u"'")
                #print(delme_key + " " + delme_value)
                my_dict[delme_key] = delme_value
        return my_dict
    else:
        print u"invalid file"
    h_file.close()


u''' compare where the keys are the same '''
def comparison(my_source_dict, my_target_dict):
    #print(my_source_dict)
    #print(my_target_dict)
    my_output_list=[]
    my_output=u"KEY,SRC,TGT,DETAIL"
    my_output_list.append(my_output)
    my_source_dict = inclusion_parameters(my_source_dict)
    #print(my_source_dict)
    for my_source_rec in sorted(my_source_dict):
        my_output = unicode(my_source_rec) + u"," + unicode(my_source_dict[my_source_rec])
        if my_source_rec in sorted(my_target_dict):
            my_output = my_output + u"," + unicode(my_target_dict[my_source_rec]) + u","
            #print(my_output)
            my_output_list.append(my_output)
        else:
            #print(my_output + ", , UNMATCHED")
            my_output_list.append(my_output)
    return (my_source_dict,my_output_list)



u''' Adds in mandatory parameters from the inclusion_list to source dict aids final output '''
def inclusion_parameters(my_source_dict):
    #print(my_source_dict)
    for my_inclusion_rec in sorted(inclusion_list):
        if my_inclusion_rec not in my_source_dict:
            my_source_dict[my_inclusion_rec] = u""
    #print(my_source_dict)
    return my_source_dict

u''' keys in target but in the source, displayed as exceptions '''
def reverse_comparison(my_source_dict, my_target_dict,my_output_list):
    my_output = u"EXCEPTIONS,SRC,TGT,DETAIL"
    #my_output_list.append(my_output)
    for my_target_rec in sorted(my_target_dict):
        if my_target_rec not in sorted(my_source_dict):
            my_output = unicode(my_target_rec) + u"," + u"-," + unicode(my_target_rec) + u"=" + unicode(my_target_dict[my_target_rec]) + u", EXCEPTIOn"
            my_output_list.append(my_output)
    return my_output_list

def generate_csv_output(output_list,target_file):
    print
    print target_file
    for rec in output_list:
        print rec

def compare_with_multiple_targets_in_same_directory(source_dict,target_dir,target_list):
    for target_rec in target_list:
        target_dict = extract_pfile(target_dir + target_file)
        (source_dict,output_list) = comparison(source_dict, target_dict)
        #print(output_list)
        output_list = reverse_comparison(source_dict, target_dict,output_list)
        #print(output_list)
        generate_csv_output(output_list,target_file)

def compare_with_single_target_in_same_directory(source_dict,target_dir,target_file):
    target_dict = extract_pfile(target_dir + target_file)
    (source_dict,output_list) = comparison(source_dict, target_dict)
    #print(output_list)
    output_list = reverse_comparison(source_dict, target_dict,output_list)
    #print(output_list)
    generate_csv_output(output_list,target_file)


source_dict = extract_pfile(gold_dir + gold_file)
#print (source_dict)


u''' Compare source against one target '''
compare_with_single_target_in_same_directory(source_dict,target_dir,target_file)

u''' This is used if multiple targets are used '''
#compare_with_multiple_targets_in_same_directory(source_dict,target_dir,target_list)

print u" --- completed ---"




