import copy
import pandas as pd
from ...fields.grid import VStack
from ...fields.inputs.hidden import InputHiddenField
from ...fields.navigation import Navigation
from ...fields.outputs.table import OutputTableField
from ...page import Page


class StatsPage(Page):
    def __init__(self, distributor):
        super(StatsPage, self).__init__()
        self.distributor = distributor

        self.fields = Navigation(VStack([
            OutputTableField("Quick"),
            OutputTableField("Stats"),
            InputHiddenField("user_id", None)
        ]))
        self.fields.add_link("Login", "/login")
        self.fields.add_link("Start Job", "/job")
        self.fields.add_link("Stats", "/stats")

    def get_content(self, **kwargs):
        fields = copy.deepcopy(self.fields)
        fields.link["Start Job"]["href"] = self.redirect_url("/job", user_id=kwargs.get("user_id"))
        return self.fill(fields, {
            "Quick": pd.DataFrame(self.distributor.quick_stats()),
            "Stats": self.create_df(current_user_id=kwargs.get("user_id")),
            "user_id": kwargs.get("user_id")
        })

    def create_df(self, current_user_id=None):
        result = self.distributor.stats()
        users = list(result.keys())
        if len(users) == 0:
            return pd.DataFrame({})
        dateindex = [r["date"].date().isoformat() for r in result[users[0]]]

        mux = pd.MultiIndex.from_product([["Date"] + users, ["Assigned", "Ended"]])
        data = {
            ("Date", "Assigned"): dateindex,
            ("Date", "Ended"): dateindex,
        }

        data.update({
            (user_id, "Assigned"): ['<br />'.join(self.create_link(f"Job {jid[-5:]}...",
                                                                   href=self.redirect_url("/view/job", job_id=jid, user_id=current_user_id))
                                                  for jid in x['assigned_jobs'])
                                    for x in result[user_id]]
            for user_id in users if user_id not in ["__sum", "__cumsum"]
        })
        data.update({
            (user_id, "Ended"): ['<br />'.join(self.create_link(f"Job {jid[-5:]}...",
                                                                   href=self.redirect_url("/view/job", job_id=jid, user_id=current_user_id))
                                                  for jid in x['ended_jobs'])
                                    for x in result[user_id]]
            for user_id in users if user_id not in ["__sum", "__cumsum"]
        })

        data.update({
            (user_id, "Assigned"): [x["assigned"]
                                    for x in result[user_id]]
            for user_id in users if user_id in ["__sum", "__cumsum"]
        })
        data.update({
            (user_id, "Ended"): [x["ended"]
                                 for x in result[user_id]]
            for user_id in users if user_id in ["__sum", "__cumsum"]
        })

        df = pd.DataFrame(columns=mux, data=data)
        return df

    def process(self, **data):
        data = self.parse(self.fields, data)
        user_id = data.get('user_id')
        if user_id is None:
            return self.redirect_url("/login")
        else:
            return self.redirect_url("/job", user_id=user_id)
