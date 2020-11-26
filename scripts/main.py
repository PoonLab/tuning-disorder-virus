import pandas as pd
from Bio import SeqIO
from threading import Thread
import queue
import joblib

import pondrfit, pondr, cspritz, espritz, iupred

def combine(sequence):
    predictors = (iupred, pondr, espritz)
    q = queue.Queue()
    threads = []

    for pred in predictors:
        t = Thread(target= pred, args=(sequence, q))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return [q.get() for x in range(len(arguments))]

seqs = {}
fa_file = SeqIO.parse("floppytest.fa", "fasta") # Open file with metadata sequences

# Store sequence and ids in a dictionary
for seq_data in fa_file:
    seqs[seq_data.id] = seq_data.seq

for header, sequence in seqs.items(): #loop through proteins in fasta file - lim 25
    sequence_aa = sequence
    seq = ">" + header + "\n" + sequence + "\n"
    print(seq)

    combine(seq)


    """
    add iupred and spotdis
    """


    q = queue.Queue()
    if __name__ == "__main__":
        # create threads for each predictor
        t_iupred = threading.Thread(target=iupred, args= (seq, q))
        t_pondrfit = threading.Thread(target=pondrfit, args= (seq, q))
        t_pondr = threading.Thread(target=pondr, args= (seq, q))
        # t_disprot = threading.Thread(target=disprot, args= (seq,))
        # t_cspritz = threading.Thread(target=cspritz, args= (seq, q))
        t_espritz = threading.Thread(target=espritz, args= (seq, q))
        threads = [t_iupred, t_pondrfit, t_pondr, t_espritz]
        for t in threads:
            t.start() # start threads
        for t in threads:
            t.join()
        results = q.get()
        print("Finished collecting data for {}".format(seq))


    # protein = pd.DataFrame(
    #             [pondrfit, pondr[0], pondr[1], pondr[2], pondr[3], pondr[4], disprot[0], disprot[1], disprot[2],
    #             disprot[3], cspritz[0], cspritz[1], espritz[0], espritz[1], espritz[2]])
    protein = pd.DataFrame(
                [pondrfit, pondr[0], pondr[1], pondr[2], pondr[3], pondr[4], espritz[0], espritz[1], espritz[2]])

    # col_names = list(joblib.load('colnames.pkl'))[2:]
    # protein = pd.DataFrame(
    #             [spotdis, pondrfit, iupred[0]. iupred[1], pondr[0], pondr[1], pondr[2], pondr[3], pondr[4], disprot[0], disprot[1], disprot[2],
    #             disprot[3], cspritz[0], cspritz[1], espritz[0], espritz[1], espritz[2]],
    #             columns = col_names)
    #
    # # load the model from disk
    # loaded_model = joblib.load('disorder_rf.pkl')
    #
    # X = protein
    # sequence = sequence_aa
    #
    # predictions = loaded_model.predict(X)