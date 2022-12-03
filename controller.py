from view import *
from PyQt5.QtWidgets import *
import math, csv

QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Controller(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.button_submit.clicked.connect(lambda: self.submit())
    def submit(self):
        input_id = self.lineEdit_id.text()
        id = 0
        input_choice = self.lineEdit_choice.text()
        id_valid = False
        choice = ''
        voters = dict()

        with open('voters.csv', 'r') as voters_file:
            voters_reader = csv.reader(voters_file)
            first = True
            for line in voters_reader:
                if not first:
                    voters[int(line[0])] = line[1]
                else:
                    first = False

        try:
            input_id.replace('-', '')
            input_id.replace(' ', '')
            id = int(input_id)

            if len(input_id) != 8:
                self.label_output.setText('Please enter your 8 digit ID.')
            else:
                if id in voters:
                    if voters[id] == 'Yes':
                            self.label_output.setText(f'ID {input_id} has already voted.')
                    else:
                        id_valid = True
                else:
                    self.label_output.setText(f'ID {input_id} is not registered.')
        except ValueError:
            self.label_output.setText('Please input a number.')
        except:
            self.label_output.setText('An error has occurred.')

        with open('candidates.csv', 'r') as candidates_file:
            candidates_reader = csv.reader(candidates_file)
            candidates = dict()
            first = True
            for line in candidates_reader:
                if not first:
                    candidates[line[0].lower()] = line[1].lower()
                else:
                    first = False

            if id_valid:
                try:
                    input_choice = input_choice.strip().lower()
                    choice_name = input_choice.split()
                    if len(choice_name) == 1:
                        last_name = choice_name[0]
                        for firstn, lastn in candidates.items():
                            if last_name == lastn:
                                choice = firstn.title() + ' ' + lastn.title()
                    elif len(choice_name) == 2:
                        last_name = choice_name[1]
                        first_name = choice_name[0]
                        for firstn, lastn in candidates.items():
                            if last_name == lastn and first_name == firstn:
                                choice = firstn.title() + ' ' + lastn.title()
                    else:
                        self.label_output.setText('Please input the name of one of the candidates above.')
                except:
                    self.label_output.setText('An error has occurred.')

        if choice != '':
            self.label_output.setText(f'You have voted for {choice}.')
            voters[id] = 'Yes'

            with open('voters.csv', 'w') as voters_file:
                voters_writer = csv.writer(voters_file)
                voters_writer.writerow(['ID','Voted'])
                for voter, voted in voters.items():
                    voters_writer.writerow([voter, voted])

        if not id_valid or choice != '':
            self.lineEdit_id.setText('')
        self.lineEdit_choice.setText('')

