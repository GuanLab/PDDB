import pandas as pd
import os,shutil, csv
demo = pd.read_csv('Demographic_survey.tsv',sep = '\t', header = 0, dtype = str)
record = pd.read_csv('Walking_Activity_training.tsv',sep = '\t', header = 0, dtype = str)
new_record = record.iloc[0:0]
for healthcode in demo['healthCode']:
        new_row = record.loc[record['healthCode'] == healthcode]
        files = []
        files.extend(new_row['accel_walking_outbound.json.items'].tolist())
        files.extend(new_row['accel_walking_rest.json.items'].tolist())
        files.extend(new_row['accel_walking_return.json.items'].tolist())
        for i in files:
                filename = '../PD_walking_project/Data/'+str(i)+'.tmp'
                #print(filename)
                if os.path.exists(filename):
                        shutil.copyfile(filename, './Data/'+str(i)+'.tmp')
        new_record = new_record.append(new_row)
new_record.to_csv('Walking_Activity_training_new.tsv',sep = '\t', escapechar='\\', quoting=csv.QUOTE_ALL, header = True, index=False)
