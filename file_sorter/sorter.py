import os
import shutil

class SortRule:
  def __init__(self, _destination_directory = '', _file_types = [], _max_file_size = -1, _min_file_size = -1, _subrules = [] ):
    self.destination_directory = _destination_directory
    self.file_types = _file_types
    self.max_file_size = _max_file_size
    self.min_file_size = _min_file_size
    self.subrules = _subrules
  
  def get_rule_print(self):
    return(f'On \{self.destination_directory}{(" put [" + (", ".join(self.file_types)) + "]") if len(self.file_types) > 0 else ""}{", max size: " + str(self.max_file_size) if self.max_file_size > 0 else ""}{", min size: " + str(self.min_file_size) if self.min_file_size > 0 else ""}')

  def print_rule(self):
    print(self.get_rule_print())

class FileSorter:
  def __init__(self, _path):
    self.objective_path = _path
  
  def list_dir(self):
    entries = os.scandir(self.objective_path)
    return entries
  
  def entry_matches_rule(self, _entry, _rule):
    matches_type = False
    for file_type in _rule.file_types:
      if _entry.name.endswith(file_type):
        matches_type = True
        break
    
    has_max_size_rule = _rule.max_file_size > 0
    has_min_size_rule = _rule.min_file_size > 0
    matches_min_size = False
    matches_max_size = False
    
    if has_max_size_rule and _entry.stat().st_size < _rule.max_file_size:
      matches_max_size = True
    if has_min_size_rule and _entry.stat().st_size > _rule.min_file_size:
      matches_max_size = True
    
    matches_size = (True if has_max_size_rule == False else matches_max_size) and (True if has_min_size_rule == False else matches_min_size)

    matches = (matches_type and matches_size)
    destiny_path = ('\\' + _rule.destination_directory) if matches else ''

    if matches_type and len(_rule.subrules) > 0:
      for subr in _rule.subrules:
        #TODO: match subtypes
        has_sub_max_size_rule = subr.max_file_size > 0
        has_sub_min_size_rule = subr.min_file_size > 0
        matches_sub_min_size = False
        matches_sub_max_size = False
        
        if has_sub_max_size_rule and _entry.stat().st_size < subr.max_file_size:
          matches_sub_max_size = True
        if has_sub_min_size_rule and _entry.stat().st_size > subr.min_file_size:
          matches_sub_max_size = True
        
        matches_sub_size = (True if has_sub_max_size_rule == False else matches_sub_max_size) and (True if has_sub_min_size_rule == False else matches_sub_min_size)

        if matches_sub_size:
          destiny_path = destiny_path+'\\'+subr.destination_directory
          break


    return [matches, destiny_path]

  def sort_sim(self, _rules):
    entries = os.scandir(self.objective_path)
    for entry in entries:
      if entry.is_file:
        for rule in _rules:
          match = self.entry_matches_rule(entry, rule)
          if match[0]:
            print(f'{entry.name} matches, path: {match[1]}')
            break
  
  def sort(self, _rules):
    for rule in _rules:
      if os.path.isdir(self.objective_path+'\\'+rule.destination_directory) == False:
        os.makedirs(self.objective_path+'\\'+rule.destination_directory)
      if(len(rule.subrules) > 0):
        for subrule in rule.subrules:
          if os.path.isdir(self.objective_path+'\\'+rule.destination_directory+'\\'+subrule.destination_directory) == False:
            os.makedirs(self.objective_path+'\\'+rule.destination_directory+'\\'+subrule.destination_directory)

    entries = os.scandir(self.objective_path)
    for entry in entries:
      if entry.is_file:
        for rule in _rules:
          match = self.entry_matches_rule(entry, rule)
          if match[0]:
            shutil.move(entry.path, self.objective_path + match[1] + '\\' )
            print(f'{entry.name} moved to: {self.objective_path+match[1]}')
            break