import numpy as np
from matplotlib import pyplot as plt
from itertools import cycle
import sys

from config import pid_noConcussion, pid_3stepProtocol, pid_testRetest, pid_concussion, feature_functions, epoch_size, \
    embedding_args, pid_testlist, channels, subfolder
from patient import Patient
from embedding import Embedding

colors = cycle(['r', 'b', 'g', 'y', 'c', 'm', 'k'])


def embed_and_plot(emb, examples, all_color=None, linewidth=2):
    pre_post_distances = []
    alpha = 0.2 / np.log(len(examples)) if len(examples) > 1 else 1
    for tup in examples:
        if all_color is None:
            if sys.version_info < (3, 0):
                # for python2 use
                color = colors.next()
            else:
                # for python3 use
                color = next(colors)
        else:
            color = all_color
        pid = tup[0]
        pre_emb = emb.embed(tup[1])
        post_emb = emb.embed(tup[2])
        plt.plot(pre_emb[:, 0], pre_emb[:, 1], linestyle='None', marker="x", color=color, label=str(pid) + "_pre", alpha=alpha)
        plt.plot(post_emb[:, 0], post_emb[:, 1], linestyle='None', marker="o", color=color, label=str(pid) + "_post", alpha=alpha)
        # calculate centriods and plot a line
        pre_cent = centroid(pre_emb)
        post_cent = centroid(post_emb)
        plt.plot([pre_cent[0], post_cent[0]], [pre_cent[1], post_cent[1]], '-', linewidth=linewidth, color=color)
        # record distance
        pre_post_distances.append(np.linalg.norm(post_cent - pre_cent))
    return pre_post_distances


def centroid(data):
    length = len(data)
    x_sum = np.sum(data[:, 0])
    y_sum = np.sum(data[:, 1])
    return np.array([float(x_sum)/length, float(y_sum)/length])

# get training data from un-concussed individuals
n_keep = 1000

train_lists = [pid_concussion, pid_noConcussion]
train_bools = [True, False]
examples_lists = [[], []]
train_examples = []
labels = ["concussion", "noconcussion"]

# for lst, pat_list in zip([pid_noConcussion, pid_3stepProtocol, pid_testRetest, pid_concussion], [noCon_pats, step_pats, retest_pats, con_pats]):
# for lst, pat_list in zip([pid_noConcussion], [noCon_pats]):
i = 0
for pid_list, train_bool in zip(train_lists, train_bools):
    for pid in pid_list:
        print("Processing pid: {}".format(pid))
        p = Patient(pid, subfolder, load_session_raw=False, load_session_examples=True)
        # get examples from pre_test
        pre = post = None
        if p.pre_test is not None:
            pre = p.pre_test.load_examples(subfolder)
            if pre is not None:
                np.random.shuffle(pre)
        # get examples from post_test
        if p.post_test is not None:
            post = p.post_test.load_examples(subfolder)
            if post is not None:
                np.random.shuffle(post)
        if post is not None and pre is not None:
            if train_bool:
                train_examples.append((pid, pre, post))
            examples_lists[i].append((pid, pre, post))
    i += 1

# create training data
train_data = np.vstack([tup[1][:n_keep] for tup in train_examples] + [tup[2][:n_keep] for tup in train_examples])
# create and train embedding
emb = Embedding(**embedding_args)
emb.train(train_data)

# plot both
# visualize embedding
colors = ["r", "b"]
f = plt.figure(figsize=(10, 10))
for label, examples_list, color in zip(labels, examples_lists, colors):
    distances = embed_and_plot(emb, examples_list, all_color=color)
plt.title("pre/post test centroid distance".format())
plt.xlabel("PC1")
plt.ylabel("PC2")
#plt.legend()
plt.savefig(subfolder + "_pc1vs2", dpi=300, transparent=True)
plt.show()
