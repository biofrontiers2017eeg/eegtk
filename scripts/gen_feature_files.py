from config import pid_noConcussion, pid_3stepProtocol, pid_testRetest, pid_concussion, feature_functions, epoch_size, \
    channels
from patient import Patient

# go through each list of ids
for lst in [pid_noConcussion, pid_3stepProtocol, pid_testRetest, pid_concussion]:
    # for each id...
    for pid in lst:
        print("Processing pid: {}".format(pid))
        p = Patient(pid, load_session_examples=False, load_session_raw=True)
        # generate file for pre_test
        if p.pre_test is not None:
            p.pre_test.remove_artifacts()
            p.pre_test.get_examples(feature_functions, epoch_size=epoch_size, channels=channels)
            p.pre_test.save_examples()
        if p.post_test is not None:
            # generate file for post_test
            p.post_test.remove_artifacts()
            p.post_test.get_examples(feature_functions, epoch_size=epoch_size, channels=channels)
            p.post_test.save_examples()
