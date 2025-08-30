# paired_stats.py
import math
from statistics import mean, stdev
from math import sqrt
from scipy import stats  # if available

# Per-stack values (from Appendix B.1 / B.2)
jenkins_cpu = [73.8, 75.2, 78.9, 76.4, 74.1, 74.8]
proposed_cpu = [45.1, 44.9, 48.2, 43.5, 44.3, 44.2]
jenkins_fail = [22,20,23,19,21,22]
proposed_fail = [6,6,7,5,6,7]

def paired_t(x,y):
    diffs = [a-b for a,b in zip(x,y)]
    n = len(diffs)
    md = mean(diffs)
    sd = stdev(diffs)
    se = sd / math.sqrt(n)
    t = md / se
    df = n-1
    # use scipy if available for p:
    p = None
    try:
        p = 2*stats.t.sf(abs(t), df)
    except:
        p = 'scipy required for p-value'
    return {'n':n,'mean_diff':md,'sd':sd,'t':t,'df':df,'p':p}

print('CPU paired test:', paired_t(jenkins_cpu, proposed_cpu))
print('Failures paired test:', paired_t(jenkins_fail, proposed_fail))
