import copy
import numpy as np
import pandas as pd
from ...fields.grid import VStack, HStack
from ...fields.inputs.hidden import InputHiddenField
from ...fields.navigation import Navigation
from ...fields.outputs.json import OutputJSONField
from ...fields.outputs.table import OutputTableField
from ...page import Page, ContentError


class JobStatusPage(Page):
    def __init__(self, distributor, dataset):
        super(JobStatusPage, self).__init__()
        self.distributor = distributor
        self.dataset = dataset

        self.fields = Navigation(HStack([
            OutputTableField("job"),
            VStack([
                OutputJSONField("progress"),
                InputHiddenField("user_id", None),
            ])
        ], xs=[10, 2]))

    def get_content(self, **kwargs):
        user_id = kwargs.get('user_id')
        if user_id is None:
            raise ContentError({"Error": "Login to setup user_id"},
                               redirect_url=self.redirect_url("/login"))

        job = self.distributor.get_job(user_id)
        length = len(job['indices'])
        data = {"indices": list(range(length)),
                "submit_count": list(job['submit_count']),
                "start": [self.create_link("Start", self.redirect_url("/job",
                                                                      user_id=user_id,
                                                                      obj_id=i))
                          for i in range(length)]}
        if hasattr(self.dataset, 'preview'):
            data.update({"preview": [self.dataset.preview(job['indices'][i]) for i in range(length)]})

        df = pd.DataFrame(data,
                          dtype=np.int64)
        fields = copy.deepcopy(self.fields)

        fields.add_link("Login", "/login")
        fields.add_link("Start Job", self.redirect_url("/job",
                                                       user_id=user_id,
                                                       obj_id=0))
        fields.add_link("Job Status", self.redirect_url("/job/status",
                                                        user_id=user_id))
        fields.add_link("Finish job", self.redirect_url("/finish",
                                                        user_id=user_id))
        fields.add_link("Stats", self.redirect_url("/stats", user_id=user_id))

        return self.fill(fields, {
            "job": df,
            "progress": f"{100 * sum([1 for c in job['submit_count'] if c > 0]) / length} %",
            "user_id": user_id,
        })

    def process(self, **data):
        user_id = data['user_id']
        return self.redirect_url("/job", user_id=user_id)
