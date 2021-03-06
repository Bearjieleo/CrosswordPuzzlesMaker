import copy,sys,random

wordstring = "buckles,killed,rubato,collect,woodier,potluck,daubers,bloom,learned,honchos,euro,wisp,hexes,earl,mass,flanged,wads,hoods,cravens,tocsins,frown,satori,gasping,tritium,finesse,macho,sharked,torsion,serest,easels,layers,ganging,amuses,rusty,encored,ditties,wombs,unzips,subset,viewed,galls,gambles,gnostic,trots,avidly,loosely,sprint,gobs,dropsy,timothy,gowning,raged,cankers,fetus,thyself,portico,muckier,daring,only,chewy,colors,person,twinkly,chumps,filming,insofar,spore,remind,despot,soother,whiles,vastly,sprouts,bicycle,users,galling,clear,keener,baling,giro,bestows,termite,decking,tankers,gerunds,boxes,news,peso,outlay,theory,repulse,bocks,junks,dopers,icicle,accrue,fatter,flower,shank,keepers"

WORDPOOL = wordstring.split(',')
random.shuffle(WORDPOOL)
BOARD_SIZE = 33

class CRecord:
    def __init__(self, m_size,m_wordpool):
        self.indexTable = [set() for x in range(26)]
        self.board = [['-' for x in range(m_size)] for x in range(m_size)]
        self.dirFlag = [[0 for x in range(m_size)] for x in range(m_size)]
        self.wordpool = m_wordpool
        self.items = []


def ShowResult(record):
    output = ""
    symble = '.-|+'
    for i in record.board:
        for j in i:
            output += j
        output += "\n"
    for i in record.dirFlag:
        for j in i:
            output += symble[j]
        output += "\n"
    print output

def GetBiad(board):
    x = 0
    y = 0
    while True:
        for j in range(BOARD_SIZE):
            if board[x][j] != '-':
                break
        else:
            x += 1
            continue
        break
    while True:
        for j in range(BOARD_SIZE):
            if board[j][y] != '-':
                break
        else:
            y += 1
            continue
        break
    return [x,y]

def ExportResult(record):
    [x,y] = GetBiad(record.board)
    fid = open('result.txt','w')
    for item in record.items:
        fid.write('%s %d %d %s\n'%(item[0],item[1]-x+1,item[2]-y+1,('-' if item[3] else '|')))
    fid.close()

def FindPuzzle(record):
    ShowResult(record)
    ExportResult(record)
    sys.exit(0)

def SetBoard(record, word, i, j, IsRow):
    record_copy = copy.deepcopy(record)
    for (idx,ch) in enumerate(word):
        ci = i + (not IsRow)*idx
        cj = j + IsRow*idx
        record_copy.dirFlag[ci][cj] |= (0x01 if IsRow else 0x02)
        record_copy.board[ci][cj] = ch
        record_copy.indexTable[ord(ch)-ord('a')].add((ci,cj))
    record_copy.items.append([word,i,j,IsRow])
    if 0 == len(record_copy.wordpool):
        FindPuzzle(record_copy)
    return record_copy

def ValidCheck(record, word, i, j, IsRow):
    L = len(word)
    if i < 0 or j < 0:
        return False
    if IsRow and j + L - 1 >= BOARD_SIZE:
        return False
    if not IsRow and i + L - 1 >= BOARD_SIZE:
        return False
    if IsRow and j-1 >= 0 and record.board[i][j-1] != '-':
        return False
    if not IsRow and i-1 >= 0 and record.board[i-1][j] != '-':
        return False
    if IsRow and j+L < BOARD_SIZE and record.board[i][j+L] != '-':
        return False
    if not IsRow and i+L < BOARD_SIZE and record.board[i+L][j] != '-':
        return False
    for (idx,ch) in enumerate(word):
        ci = i + (not IsRow)*idx
        cj = j + IsRow*idx
        if record.board[ci][cj] != '-' and record.board[ci][cj] != ch:
            return False
        if record.board[ci][cj] == '-':
            if IsRow and ci-1 >= 0 and record.board[ci-1][cj] != '-' and record.dirFlag[ci-1][cj] & 0x02:
                return False
            if IsRow and ci+1 < BOARD_SIZE and record.board[ci+1][cj] != '-' and record.dirFlag[ci+1][cj] & 0x02:
                return False
            if not IsRow and cj-1 >= 0 and record.board[ci][cj-1] != '-' and record.dirFlag[ci][cj-1] & 0x01:
                return False
            if not IsRow and cj+1 < BOARD_SIZE and record.board[ci][cj+1] != '-' and record.dirFlag[ci][cj+1] & 0x01:
                return False
    return True

def Calculate(record, curWord, i, j, isrow):
    if ValidCheck(record, curWord, i, j, isrow):
        record_t = SetBoard(record, curWord, i, j, isrow)
        for word in record.wordpool:
            Iter(copy.deepcopy(record_t), word)

def RandomSort(l):
    random.shuffle(l)
    for i in l:
        yield i

def Iter(record, curWord):
    global WORDPOOL
    global BOARD_SIZE
    record.wordpool.remove(curWord)
    if len(record.wordpool) == len(WORDPOOL)-1:
        for isrow in RandomSort([True,False]):
            Calculate(record, curWord, (BOARD_SIZE-len(curWord)*(not isrow))//2, (BOARD_SIZE-len(curWord)*isrow)//2, isrow)
    else:
        for (idx, ch) in enumerate(curWord):
            for pos in RandomSort(list(record.indexTable[ord(ch)-ord('a')])):
                for isrow in RandomSort([True,False]):
                    Calculate(record, curWord, pos[0]-idx*(not isrow), pos[1]-idx*isrow, isrow)

if __name__ == "__main__":
    record = CRecord(BOARD_SIZE, WORDPOOL)
    for word in record.wordpool:
        Iter(copy.deepcopy(record), word)