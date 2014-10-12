#!/usr/bin/env python

import threading
import select
import sys
import os
import time
import random
from sys import stdout
from time import sleep
import math
import termios


class QuestionInput:
    def __init__(self):
        self.epoll = select.epoll()
        self.epoll.register(sys.stdin, select.EPOLLIN)
        self.last = None

    def pose_query(self, question, time_limit):
        self.time_left = time_limit
        self.template = "\r" + question + "(%d s remaining): "
        self._update()
        self.template = "\033[s" + self.template + "\033[u"

        ret = None
        tl = None

        try:
            # This checks to see if there is activity on the file descriptor
            # we registered above (stdin)
            resp = self.epoll.poll(time_limit)

            # Don't worry too much about what epoll.poll returns,
            # just know that in this case if it returns a tuple of length > 0
            # that means the user typed something AND pressed enter
            if len(resp) == 0:
                sys.stdout.write("\n")
                print 'Your time is out.'
                user_input = ''
                tl = 0
            else:
                # Read what the user typed from stdin
                # this will have the trailing newline
                user_input = raw_input()
                try:
                    ret = int(user_input.strip())
                    tl = self.time_left
                except:
                    ret = user_input
        except:
            pass

        self.timer.cancel()
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
        return ret, tl

    def _update(self):
        sys.stdout.write((self.template % self.time_left))
        sys.stdout.flush()

        self.time_left -= 1
        if self.time_left < 0:
            self.time_left = 0
        else:
            self.timer = threading.Timer(1, self._update)
            self.timer.start()


def read_in_ex_data(file_in):
    '''
    takes in a file and returns
    parameters
    ----------
    file_in: string that represents the csv file for the example cases

    returns
    -------
    data of the file read in
    list_of_data: a 2d list, that is a list of the lines in the file,
                  where each line of the file is converted into a list
                  of the individual parts of the line
    d_solutions: dictionary where the key is the trialnumber,
                 and value is the correct stock price response

    # for each line we split it by comma
    # assign each value to:
    # id: question ID number
    # random_id is the integer representatino of the ID
    # adv:
    # mrksh:
    # revg:
    # price_d:
    # price_correct: the correct price
    # price_guess:
    # time:
    # difference:
    # d_solutions: dictionary where key is the ID, value is the correct answer
    # data_tuple: is a list (not a tuple) of the parts of the file read in

    '''
    list_of_data = []
    d_solutions = {}
    for n, line in enumerate(file_in):
        if n > 0:
            dat = line.rstrip().split(',')
            # id is a built in python function... why is this assigned a value?
            id = int(dat[0])
            random_id = id
            adv = dat[1]
            mrksh = dat[2]
            revg = dat[3]
            price_d = dat[4]
            price_correct = dat[5]
            price_guess = '?'
            time = ''
            difference = "?"
            d_solutions[id] = price_correct
            data_tuple = [random_id, id, adv, mrksh, revg, price_d,
                          price_correct, price_guess, time, difference]
            list_of_data.append(data_tuple)
    return list_of_data, d_solutions


def create_backup_file(prefix, list):
    '''
    writes a lastName_id_rawdata.csv file given the given the prefix
    and writes a tab-delimited file where each line is the d1 of the list
    and the individual elements are d2 of the list separated by tabs

    parameters
    ----------
    prefix: string, lastName_id
    list: 2d list of questions

    returns
    ------
    None
    '''

    fp = open(prefix + "_rawdata.csv", 'w')
    for x in list:
        for y in x:
            fp.write('%s\t' % y)
        fp.write("\n")


def read_in_backup_data(file_in):
    list_of_data = []
    d_solutions = {}
    for n, line in enumerate(file_in):
        if n > 0:
            dat = line.rstrip().split('\t')
            id = int(dat[0])
            random_id = id
            adv = dat[1]
            mrksh = dat[2]
            revg = dat[3]
            price_d = dat[4]
            price_correct = dat[5]
            price_guess = '?'
            time = ''
            difference = "?"
            d_solutions[id] = price_correct
            data_tuple = [random_id, id, adv, mrksh, revg, price_d,
                          price_correct, price_guess, time, difference]
            list_of_data.append(data_tuple)
    return list_of_data, d_solutions


def read_in_question_data(file_in):
    '''
    parameters
    ----------
    file to read in

    returns
    -------
    list1: shuffled list of the file that contain the line parts
    d_solutions: dictionary where the key is the ID,
                 and value is the correct answer
    '''
    # these cutoffs are to break up the file that is read in
    # so 3 lists can be created, then suffeled, and finally stiched back
    random1_start = 0
    random1_end = 90
    random2_start = 90
    random2_end = 180
    random3_start = 180
    random3_end = 270
    list_of_data = []
    d_solutions = {}
    for n, line in enumerate(file_in):
        if n > 0:
            dat = line.rstrip().split(',')
            id = int(dat[0])
            adv = dat[1]
            mrksh = dat[2]
            revg = dat[3]
            price_d = dat[4]
            price_correct = dat[5]
            price_guess = '?'
            random_id = ''
            time = ''
            last_guess = "NA"
            d_solutions[id] = price_correct
            data_tuple = [random_id, id, adv, mrksh, revg, price_d,
                          price_correct, price_guess, time, last_guess]
            list_of_data.append(data_tuple)
    # splits the list of data into 3 parts
    # and randomly shuffles each part before combining it back
    list1 = list_of_data[random1_start:random1_end]
    list2 = list_of_data[random2_start:random2_end]
    list3 = list_of_data[random3_start:random3_end]
    random.shuffle(list1)
    random.shuffle(list2)
    random.shuffle(list3)
    list1.extend(list2)
    list1.extend(list3)

    # reset the index after the shuffle for the list so it is sequential
    for n, x in enumerate(list1):
        x[0] = n

    return list1, d_solutions


def example_screen(example_data_list):
    '''
    clears the screen
    gets the first name, last name, id
    names file using lastname_id

    iterates through example_data_list

    parameters
    ----------
    example_data_list: 2d list of example questions returned by the
                       read_in_ex_data function

    returns
    -------
    fileout: lastName_id.txt file in write mode
    prefix: lastName_id that will be used to name the file
    '''
    os.system(['clear', 'cls'][os.name == 'nt'])
    first_name = raw_input("Please type in your FIRST name and press ENTER:")
    last_name = raw_input("Please type in your LAST name and press ENTER:")
    id = raw_input("Please type in your PID for this test and press ENTER:")
    prefix = last_name + "_" + id
    fileout = open(last_name + "_" + id + ".txt", 'w')
    raw_input("We'll start with a practice input.  Press ENTER to BEGIN...")
    os.system(['clear', 'cls'][os.name == 'nt'])
    answer_list = []
    last = "NA"
    for n, x in enumerate(example_data_list):
        os.system(['clear', 'cls'][os.name == 'nt'])
        answer_list.append(x)
        print_summary_ex(answer_list, last)
        print "Do not enter your estimate until prompted."
        time.sleep(4.5)
        qi = QuestionInput()
        resp, t = qi.pose_query("Based on the performance information above,\
                                 what is your estimated stock price for this\
                                 organization?  ", 15)
        guess = 0
        if guess == '':
            guess = None
            print "Your guess was recorded as $None", guess
        else:
            guess = resp
            print "Your guess was recorded as $", guess
        answer_list[n][7], answer_list[n][8] = resp, t
        last = guess
        answer_list[n][9] = last
        time.sleep(1)
        os.system(['clear', 'cls'][os.name == 'nt'])
    return fileout, prefix


def survey(data_list, file_out):
    '''
    Main survey call, writes user responses into a lastName_id.txt file

    parameters
    ----------
    data_list: 2d list where d1 is the information for each question
               d2 is the individual components of each question to be used
               is the user prompt
    file_out: file handler, lastName_id.txt, from example_screen()

    returns
    -------
    none

    variables used in function
    --------------------------
    answer_list: list: elements of each question is appended here
    '''
    os.system(['clear', 'cls'][os.name == 'nt'])
    answer_list = []
    last = "NA"
    for n, x in enumerate(data_list):
        os.system(['clear', 'cls'][os.name == 'nt'])
        answer_list.append(x)

        print_summary(answer_list, last)
        print "Do not enter your estimate until prompted"
        time.sleep(4.5)
        qi = QuestionInput()
        resp, t = qi.pose_query("Based on the performance information above,\
        what is your estimated stock price for this organization?  ", 15)
        guess = 0
        if guess == '':
            guess = 0
            print "Your guess was recorded as $None", guess
        else:
            guess = resp
            print "Your guess was recorded as $", guess
        answer_list[n][7], answer_list[n][8] = resp, t
        last = guess
        answer_list[n][9] = last
        time.sleep(1)
        for x in answer_list[n]:
            file_out.write('%s,' % str(x))
        file_out.write('\n')
        file_out.flush()
        os.system(['clear', 'cls'][os.name == 'nt'])



def print_condition_text(condition_text):
    os.system(['clear', 'cls'][os.name == 'nt'])
    text = '''\n\n\n\n\n '''
    text += condition_text
    text += '''\n\n\n\n\n'''
    print text
    response = raw_input('''press continue key to continue... ''')
    os.system(['clear', 'cls'][os.name == 'nt'])



def print_summary(data_list, last):
    '''
    prints the past 5 questions and user responses to screen
    '''
    last_five = []
    length_list = len(data_list)
    count = 0
    if length_list < 5:
        for i in range(0, length_list):
            dat = data_list[i]
            last_five.append(dat)
        count += 1
    else:
        for i in range(length_list - 5, length_list):
            dat = data_list[i]
            last_five.append(dat)
        count += 1

    print "Summary of Past Performance (Last 4 weeks)"
    print '\n'
    print "\t",
    for n, x in enumerate(last_five):
        if n == (len(last_five) - 1):
            print "\tCurrent Week",
        elif n == (len(last_five) - 2):
            print "\t1 Week Ago",
        elif n == (len(last_five) - 3):
            print "\t2 Weeks Ago",
        elif n == (len(last_five) - 4):
            print "\t3 Weeks Ago",
        elif n == (len(last_five) - 5):
            print "\t4 Weeks Ago",
    print '\n',
    print '\t',

    for n, x in enumerate(last_five):
        print "\t(Week " + str(x[0]) + ") ",

    print '\n',

    print "\nAdvertising",
    for x in last_five:
        print "\t" + x[2] + "\t",

    print "\nMarket Share",
    for x in last_five:
        print "\t" + x[3] + "\t",

    print "\nRevenue Growth",
    for x in last_five:
        print "\t" + x[4] + "\t",

    print '\n',

    print "\nStock Price",
    for n, x in enumerate(last_five):
        if n == (len(last_five) - 1):
            print "\t$" + "?" + "\t",
        else:
            print "\t$" + x[6] + "\t",

    print "\nYour Estimate",
    for x in last_five:
         print "\t$" + str(x[7]) + "\t",

    print "\n\nDifference",
    for n, x in enumerate(last_five):
        if n == (len(last_five) - 1):
            diff = "?"
        else:
            try:
                int(x[7])
                diff = int(x[7]) - int(x[6])
            except ValueError:
                diff = "NA"
            except TypeError:
                diff = "NA"


        print "\t$" + str(diff) + "\t",

    print "\nAchieved Goal",
    for n, x in enumerate(last_five):
        if n == (len(last_five) - 1):
            goal_check = ""
        else:
            if isinstance(x[7], int) and isinstance(last, int):
                diff = int(x[7]) - int(x[6])
                if math.fabs(diff) <= 7:
                    goal_check = "YES"
                else:
                    goal_check = "NO"
            else:
                goal_check = "NO"
        print "\t" + goal_check + "\t",

    print "\n"
    print "Remember, this task is an important determinant of your performance evaluation."
    print "Your goal is to be within +/- $7 of the actual stock price for this week's estimate."
    print "\n"


def print_summary_ex(data_list, last):
    last_five = []
    length_list = len(data_list)
    count = 0
    if length_list < 5:
        for i in range(0, length_list):
            dat = data_list[i]
            last_five.append(dat)
        count += 1
    else:
        for i in range(length_list - 5, length_list):
            dat = data_list[i]
            last_five.append(dat)
        count += 1

    print "Summary of Past Performance (Last 4 weeks)"
    print '\n'
    print "\t",
    for n, x in enumerate(last_five):
        if n == (len(last_five) - 1):
            print "\tCurrent Week",
        elif n == (len(last_five) - 2):
            print "\t1 Week Ago",
        elif n == (len(last_five) - 3):
            print "\t2 Weeks Ago",
        elif n == (len(last_five) - 4):
            print "\t3 Weeks Ago",
        elif n == (len(last_five) - 5):
            print "\t4 Weeks Ago",
    print '\n',
    print '\t',

    for n, x in enumerate(last_five):
        print "\t(Week " + str(x[0]) + ") ",

    print '\n',

    print "\nSocial Rep",
    for x in last_five:
        print "\t" + x[2] + "\t",

    print "\nSales\t",
    for x in last_five:
        print "\t" + x[3] + "\t",

    print "\nR&D\t",
    for x in last_five:
        print "\t" + x[4] + "\t",

    print '\n',

    print "\nStock Price",
    for n, x in enumerate(last_five):
        if n == (len(last_five) - 1):
            print "\t$" + "?" + "\t",
        else:
            print "\t$" + x[6] + "\t",

    print "\nYour Estimate",
    for x in last_five:
         print "\t$" + str(x[7]) + "\t",

    print "\n\nDifference",
    for n, x in enumerate(last_five):
        if n == (len(last_five) - 1):
            diff = "?"
        else:
            try:
                int(x[7])
                diff = int(x[7]) - int(x[6])
            except ValueError:
                diff = "NA"
            except TypeError:
                diff = "NA"


        print "\t$" + str(diff) + "\t",

    print "\nAchieved Goal",
    for n, x in enumerate(last_five):
        if n == (len(last_five) - 1):
            goal_check = ""
        else:
            if isinstance(x[7], int) and isinstance(last, int):
                diff = int(x[7]) - int(x[6])
                if math.fabs(diff) <= 7:
                    goal_check = "YES"
                else:
                    goal_check = "NO"
            else:
                goal_check = "NO"
        print "\t" + goal_check + "\t",

    print "\n"
    print "Remember, this task is an important determinant of your performance evaluation."
    print "Your goal is to be within +/- $7 of the actual stock price for this week's estimate."
    print "\n"

def print_file(list, file):
    for x in list:
        for y in x:
            file.write("%s\t" % y)
        file.write("\n")


def pick_condition_file():
    conditions = glob.glob("./messageConditions/*.txt")
    condition = random.sample(conditions, 1)[0]
    print condition
    return condition


def read_condition_file_to_list(condition_file_dir):
    list_of_text = []
    with open(condition_file_dir, 'r') as f:
        for line in f:
            line_string = str(line)
            # print line_string
            list_of_text.append(line)
    return list_of_text


if __name__ == "__main__":
    number_of_trials = 180
    file_in = open("./chosen_sim_data.csv")
    file_in_ex = open("./example.csv")

    example_list, example_sol = read_in_ex_data(file_in_ex)
    data_list, dict_sol = read_in_question_data(file_in)
    test_list = data_list[:number_of_trials]
    fp, prefix = example_screen(example_list[0:6])
    create_backup_file(prefix, data_list)

    print "This concludes your practice trials."
    raw_input("Do not press anything until instructed.")

    condition = pick_condition_file()
    list_of_condition_text = read_condition_file_to_list(condition)

    survey(test_list, fp, list_of_condition_text)

    os.system(['clear', 'cls'][os.name == 'nt'])
    print "Thank you, this completes the exercise."
