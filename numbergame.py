import sys
import random

size = 4

def swipeUp(board):
	res = transform(zip(*board))
	res = [x+[0]*(size-len(x)) for x in res]
	return [list(x) for x in zip(*res)]

def swipeDown(board):
	res = transform(x[::-1] for x in zip(*board))
	res = [[0]*(size-len(x))+x for x in [y[::-1] for y in res]]
	return [list(x) for x in zip(*res)]

def swipeLeft(board):
	res = transform(board)
	return [x+[0]*(size-len(x)) for x in res]

def swipeRight(board):
	res = transform([x[::-1] for x in board])
	return [[0]*(size-len(x))+x for x in [y[::-1] for y in res]]

def transform(board):
	res = []
	for row in board:
		sub, pre = [], -1
		for v in filter(lambda x : x != 0, row):
			if pre == -1: 
				pre = v
			elif pre == v:
				sub.append(2*int(v))
				pre = -1
			else:
				sub.append(pre)
				pre = v
		if pre != -1: sub.append(pre)
		res.append(sub)
	return res

def cal(board):
	return sum([len(filter(lambda x: x != 0, r)) for r in board])



class Game(object):
	"""docstring for Game"""
	def __init__(self, board):
		self.board, self.step, self.move, self.maxnumber = board, 0, 'none', 4

	def generate(self, pos):
		self.board[int(pos[0])][int(pos[1])] = int(pos[2])

	def play(self, way):
		self.step += 1
		if way == 'w':   self.board, self.move = swipeUp(self.board), 'up'
		elif way == 's': self.board, self.move = swipeDown(self.board), 'down'
		elif way == 'a': self.board, self.move = swipeLeft(self.board), 'left'
		elif way == 'd': self.board, self.move = swipeRight(self.board), 'right'
		else:
			print 'wrong input direction - ' + way
			self.step -= 1
		self.maxnumber = max([self.board[x][y] for x in range(0,size) for y in range(0,size)])

	# def think(self):
	# 	o = [r[:] for r in self.board] 
	# 	l,r,u,d = swipeLeft(o),swipeRight(o),swipeUp(o),swipeDown(o)
	# 	if o == l == r == u == d: return 'e'
	# 	if l != o: return 'a'
	# 	if u != o: return 'w'
	# 	return 's' if cal(d) < cal(r) else 'd'

	def think(self):
		o = [r[:] for r in self.board]
		l,r,u,d = swipeLeft(o),swipeRight(o),swipeUp(o),swipeDown(o)
		if o == l == r == u == d: return 'e' 
		lc,rc,uc,dc = cal(l),cal(r),cal(u),cal(d)
		minC = min(lc,rc,uc,dc)
		if minC == lc: return 'a'
		if minC == rc: return 'd'
		if minC == uc: return 'w'
		if minC == dc: return 's'


	def random(self):
		possible = [(x,y) for x in range(0,size) for y in range(0,size) if self.board[x][y] == 0]
		return possible[random.randrange(0,len(possible))] + (random.choice([2,2,2,4]),) 

	def __str__(self):
		s = '====>>>> step {0} - {1} <<<<====\n'.format(self.step, self.move)
		s += '-'*26 + '\n'
		for row in self.board:
			s += '|'
			for c in row: s += '{:^6}'.format(str(c))
			s += '|\n'
		s += '-'*26 + '\n'		
		return s



def playGame(game, cmd):
	if len(cmd) != 2 or (cmd[1] != '-auto' and cmd[1] != '-manual'):
		print 'Wrong Command ! -auto or -manual'
		return
	f = open('gameResult','w')
	mode = sys.argv[1] == '-auto'
	if mode: f.write(str(game) + '\n')
	else: print game
	while True:
		c =  game.think() if mode else raw_input("please swipe:\nw. UP\ns. DOWN\na. LEFT\nd. RIGHT\ne. EXIT\n")
		if c == 'e': break
		game.play(c)
		if mode: f.write(str(game))
		else: print game
		pos = game.random() if mode else tuple(raw_input("input new number to empty slot ([0-3],[0-3],[2 or 4]): ").split(','))
		game.generate(pos)
		if mode:
			f.write('~~~~ generate {0} in ({1},{2}) ~~~~'.format(pos[2],pos[0],pos[1]) + '\n')
			f.write(str(game) + '\n')
		else:
			print '~~~~ generate {0} in ({1},{2}) ~~~~'.format(pos[2],pos[0],pos[1])
			print game
	f.close()
	print 'Good Bye ! Your best score is ' + str(game.maxnumber) + ' using ' + str(game.step) + ' steps'


if __name__ == '__main__':
	matrix = [
	    [0, 0, 0, 0],
	    [0, 0, 0, 2],
	    [0, 4, 0, 4],
	    [0, 2, 2, 0],
	]
	game = Game(matrix)
	playGame(game, sys.argv)
