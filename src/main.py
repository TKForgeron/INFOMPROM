# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



# Press the green button in the gutter to run the script.


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import seaborn as sns



if __name__ == '__main__':
    # retriever = DataRetriever("incidentProcess_custom.csv")
    #
    # event_log = retriever.create_event_log(case_col='Incident ID',
    #                                        act_col='Activity',
    #                                        time_col='ActivityTimeStamp')
    #
    # retriever.create_diagram(event_log)
    # retriever.get_dataHead()
    #
    # print(retriever.getDescribe())


    # df = pd.read_excel("data/numberofactivities.xlsx")
    # plt.boxplot(df)
    # plt.xticks([1], ['Number of activities per trace'])
    # plt.show()


    # duration priorities
    # df = pd.read_excel("data/DURATION PER PRIORIT.xlsx")
    # allDuration = df['DURATION_IN_HOURS'].tolist()
    # durarionPrio1 = df['TOTAL_PRIO_1'].tolist()
    # durarionPrio2 = df['TOTAL_PRIO_2'].tolist()
    # durarionPrio3 = df['TOTAL_PRIO_3'].tolist()
    # durarionPrio4 = df['TOTAL_PRIO_4'].tolist()
    # durarionPrio5 = df['TOTAL_PRIO_5'].tolist()
    # dataFrame = pd.DataFrame({'Duration of All Incidents': allDuration,
    #                           'Priority 1': durarionPrio1,
    #                           'Priority 2': durarionPrio2,
    #                           'Priority 3': durarionPrio3,
    #                           'Priority 4': durarionPrio4,
    #                           'Priority 5': durarionPrio5})
    # df_melted = pd.melt(dataFrame)
    # ax = sns.boxplot(x='variable', y='value', data=df_melted, showfliers=False)
    # ax.set(ylabel='Days', xlabel = '')
    # plt.show()

    # number of activities priorities
    # df = pd.read_excel("data/numberofactivities.xlsx")
    # allDuration = df['NumberOfActivities'].tolist()
    # durarionPrio1 = df['Priority 1'].tolist()
    # durarionPrio2 = df['Priority 2'].tolist()
    # durarionPrio3 = df['Priority 3'].tolist()
    # durarionPrio4 = df['Priority 4'].tolist()
    # durarionPrio5 = df['Priority 5'].tolist()
    # dataFrame = pd.DataFrame({'Number of Activities': allDuration,
    #                           'Priority 1': durarionPrio1,
    #                           'Priority 2': durarionPrio2,
    #                           'Priority 3': durarionPrio3,
    #                           'Priority 4': durarionPrio4,
    #                           'Priority 5': durarionPrio5})
    # df_melted = pd.melt(dataFrame)
    # ax = sns.boxplot(x='variable', y='value', data=df_melted, showfliers=False)
    # ax.set(ylabel='Number of Activities', xlabel = '')
    # plt.show()


    # df = pd.read_excel("data/incidentsPerTeam.xlsx")
    # plt.boxplot(df)
    # plt.xticks([1], ['Number of activities per team'])
    # plt.show()


    # df = pd.read_excel("data/incidentsPerPriority.xlsx")
    # plt.boxplot(dataFrame)
    # plt.show()

    #AE boxplot
    df = pd.read_excel("data/converted_df.xlsx")
    ae_timeList = df['AE_time_days'].tolist()
    dataFrame = pd.DataFrame({' ': ae_timeList})
    df_melted = pd.melt(dataFrame)
    ax = sns.boxplot(x='variable', y='value', data=df_melted, showfliers=False)
    ax.set(xlabel='Naive Absolute Error', ylabel= 'Days')

    # AEList = df['AE'].tolist()
    # dataFrame = pd.DataFrame({'AE': AEList})
    # df_melted = pd.melt(dataFrame)
    # ax = sns.boxplot(x='variable', y='value', data=df_melted)
    # ax.set(xlabel='MAE')
    plt.show()

    # flights_long = pd.read_excel("data/AE-test.xlsx")
    # weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    # flights = flights_long.pivot_table(index='Day', columns='Hour', values='Sessions')
    # days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # df_hourly = flights.groupby(['Day']).sum().reindex(days)
    # f, ax = plt.subplots(figsize=(14, 13))
    # sns.heatmap(df_hourly,  annot=True,
    #                 fmt="d", cmap="Greens")
    # plt.show()