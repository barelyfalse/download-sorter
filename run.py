import file_sorter.sorter as fs

def run():
  srtr = fs.FileSorter(OBJECTIVE_PATH)
  rules = [
    fs.SortRule('image', ['.jpeg', '.png', '.jpg', '.gif', '.svg']),
    fs.SortRule('video', ['.mp4', '.mov', '.webm', '.3gpp'], _subrules=[
      fs.SortRule('videoMemes', _max_file_size=8000000)
    ]),
    fs.SortRule('audio', ['.wav', '.mp3', '.ogg']),
    fs.SortRule('documents', ['.doc', '.docx', '.pptx', '.xlxs', '.pdf']),
    fs.SortRule('executables', ['.bin', '.exe', '.msi']),
    fs.SortRule('compressed', ['.zip', '.rar', '.tar', '.7z', '.iso', '.img'])
  ]
  srtr.sort(rules)

if __name__ == '__main__':
  OBJECTIVE_PATH = 'D:\Documentos\Descargas'
  run()