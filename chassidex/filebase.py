import os
import json


this_folder = os.path.dirname(os.path.abspath(__file__))    # __file__ refers to the location of this python script

# Function to add a new entry to the database, every time the form is filled
def add(entry):
    data_folder=os.path.join(this_folder,'data')            # Providing path to data folder
    folders=[int(i) for i in os.listdir(data_folder)]       # A list of the names of the data folders
    new_id=max(folders)+1                                   # Marks the new id for the incoming data entry
    os.mkdir(os.path.join(data_folder,str(new_id)))
    entry['index']=new_id                                   # Entry is a dictionary datatype, setting index to new_id
    path=os.path.join(data_folder,str(new_id))
    with open(os.path.join(path,'v1.json'),'w') as f:
        f.write(json.dumps(entry))                          # Entry dict converted to json and dumped into v1.json
        f.close()
# Index file contains the index and the species,genus and strain of the organism
    with open(os.path.join(this_folder,'index_file.txt'),'a') as f:
        f.write(str(new_id)+'\n')
        f.close()
    with open(os.path.join(this_folder,'index_file.txt'),'a') as f:
        f.write(' '.join([entry['genus'],entry['species'],entry['strain']])+'\n')
        f.close()
    return(entry['index'])

# Every time the already added entry is edited, this functions updates the entry
def update(entry):
    data_folder=os.path.join(this_folder,'data')
    path=os.path.join(data_folder,str(entry['index']))
    version='v'+str(len(os.listdir(path))+1)+'.json'        # Existing file name 'v''+ 1''.json'
    with open(os.path.join(path,version),'w+') as f:        # w+ used for writing and reading
        f.write(json.dumps(entry))
        f.close()
    lines=list()
    with open(os.path.join(this_folder,'index_file.txt'),'r') as f:
        lines=f.readlines()
        for i in range(len(lines)):
            if lines[i].startswith(str(entry['index'])):
                lines[i+1]=(' '.join([entry['genus'],entry['species'],entry['strain']])+'\n')   # Changes to index file entry
        f.close()

    with open(os.path.join(this_folder,'index_file.txt'),'w') as f:
        f.write(''.join(lines))                             # Writing changes to index file
        f.close()

def get_data(index):
    data_folder=os.path.join(this_folder,'data')
    path=os.path.join(data_folder,str(index))
    version='v'+str(len(os.listdir(path)))+'.json'          # Returns only the latest entry, len(os.listdir(path)) gives the value of the latest version
    with open(os.path.join(path,version)) as f:
         data=json.loads(f.read())
         data['index'] = index
    return(data)
# Function to return entire index file
def get_full_index():
    with open(os.path.join(this_folder,'index_file.txt')) as f:
        data = f.readlines()
        index = []
        for i in range(0,len(data),2):                      # Steps as two as file has index on one line and the organism name on the next line
            index.append(data[i+1][:-1])                    # -1 to exclude the trailing \n
        f.close()
        return index
# Addind data collected from the form data
def store_data_add(form_data):
    data = {}

    data['genus'] = form_data['genus']
    data['species'] = form_data['species']
    data['strain'] = form_data['strain']
    data['tax_id'] = form_data['tax_id']

    data['safety_level'] = form_data['safety_level']
    data['safety_level_ref'] = form_data['safety_level_ref']

    data['description'] = form_data['description']
    i = 0                                                       # Iterating over all the description references from the form
    data['description_refs'] = []
    while('description_ref'+str(i) in form_data.keys()):
        data['description_refs'].append(form_data['description_ref'+str(i)])
        i = i + 1

    data['genotype'] = form_data['genotype']
    data['genotype_description'] = form_data['genotype_description']
    i = 0
    data['genotype_refs'] = []
    while('genotype_ref'+str(i) in form_data.keys()):
        data['genotype_refs'].append(form_data['genotype_ref'+str(i)])
        i = i + 1

    data['growth'] = form_data['growth']
    i = 0
    data['growth_refs'] = []
    while('growth_ref'+str(i) in form_data.keys()):
        data['growth_refs'].append(form_data['growth_ref'+str(i)])
        i = i + 1

    i = 0
    data['culture_sources'] = []
    while('culture_source'+str(i) in form_data.keys()):
        data['culture_sources'].append([form_data['culture_source'+str(i)],form_data['culture_source_ref'+str(i)]])
        i = i + 1

    i = 0
    data['maintenance_protocols'] = []
    while('maintenance_protocol'+str(i) in form_data.keys()):
        data['maintenance_protocols'].append([form_data['maintenance_protocol'+str(i)],form_data['maintenance_protocol_ref'+str(i)]])
        i = i + 1

    i = 0
    data['transformation_protocols'] = []
    while('transformation_protocol'+str(i) in form_data.keys()):
        data['transformation_protocols'].append([form_data['transformation_protocol'+str(i)],form_data['transformation_protocol_ref'+str(i)]])
        i = i + 1

    i = 0
    data['other_protocols'] = []
    while('other_protocol'+str(i) in form_data.keys()):
        data['other_protocols'].append([form_data['other_protocol'+str(i)],form_data['other_protocol_ref'+str(i)]])
        i = i + 1

    i = 0
    data['biobrick_parts'] = []
    while('biobrick_part'+str(i) in form_data.keys()):
        data['biobrick_parts'].append([form_data['biobrick_part'+str(i)],form_data['biobrick_part_ref'+str(i)]])
        i = i + 1

    i = 0
    data['vectors'] = []
    while('vector'+str(i) in form_data.keys()):
        data['vectors'].append([form_data['vector'+str(i)],form_data['vector_ref'+str(i)]])
        i = i + 1

    i = 0
    data['metabolic_models'] = []
    while('metabolic_model'+str(i) in form_data.keys()):
        data['metabolic_models'].append([form_data['metabolic_model'+str(i)],form_data['metabolic_model_ref'+str(i)]])
        i = i + 1

    data['genome_sequence'] = form_data['genome_sequence']

    data['contributor_name'] = form_data['contributor_name']
    data['contributor_designation'] = form_data['contributor_designation']
    data['contributor_affiliation'] = form_data['contributor_affiliation']
    data['contributor_email'] = form_data['contributor_email']
    return add(data)                    # Finally adding the data from the form data
# Adding data collected from the edited form
def store_data_update(form_data):
    data = {}

    data['index'] = form_data['index']
    data['genus'] = form_data['genus']
    data['species'] = form_data['species']
    data['strain'] = form_data['strain']
    data['tax_id'] = form_data['tax_id']

    data['safety_level'] = form_data['safety_level']
    data['safety_level_ref'] = form_data['safety_level_ref']

    data['description'] = form_data['description']
    i = 0
    data['description_refs'] = []
    while('description_ref'+str(i) in form_data.keys()):
        data['description_refs'].append(form_data['description_ref'+str(i)])
        i = i + 1

    data['genotype'] = form_data['genotype']
    data['genotype_description'] = form_data['genotype_description']
    i = 0
    data['genotype_refs'] = []
    while('genotype_ref'+str(i) in form_data.keys()):
        data['genotype_refs'].append(form_data['genotype_ref'+str(i)])
        i = i + 1

    data['growth'] = form_data['growth']
    i = 0
    data['growth_refs'] = []
    while('growth_ref'+str(i) in form_data.keys()):
        data['growth_refs'].append(form_data['growth_ref'+str(i)])
        i = i + 1

    i = 0
    data['culture_sources'] = []
    while('culture_source'+str(i) in form_data.keys()):
        data['culture_sources'].append([form_data['culture_source'+str(i)],form_data['culture_source_ref'+str(i)]])
        i = i + 1

    i = 0
    data['maintenance_protocols'] = []
    while('maintenance_protocol'+str(i) in form_data.keys()):
        data['maintenance_protocols'].append([form_data['maintenance_protocol'+str(i)],form_data['maintenance_protocol_ref'+str(i)]])
        i = i + 1

    i = 0
    data['transformation_protocols'] = []
    while('transformation_protocol'+str(i) in form_data.keys()):
        data['transformation_protocols'].append([form_data['transformation_protocol'+str(i)],form_data['transformation_protocol_ref'+str(i)]])
        i = i + 1

    i = 0
    data['other_protocols'] = []
    while('other_protocol'+str(i) in form_data.keys()):
        data['other_protocols'].append([form_data['other_protocol'+str(i)],form_data['other_protocol_ref'+str(i)]])
        i = i + 1

    i = 0
    data['biobrick_parts'] = []
    while('biobrick_part'+str(i) in form_data.keys()):
        data['biobrick_parts'].append([form_data['biobrick_part'+str(i)],form_data['biobrick_part_ref'+str(i)]])
        i = i + 1

    i = 0
    data['vectors'] = []
    while('vector'+str(i) in form_data.keys()):
        data['vectors'].append([form_data['vector'+str(i)],form_data['vector_ref'+str(i)]])
        i = i + 1

    i = 0
    data['metabolic_models'] = []
    while('metabolic_model'+str(i) in form_data.keys()):
        data['metabolic_models'].append([form_data['metabolic_model'+str(i)],form_data['metabolic_model_ref'+str(i)]])
        i = i + 1

    data['genome_sequence'] = form_data['genome_sequence']

    data['contributor_name'] = form_data['contributor_name']
    data['contributor_designation'] = form_data['contributor_designation']
    data['contributor_affiliation'] = form_data['contributor_affiliation']
    data['contributor_email'] = form_data['contributor_email']

    update(data)        # Finally updating the data from the edited form data
