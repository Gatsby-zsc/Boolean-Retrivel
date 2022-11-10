import argparse
import json
import nltk
from nltk import pos_tag
from nltk import WordNetLemmatizer
from nltk import word_tokenize
from collections import deque



nltk.download('wordnet', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

'''
prints the proper command usage
'''

parser = argparse.ArgumentParser(
    description='Index data for boolean retrieval')
parser.add_argument('input_path', help='indexes to be searched')
args = parser.parse_args()

# Get arguments
folder_of_indexes = args.input_path


with open(str(folder_of_indexes) + '/' + 'positional index.json', 'r') as f:
    positional_index = json.load(f)
    f.close()


# define boolean and
def intersect(p1, p2):
    p1_index = 0
    p2_index = 0
    answer = []
    while p1_index < len(p1) and p2_index < len(p2):
        if p1[p1_index][0] == p2[p2_index][0]:
            answer.append(p1[p1_index])
            p1_index += 1
            p2_index += 1
        elif p1[p1_index][0] < p2[p2_index][0]:
            p1_index += 1
        else:
            p2_index += 1
    return answer


# define boolean or/space
def or_function(p1, p2):
    p1_index = 0
    p2_index = 0
    answer = []
    while p1_index < len(p1) or p2_index < len(p2):
        # if two lists don't have the same length
        # when one list was iterated, we need iterated the other
        if p1_index == len(p1):
            answer += p2[p2_index:]
            break
        elif p2_index == len(p2):
            answer += p1[p1_index:]
            break

        elif p1[p1_index][0] == p2[p2_index][0]:
            answer.append(p1[p1_index])
            p1_index += 1
            p2_index += 1
        elif p1[p1_index][0] < p2[p2_index][0]:
            answer.append(p1[p1_index])
            p1_index += 1
        elif p1[p1_index][0] > p2[p2_index][0]:
            answer.append(p2[p2_index])
            p2_index += 1
    return answer


# define "/n" function
def slash_n(p1, p2, k):
    answer = []
    p1_index = 0
    p2_index = 0
    while p1_index < len(p1) and p2_index < len(p2):
        # indexes of docID p1, p2
        if p1[p1_index][0] == p2[p2_index][0]:
            l = []
            pp1 = p1[p1_index][1]  # pp1 <- positions(p1)
            pp2 = p2[p2_index][1]  # pp2 <- positions(p2)

            pp1_index = pp2_index = 0
            while pp1_index < len(pp1):  # while (pp1 != nil)
                while pp2_index < len(pp2):  # while (pp2 != nil)
                    if abs(pp1[pp1_index][0] - pp2[pp2_index][0]) <= k:  # if (|pos(pp1) - pos(pp2)| <= k)
                        l.append(pp2[pp2_index][0])  # l.add(pos(pp2))
                    elif pp2[pp2_index][0] > pp1[pp1_index][0]:  # else if (pos(pp2) > pos(pp1))
                        break
                    pp2_index += 1  # pp2 <- next(pp2)
                while l != [] and abs(l[0] - pp1[pp1_index][0]) > k:  # while (l != () and |l(0) - pos(pp1)| > k)
                    l.remove(l[0])  # delete(l[0])
                for ps in l:
                    if p1[p1_index][0] not in answer:  # for each ps in l
                        answer.append(p1[p1_index])  # add answer(docID(p1), pos(pp1), ps)
                pp1_index += 1  # pp1 <- next(pp1)
            p1_index += 1  # p1 <- next(p1)
            p2_index += 1  # p2 <- next(p2)
        elif p1[p1_index][0] < p2[p2_index][0]:  # else if (docID(p1) < docID(p2))
            p1_index += 1  # p1 <- next(p1)
        else:
            p2_index += 1  # p2 <- next(p2)
    return answer


# define "+n" function
def plus_n(p1, p2, k):
    answer = []
    p1_index = 0
    p2_index = 0
    while p1_index < len(p1) and p2_index < len(p2):
        # indexes of docID p1, p2
        if p1[p1_index][0] == p2[p2_index][0]:
            l = []
            pp1 = p1[p1_index][1]  # pp1 <- positions(p1)
            pp2 = p2[p2_index][1]  # pp2 <- positions(p2)

            pp1_index = pp2_index = 0
            while pp1_index < len(pp1):  # while (pp1 != nil)
                while pp2_index != len(pp2):  # while (pp2 != nil)
                    if abs(pp1[pp1_index][0] - pp2[pp2_index][0]) <= k:  # if (|pos(pp1) - pos(pp2)| <= k)
                        l.append(pp2[pp2_index][0])  # l.add(pos(pp2))
                    elif pp2[pp2_index][0] > pp1[pp1_index][0]:  # else if (pos(pp2) > pos(pp1))
                        break
                    pp2_index += 1  # pp2 <- next(pp2)
                while l != [] and abs(l[0] - pp1[pp1_index][0]) > k:  # while (l != () and |l(0) - pos(pp1)| > k)
                    l.remove(l[0])  # delete(l[0])
                for ps in l:
                    if pp1[pp1_index][0] <= ps and p1[p1_index][0] not in answer:  # for each ps in l
                        answer.append(p1[p1_index])  # add answer(docID(p1), pos(pp1), ps)
                pp1_index += 1  # pp1 <- next(pp1)
            p1_index += 1  # p1 <- next(p1)
            p2_index += 1  # p2 <- next(p2)
        elif p1[p1_index][0] < p2[p2_index][0]:  # else if (docID(p1) < docID(p2))
            p1_index += 1  # p1 <- next(p1)
        else:
            p2_index += 1  # p2 <- next(p2)
    return answer


# define "/s" function
# p1, p2 positional index list
# [[docID, [[pos_in_doc, sentenceID],[pos_in_doc, sentenceID],...]]]
def slash_s(p1, p2):
    answer = []
    p1_index = 0
    p2_index = 0
    while p1_index < len(p1) and p2_index < len(p2):
        # indexes of docID p1, p2
        if p1[p1_index][0] == p2[p2_index][0]:
            pp1 = p1[p1_index][1]  # pp1 <- positions(p1)
            pp2 = p2[p2_index][1]  # pp2 <- positions(p2)
            pp1_index = pp2_index = 0
            break_flag = False
            while pp1_index < len(pp1):
                pp2_index = 0  # while (pp1 != nil)
                while pp2_index < len(pp2):  # while (pp2 != nil)
                    if pp1[pp1_index][1] == pp2[pp2_index][1]:
                        if p1[p1_index][0] not in answer:
                            answer.append(p1[p1_index])
                            break_flag = True
                            break
                    pp2_index += 1
                if break_flag:
                    break
                pp1_index += 1  # pp1 <- next(pp1)
            p1_index += 1  # p1 <- next(p1)
            p2_index += 1  # p2 <- next(p2)
        elif p1[p1_index][0] < p2[p2_index][0]:  # else if (docID(p1) < docID(p2))
            p1_index += 1  # p1 <- next(p1)
        else:
            p2_index += 1  # p2 <- next(p2)
    return answer


# define "+s" function
# p1, p2 positional index list
# [[docID, [[pos_in_doc, sentenceID],[pos_in_doc, sentenceID],...]]]
def plus_s(p1, p2):
    answer = []
    p1_index = 0
    p2_index = 0
    while p1_index < len(p1) and p2_index < len(p2):
        # indexes of docID p1, p2
        if p1[p1_index][0] == p2[p2_index][0]:
            pp1 = p1[p1_index][1]  # pp1 <- positions(p1)
            pp2 = p2[p2_index][1]  # pp2 <- positions(p2)
            pp1_index = pp2_index = 0
            break_flag = False
            while pp1_index < len(pp1):
                pp2_index = 0  # while (pp1 != nil)
                while pp2_index < len(pp2):  # while (pp2 != nil)
                    if pp1[pp1_index][1] == pp2[pp2_index][1] and pp1[pp1_index][0] <= pp2[pp2_index][0]:
                        if p1[p1_index][0] not in answer:
                            answer.append(p1[p1_index])
                            break_flag = True
                            break
                    pp2_index += 1
                if break_flag:
                    break
                pp1_index += 1  # pp1 <- next(pp1)
            p1_index += 1  # p1 <- next(p1)
            p2_index += 1  # p2 <- next(p2)
        elif p1[p1_index][0] < p2[p2_index][0]:  # else if (docID(p1) < docID(p2))
            p1_index += 1  # p1 <- next(p1)
        else:
            p2_index += 1  # p2 <- next(p2)
    return answer


# shunting_yard algorithm
def shunting_yard(infix_tokens):
    # define precedences
    precedence = {}
    precedence["("] = 0
    precedence[")"] = 0
    # define "''" as "[]"
    precedence["["] = 1
    precedence["]"] = 1
    precedence[" "] = 5
    precedence["+n"] = 4
    precedence["/n"] = 4
    precedence["+s"] = 3
    precedence["/s"] = 3
    precedence["&"] = 2
    # define data structures
    output = []
    operator_stack = []

    # while we read query
    for token in infix_tokens:
        if token[0] == "/" and token[1:].isdigit():
            precedence[token] = precedence["/n"]
        elif token[0] == "+" and token[1:].isdigit():
            precedence[token] = precedence["+n"]

        # if left bracket
        if token == "(":
            operator_stack.append(token)

        # if right bracket, pop item from stack till we get left bracket
        elif token == ")":
            operator = operator_stack.pop()
            while operator != "(":
                output.append(operator)
                operator = operator_stack.pop()

        # if left bracket
        elif token == "[":
            operator_stack.append(token)

        # if right bracket, pop item from stack till we get left bracket
        elif token == "]":
            operator = operator_stack.pop()
            while operator != "[":
                output.append(operator)
                operator = operator_stack.pop()

        # if operator, pop operators from operator stack to queue if they are of higher precedence
        elif token in precedence.keys() or token[0] == "/" or token[0] == "+":
            # if operator stack is not empty
            if operator_stack:
                current_operator = operator_stack[-1]
                while operator_stack and precedence[current_operator] >= precedence[token]:
                    output.append(operator_stack.pop())
                    if operator_stack:
                        current_operator = operator_stack[-1]

            operator_stack.append(token)  # add token to stack

        # else if operands, add to output list
        else:
            output.append(token)

    # while there are still operators on the stack, pop them into the queue
    while operator_stack:
        output.append(operator_stack.pop())
    # print ('postfix:', output)  # check
    return output


lemma = WordNetLemmatizer()


def preprocessing_query(query):
    # query preprocessing
    temp_query = []
    final_query = []
    query = query.lower()
    query = query.replace(".", "")
    word_list = word_tokenize(query)
    start_index = 0
    end_index = 0
    interval = []
    for index, item in enumerate(pos_tag(word_list)):
        if item[0] == '``':
            word_list[index] = "["
            start_index = index
            continue
        if item[0] == "''":
            word_list[index] = "]"
            end_index = index
            interval.append((start_index, end_index))
            continue
    output = []
    operator = ["(", ")", " ", "[", "]", "&"]
    if interval:
        for i in interval:
            j = 0
            while i[0] + j <= i[1]:
                if word_list[i[0] + j] != "/" and word_list[i[0] + j] != "+" and word_list[i[0] + j] not in operator:
                    j += 1
                    if word_list[i[0] + j] != "/" and word_list[i[0] + j] != "+" and word_list[
                        i[0] + j] not in operator:
                        word_list.insert(i[0] + j, "+1")
                j += 1

    for index, item in enumerate(word_list):
        output.append(item)
        if index < len(word_list) - 1:
            if item[0] != "/" and item[0] != "+" and item not in operator:
                if word_list[index + 1][0] != "/" and word_list[index + 1][0] != "+" and word_list[
                    index + 1] not in operator:
                    output.append(" ")
            if item == ")" and word_list[index + 1] == "(":
                output.append(" ")
            elif item == ")" and word_list[index + 1][0] != "/" and word_list[index + 1][0] != "+" and word_list[
                index + 1] not in operator:
                output.append(" ")
            elif word_list[index + 1] == "(" and word_list[index][0] != "/" and word_list[index][0] != "+" and \
                    word_list[
                        index] not in operator:
                output.append(" ")
            if item == "]" and word_list[index + 1] == "[":
                output.append(" ")
            elif item == "]" and word_list[index + 1][0] != "/" and word_list[index + 1][0] != "+" and word_list[
                index + 1] not in operator:
                output.append(" ")
            elif word_list[index + 1] == "[" and word_list[index][0] != "/" and word_list[index][0] != "+" and \
                    word_list[
                        index] not in operator:
                output.append(" ")
            if item == "]" and word_list[index + 1] == "(":
                output.append(" ")
            if item == ")" and word_list[index + 1] == "[":
                output.append(" ")
    temp_query = []
    for item in pos_tag(output):
        if item[1][0] == "N" and item[0] != "ios":
            temp_query.append(lemma.lemmatize(item[0], "n"))
            continue
        temp_query.append(item[0])
    pos = pos_tag(temp_query)
    final_query = []
    for word in pos:
        final_query.append(lemma.lemmatize(word[0], "v"))
    return final_query


def search(query, positional_index):
    query = preprocessing_query(query)
    result_stack = []
    postfix_queue = deque(shunting_yard(query))
    while postfix_queue:
        token = postfix_queue.popleft()
        temp_result = []
        if token != '&' and token != ' ' and token[0] != "+" and token[0] != "/":
            if token in positional_index.keys():
                temp_result = positional_index[token]
            else:
                return
        elif token == "&":
            right_operand = result_stack.pop()
            left_operand = result_stack.pop()
            temp_result = intersect(left_operand, right_operand)
        elif token == " ":
            right_operand = result_stack.pop()
            left_operand = result_stack.pop()
            temp_result = or_function(left_operand, right_operand)
        elif token[0] == "/" and token[1:].isdigit():
            right_operand = result_stack.pop()
            left_operand = result_stack.pop()
            temp_result = slash_n(left_operand, right_operand, int(token[1:]))
        elif token[0] == "+" and token[1:].isdigit():
            right_operand = result_stack.pop()
            left_operand = result_stack.pop()
            temp_result = plus_n(left_operand, right_operand, int(token[1:]))
        elif token == "/s":
            right_operand = result_stack.pop()
            left_operand = result_stack.pop()
            temp_result = slash_s(left_operand, right_operand)
        elif token == "+s":
            right_operand = result_stack.pop()
            left_operand = result_stack.pop()
            temp_result = plus_s(left_operand, right_operand)

        result_stack.append(temp_result)
    if len(result_stack) == 1:
        return result_stack.pop()


while True:
    query = input()
    if query:
        result = search(query, positional_index)
        temp = []
        if result:
            for i in result:
                if i[0] not in temp:
                    temp.append(int(i[0]))
            for x in sorted(list(set(temp))):
                print(x)
