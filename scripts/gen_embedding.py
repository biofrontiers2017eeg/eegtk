import numpy as np
from matplotlib import pyplot as plt
from itertools import cycle
import sys

from config import pid_noConcussion, pid_3stepProtocol, pid_testRetest, pid_concussion, feature_functions, epoch_size, \
    embedding_args, pid_testlist
from patient import Patient
from embedding import Embedding

def centroid(data):
    length = len(data)
    x_sum = np.sum(data[:, 0])
    y_sum = np.sum(data[:, 1])
    return np.array([float(x_sum)/length, float(y_sum)/length])

# get training data from un-concussed individuals
noCon_pats= []
step_pats = []
retest_pats = []
con_pats =[]
# for lst, pat_list in zip([pid_noConcussion, pid_3stepProtocol, pid_testRetest, pid_concussion], [noCon_pats, step_pats, retest_pats, con_pats]):
#for lst, pat_list in zip([pid_noConcussion], [noCon_pats]):
for lst, pat_list in zip([pid_testlist], [noCon_pats]):
    for pid in lst:
        print("Processing pid: {}".format(pid))
        p = Patient(pid)
        # get examples from pre_test
        if p.pre_test is not None:
            p.pre_test.remove_artifacts()
            p.pre_test.get_examples(feature_functions, epoch_size=epoch_size)
        # get examples from post_test
        if p.post_test is not None:
            p.post_test.remove_artifacts()
            post = p.post_test.get_examples(feature_functions, epoch_size=epoch_size)
        if p.pre_test is not None and p.post_test is not None:
            pat_list.append(p)
# create training data
train_data = np.vstack([p.pre_test.examples for p in noCon_pats if p.pre_test is not None] +
                       [p.post_test.examples for p in noCon_pats if p.post_test is not None])
# create and train embedding
emb = Embedding(**embedding_args)
emb.train(train_data)


# visualize embedding
colors = cycle(['r', 'b', 'g', 'y'])
pre_post_distances = []
for p in noCon_pats:
    if (sys.version_info < (3,0)):
        # for python2 use
        color = colors.next()
    else:
        # for python3 use
        color = next(colors)

    pre_emb = emb.embed(p.pre_test.examples)
    post_emb = emb.embed(p.post_test.examples)
    plt.plot(pre_emb[:, 0], pre_emb[:, 1], linestyle='None', marker="x", color=color, label=p.pid + "_pre")
    plt.plot(post_emb[:, 0], post_emb[:, 1], linestyle='None', marker="o", color=color, label=p.pid + "_post")
    # calculate centriods and plot a line
    pre_cent = centroid(pre_emb)
    post_cent = centroid(post_emb)
    plt.plot([pre_cent[0], post_cent[0]], [pre_cent[1], post_cent[1]], '-', linewidth=4, color=color)
    # record distance
    pre_post_distances.append(np.linalg.norm(post_cent - pre_cent))
plt.legend()
plt.show()

plt.hist(pre_post_distances)
plt.show()