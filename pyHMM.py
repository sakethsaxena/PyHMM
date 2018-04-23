import json
import os
import sys
from largeNumCalc import LargeNumberHandler
from math import log
import operator
from collections import Counter

class HMM:

    def __init__(self, sequence, hmm):        
        self.sequence = sequence
        self.hmm = self.read_model(hmm)

    # adjust probs for outgoing delete states
    def find_consecutivedels(self,index,sequence):
        if index < len(sequence):
            if sequence[index] == "-":
                return self.find_consecutivedels(index+1,sequence)
        return index       

    def viterbi_algorithm(self):
        
        max_prob = 0
        # write new viterbi based on new model
        # return max path and max probability
        
        # for sequence of same length or "aligned  and shorter"
        if len(self.sequence) == len(self.hmm.keys())-2:
            # all reads match
            stIndex = 0
            while stIndex < len(self.sequence):
                char = self.sequence[stIndex]
                if char != '-':
                    max_prob += self.hmm[str(stIndex-1)]['transition'][str(stIndex)] * self.hmm[str(stIndex)]['emission'][char]
                    stIndex +=1
                else:

                    max_prob += self.hmm[str(stIndex)]['transition']['del']['outgoing'] + 1.0/self.hmm[str(stIndex)]['transition']['del']['otherstates']

                    stIndex = self.find_consecutivedels(stIndex+1,self.sequence)

            return max_prob

        elif len(self.sequence) > len(self.hmm.keys())-2:
            
            difference = len(self.sequence)-len(self.hmm.keys())
            stIndex = 0

            prob_1=c1  = 0
            prob_2=c2 = 0
            prob_3=c3  = 0

            # create three possible paths
            # start - mid - end
            while stIndex < len(self.sequence):
                
                char = self.sequence[stIndex]
                # start - first case
                if char != '-':
                    prob_1 += self.hmm[str(c1-1)]['transition'][str(c1)] * self.hmm[str(c1)]['emission'][char]
                    c1 += 1
                    if c1 < difference:
                        prob_1 += self.hmm[str(c1)]['transition']['insert'] * 1.0/21.0 * 0.99
                        c1 +=1
                    
                    prob_2 += self.hmm[str(c2-1)]['transition']['insert'] *self.hmm[str(c2)]['emission'][char]
                    c2 +=1

                    if c2 > 1/4 * len(self.sequence) and c2 < len(self.sequence)-difference:
                        prob_2 += self.hmm[str(c2)]['transition']['insert'] * 1.0/21.0 * 0.99
                        c2 +=1

                    prob_3 += self.hmm[str(c3-1)]['transition']['insert'] *self.hmm[str(c3)]['emission'][char]
                    c2 +=1

                    if c3 < len(self.sequence)-difference:
                        prob_3 += self.hmm[str(c3)]['transition']['insert'] * 1.0/21.0 * 0.99
                        c3 +=1
                    stIndex +=1 

                else:
                    prob_1 += self.hmm[str(stIndex)]['transition']['del']['outgoing'] + 1.0/self.hmm[str(stIndex)]['transition']['del']['otherstates']
                    prob_2 += self.hmm[str(stIndex)]['transition']['del']['outgoing'] + 1.0/self.hmm[str(stIndex)]['transition']['del']['otherstates']
                    prob_3 += self.hmm[str(stIndex)]['transition']['del']['outgoing'] + 1.0/self.hmm[str(stIndex)]['transition']['del']['otherstates']
                    stIndex = self.find_consecutivedels(stIndex+1,self.sequence)
                    c1 = c2 = c3 = stIndex

                return max([prob_1,prob_2,prob_3])


    def forward_algorithm(self):

        max_prob = "0"
        # write new viterbi based on new model
        # return max path and max probability
        arithIns = LargeNumberHandler()
        # for sequence of same length or "aligned  and shorter"
        if len(self.sequence) == len(self.hmm.keys())-2:
            # all reads match
            stIndex = 0
            while stIndex < len(self.sequence):
                char = self.sequence[stIndex]
                if char != '-':
                    max_prob = arthIns.large_num_add(str(max_prob),arthIns.large_num_mul(str(self.hmm[str(stIndex-1)]['transition'][str(stIndex)]),str(self.hmm[str(stIndex)]['emission'][char])))
                    stIndex +=1
                else:
                    max_prob = arthIns.large_num_add(str(max_prob),arthIns.large_num_add(str(self.hmm[str(stIndex)]['transition']['del']['outgoing']), str(1.0/self.hmm[str(stIndex)]['transition']['del']['otherstates'])))
                    stIndex = self.find_consecutivedels(stIndex+1,self.sequence)
            return max_prob

        elif len(self.sequence) > len(self.hmm.keys())-2:
            
            difference = len(self.sequence)-len(self.hmm.keys())
            stIndex = 0

            prob_1 = "0"
            prob_2 = "0"
            prob_3 = "0"
            max_prob = "0"
            c1 = c2 = c3 = 0

            # create three possible paths
            # start - mid - end

            while stIndex < len(self.sequence)-2 and c1 < len(self.sequence)-2 and c2 < len(self.sequence)-2 and c3 < len(self.sequence)-2:
                
                char = self.sequence[stIndex]

                # start - first case
 
              
                if char != "-":
                    try:
                        prob_1 = arithIns.large_num_add(prob_1, arithIns.large_num_mul(str(self.hmm[str(c1-1)]['transition']['insert']),str(self.hmm[str(c1)]['emission'][char])))
                        c1 +=1
                    except:
                        pass
                    if c1 < difference:
                        try:
                            prob_1 =arithIns.large_num_add(prob_1, arithIns.large_num_mul(str(0.99), arithIns.large_num_mul(str(self.hmm[str(c1)]['transition']['insert']), str(1.0/21.0))))
                            c1 +=1
                        except:
                            pass

                    try:
                        prob_2 = arithIns.large_num_add(prob_2, arithIns.large_num_mul(str(self.hmm[str(c2-1)]['transition']['insert']),str(self.hmm[str(c2)]['emission'][char])))
                        c2 +=1
                    except:
                        pass

                    if c2 > 1/4 * len(self.sequence) and c2 < len(self.sequence)-difference:
                        try:
                            prob_2 =arithIns.large_num_add(prob_2, arithIns.large_num_mul(str(0.99), arithIns.large_num_mul(str(self.hmm[str(c2)]['transition']['insert']), str(1.0/21.0))))
                            c2 +=1
                        except:
                            pass
                    try:
                        prob_3 = arithIns.large_num_add(prob_3, arithIns.large_num_mul(str(self.hmm[str(c3-1)]['transition']['insert']),str(self.hmm[str(c3)]['emission'][char])))
                        c3 +=1
                    except:
                        pass

                    if c3 < len(self.sequence)-difference:
                        try:
                            prob_3 =arithIns.large_num_add(prob_3, arithIns.large_num_mul(str(0.99), arithIns.large_num_mul(str(self.hmm[str(c3)]['transition']['insert']), str(1.0/21.0))))
                            c3 +=1
                        except:
                            pass
                    stIndex +=1
                else:
                    try:
                        prob_1 =arithIns.large_num_add(prob_1, arithIns.large_num_mul(self.hmm[str(c1)]['transition']['del']['outgoing'], str(1.0/self.hmm[str(c1)]['transition']['del']['otherstates'])))
                        prob_2 =arithIns.large_num_add(prob_2, arithIns.large_num_mul(self.hmm[str(c2)]['transition']['del']['outgoing'], str(1.0/self.hmm[str(c2)]['transition']['del']['otherstates'])))
                        prob_3 =arithIns.large_num_add(prob_3, arithIns.large_num_mul(self.hmm[str(c3)]['transition']['del']['outgoing'], str(1.0/self.hmm[str(c3)]['transition']['del']['otherstates'])))
                    except:
                        pass

                    stIndex = self.find_consecutivedels(stIndex+1,self.sequence)

                    c1=c2=c3=stIndex

                max_prob = arithIns.large_num_add(prob_1, arithIns.large_num_add(prob_2, prob_3))

            return max_prob

    def read_model(self,model_file):
        with open(model_file) as input_file:
            return json.load(input_file)



def parse_data_file(data_file):
    
    rows = []

    with open(data_file) as aligned_input_file:

        sequence = []
        last_row = []
        for line in aligned_input_file:
            
            
            if line[0] =='>':
                rows.append(sequence)
                sequence = []
                continue
            else:
                line = list(line.strip())
                sequence = sequence + line
            last_row = sequence

        rows.append(last_row)

    return zip(*rows[1:]),rows[1:]

def generate_model(data_file):
    
    aas = ['A','R','N','D','B','C','E','Q','Z','G','H','I','L','K','M','F','P','S','T','W','Y','V']
    states, rows = parse_data_file(data_file) # this contains a list of tuples each list containing the emissions in first column


    no_of_states = len(states)
    model = {}

    model[-1] = {} # start state
    model[-1]['transition'] = {}
    model[no_of_states] = {} # end state



    for stIndex, state in enumerate(states):

        model[stIndex] = {}
        model[stIndex]['transition'] = {}
        model[stIndex]['emission'] = {}

        model[stIndex]['transition']['del'] = {}
        model[stIndex]['transition']['del']['outgoing'] = 0

        # update this outside in another pass
        model[stIndex]['transition']['del']['otherstates'] = 1
        
        model[stIndex]['transition']['insert'] = 0


        emission_freqs = Counter(state)
        del_flag = 0
        # adjust freqs for unemitted aas
        for emm in aas:
            if emm not in emission_freqs.keys():
                emission_freqs[emm] = 1
        
        no_of_emissions = sum(emission_freqs.values())
        
        for emission, freq in emission_freqs.items():            

            if emission == '-':                
                model[stIndex]['transition']['del']['outgoing'] = freq/no_of_emissions
                model[stIndex]['transition']['del']['otherstates'] = 0
                del_flag = 1
            else:
                model[stIndex]['emission'][emission] = freq/no_of_emissions

        if del_flag == 1:
            model[stIndex]['transition'][stIndex+1] = 1 - model[stIndex]['transition']['del']['outgoing']        
            # if in insert state since it either goes back to itself or goes to the immediate next transition 
            # for the outgoing transition and emission probs just model it into your Fa/ viterbi algos
            model[stIndex]['transition']['insert'] = 0.01*(model[stIndex]['transition'][stIndex+1]+model[stIndex]['transition']['del']['outgoing'])        
            model[stIndex]['transition']['del']['outgoing'] = model[stIndex]['transition']['del']['outgoing'] - (model[stIndex]['transition']['insert']/2.0)
            model[stIndex]['transition'][stIndex+1] = model[stIndex]['transition'][stIndex+1]- (model[stIndex]['transition']['insert']/2.0)
        else:
            model[stIndex]['transition'][stIndex+1] = 0.99
            model[stIndex]['transition']['insert'] = 0.01
    
    model[-1]['transition'][0] = 1 - model[1]['transition']['del']['outgoing']
    model[-1]['transition']['insert'] = 0.01*(model[1]['transition']['del']['outgoing']+model[-1]['transition'][0])
    
    model[-1]['transition'][0] -= model[-1]['transition']['insert']/2.0
    model[1]['transition']['del']['outgoing'] -= model[-1]['transition']['insert']/2.0

    # adjust probs for outgoing delete states
    def find_consecutivedels(index,sequence):

        if index < len(sequence):
            if sequence[index] == "-":
                return find_consecutivedels(index+1,sequence)
        
        return index                
        
    for seqID,sequence in enumerate(rows):

        if "-" not in sequence:
            continue

        for stIndex,element in enumerate(sequence):
            if element == "-":                                    
                noOutgoing = 0
                noOutgoing = find_consecutivedels(stIndex+1, sequence)
                noOutgoing = noOutgoing - stIndex
                if noOutgoing > model[stIndex]['transition']['del']['otherstates']:
                    model[stIndex]['transition']['del']['otherstates'] = noOutgoing


    with open('result.json', 'w') as fp:
        json.dump(model, fp)




if __name__ == "__main__":

    sequence = sys.argv[1]
    model_file = sys.argv[2]
    # generate_model(model_file)
    throw_away, sequences = parse_data_file(sequence)
    results = ["Viterbi Scores \t Forward Algorithm Scores\n"]

    
    for sequence in sequences:
        testHmm = HMM(sequence,model_file)
        results.append(str(testHmm.viterbi_algorithm())+"\t"+testHmm.forward_algorithm()+"\n")

    with open("long_results.txt","a+") as output_file:

        for result in results:
            output_file.write(result)


