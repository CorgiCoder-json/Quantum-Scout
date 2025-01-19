# Quantum Scout

## Purpose?
This algorithm attempts to find the probability of an alliance scoring some value by leveraging previous score values bit strings. See how it works for a deep dive on the algorithm. For this type of activity, this is probably overkill, but this is meant to experiment with quantum computing on something I am more framiliar with. 

## How it works

Theory:
- Every integer can be represented in a binary format
- FRC match scores are integers
- By counting the number of bits that are 1 in each place, we can see that some digits appear more than others
- We can leverage this by converting these amounts into rotations from 0-pi (see score conversion)
- then, initialize the qubits all to state 000...0
- Apply an RX gate for each theta on each qubit. This will give a probability of a certain bit being 1 or 0, allowing for many bitstrings to be concurrently "checked" simultaneously.
- So when we measure the result of the qubits, certain bitstrings will appear more than others, this resulting in our prediction

Score conversion:
1. Get the scores of each of the members of an alliance.
2. Convert those numbers to their binary representations (make sure all are the same length)
3. count the number of 1s in each place 
4. Divide each result by (# of matches used * 3), then multiply by pi to get theta values 

Key note: RX(pi) forces qubit to |1> state, RX(0) forces qubit to |0> state 

Quantum Circuit:
1. Initialize all qubits to |0> state
2. apply RX(theta) to each qubit, where theta is equal to one of the values previously scaled
3. Read the output to a classical register

Results:
1. run with decent number of shots (4000 should be fine)
2. plot the amount of times a bit string is produced

## Some notes

1. Sometimes a number will not appear in a given distribution. This can be for 1 of two reasons:

    1) The shot count is low (won't get multiple attempts to find the number given a low probability)
    2) The probability is so low that it is basically zero
    
The second option is more likely depending on what value of theta is in the RZ gate. The closer to zero a theta is, the more likely a qubit is to get 0 over one, even though it still is possible.

## Analysis

So there are two parts to this algorithm: the preprocessing, and the prediction. Since preprocessing happens in both algorithms, we don't need to worry about that part. The only reason this may come into effect is if the preprocessing for the classical case is faster, but I think that the only reason it would be faster is because it doesn't have the extra step of converting the calculated totals to values scaled from 0-pi, which is a small speedup. For now, this will only focus on the actual prediction algorithm. My thought process is, assuming some classical function f(x) that runs in O(1) time to do the same thing the quantum algorithm does, there is still an O(n) performance in the classical case, since it would need to go through all of the values between 0-[max score]. Since the quantum algorithm predicts all possible answers at once, it technically runs in O(1), making the speedup provided by the quantum computer AT WORST linear. Worth it? I don't know, but it is pretty neat.

## Other Use cases
This algorithm can actually be applied to any set of integers from a given population. I don't know about the efficacy of smaller sample sizes, but the whole idea of the algorithm is to mimic the distribution that the sample may come from. In my opinion, this quantum algorithm can be compared to the classical bootstrapping algorithm.

As of 1/18/2025: Having smaller sample sizes does effect outcome, but in the sense that if a score hasn't been seen yet, then it just won't add it. So in a way, this is a bootstrap-esk algorithm.