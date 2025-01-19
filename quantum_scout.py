#Library imports
import copy
import requests
import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import pandas as pd
from analysis import QuantumDistribution

#Global variables
KEY = "sTj4kOOM9vEIoeSHCUYq6G7nSgpznXH7Bi1PXe0ZOR5uwRpEjzb4c1qILhZuzwVN"
SHOTS = 10000
TEAM1 = 2363
TEAM2 = 1731
TEAM3 = 2421
EVENT = "2024vafal"


def get_scores_from_event(team, event, num_matches=12):
    """
    Gets the scores from the matches a team participated in at an event to convert to binary 
    for use in score_conversion.

    Args:
        team (int): the team number to get scores of (ex. 4472)
        event (str): the event code to get the scores from (ex. 2024vafal)
        num_matches (int): the number of qual matches to return (1-12 only)

    Returns:
        List[str]: a list of strings that are the binary form of the gotten scores
    """
    global KEY
    team_id = f"frc{team}"
    team_data = requests.get("https://www.thebluealliance.com/api/v3/team/"+team_id+"/event/"+event+"/matches/simple?X-TBA-Auth-Key="+KEY).json()
    team_data = [match for match in team_data if match["comp_level"] == "qm"]
    team_scores = []
    for match in range(len(team_data)):
        val = team_data[match]["alliances"]["red"]["score"] if team_id in team_data[match]["alliances"]["red"]["team_keys"] else team_data[match]["alliances"]["blue"]["score"]
        team_scores.append(f"{val:07b}")
    return team_scores[:num_matches]

def convert_list_2d(data):
    """
    converts a 1d list of str values to a 2d list of ints to make summation of
    columns easier in the score_conversion function

    Args:
        data (List[str]): the list fo binary values

    Returns:
        np.matrix[int]: a 2d list containing the split binary values as each row 
    """
    return np.matrix([list(item) for item in data], dtype=np.int8)

def score_conversion(team1, team2, team3, event, matches_complete=12):
    """
    Converts the scores of the three teams to binary, sums them, and converts them to values
    between 0 and pi. This will be used in the quantum circuit to effect the probability
    of getting certain bitstrings from measurement

    Args:
        team1 (int): the number of a team (ex. 4472)
        team2 (int): the number of a team
        team3 (int): the number fo a team
        event (str): the event code to pull data from (ex. 2024vafal)
        matches_complete (int, optional): represents the total number of matches to include. Defaults to 12.

    Returns:
        List[float]: returns the thetas to be used in quantum circuit construction
    """
    scores = np.zeros((7,), dtype=np.int8)
    team1_vals = convert_list_2d(get_scores_from_event(team1, event, matches_complete)).tolist()
    team2_vals = convert_list_2d(get_scores_from_event(team2, event, matches_complete)).tolist()
    team3_vals = convert_list_2d(get_scores_from_event(team3, event, matches_complete)).tolist()
    scores = scores + np.sum(team1_vals, axis=0) + np.sum(team2_vals, axis=0) + (np.sum(team3_vals, axis=0))
    print(scores)
    thetas = (scores/(3*(matches_complete)))*np.pi
    print(thetas)
    return thetas 

def make_circuit(thetas):
    """
    Generates a quantum circuit to calculate alliance score predictions from a given set
    of thetas made from the score_conversion function

    Args:
        thetas (List[float]): a list containing values that range from 0 to pi

    Returns:
        QuantumCircuit: the fully constructed circuit
    """
    qc = QuantumCircuit(len(thetas))
    for i, val in enumerate(thetas):
        qc.rx(val, i)
    qc.measure_all()
    return qc


    
if __name__ == "__main__":
    # Construct and show the Quantum circuit
    algo = make_circuit(score_conversion(TEAM1, TEAM2, TEAM3, EVENT, 8))
    algo.draw("mpl")
    plt.show()
    
    # Transpile for simulator
    simulator = AerSimulator()
    circ = transpile(algo, simulator)

    # Run and get counts
    result = simulator.run(circ, shots=SHOTS).result()
    counts = result.get_counts(circ)
    print(counts)
    
    #printing out odds for certain ranges
    dist = QuantumDistribution(counts, SHOTS, TEAM1, TEAM2, TEAM3)
    key_vals = list(dist.from_binary(counts).keys())
    key_vals.sort()
    dist.plot()
    print(len(key_vals))
    print(len(list(counts.keys())))
    print(key_vals)
    print(dist.cdf(-1, 100))
    print(dist.cdf(50, -1))
    print(dist.cdf(0, 127))