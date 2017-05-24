import numpy as np
from matplotlib import pyplot as plt
from itertools import cycle
import sys

from config import pid_noConcussion, pid_3stepProtocol, pid_testRetest, pid_concussion, feature_functions, epoch_size, \
    embedding_args, pid_testlist, channels
from patient import Patient
from embedding import Embedding

colors = cycle(['r', 'b', 'g', 'y', 'c', 'm', 'k'])


def embed_and_plot(emb, examples):
    pre_post_distances = []
    alpha = 0.5 / np.log(len(examples)) if len(examples) > 1 else 1
    for tup in examples:
        if sys.version_info < (3, 0):
            # for python2 use
            color = colors.next()
        else:
            # for python3 use
            color = next(colors)
        pid = tup[0]
        pre_emb = emb.embed(tup[1])
        post_emb = emb.embed(tup[2])
        plt.plot(pre_emb[:, 0], pre_emb[:, 1], linestyle='None', marker="x", color=color, label=str(pid) + "_pre", alpha=alpha)
        plt.plot(post_emb[:, 0], post_emb[:, 1], linestyle='None', marker="o", color=color, label=str(pid) + "_post", alpha=alpha)
        # calculate centriods and plot a line
        pre_cent = centroid(pre_emb)
        post_cent = centroid(post_emb)
        plt.plot([pre_cent[0], post_cent[0]], [pre_cent[1], post_cent[1]], '-', linewidth=3, color=color)
        # record distance
        pre_post_distances.append(np.linalg.norm(post_cent - pre_cent))
    return pre_post_distances


def centroid(data):
    length = len(data)
    x_sum = np.sum(data[:, 0])
    y_sum = np.sum(data[:, 1])
    return np.array([float(x_sum)/length, float(y_sum)/length])

# get training data from un-concussed individuals
noCon_ex= []
step_ex = []
retest_ex = []
con_ex =[]

n_keep = -1

# for lst, pat_list in zip([pid_noConcussion, pid_3stepProtocol, pid_testRetest, pid_concussion], [noCon_pats, step_pats, retest_pats, con_pats]):
#for lst, pat_list in zip([pid_noConcussion], [noCon_pats]):
for pid in pid_noConcussion:
    print("Processing pid: {}".format(pid))
    p = Patient(pid, load_session_raw=False, load_session_examples=True)
    # get examples from pre_test
    post = None
    # get examples from post_test
    if p.post_test is not None:
        post = p.post_test.load_examples()
        if post is not None:
            np.random.shuffle(post)
    if post is not None:
        noCon_ex.append((pid, post))

for pid in pid_concussion:
    print("Processing pid: {}".format(pid))
    p = Patient(pid, load_session_raw=False, load_session_examples=True)
    # get examples from pre_test
    post = None
    # get examples from post_test
    if p.post_test is not None:
        post = p.post_test.load_examples()
        if post is not None:
            np.random.shuffle(post)
            post = post[:n_keep]
    if post is not None:
        con_ex.append((pid, post))

# create training data
train_data = np.vstack([tup[1][:n_keep] for tup in noCon_ex] +
                       [tup[1][:n_keep] for tup in con_ex])
# create and train embedding
emb = Embedding(**embedding_args)
emb.train(train_data)

# visualize embedding
nocon_distances = embed_and_plot(emb, noCon_ex)
plt.title("No concussion, pre/post test centroid distance")
plt.legend()
plt.show()
plt.savefig()
con_distances = embed_and_plot(emb, con_ex)
plt.title("Concussion, pre/post test centroid distance")
plt.legend()
plt.show()

plt.hist(nocon_distances)
plt.title("No concussion, pre/post test centroid distance")
plt.show()
plt.hist(con_distances)
plt.title("Concussion, pre/post test centroid distance")
plt.show()