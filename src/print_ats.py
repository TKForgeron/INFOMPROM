import networkx as nx
import pylab as plt

import matplotlib.patches as patches
import matplotlib.pyplot as plt


def rewrite_activity(idx, table, act):

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    if act not in table:
        table[act] = alphabet[idx]
        idx += 1

    return table, idx


def rewrite_activities(idx, table, activities):

    for act in activities:
        table, idx = rewrite_activity(idx, table, act)

    activities = [table[act] for act in activities]

    return idx, table, activities


def print_ATS(ATS):

    idx = 0
    table = {}

    G = nx.DiGraph()
    for state in ATS.states:

        idx, table, transf_acts = rewrite_activities(idx, table, state.activities)
        G.add_node(str(transf_acts))

    for state in ATS.states:

        for id in state.subsequent_states:

            idx, table, transf_acts = rewrite_activities(idx, table, state.activities)

            state_2 = ATS.states[id].activities

            idx, table, transf_acts_2 = rewrite_activities(idx, table, state_2)

            G.add_edge(str(transf_acts), str(transf_acts_2))

    handles_dict = {
        patches.Patch(color="white", label=f"{v} : {k}") for k, v in table.items()
    }

    nx.draw(G, with_labels=True, font_size=8)
    plt.legend(handles=handles_dict)
    plt.savefig("plots/labels.png")

    # plt.show()
