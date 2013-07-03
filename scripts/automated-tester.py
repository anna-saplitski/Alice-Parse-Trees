import sys
import os
import subprocess

def get_test_files():
  test_file_directory = r'..\tests'
  test_files = []
  files = os.listdir(test_file_directory)
  for file_name in files:
    if file_name.endswith('.html'):
      test_file_path = os.path.abspath(os.path.join(test_file_directory,file_name))
      test_files.append(file_name)
  return test_files

def run_parser_on_file(test_file_path):
  python_cmd = r'C:\Python27\python'
  parser_cmd = r'..\parser.py'

  command = python_cmd + ' ' + parser_cmd + ' ' + test_file_path
  output = subprocess.check_output(command)

  output_file = open(test_file_path + '-output','w')
  output.write(output)
  output_file.close()

  print test_file_path
  print output
  print '\n\n\n'

#must be cd'd into the scripts directory
#no input, just run from github directly
def main():
  list_of_test_files = get_test_files()
  for test_file_path in list_of_test_files:
    run_parser_on_file(test_file_path)


if __name__ == "__main__":
  main()
