import pandas as pd
import numpy as np
import pickle


class DataCleaner(object):

    def __init__(self, data_frame):
        """
        Instantiate with a one row dataframe (from HTML cleaning class)

        ex:
            X = DataCleaner(data_frame)
            X_vals = X.get_array_of_values()
        """
        self.single_df = data_frame
        self.total_vars = 0
        self.engineer_features()
        if self.total_vars < 1:
            self.whole_df = self.single_df
            self.total_vars = 1
        else:
            self.whole_df.append(self.single_df)
            self.total_vars += 1
        self.X = self.single_df.values[0]
    
    def set_new_data_point(self, data_frame):
        self.single_df = data_frame
        self.whole_df.append(self.single_df)
        self.total_vars += 1

    def engineer_features(self):
        self.single_df.fillna({"has_analytics" : 0, "has_header" : 0, "has_logo" : 0, "delivery_method" : 0}, inplace=True)
        self.single_df["event_duration"] = self.single_df["event_end"] - self.single_df["event_start"]
        self.single_df["event_turnover"] = self.single_df["event_published"] - self.single_df["event_created"]
        self.single_df["user_turnover"] = self.single_df["event_created"] - self.single_df["user_created"]
        self.single_df['has_something'] = self.single_df['has_analytics'] + self.single_df['has_header'] + self.single_df['has_logo']
        self.single_df['num_ticket_types'] = [len(i) for i in self.single_df['ticket_types']]
        self.single_df['num_prev_payouts'] = [len(i) for i in self.single_df['previous_payouts']]
        self.single_df["payout_specified"] = [0 if method == '' else 1 for method in self.single_df["payout_type"]]
        self.single_df["is_channel_0"] = [1 if channel == 0 else 0 for channel in self.single_df["channels"]]
        self.single_df["is_delivery_0"] = [1 if method == 0 else 0 for method in self.single_df["delivery_method"]]
        self.set_rounded_ticket_averages()
        self.set_country_matching_event()
        self.set_bad_email_labels()
        self.drop_extra_cols()
        self.single_df.fillna(0, inplace=True)
        
    def set_rounded_ticket_averages(self):
        averages = [] 
        for i in self.single_df['ticket_types']: 
            avg_price = []
            for y in i: 
                price = y['cost']
                avg_price.append(price)
                avg = np.mean(avg_price)
            averages.append(avg)
        self.rounded_averages = [round(i, 2) for i in averages] 
        self.single_df['average_ticket_price'] = self.rounded_averages

    def set_country_matching_event(self):
        for i in range(len(self.single_df)):
            v_cond1 = self.single_df.loc[i, "venue_country"] == None
            v_cond2 = self.single_df.loc[i, "venue_country"] == ""
            c_cond1 = self.single_df.loc[i, "country"] == None
            c_cond2 = self.single_df.loc[i, "country"] == ""
            if v_cond1 or v_cond2:
                self.single_df.loc[i, "venue_country"] = self.single_df.loc[i, "country"]
            if c_cond1 or c_cond2:
                self.single_df.loc[i, "country"] = self.single_df.loc[i, "venue_country"]
        self.single_df["country_matching_event"] = self.single_df["country"] == self.single_df["venue_country"]

    def set_bad_email_labels(self): 
        with open("bad_email_domains.p", 'rb') as f:
            self.bad_emails = pickle.load(f)

        self.single_df["bad_email"] = 0
        for i in range(len(self.single_df)):
            cond1 = self.single_df.loc[i, "email_domain"] in self.bad_emails
            if cond1:
                self.single_df.loc[i, "bad_email"] = 1

    def drop_extra_cols(self):
        self.single_df.drop(["org_facebook", "org_twitter", "channels", "venue_name", "email_domain",
                "previous_payouts", "ticket_types", "payee_name", "payout_type",
                "country", "venue_country", "has_analytics", "has_header", "delivery_method",
                "has_logo", "event_created", "event_end", "event_published",
                "event_start", "user_created", "approx_payout_date", "currency",
                "fb_published", "gts", "name_length", "num_order", "num_payouts",
                "listed", "object_id", "sale_duration", "sale_duration2", "venue_address",
                "venue_latitude", "venue_longitude", "venue_state", "description", "name", "org_desc",
                "org_name"], axis=1, inplace=True)