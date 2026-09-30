import json
def compute_percentage_change_v1(current,previous):
  if previous==0:
   return 0

  return((current-previous)/previous*100)  
def flag_sinificant_regions_v1(changes,threshold=8):
  flagged={}
  for region,change in changes.items():
    if(abs(change)>threshold):
      flagged[region]=change
  return flagged
def save_state_v1(month_summary, path):
  with open(path,'w') as file:
    json.dump(month_summary,file,indent=4)
def load_previous_state_v1(path):
  with open(path,'r') as file:
    return json.load(file)

