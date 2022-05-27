class SortRule:
  def __init__(self, _subrule, _destination_directory = '', _file_types = [], _max_file_size = -1, _min_file_size = -1):
    self.destination_directory = _destination_directory
    self.file_types = _file_types
    self.max_file_size = _max_file_size
    self.min_file_size = _min_file_size
    self.subrule = _subrule