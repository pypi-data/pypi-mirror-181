import copy
import pandas as pd
from ...fields.grid import VStack, HStack
from ...fields.inputs.hidden import InputHiddenField
from ...fields.navigation import Navigation
from ...fields.outputs.table import OutputTableField
from ...fields.outputs.json import OutputJSONField
from ...page import Page


class FinishJob(Page):
    def __init__(self, distributor):
        super(FinishJob, self).__init__()
        self.error_fields = VStack([
            OutputJSONField("Error"),
            InputHiddenField("user_id", None),
        ])
        self.fields = Navigation(VStack([
            OutputTableField("JobStats"),
            OutputTableField("JobTasksStats"),
            InputHiddenField("user_id", None),
        ]))
        self.fields.add_link("Login", "/login")
        self.fields.add_link("Stats", "/stats")

        self.distributor = distributor

    def get_content(self, **kwargs):
        user_id = kwargs.get('user_id')
        if user_id is None:
            error_fields = copy.deepcopy(self.error_fields)
            error_fields["Error"].set_output({"Error": "Login to setup user_id"})
            return error_fields.generate()

        job = self.distributor.get_job(user_id)
        length = len(job['indices'])
        not_submitted = [idx for idx in range(length) if job['submit_count'][idx] == 0]
        if len(not_submitted) > 0:
            error_fields = copy.deepcopy(self.error_fields)
            error_fields["Error"].set_output({"Error": f"Can't finish job, not submitted: {not_submitted}",
                                              "user_id": user_id})
            error_fields["user_id"].set_output(user_id)
            return error_fields.generate()

        self.distributor.finish_job(job)
        stats, tasks_stats = self.distributor.job_stats(job)
        fields = copy.deepcopy(self.fields)
        fields.link["Stats"]["href"] = self.redirect_url("/stats", user_id=user_id)
        return self.fill(fields, {
            "JobStats": pd.DataFrame(
                stats
            ),
            "JobTasksStats": pd.DataFrame(
                tasks_stats
            ),
            "user_id": user_id,
        })

    def process(self, **data):
        data = self.parse(self.fields, data)
        user_id = data.get('user_id')
        if user_id is None:
            return self.redirect_url('/login')

        return self.redirect_url("/job", user_id=user_id, obj_id=0)
