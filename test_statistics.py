from scipy import stats

def ks(dist1, dist2):
	"""	
	2 sample kolmogorov-smirnov test
	"""
	kd_dict = {}
	ks_statistics, p = stats.ks_2samp(dist1, dist2)
	ks_dict['statistics'] = ks_statistics
	ks_dict['p'] = p
	return ks_dict

test = {
    "ks": ks,
}