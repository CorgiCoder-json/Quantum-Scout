import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class QuantumDistribution:
    """
    This class represents a distribution that was created from 
    a quantum computer. this distirbution can be found from the circuit creation
    in quantum_scout.py
    """
    def __init__(self, count_set, shots, team1, team2, team3):
        """
        Runs the creation code. converts the counts to actual distribution
        and allows for easy graphing

        Args:
            count_set (Dictionary): The output from a quantum computer or simulator
            shots (int): The number of shots used on the computer
            team1 (str): One team on the allinace the scores comes from
            team2 (str): Another team on the alliance the scores come from
            team3 (str): Another team on the alliance the scores come from
        """
        self.counts_data = self._format(count_set, shots)
        self.team_1 = team1
        self.team_2 = team2
        self.team_3 = team3
    
    def from_binary(self, data):
        """
        Converts binary keys to integer values in a dictionary and sorts the result by key
        for easier interpretibility of quantum circuit results

        Args:
            data (dictionary): the data dictionary with keys in binary format

        Returns:
            dictionary: a sorted by key dictionary with integer values as keys
        """
        new_dict = {}
        for key, val in data.items():
            new_dict.update({int(key[::-1], 2): val})
        temp_keys = list(new_dict.keys())
        temp_keys.sort()
        new_dict = {i: new_dict[i] for i in temp_keys}
        return new_dict
    
    def _format(self, counts, shots):
        """
        Rescales the binary counts to numerical values and converts
        the counts into actual probabillity values for the pdf as cdf
        functions.
        
        THIS FUNCTION SHOULD ONLY BE USED IN __init__!

        Args:
            counts (Dictionary): the output of a quantum computer/simulator
            shots (int): the number of shots used when running the computer/simulation 

        Returns:
            pandas.Series: The formatted set of numbers and probabilities
        """
        formatted_counts = self.from_binary(counts)
        new_counts = pd.Series(formatted_counts)
        new_counts = (new_counts/shots)*100
        return new_counts
    
    def pdf(self, val):
        """
        Find the probability of a certain value in the counts. Returns 0 if not found

        Args:
            val (int): Some integer value representing the score you want to find the probability of

        Returns:
            float: The probability of the val in the distribution
        """
        try:
            return self.counts_data[val]
        except:
            print(f"The value {val} is not in the distribution!")
            return 0
        
    def cdf(self, start, end):
        """
        Finds the cumulative probabillity between two values [start, end]. -1 for start
        sums all probabillities from the start, and -1 for the end would sum everything up until 
        that point starting at 0.

        Args:
            start (int): The first value to sum probabillities from
            end (int): The final value to sum probabillities from

        Returns:
            float: The cumulative probabillity
        """
        sum = 0
        if end == -1:
            for key in self.counts_data.to_dict():
                if key < start:
                    continue
                else:
                    sum += self.pdf(key)
        elif start == -1:
            for key in self.counts_data.to_dict():
                if key == end:
                    break
                else:
                    sum += self.pdf(key)
        else:
            for key in self.counts_data.to_dict():
                if key < start:
                    continue
                elif key == end:
                    break
                else:
                    sum += self.pdf(key)
        return sum
    
    def plot(self):
        """
        Plots and shows the calculated distribution
        """
        self.counts_data.plot()
        plt.title(f"{self.team_1} + {self.team_2} + {self.team_3} Score Distribution")
        plt.show()         