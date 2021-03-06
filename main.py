import logging
import time
import hanasim.hanasim as hs
# import agents.cheater_discard_random as agent
import agents.cheater_smart as agent

import pandas as pd
import numpy as np

# Number of cards each player has in their hand
HANDSIZE = {2: 5,
            3: 5,
            4: 4,
            5: 4}

# Configure logger
logLevel = logging.DEBUG

formatter = logging.Formatter('%(levelname)s:%(message)s')
fh = logging.FileHandler(filename='hanabi.log', mode='w')
fh.setLevel(logLevel)
fh.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logLevel)
logger.addHandler(fh)

# Set up game
nPlayers = 2
handSize = HANDSIZE[nPlayers]
seed = 0
game = hs.GameState(nPlayers, handSize, seed, logger=None)
game.setup()

# Set up players
players = [agent.Agent(ii, game) for ii in range(nPlayers)]

N = 100
scores = np.zeros(N)
times = np.zeros(N)
for i in range(N):
    ply = 0
    tic = time.perf_counter()
    while (not game.isOver):
        turn = ply % nPlayers
        ply=ply+1
        move = players[turn].findMove()
        game.doMove(move)

    toc = time.perf_counter()
    scores[i] = game.score
    times[i] = toc-tic
    game.reset()
    game.setup()

df = pd.DataFrame({'Scores': scores})
print(df.describe())

dfTime = pd.DataFrame({'Time': times})
print(dfTime.describe())

