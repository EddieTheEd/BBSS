class scriptManager:
    def __init__(self):
        self.scripts = [
            ['RNG', '''
import random as r
action = ''
choices = ['r','r','b','b b','s','ss'] # equal chances to reload, block or shoot
action += r.choice(choices)
if action == 's':
    action += ' '  
    alivePlayers = []
    for i in range(len(gamestate['players'])):
        if gamestate['players'][i].alive and i != playerNumber:
            alivePlayers.append(i)
    action += str(r.choice(alivePlayers)+1)
if action == 'ss':
    action += ' '  
    alivePlayers = []
    for i in range(len(gamestate['players'])):
        if gamestate['players'][i].alive and i != playerNumber:
            alivePlayers.append(i)
    action += str(r.choice(alivePlayers)+1)
    action += ' '  
    alivePlayers = []
    for i in range(len(gamestate['players'])):
        if gamestate['players'][i].alive and i != playerNumber:
            alivePlayers.append(i)
    action += str(r.choice(alivePlayers)+1)
'''],
            ['temp', '''
 
'''],
        ]
    

class player:
    def __init__(self, mode='RNG'):
        self.bullets = 0
        self.defense = 0
        self.shots = 0
        self.alive = True
        self.ai = mode
        self.action = None
    
    def pickAction(self, scripts, gamestate, pNum):
        for script in scripts:
            if self.ai == script[0]:
                action = None
                local = {'action': action, 'gamestate': gamestate, 'playerNumber': pNum}
                exec(script[1], globals(), local)
                return local['action']
    
    def reset(self):
        self.action = None
        self.shots = 0
        self.defense = 0

class BBSS:
    def __init__(self, players, scripts, pScripts=None):
        self.players = []
        for i in range(players):
            if pScripts:
                self.players.append(player(pScripts[i]))
            else:
                self.players.append(player())
        self.turn = 0
        self.remainingPlayers = players
        self.scripts = scripts
    
    def set(self, nPlayers, nTurn):
        self.players = nPlayers
        self.turn = nTurn

    def rules():
        return '''---------------------- BBSS avalaible moves ----------------------
r                     reload
b                     block
b b                   double block
s [player]            shoot player
ss [player] [player]  double shoot
Note: spacing and case is important
------------------------------------------------------------------'''

    def getInput(self, player, action):
        #action = input(f'Player {player+1} enter your move: ')
        if (action):
            self.players[player].action = action
            processed = action.split(' ')
            match processed[0]:
                case 'r': 
                    self.players[player].bullets += 1
                    self.players[player].defense = 0
                    #print(f'Player {player+1} reloads, you now have {self.players[player].bullets} bullets.')
                case 'b': 
                    self.players[player].defense = min(len(processed), 2)
                    #print(f'Player {player+1} defends against exactly {self.players[player].defense} bullets.')
                case 's': 
                    if (self.players[player].bullets >= 1):
                        self.players[int(processed[1])-1].shots += 1
                        self.players[player].bullets -= 1
                        #print(f'Player {player+1} shoots {self.players[processed[1]]}')
                    else:
                        self.players[player].shots += 69
                        #print(f'Player {player+1} shoots themselves')
                case 'ss':
                    if (self.players[player].bullets >= 2):
                        self.players[int(processed[1])-1].shots += 1
                        self.players[int(processed[2])-1].shots += 1
                        self.players[player].bullets -= 2
                        #print(f'Player {player+1} shoots {self.players[processed[1]]} and {self.players[processed[2]]}')
                    else:
                        self.players[player].shots += 69
                        #print(f'Player {player+1} shoots themselves')
        
    def simRound(self):
        for player in self.players:
            if (player.shots and player.shots != player.defense and player.alive):
                player.alive = False
                self.remainingPlayers -= 1

    def __str__(self):
        status = ''
        acts = ''
        for i in range(len(self.players)):
            status += f'Player {i+1} has {self.players[i].bullets} bullets, was shot {self.players[i].shots} times this round, blocked against {self.players[i].defense} shots, uses {self.players[i].ai} algorithm and is {"alive" if self.players[i].alive else "dead"}. \n'
            acts += f'Player {i+1} executed action {self.players[i].action} \n'
        return f'''
----------------------------------------------------------------- BBSS Game Review -----------------------------------------------------------------
Current Round: {self.turn}
Players Remaining: {self.remainingPlayers}
Player Statuses:
{status}

{acts}
----------------------------------------------------------------------------------------------------------------------------------------------------
'''

    def runGame(self, logging=True):
        while self.remainingPlayers > 1:
            self.turn += 1
            for player in self.players:
                player.reset()
            for i in range(len(self.players)):
                if self.players[i].alive:
                    self.getInput(i, self.players[i].pickAction(self.scripts, self.getGamestate(), i))
            self.simRound()
            if logging:
                print(self)
        if logging:
            print('Game Over')
    
    def step(self, logging=True):
        if self.remainingPlayers > 1:
            self.turn += 1
            for player in self.players:
                player.reset()
            for i in range(len(self.players)):
                if self.players[i].alive:
                    self.getInput(i, self.players[i].pickAction(self.scripts, self.getGamestate(), i))
            self.simRound()
            if logging:
                print(self)
        else:
            if logging:
                print('Game Over')

    def getGamestate(self):
        return {'players': self.players, 'round': self.turn, 'remainingPlayers': self.remainingPlayers}

# Testing Code
scripts = scriptManager()                                                            # create a new script manager
scripts.scripts.append(['terrorist', '''
import random as r
if gamestate['players'][playerNumber].bullets == 0:
    action = 'r'
else:
    action = 's '  
    alivePlayers = []
    for i in range(len(gamestate['players'])):
        if gamestate['players'][i].alive and i != playerNumber:
            alivePlayers.append(i)
    action += str(r.choice(alivePlayers)+1)
'''],)                                                                               # add the 'terrorist' script (alternate between reload and shoot)
scripts.scripts.append(['smart RNG', '''
import random as r
action = ''

choices = ['r','r','b','b b']
if gamestate['round'] == 1:
    choices = ['r']
if gamestate['players'][playerNumber].bullets >= 1:
    choices.append('s')
if gamestate['players'][playerNumber].bullets >= 2:
    choices.append('ss')
if gamestate['players'][playerNumber].bullets >= 3:
    choices = ['ss', 's']
action += r.choice(choices)
if action == 's':
    action += ' '  
    alivePlayers = []
    for i in range(len(gamestate['players'])):
        if gamestate['players'][i].alive and i != playerNumber:
            alivePlayers.append(i)
    action += str(r.choice(alivePlayers)+1)
if action == 'ss':
    action += ' '  
    alivePlayers = []
    for i in range(len(gamestate['players'])):
        if gamestate['players'][i].alive and i != playerNumber:
            alivePlayers.append(i)
    action += str(r.choice(alivePlayers)+1)
    action += ' '  
    alivePlayers = []
    for i in range(len(gamestate['players'])):
        if gamestate['players'][i].alive and i != playerNumber:
            alivePlayers.append(i)
    action += str(r.choice(alivePlayers)+1)
'''],)                                                                               # smarter RNG bot that does not self unalive
newGame = BBSS(3, scripts.scripts)                                                   # create a game
print(BBSS.rules())                                                                  # print the rules of BBSS
#print(newGame)                                                                      # print the current gamestate
#print(newGame.getGamestate())                                                       # print the data that scripts get access to
#newGame.step()                                                                      # run 1 round of the game
newGame.runGame()                                                                    # run game until completion


