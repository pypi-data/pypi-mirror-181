import pytd, tdclient 
import requests 
import json
import pandas as pd

#Create variables and objects needed by the Python functions
segment_params = [dict(src_table = ml_table['name'], attribute = col['name']) for col in ml_table['cols'] if col['build_segments'] == 'yes']
headers = {'Authorization': 'TD1 '+ td_api_key}
query_syntax = f"SELECT ps_id, v4_id, ps_name FROM {ps_stats_table} WHERE REGEXP_LIKE(ps_name, '{ps_name}') AND v5_flag = {v5_flag} LIMIT 1"

### Main Function that executes all sub-functions below
def main_function(database = database, query_syntax=query_syntax, headers=headers, segment_params=segment_params, ml_table=ml_table, main_id=main_id, rerun_ps=rerun_ps, segment_api=segment_api, ml_folder=ml_folder, sub_folder=sub_folder, attr_group=attr_group):

    #Extract ps_id
    ps_info = query(database, query_syntax)
    ps_id = ps_info.ps_id[0]
    v4_id = ps_info.v4_id[0]
    
    #Try to add attributes to PS
    print('------------- Add attriburtes to PS...')
    add_attribute_to_parent(v4_id, headers, database, ml_table, main_id, rerun_ps, segment_api, attr_group)
    
    #Try to Build Segment Folders
    print('------------- Create Audience Studio Folders...')
    ml_folders_created = create_ml_folders(ml_folder, sub_folder, ps_id, headers, segment_api)
    
    ###If new Folders were created, trigger automatic segment build next
    print('------------- Create Audiences in Audience Studio...')
    if ml_folders_created[0]:
        
      f_id = ml_folders_created[1]
      create_new_segments(f_id, sub_folder, segment_params, headers, segment_api)

    #Check if PS Re-build should be triggered
    print('------------- Check if PS re-run is required...')
    if rerun_ps=='yes':
        run_master = requests.post(f'{segment_api}/audiences/{v4_id}/run', headers=headers)
        if run_master.status_code == 200:
            print(f'Successfully triggered rerun of Master Segment: {ps_name}')
        else:
            print(run_master.json())

### Function to query tables from TD and output results as DF
def query(database, query_syntax):
    with tdclient.Client(apikey=td_api_key, endpoint=endpoint) as td:
        job = td.query(database, query_syntax, type='presto')
        job.wait()
        data = job.result()
        columns = [f[0] for f in job.result_schema]
        return pd.DataFrame(data, columns=columns)

### Function to add attributes to Parent Segment
def add_attribute_to_parent(v4_id, headers, database, ml_table, main_id, rerun_ps, segment_api, attr_group):
    
    #Extract current PS configuration
    parent = f'{segment_api}/audiences/{v4_id}'
    parent_all = requests.put(parent, headers=headers).json()
    parent_attr = parent_all['attributes']
    
    #Add new attributes to PS
    for col in ml_table['cols']:
        new_attr = dict(audienceId = str(v4_id), name = col['name'], type = col['type'], parentDatabaseName = database, 
                        parentTableName = ml_table['name'], parentColumn = col['name'], parentKey = ml_table['join_key'],
                       foreignKey = main_id, matrixColumnName = col['name'], groupingName = attr_group)

        parent_attr.append(new_attr)
        
    
    update_ms = requests.put(parent, headers=headers, json=parent_all)
    
    if update_ms.status_code == 200:
        print("Successfully added attribute to Parent Segment. Checking if segment rerun needed next...")
    else:
        try: 
            'not unique' in update_ms.json()['base'][0]
            print("Attributes already exist in Parent Segment")
        except:
            print(update_ms.json())
        
    return update_ms


### Function to create ML Folders in PS
def create_ml_folders(ml_folder, sub_folder, ps_id, headers, segment_api):
    #Generate Base ML Folder JSON
    base_folder = {'attributes': {'name': ml_folder, 
                             'description': 'ML Segments automatically created'},
             'relationships': {'parentFolder': {'data': {'id': str(ps_id), 'type': "folder-segment"}}}}
    
    #Try to create Base ML Folder and get folder_id to create sub-folder
    try: 
        audience = requests.post(f'{segment_api}/entities/folders/', 
                                 headers=headers, json=base_folder)

        if audience.status_code == 200:
            f_id = audience.json()['data']['id']
            print(f'Base ML Folder ##{ml_folder}## successfully created with folder_id = {f_id}')

        else:
            # if folder already exists get folder id
            try:
                objs = requests.get(f'{segment_api}/entities/by-folder/{ps_id}', 
                                              headers=headers, json={'depth':2}).json()

                f_id = [o for o in objs['data'] if o['attributes']['name']== ml_folder][0]['id']
                print(f'Base ML Folder ##{ml_folder}## already exists with folder_id = {f_id}. Try to create sub-folder next...')

            except:
                print("Unable to create segment folder")
                f_id = ps_id
                print(audience.json())

    except Exception as e: 
        f_id = ps_id
        print(e)
     
    
    #Generate Sub-Folder JSON
    subfolder =  {'attributes': {'name': sub_folder, 
                             'description': 'ML Segments automatically created'},
             'relationships': {'parentFolder': {'data': {'id': str(f_id), 'type': "folder-segment"}}}}
    
    
    #Try to create Sub-folder next
    try: 
        audience = requests.post(f'{segment_api}/entities/folders/', 
                                 headers=headers, json=subfolder)

        if audience.status_code == 200:
            f_id = audience.json()['data']['id']
            print(f'Sub-folder ##{sub_folder}## successfully created with folder_id = {f_id}')
            return (True, f_id)

        else:
            # if folder already exists get folder id
            try:
                objs = requests.get(f'{segment_api}/entities/by-folder/{ps_id}', 
                                              headers=headers, json={'depth':2}).json()

                f_id = [o for o in objs['data'] if o['attributes']['name']== sub_folder][0]['id']
                print(f'Sub-folder ##{sub_folder}## already exists with folder_id = {f_id}. No new segments to be created')
                return (False, f_id)
            
            except:
                print("Unable to create segment folder")
                f_id = ps_id
                print(audience.json())
                return (False, f_id)

    except Exception as e: 
        f_id = ps_id
        print(e)
        return (False, f_id) 

### Function to add audiences to ML Folders in PS
def create_new_segments(f_id, sub_folder, segment_params, headers, segment_api):
    
    #Create a dictionary for each attribute name and a list of its distinct values
    attribute_dict = {item['attribute']: [] for item in segment_params}
    attribute_dict
    
    #Get Distinct value of each attrib column and append to the attribute_dict
    for param in segment_params:
        src_table = param['src_table']
        attrib = param['attribute']
        query_syntax = f"SELECT DISTINCT {attrib} as attributes FROM {src_table}"
        cols = query(database, query_syntax)
        cols_list = list(cols.attributes)
        try:
          cols_list.remove(None)
        except:
          pass
        attribute_dict[attrib] = cols_list
    
    
    #Loop through segment_params list and get the distinct column values for each attribute from attribute_dict
    for param in segment_params:
        attrib = param['attribute']
        attrib_vals = attribute_dict[attrib]
        
        #Loop through segment_params list and create a rule for each distinct column value
        for attribu_value in attrib_vals:
            rule = {'type': 'And',
                 'conditions': [{'conditions': [{'type': 'Value',
                     'leftValue': {'name': attrib, 'visibility': 'clear'},
                     'operator': {'not': False, 'rightValue': attribu_value, 'type': 'Equal'},
                     'arrayMatching': None,
                     'exclude': False}],
                   'type': 'And',
                   'description': '',
                   'expr': ''}],
                 'expr': ''}

            #Create segment name in TD UI from the column_name
            name = attrib.replace('_', ' ').title() + ' = ' + str(attribu_value).title()

            #Create JSON for each segment rule 
            json_payload = {
                    'attributes': {'name': name, 
                                   'description': f'{attrib} = {attribu_value}', 
                                   'rule': rule,},
                    'relationships': {'parentFolder': {'data': {'id': f_id, 'type': 'folder-segment'}}
                }
            }

            segment_creation = requests.post(f'{segment_api}/entities/segments',
                                             headers=headers, json=json_payload)
#             print(segment_creation.json())

            if segment_creation.status_code == 200:
                print(f'Segment successfully created: {name}')
            else:
                try:
                    segment_creation.json()['errors']['name'][0] == 'has already been taken'
                    print(f'Segment: "{name}" already exists')
                except:
                    print(segment_creation.json()) ### check to see if segment already exists