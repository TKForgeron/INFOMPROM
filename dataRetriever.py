import pandas as pd
import pm4py as pm


class DataRetriever():
    """ Class that is used to read data from a file and transforms it into
    the necessary format. Some simple analysis is performed to get an impression
    of the data.
    """

    def __init__(self, filename, sep='\t') -> None:
        """Initiates the class and creates a dataframe given the filename."""

        self.df = pd.read_csv("data/" + str(filename), sep=sep, engine='python')

    def get_dataframe(self):
        """"Returns the dataframe"""

        return self.df

    def get_dataHead(self):
        print( self.df.head())

    def getShape(self):
        """returns the number of columns and the number of rows"""
        return self.df.shape
    def getInfo(self):
        return self.df.info

    def getDescribe(self):
        "returns statistical properties for the data set like the mean, count"
        return self.df.describe()

    def create_event_log(self, case_col, act_col, time_col):
        """Creates an event log in the correct format given a pandas dataframe
        TODO: We might want to merge this with the constructor.
        """

        event_log = pm.format_dataframe(self.df,
                                        case_id=case_col,
                                        activity_key=act_col,
                                        timestamp_key=time_col)

        return event_log

    def create_diagram(self, event_log):
        """Visualizes the data in a model"""

        process_tree = pm.discover_process_tree_inductive(event_log)
        bpmn_model = pm.convert_to_bpmn(process_tree)
        pm.view_bpmn(bpmn_model)

    def create_overview(self, log):
        # print(log.describe())
        print(log.columns)

        unique_act = log["Activity"].unique()
