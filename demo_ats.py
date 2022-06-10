from ats import *
import pandas as pd
import numpy as np
from print_ats import *

# Some code to test the code carefully (i.e. not run it with the full event log)
data = pd.read_csv("data/incidentProcess_custom.csv", sep="\t")
data = data[data["Incident ID"].isin(["IM0000004", "IM0000005", "IM0000006"])]

ats = ATS("Incident ID", "Activity", "trace", horizon=2)
ats.create_ATS(data)
print_ATS(ats)
ats.print()



