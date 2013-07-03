import sys
import re

#Constants that represent the header, middle, and footer of the merged HTML file
header = r"""<html>
<table width="1300", cellpadding="15",cellspacing="0">

<th>Sample 1</th>
<th>Sample 2</th>

<tr>
<td valign="top">
"""

middle = r'''<td valign="top">
'''

footer = r"""</td>
</tr>
</table>
</html>
"""


#Extract the body of a string of HTML code. Returns the matching string.
def get_body_text_from_html_file(file_name):
  try:
    open_file = open(file_name,'rU')
  except IOError:
    print r'Failed to open ' + file_name + '\nProgram closing.'
    sys.exit(1)


  match = re.search(r'<html>(.+)</html>',open_file.read(),re.DOTALL)
  
  if not match:
    print r'HTML file ' + file_name + r' formatted incorrectly. Program closing.'
    sys.exit(1)
  
  open_file.close()

  return match.group(1)


#Takes the bodies of two HTML files and inserts them into a properly formatted, new HTML file. Returns the name of the HTML file
def merge_into_new_file(first_text,second_text,merged_file_name):
  merged_text = header + first_text + middle + second_text + footer

  if merged_file_name == '':
    merged_file_name = 'merged-html-file.html'

  merged = open(merged_file_name,'w')
  merged.write(merged_text)

  merged.close()
  return merged_file_name


#Takes two input HTML files and returns the name of a merged file that contains the two HTML files side-by-side
def merge_html_files(first_file,second_file,merged_file_name):
  first_text = get_body_text_from_html_file(first_file)
  second_text = get_body_text_from_html_file(second_file)

  merged_file_name = merge_into_new_file(first_text,second_text,merged_file_name)

  return merged_file_name


#Runs the program on two input files
def main():
  if len(sys.argv) < 3:
    print r'usage: [first_html_file] [second_html_file] [opt. merged_html_file]'
    sys.exit(1)

  merged_file_name = ''
  if len(sys.argv) > 3:
    merged_file_name = sys.argv[3]

  first_file = sys.argv[1]
  second_file = sys.argv[2]
  merged_file = merge_html_files(first_file,second_file,merged_file_name)


if __name__ == '__main__':
  main()