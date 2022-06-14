# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
from other.data_retriever import DataRetriever

if __name__ == "__main__":
    retriever = DataRetriever("incidentProcess_custom.csv")

    event_log = retriever.create_event_log(
        case_col="Incident ID", act_col="Activity", time_col="ActivityTimeStamp"
    )

    retriever.create_diagram(event_log)
    retriever.get_dataHead()

    # retriever.create_diagram()

    print(retriever.getDescribe())
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
