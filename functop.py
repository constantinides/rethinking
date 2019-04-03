# functop - experiment to determine ability to separate Boolean function from topology when meeting Lipschitz condition

lipschitzbound = 2  # the max allowable change in output metric due to a change of one in input metric

# CSV file for storing biadjacency
adjfile = open("biadj.csv","w")

# All useful two-input Boolean functions, i.e. those where the output does not only depend on zero or one inputs
usefulfuncs = [
    # first those with one minterm
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0],
    # now those with two minterms
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    # finally those with three minterms
    [0, 1, 1, 1],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 0]
]

numfuncs = len(usefulfuncs)
outputs = [0]*8;
total_successes = 0;
successrecord = [0]*numfuncs*numfuncs*numfuncs*numfuncs;

for funcasumindex in range(numfuncs):
    funcasum = usefulfuncs[funcasumindex];

    for funcacarryindex in range(numfuncs):
        funcacarry = usefulfuncs[funcacarryindex];

        for funcbsumindex in range(numfuncs):
            funcbsum = usefulfuncs[funcbsumindex];

            for funcbcarryindex in range(numfuncs):
                funcbcarry = usefulfuncs[funcbcarryindex];

                for inputword in range(8):
                    # extract the primary inputs
                    cin = (inputword >> 2) & 0b01;
                    a1 = (inputword >> 1) & 0b01;
                    a0 = (inputword) & 0b01;

                    # simulate the circuit
                    s1 = funcasum[(cin << 1) | a1];
                    cinternal = funcacarry[(cin << 1) | a1];
                    s0 = funcbsum[(cinternal << 1) | a0];
                    cout = funcbcarry[(cinternal << 1) | a0];
                    outputword = (s1 << 2) | (s0 << 1) | cout;

                    # record the result
                    outputs[inputword] = outputword;
                    
                # now check whether this function meets the metric requirements
                successflag = 1;
                for inputword in range(7):
                    if abs(outputs[inputword] - outputs[inputword+1]) > lipschitzbound:
                        successflag = 0;
                
                adjfile.write(str(successflag));
                adjfile.write(", ")
                if successflag == 1:
                    total_successes = total_successes + 1;

        
        adjfile.write('\n') #newline for new A function

print ("Total functions meeting metric criteria: ", total_successes, " out of ", numfuncs*numfuncs*numfuncs*numfuncs);

