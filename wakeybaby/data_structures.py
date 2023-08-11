import pandas as pd


class OnDiskData:

    filesep: str = None

    # regularized column names
    t0: str = None
    t1: str = None
    dt: str = None
    entry_type: str = None
    feed_name: str = None
    sleep_name: str = None

    def __init__(self, filename):
        self.filename = filename
        self.df = pd.read_csv(filename, sep=self.filesep)
        self._clean_df()

    def _clean_df(self):
        self._pre_cleaning()
        for col in [self.t0, self.t1]:
            self.df[col] = pd.to_datetime(self.df[col])

        self.df[self.dt] = pd.to_timedelta(self.df[self.dt])

    def _pre_cleaning(self):
        pass

    def wake_window(self, min_nap_sep_mins=20, day_start_hr=7, day_end_hr=19):
        df = self.df[self.df[self.entry_type] == self.sleep_name].copy(deep=True)
        df = df.sort_values(by=self.t0).reset_index()
        # dt = pd.to_timedelta(min_nap_sep_mins, unit="m")

        df["time_awake"] = df[self.t0] - df[self.t1].shift(1)
        return df


class Huckle(OnDiskData):

    filesep = ","

    t0: str = "Start"
    t1: str = "End"
    dt: str = "Duration"
    entry_type: str = "Type"
    feed_name: str = "Feed"
    sleep_name: str = "Sleep"

    def _pre_cleaning(self):
        df = self.df
        df = df[df["Type"] != "Diaper"]
        df = df.reset_index()
        dt = self.dt
        df[dt] = df[dt] + ":00"
        df[dt] = pd.to_timedelta(df[dt])

        self.df = df
