#!/usr/bin/env python

import threading
import select
import sys, os
import time
import random
from sys import stdout
from time import sleep

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
            resp = self.epoll.poll(time_limit) #This checks to see if there is activity on the file descriptor we registered above (stdin)
            
            # Don't worry too much about what epoll.poll returns, 
            # just know that in this case if it returns a tuple of length > 0 that means the user typed something AND pressed enter
            if len(resp) == 0:
                sys.stdout.write("\n")
                print 'Your time is out.'
                user_input = ''
                tl = 0
            else:
                user_input = raw_input() #Read what the user typed from stdin this will have the trailing newline
                try:
                    ret = int(user_input.strip())
                    tl = self.time_left
                except:
                    ret = user_input
        except:
            pass

        self.timer.cancel()
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
    list_of_data = []
    d_solutions = {}
    for n, line in enumerate(file_in):
        if n > 0:
            dat = line.rstrip().split(',')
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
            data_tuple = [random_id, id, adv, mrksh, revg, price_d, price_correct, price_guess, time, difference]
            list_of_data.append(data_tuple)
    return list_of_data, d_solutions

def read_in_question_data(file_in):
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
            data_tuple = [random_id, id, adv, mrksh, revg, price_d, price_correct, price_guess, time, last_guess]
            list_of_data.append(data_tuple)
    list1 = list_of_data[random1_start:random1_end]
    list2 = list_of_data[random2_start:random2_end]
    list3 = list_of_data[random3_start:random3_end]
    random.shuffle(list1)
    random.shuffle(list2)
    random.shuffle(list3)
    list1.extend(list2)
    list1.extend(list3)
    for n, x in enumerate(list1):
        x[0] = n

    return list1, d_solutions


def example_screen(example_data_list):
    os.system(['clear', 'cls'][os.name == 'nt'])
    print "Remember, this task is an important determinant of your performance evaluation.\n\nYour goal is to be within +/- $10 of the actual stock price for this week's estimate.\n\n"
    first_name = raw_input("Please type in your FIRST name and press ENTER:")
    last_name = raw_input("Please type in your LAST name and press ENTER:")
    id = raw_input("Please type in your ID for this test and press ENTER:")
    fileout = open(last_name + "_" + id + ".txt", 'w')
    raw_input("We'll start with a practice input.  Press ENTER to BEGIN...")
    os.system(['clear', 'cls'][os.name == 'nt'])
    answer_list = []
    last = "NA"
    for n, x in enumerate(example_data_list):
        os.system(['clear', 'cls'][os.name == 'nt'])
        answer_list.append(x)
        print_summary(answer_list, last)
        print "Do not enter anything until prompted."
        time.sleep(3)
        qi = QuestionInput()
        resp, t = qi.pose_query("Guess the stock price?", 5)
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
        time.sleep(3)
        os.system(['clear', 'cls'][os.name == 'nt'])
    return fileout

def survey(data_list, file_out):
    os.system(['clear', 'cls'][os.name == 'nt'])
    answer_list = []
    last = "NA"
    for n, x in enumerate(data_list):
        os.system(['clear', 'cls'][os.name == 'nt'])
        answer_list.append(x)

        print_summary(answer_list, last)
        print "Do not enter anything until prompted."
        time.sleep(3)
        qi = QuestionInput()
        resp, t = qi.pose_query("Guess the stock price?", 5)
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
        time.sleep(3)
        file_out.write('%s' % str(answer_list[n]))
        os.system(['clear', 'cls'][os.name == 'nt'])


def print_summary(data_list, last):
    last_five = []
    length_list = len(data_list)

    if length_list < 5:
        for i in range(0, length_list):
            dat = data_list[i]
            last_five.append(dat)
    else:
        for i in range(length_list - 5, length_list):
            dat = data_list[i]
            last_five.append(dat)

    print "Summary of Past Performance (Last 4 weeks)"

    print "\t",
    for n, x in enumerate(last_five):
        if n == (len(last_five) - 1):
            print "\tCurrent Week",
        else:
            print "\tWeek " + str(x[0]) + " ",

    print "\nAdvertising", 
    for x in last_five:
        print "\t$" + x[2] + "\t",

    print "\nMarket Share",
    for x in last_five:
        print "\t$" + x[3] + "\t",

    print "\nRevenue Growth",
    for x in last_five:
        print "\t$" + x[4] + "\t",

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
        if isinstance(x[7], int) and isinstance(last, int):
            diff = int(x[7]) - int(x[6])
            print "\t" + str(diff) + "\t",
            
        else:
            print "\t" + str(x[8]) + "\t",
    print "\n"
    print "Remember, this task is an important determinant of your performance evaluation." 
    print "Your goal is to be within +/- $10 of the actual stock price for this week's estimate."
    print "\n"
    print "Based on the performance information above, what is your estimated stock price for this organization?"
    print "\n"

def print_file(list, file):
    for x in list:
        for y in x:
            file.write("%s\t" % y)
        file.write("\n")

if __name__ == "__main__":
    file_in = open("/home/ubuntu/mike/chosen_sim_data.csv")
    file_in_ex = open("/home/ubuntu/mike/example.csv")
 
    example_list, example_sol = read_in_ex_data(file_in_ex)
    data_list, dict_sol = read_in_question_data(file_in)
    test_list = data_list
    fp = example_screen(example_list[0:5])
    print "Now begin the real deal"
    raw_input("Press ENTER to BEGIN...")
    survey(test_list[0:10], fp)
    os.system(['clear', 'cls'][os.name == 'nt'])
    print "THE END"
    raw_input("Please do not touch anything else!")

