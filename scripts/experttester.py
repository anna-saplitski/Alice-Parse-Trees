import Tkinter
import tkMessageBox
import sys
import htmlmerger
import os
import random
import webbrowser

response_window = Tkinter.Tk()
expert_opinion_file = open(sys.argv[1],'w')
current_directory = sys.argv[2]
testing_files = [os.path.abspath(os.path.join(current_directory,file_name)) for file_name in os.listdir(current_directory)]
merge_file = 'merged-file.html'

def prepare_next_pair_of_programs():

  first_file = random.choice(testing_files)
  second_file = random.choice(testing_files)
  while(first_file == second_file):
    second_file = random.choice(testing_files)

  expert_opinion_file.write(first_file + '\n' + second_file + '\n')
  
  htmlmerger.merge_html_files(first_file,second_file,merge_file)


def similar_response_received():
  expert_opinion_file.write('SIMILAR\n\n')
  prepare_next_pair_of_programs()
  tkMessageBox.showinfo("Expert Test","Similar response received. Next pair of programs.")
  webbrowser.open(merge_file)


def different_response_received():
  expert_opinion_file.write('DIFFERENT\n\n')
  prepare_next_pair_of_programs()
  tkMessageBox.showinfo('Expert Test','Different response received. Next pair of programs')
  webbrowser.open(merge_file)


similar_button = Tkinter.Button(response_window,text='similar',command = similar_response_received)
different_button = Tkinter.Button(response_window,text='different',command = different_response_received)


def main():
  if len(sys.argv) < 4:
    print 'usage: [result-file] [test-file-directory] [num-tests]'
    sys.exit(1)

  prepare_next_pair_of_programs()
  webbrowser.open(merge_file)

  similar_button.pack()
  different_button.pack()
  response_window.mainloop()
  expert_opinion_file.close()
  #print out absolute path of file for user to send the results file back to us


if __name__ == '__main__':
  main()