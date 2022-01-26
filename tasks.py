from typing import List
from board import Board
from warband import Warband
from celery_local import app
import redis
import pickle


@app.task
def add(x, y):
    return y + x


@app.task
def perform_simulation(warbands_pickle, iterations: int):
    warband1 = pickle.loads(warbands_pickle[0])
    warband2 = pickle.loads(warbands_pickle[1])
    warbands = [warband1, warband2]
    results = [0] * 4
    results[3] = iterations
    for _ in range(iterations):
        board = Board(warbands[1], warbands[0])
        outcome = board.battle()
        results[outcome[0]] += 1
    return results
