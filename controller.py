from view import *
from PyQt5.QtWidgets import *
import math, csv

QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Controller(QMainWindow, Ui_MainWindow):
    '''
    Class that allows interatction with the GUI.
    '''

    def __init__(self, *args, **kwargs):
        '''
        Constructor to create the inital state of the Controller object.
        '''
        super(Controller, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.button_submit.clicked.connect(lambda: self.submit())
        
        self.__candidates_votes = dict() # canditate last names as keys and number of votes as values
        with open('candidates.csv', 'r') as csvfile:
            candidates_reader = csv.reader(csvfile)
            for line in candidates_reader:
                self.__candidates_votes[line[1]] = 0
        self.__candidates_votes.pop('Last Name')

    def submit(self):
        '''
        Method to validate a voter's id, update a candidate's number of votes,
        and update the GUI.
        '''
        input_id = self.lineEdit_id.text() # the user's numeric id
        input_choice = self.lineEdit_choice.text() # name of the candidate the user chooses
        id_valid = False # remains False if id is not valid, True if it is valid
        choice = '' # entered candidate name standardized
        voters = dict() # voters' ids as keys and if they have voted ('Yes' or 'No') as values
        candidates = dict() # candidate first names as keys and last names as values

        with open('voters.csv', 'r') as voters_file:
            voters_reader = csv.reader(voters_file)
            first = True
            for line in voters_reader:
                if not first:
                    voters[line[0]] = line[1]
                else:
                    first = False

        # Verifies that an entered id is 8 digits, exists in voters.csv, and has not voted
        try:
            input_id.replace('-', '')
            input_id.replace(' ', '')

            if len(input_id) != 8:
                self.label_output.setText('Please enter your 8 digit ID.')
            else:
                if input_id in voters:
                    if voters[input_id] == 'Yes':
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
            first = True
            for line in candidates_reader:
                if not first:
                    candidates[line[0].lower()] = line[1].lower()
                else:
                    first = False
                    
        # matches the user's entered name to a candidate's name
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
                    
        # updates __candidates_votes and updates the GUI
        if choice != '':
            self.label_output.setText(f'You have voted for {choice}.')
            voters[input_id] = 'Yes'

            with open('voters.csv', 'w') as voters_file:
                voters_writer = csv.writer(voters_file)
                voters_writer.writerow(['ID','Voted'])
                for voter, voted in voters.items():
                    voters_writer.writerow([voter, voted])

            self.__candidates_votes[choice.split()[-1]] += 1
                    
            votes_output = 'Total Votes:\n\n'
            for name in self.__candidates_votes:
                votes_output += str(self.__candidates_votes[name]) + '\n'

            self.label_vote_count.setText(votes_output)

        if not id_valid or choice != '':
            self.lineEdit_id.setText('')
        self.lineEdit_choice.setText('')

