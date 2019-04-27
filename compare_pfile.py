##from dictdiffer import diff, patch, swap, revert
#!/Library/Frameworks/Python.framework/Versions/3.6/bin
'''
 utility to compare oracle pfiles source against a target and generate output in csv
 The first output is where the parameters are identical
 The second is where the parameters from source are not in the target so they are exceptions
'''
#target_list=()
gold_dir = "/Users/pmistry/PycharmProjects/test1/"
gold_file = "initowb11g.ora"

target_dir = "/Users/pmistry/PycharmProjects/test1/"
target_file = "inittemplat1.ora"
target_list = ('inittemplat1.ora','inittemplat1.ora')

exclusion_list = ('audit_file_dest','control_files','db_create_file_dest','db_recovery_file_dest',
                  'diagnostic_dest','dispatchers','local_listener','remote_login_passwordfile',
                  'log_archive_format','db_domain')
inclusion_list = ('db_name','db_unique_name','pga_aggregate_target')
source_dict = {}
target_dict = {}
output_list = []

''' Extracts the contents of a file into a python dictionary '''
def extract_pfile(file_name):
    h_file = open(file_name, "r")
    if h_file.readable():
        ln_counter = 0
        my_dict={}
        for rec in h_file:
            #print(rec)
            delme_key = rec.rsplit(".", -1)[1].rsplit("=", -1)[0]
            if "__" not in rec and "control_files" not in rec and delme_key not in exclusion_list:
                #print(delme_key)
                # additionally removes new line character
                delme_value = rec.rsplit(".", -1)[1].rsplit("=", -1)[1].rstrip().strip("'")
                #print(delme_key + " " + delme_value)
                my_dict[delme_key] = delme_value
        return my_dict
    else:
        print("invalid file")
    h_file.close()


''' compare where the keys are the same '''
def comparison(my_source_dict, my_target_dict):
    #print(my_source_dict)
    #print(my_target_dict)
    my_output_list=[]
    my_output="KEY,SRC,TGT,DETAIL"
    my_output_list.append(my_output)
    my_source_dict = inclusion_parameters(my_source_dict)
    #print(my_source_dict)
    for my_source_rec in sorted(my_source_dict):
        my_output = str(my_source_rec) + "," + str(my_source_dict[my_source_rec])
        if my_source_rec in sorted(my_target_dict):
            my_output = my_output + "," + str(my_target_dict[my_source_rec]) + ","
            #print(my_output)
            my_output_list.append(my_output)
        else:
            #print(my_output + ", , UNMATCHED")
            my_output_list.append(my_output)
    return (my_source_dict,my_output_list)



''' Adds in mandatory parameters from the inclusion_list to source dict aids final output '''
def inclusion_parameters(my_source_dict):
    #print(my_source_dict)
    for my_inclusion_rec in sorted(inclusion_list):
        if my_inclusion_rec not in my_source_dict:
            my_source_dict[my_inclusion_rec] = ""
    #print(my_source_dict)
    return my_source_dict

''' keys in target but in the source, displayed as exceptions '''
def reverse_comparison(my_source_dict, my_target_dict,my_output_list):
    my_output = "EXCEPTIONS,SRC,TGT,DETAIL"
    #my_output_list.append(my_output)
    for my_target_rec in sorted(my_target_dict):
        if my_target_rec not in sorted(my_source_dict):
            my_output = str(my_target_rec) + "," + "-," + str(my_target_rec) + "=" + str(my_target_dict[my_target_rec]) + ", EXCEPTIOn"
            my_output_list.append(my_output)
    return my_output_list

def generate_csv_output(output_list,target_file):
    print()
    print(target_file)
    for rec in output_list:
        print(rec)

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


''' Compare source against one target '''
compare_with_single_target_in_same_directory(source_dict,target_dir,target_file)

''' This is used if multiple targets are used '''
#compare_with_multiple_targets_in_same_directory(source_dict,target_dir,target_list)

print(" --- completed ---")




