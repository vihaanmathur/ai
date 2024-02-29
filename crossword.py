# Name: Vihaan Mathur
# Date: 2/14/22
#Creates a crossword puzzle based on a text file of words. 


import sys; args = sys.argv[1:]
import re, random, os

BLOCKCHAR = '#'
OPENCHAR = '-'
PROTECTEDCHAR = '~'

#python crossword.py words.txt 13x13 32 H1x4#Toe# H9x2# V3x6# H10x0Scintillating V0x5stirrup H4x2##Ordained V0x1Clam V0x12Imf V5x0pew

#ctrl+c to stop 

def area_fill(board_list, sp, width):
    if sp < 0 or sp >= len(board_list): return board_list
    if (board_list[sp] == OPENCHAR) or (board_list[sp] == PROTECTEDCHAR):
        board_list[sp] = '?'
        if sp % width != 0 and sp-1 >= 0:
            area_fill(board_list, sp-1, width)
        if sp not in range(0, width) and sp-width >= 0:
            area_fill(board_list, sp-width, width)
        if sp % width != width-1 and sp+1 < len(board_list):
            area_fill(board_list, sp+1, width)
        if sp not in range(len(board_list) - width, len(board_list)) and sp+width < len(board_list):
            area_fill(board_list, sp+width, width)
    return board_list
        
        

def check_illegal(xword, width, num_of_blocks, totalnum):
    #if theres more blocks in board then initially set, board doesnt connect, or if theres short of a sequence of protected characters 
    if num_of_blocks > totalnum or xword.count(OPENCHAR) == 0:
        return True 
    count, startpos = 0, 0
    while startpos < len(xword) and xword[startpos] == BLOCKCHAR:
        startpos += 1
    board_list = list(xword)
    board = ''.join(area_fill(board_list, startpos, width))
    count = len([x for x in range(len(board)) if board[x] == '?'])
    count2 = xword.count(OPENCHAR) + xword.count(PROTECTEDCHAR)
    return count == count2

def transpose(xw, newWidth):
    return ''.join([xw[col::newWidth] for col in range(newWidth)])

def csp_helper(board, width):
    xw = BLOCKCHAR*(width+3) + (BLOCKCHAR*2).join([board[p:p+width] for p in range(0, len(board),width)]) + BLOCKCHAR*(width+3)
    subRE = "[{}]{}(?=[{}])".format(BLOCKCHAR, OPENCHAR, BLOCKCHAR)
    subRE2 = "[{}]{}{}(?=[{}])".format(BLOCKCHAR, OPENCHAR, OPENCHAR, BLOCKCHAR)
    subRE3="[#](-~-|--~|~--|~~-|-~~|~-~)(?=[#])"
    illegRE = "[{}](.?[{}]|[{}].?)[{}]".format(BLOCKCHAR, PROTECTEDCHAR, PROTECTEDCHAR, BLOCKCHAR)
    newH = len(xw) // (width + 2)
    for turn in range(2):
        if re.search(illegRE, xw):   
            return board, len(board)
        xw = transpose(xw, len(xw) // newH)
        newH = len(xw) // newH
    newH = len(xw) // (width + 2)
    for turn in range(2):
        xw = re.sub(subRE, BLOCKCHAR*2, xw)
        xw = re. sub(subRE2, BLOCKCHAR*3, xw)
        xw = re.sub(subRE3, BLOCKCHAR+PROTECTEDCHAR*3, xw)
        xw = transpose(xw, len(xw) // newH)
        newH = len(xw) // newH
    new_board = ''
    for row in range (width+2, len(xw) - (width+2), width+2): 
        new_board += xw[row+1:width+row+1]
    new_board, count = make_palindrome(new_board)
    return new_board, new_board.count(BLOCKCHAR)

def csp(board, block_count, height, width):
    temp = [] 
    for b in board:
        if b != BLOCKCHAR and b != OPENCHAR:
            temp.append(PROTECTEDCHAR)
        else:
            temp.append(b)
    if (height*width == block_count):
        return BLOCKCHAR*len(board)
    if(height*width % 2 == 1 and block_count % 2 == 1):
        temp[len(board)//2] = BLOCKCHAR
    elif(height*width % 2 == 1 and block_count % 2 == 0):
        temp[len(board)//2] = PROTECTEDCHAR
    new_board = ''.join(temp)
    new_board, numblocks = make_palindrome(new_board)
    new_board, numblocks = csp_helper(new_board, width)
    if numblocks >= block_count:
        return readdwords(board, new_board)
    pos_list = [x for x in range(len(new_board)) if new_board[x] == OPENCHAR and new_board[len(new_board)-x-1] == OPENCHAR]
    temp_board, numblocks = add_helper(new_board, height, width, block_count, numblocks, pos_list)
    temp_board, numblocks = csp_helper(temp_board, width)
    while (check_illegal(temp_board, width, numblocks, block_count) == False or numblocks != block_count): 
        pos_list = [x for x in range(len(new_board)) if new_board[x] == OPENCHAR and new_board[len(new_board)-x-1] == OPENCHAR]
        temp_board, numblocks = add_helper(new_board, height, width, block_count, numblocks, pos_list)        
        temp_board, numblocks = csp_helper(temp_board, width)
    board = readdwords(board, temp_board)
    return board

def add_helper(board, height, width, numofblocks, currnum, pos_list):
    if currnum == numofblocks:
        return board, currnum
    print('pos list is:', pos_list)
    display(board, height, width)
    if(len(pos_list) == 0):
        return board, currnum
    pos1 = random.randint(0, len(pos_list) - 1)
    pos = pos_list[pos1]
    pos_list = pos_list[0:pos1] + pos_list[pos1+1:]
    board = board[0:pos] + BLOCKCHAR + board[pos+1:]
    new_board, currnum = csp_helper(board, width)
    print("New board", currnum)
    display(new_board, height, width)
    if(currnum > numofblocks):
        board = board[0:pos] + OPENCHAR + board[pos+1:]
        currnum = board.count(BLOCKCHAR)
    else:
        new_board, currnum = make_palindrome(new_board) 
        if currnum > numofblocks:
            board = board[0:pos] + OPENCHAR + board[pos+1:]
            currnum = board.count(BLOCKCHAR)
        else:
            board = new_board
    pos_list = [a for a in pos_list if board[a] == OPENCHAR]
    return add_helper(board, height, width, numofblocks, currnum, pos_list)


def readdwords(xword, new_x):
    l = list(new_x)
    for x in range(len(xword)):
        if xword[x] not in {BLOCKCHAR, PROTECTEDCHAR, OPENCHAR}:
            l[x] = xword[x]
    return ''.join(l)

def initialize(height, width, prefilled_words):
    xword = '-'*(height*width)
    for word in prefilled_words: 
        d, r, c, w = word
        r = int(r)
        c = int(c)
        w = w.upper()
        if d.lower() == 'h':
            start = r*width + c
            xword = xword[:start] + w + xword[start + len(w):]
        else:
            xword_list = list(xword)
            for i in range(len(w)):
                xword_list[(r+i)*width+c] = w[i]
            xword = ''.join(xword_list)
    return xword

def display(xword, height, width):
    print('\n'.join([xword[width*k:width*(k+1)] for k in range(height)]))

def clean_words(xword):
    xword = re.sub(r'\w', PROTECTEDCHAR, xword)
    return xword

def clean_protected(xword):
    xword = re.sub(PROTECTEDCHAR, OPENCHAR, xword)
    return xword

def make_palindrome(xword):
    xword_list, n = list(xword), len(xword)-1
    for i in range(len(xword_list)//2):
        if {xword_list[i], xword_list[n-i]} == {OPENCHAR, BLOCKCHAR}:
            xword_list[i], xword_list[n-i] = BLOCKCHAR, BLOCKCHAR
        elif {xword_list[i], xword_list[n-i]} == {OPENCHAR, PROTECTEDCHAR}:
            xword_list[i], xword_list[n-i] = PROTECTEDCHAR, PROTECTEDCHAR
        elif {xword_list[i], xword_list[n-i]} == {BLOCKCHAR, PROTECTEDCHAR}:
            return xword, len(xword)
    return (''.join(xword_list)), xword.count(BLOCKCHAR)


def make_xword(board, dictionary, height, width):
    pos_list = [x for x in range(len(board)) if board[x] == OPENCHAR]
    blist = list(board)
    line = [blist[x:x+width] for x in range(0, len(blist), width)]
    
    return board

def garanteed_start_positions(board, height, width, all_words):

    xw = BLOCKCHAR*(width+3)
    xw += (BLOCKCHAR*2).join([board[p:p+width] for p in range(0, len(board), width)])
    xw += BLOCKCHAR*(width+3)
    pattern = r'[{}]({}|\w)*(?=[{}])'.format(BLOCKCHAR, OPENCHAR, BLOCKCHAR)
    regex = re.compile(pattern)
    width_turn = [width+2, height+2]
    pos_word_list = [] # In your own way, fill this list or other type of data structure.
    for turn in range(2):
        for m in regex.finditer(xw): # finditer(subject) after compile → list of matches
            pos = 0
            word = xw[m.start()+1:m.end()]
            regex2 = re.compile('\\b' + word.replace(OPENCHAR, '\\w') + '\\b')
            if len(word)>0 and word.count(OPENCHAR) == 0 and turn == 0:
                pos_word_list.append([0, pos_list, 'H', word, []])
            elif len(word)>0 and word.count(OPENCHAR) == 0 and turn == 1:
                pos_word_list.append([0, pos_list, 'V', word, []])
            elif len(word)>0 and turn==0:
                candidates = all_words[len(word)]
                pos = ((m.start()+1)//(width+2)-1)*width + (m.start()+1) % (width+2) -1
                pos_list = [p for p in range(pos, pos+len(word))]
                pos_word_list.append([len(candidates), pos_list, 'H', word, candidates])
            elif len(word)>0 and turn == 1:
                candidates = all_words[len(word)]
                pos = (((m.start()+1) % (height+2))-1)*width + (m.start()+1)//(height+2)-1
                pos_list = [pos + p*width for p in range(len(word))]
                pos_word_list.append([len(candidates), pos_list, 'V', word, candidates])
    xw = transpose(xw, width_turn[turn])
    for item in pos_word_list:
        num_of_o = item[3].count(OPENCHAR)
    return pos_word_list, all_words

def main():
    number_of_blocks, height, width, prefilled_words = 0,4,4, []
    dictl = []
    for arg in args:
        if os.path.isfile(arg):
            dictl = open(arg, 'r').read().splitlines()
            continue
        if re.search(r'^\d+$', arg):
            number_of_blocks = int(arg) 
        elif re.search(r'^\d+x\d+$', arg, re.I):
            x = arg.lower().index('x')
            height = int(arg[:x])
            width = int(arg[x+1:])
        elif re.search(r'^[vh]\d+x\d(\w*|#|#\w*#|##\w*|\w*#\w*)?', arg, re.I):
            match = re.search(r'^(v|h)(\d+)x(\d+)(\w*|#|#\w*#|##\w*|\w*#\w*)?$', arg, re.I)
            if match != None:
                direction = match.group(1)
                row, col, word_or_block = match.group(2), match.group(3), match.group(4)
                prefilled_words.append((direction, row, col, word_or_block))
    xword = initialize(height, width, prefilled_words)

    dictlen = {}
    for x in dictl:
        dictlen[len(x)] = x
    print(dictlen)

    #display(xword, height, width)
    newone = csp(xword, number_of_blocks, height, width)
    #display(newone, height, width) 
    newone = clean_protected(newone)
    display(newone, height, width)
    finalb = make_xword(newone, dictlen, height, width)
    display(finalb, height, width)
    start_pos_list, all_words = garanteed_start_positions(finalb, height, width, dictl)
    for each in start_pos_list:
        print (each)
    board = make_xword(finalb, height, width, start_pos_list, all_words)
    display(board, height, width)



if __name__ == "__main__":
    main()

#Vihaan Mathur Period 7 2023

