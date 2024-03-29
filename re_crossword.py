import string
import argparse
import csv
import re
import sre_yield

parser = argparse.ArgumentParser()
parser.add_argument("crossword_file", help="name of input file")
parser.add_argument("regular_expressions_file", help="name of input file")
args = parser.parse_args()


with open(args.crossword_file) as input_file:
    word_dict = {}
    cross_dict = {}
    for line in input_file:
        parts = line.rstrip()
        parts = parts.split(",")
        word_dict.update({parts[0]: parts[1]})
        table = []
        for x in range(2, len(parts)):
            table.append(parts[x])
            cross_dict.update({parts[0]: table})

with open(args.regular_expressions_file) as input_file:
    regular_exp = []
    for line in input_file:
        regular_exp.append(line.rstrip())


def correction(key, word_dict, cross_dict, regular_perposition,used_reg_position, pq):

    x = 0
    for item in cross_dict.get(key):
        if x == 0 or x == 2 or x % 2 == 0:
            if item in pq:
                continue
            if len(regular_perposition.get(item)) == 0:
                word_dict, regular_perposition, used_reg_position, pq = correction(item, word_dict, cross_dict, regular_perposition, used_reg_position, pq)
            else:
                word_dict.update({item: regular_perposition.get(item)[0]})
                regular_perposition.get(item).pop(0)
                used_reg_position.get(item).pop(0)
                z = 0
                spot = 1000
                for reg in cross_dict.get(item):
                    if z == 0 or z == 2 or z % 2 == 0:
                        for y in range(0, len(cross_dict.get(reg)), 2):
                            if cross_dict.get(reg)[y] == item:
                                spot = y + 1
                        if reg not in pq and reg != key:
                            if len(regular_perposition.get(reg)) != 0:
                                regular_perposition.get(reg).clear()  # not sure for clear()
                                used_reg_position.get(reg).clear()
                            pq.append(reg)
                    if z == 1 or z % 2 != 0:
                        for i in range(len(word_dict.get(item))):
                            if i == int(cross_dict.get(cross_dict.get(item)[z - 1])[spot]):
                                letter = word_dict.get(item)[i]
                        new_string = []
                        for i in range(len(word_dict.get(cross_dict.get(item)[z - 1]))):
                            if i == int(reg):
                                new_string.insert(i, letter)
                            else:
                                position = []
                                m = 0
                                for star in cross_dict.get(cross_dict.get(item)[z-1]):          #will change letters of words but what about words?
                                    if m == 0 or m == 2 or m % 2 == 0:
                                        for yolo in range(0, len(cross_dict.get(star)), 2):
                                            if cross_dict.get(star)[yolo] == cross_dict.get(item)[z-1]:
                                                position.append(int(cross_dict.get(star)[yolo + 1]))
                                    m += 1

                                if i in position:
                                    new_string.insert(i, word_dict.get(cross_dict.get(item)[z - 1])[i])
                                else:
                                    new_string.insert(i, '.')
                        word_dict.update({cross_dict.get(item)[z - 1]: new_string})
                    z += 1
        x += 1
    return word_dict, regular_perposition, used_reg_position, pq



temp_regexp = []
for i in range(len(regular_exp)):
    temp_regexp.append(regular_exp[i])
nodes = word_dict.keys()
elements_in_queue = len(nodes)
pq = []
for key in word_dict.keys():
    pq.append(key)
reg_exp_per_position = {}
used_reg_exp_position = {}

while len(pq) != 0:
    to_change = 0
    max_word = 0
    for v in word_dict.keys():
        if v not in pq:
            continue
        x = 0
        word = word_dict.get(v)
        for letter in word:
            if letter != '.':
                x += 1
        word_to_choose = x / len(word)
        if word_to_choose > max_word:
            max_word = word_to_choose
            key_chosen = v
    pq.remove(key_chosen)
    list1 = []
    words = False
    for v in regular_exp:
        list1 = sre_yield.AllStrings(v, max_count=5, charset=string.ascii_uppercase)
        for item in list1:
            if len(item) == len(word_dict.get(key_chosen)):   # and v in temp_regexp
                listA = []
                listB = []
                for letter in item:
                    listA.append(letter)
                for letter in word_dict.get(key_chosen):
                    listB.append(letter)
                for i in range(len(item)):
                    if listA[i] == listB[i] or listB[i] == '.':
                        condition = True
                    else:
                        condition = False
                        break
                if condition:
                    reg_exp_per_position.setdefault(key_chosen, []).append(item)
                    used_reg_exp_position.setdefault(key_chosen, []).append(v)
                    words = True
    if words:
        if len(reg_exp_per_position.get(key_chosen)) == 1 and used_reg_exp_position.get(key_chosen)[0] in temp_regexp:  # final word to position
            word_dict.update({key_chosen: reg_exp_per_position.get(key_chosen)[0]})
            z = 0
            spot = 1000
            for item in cross_dict.get(key_chosen):
                if z == 0 or z == 2 or z % 2 == 0 and item in pq:
                    for v in range(0, len(cross_dict.get(item)), 2):
                        if cross_dict.get(item)[v] == key_chosen:
                            spot = v + 1  #temnousa leksi
                if z == 1 or z % 2 != 0 and cross_dict.get(key_chosen)[z-1] in pq:
                    for i in range(len(word_dict.get(key_chosen))):
                        if i == int(cross_dict.get(cross_dict.get(key_chosen)[z-1])[spot]):
                            letter = word_dict.get(key_chosen)[i]
                    new_string = []
                    for i in range(len(word_dict.get(cross_dict.get(key_chosen)[z-1]))):
                        if i == int(item):
                            new_string.insert(i, letter)
                        else:
                            new_string.insert(i, word_dict.get(cross_dict.get(key_chosen)[z-1])[i])
                    word_dict.update({cross_dict.get(key_chosen)[z-1]: new_string})
                z += 1
            regular_exp.remove(used_reg_exp_position.get(key_chosen)[0])
            temp_regexp.remove(used_reg_exp_position.get(key_chosen)[0])
            elements_in_queue -= 1
        else:
            flag1 = False
            for i in range(len(reg_exp_per_position[key_chosen])):
                if used_reg_exp_position.get(key_chosen)[i] in temp_regexp:
                    flag1 = True
                    cell = i
            if flag1:
                word_dict.update({key_chosen: reg_exp_per_position.get(key_chosen)[cell]})
                reg_exp_per_position.get(key_chosen).pop(cell)
                temp_regexp.remove(used_reg_exp_position.get(key_chosen)[cell])
                used_reg_exp_position.get(key_chosen).pop(cell)
                z = 0
                spot = 1000
                for item in cross_dict.get(key_chosen):
                    if z == 0 or z == 2 or z % 2 == 0 and item in pq:
                        for v in range(0, len(cross_dict.get(item)), 2):
                            if cross_dict.get(item)[v] == key_chosen:
                                spot = v + 1
                    if z == 1 or z % 2 != 0 and cross_dict.get(key_chosen)[z-1] in pq:
                        for i in range(len(word_dict.get(key_chosen))):
                            if i == int(cross_dict.get(cross_dict.get(key_chosen)[z - 1])[spot]):
                                letter = word_dict.get(key_chosen)[i]
                        new_string = []
                        for i in range(len(word_dict.get(cross_dict.get(key_chosen)[z - 1]))):
                            if i == int(item):
                                new_string.insert(i, letter)
                            else:
                                new_string.insert(i, word_dict.get(cross_dict.get(key_chosen)[z - 1])[i])
                        word_dict.update({cross_dict.get(key_chosen)[z - 1]: new_string})
                    z += 1
                elements_in_queue -= 1
            else:
                word_dict.update({key_chosen: reg_exp_per_position.get(key_chosen)[0]})
                reg_exp_per_position.get(key_chosen).pop(0)
                used_reg_exp_position.get(key_chosen).pop(0)
                z = 0
                spot = 1000
                for item in cross_dict.get(key_chosen):
                    if z == 0 or z == 2 or z % 2 == 0 and item in pq:
                        for v in range(0, len(cross_dict.get(item)), 2):
                            if cross_dict.get(item)[v] == key_chosen:
                                spot = v + 1
                    if z == 1 or z % 2 != 0 and cross_dict.get(key_chosen)[z-1] in pq:
                        for i in range(len(word_dict.get(key_chosen))):
                            if i == int(cross_dict.get(cross_dict.get(key_chosen)[z - 1])[spot]):
                                letter = word_dict.get(key_chosen)[i]
                        new_string = []
                        for i in range(len(word_dict.get(cross_dict.get(key_chosen)[z - 1]))):
                            if i == int(item):
                                new_string.insert(i, letter)
                            else:
                                new_string.insert(i, word_dict.get(cross_dict.get(key_chosen)[z - 1])[i])
                        word_dict.update({cross_dict.get(key_chosen)[z - 1]: new_string})
                    z += 1
            elements_in_queue -= 1
    else:
        word_dict, reg_exp_per_position, used_reg_exp_position, pq = correction(key_chosen, word_dict, cross_dict, reg_exp_per_position, used_reg_exp_position, pq)
        pq.append(key_chosen)




