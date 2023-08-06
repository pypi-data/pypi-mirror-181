import copy
import os
from pathlib import Path
from pprint import pprint
import numpy as np
from datetime import datetime
import pandas as pd
from pymongo import MongoClient
from pymongo.database import Database
from ..cache import try_int
from ..fields.grid import Stack, VStack, HStack
from ..fields.inputs.hidden import InputHiddenField
from ..fields.inputs.text import InputTextField
from ..fields.navigation import Navigation
from ..fields.outputs.json import OutputJSONField
from ..fields.outputs.table import OutputTableField
from ..fields.redirect import SubmitButton
from ..web import Web
from ..page import Page


class LoginPage(Page):
    def __init__(self):
        super(LoginPage, self).__init__()
        self.fields = VStack([
            InputTextField("user_id")
        ])

    def get_content(self, **kwargs):
        return self.fields.generate()

    def process(self, **data):
        user_id = data['user_id']
        return self.redirect_url("/job",
                                 user_id=user_id,
                                 obj_id=0)


class JobStatusPage(Page):
    def __init__(self, distributor, dataset):
        super(JobStatusPage, self).__init__()
        self.error_fields = OutputJSONField("Error")
        self.distributor = distributor
        self.dataset = dataset

        self.fields = Navigation(HStack([
            OutputTableField("job"),
            VStack([
                OutputJSONField("progress"),
            ])
        ], xs=[10, 2]))

    def get_content(self, **kwargs):
        user_id = kwargs.get('user_id')
        if user_id is None:
            error_fields = copy.deepcopy(self.error_fields)
            error_fields.set_output({"Error": "Login to setup user_id"})
            return error_fields.generate()

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
        fields.add_link("Stats", "/stats")

        return self.fill(fields, {
            "job": df,
            "progress": f"{100 * sum([1 for c in job['submit_count'] if c > 0]) / length} %"
        })

    def process(self, **data):
        if "user_id" not in data:
            return self.redirect_url("/login")
        user_id = data['user_id']
        return self.redirect_url("/job/status", user_id=user_id)


class JobPage(Page):
    def __init__(self,
                 fields,
                 dataset,
                 saver,
                 distributor,
                 hook=lambda a, b: None):
        super(JobPage, self).__init__()

        self.fields = Navigation(VStack([
            fields,
            InputHiddenField("user_id", None),
            InputHiddenField("obj_id", None),
            InputHiddenField("start_time", None),
        ]))

        self.error_fields = OutputJSONField("Error")

        self.distributor = distributor
        self.dataset = dataset
        self.saver = saver
        self.hook = hook

    def get_content(self, **kwargs):
        user_id = kwargs.get('user_id')
        obj_id = try_int(kwargs.get('obj_id', 0), 0)
        if user_id is None:
            error_fields = copy.deepcopy(self.error_fields)
            error_fields.set_output({"Error": "Login to setup user_id"})
            return error_fields.generate()

        job = self.distributor.get_job(user_id)
        print("Job: ", job)
        idx = job['indices'][obj_id]
        length = len(job['indices'])

        fields = copy.deepcopy(self.fields)
        fields.add_link("Prev", self.redirect_url("/job",
                                                  user_id=user_id,
                                                  obj_id=max(0, obj_id - 1)))
        fields.add_link("Next", self.redirect_url("/job",
                                                  user_id=user_id,
                                                  obj_id=min(length - 1, obj_id + 1)))
        fields.add_link("Job status", self.redirect_url("/job/status",
                                                        user_id=user_id))
        fields.add_link("Stats", self.redirect_url("/stats",
                                                   user_id=user_id))

        fields["user_id"].set_output(user_id)
        fields["obj_id"].set_output(obj_id)
        fields["start_time"].set_output(datetime.now().isoformat())
        self.fill(fields[0], self.dataset[idx], inplace=True, generate=False,
                  hook=self.hook)
        return fields.generate()

    def process(self, **data):
        if "user_id" not in data:
            return "/login"
        data = self.parse(self.fields, data)
        user_id = data.pop('user_id')
        obj_id = int(data.pop('obj_id'))
        started_at = datetime.fromisoformat(data.pop('start_time'))
        submit_at = datetime.now()

        job = self.distributor.get_job(user_id)
        self.distributor.submit(job, obj_id,
                                started_at=started_at,
                                submit_at=submit_at)
        idx = job['indices'][obj_id]
        length = len(job['indices'])
        self.saver.save(idx, data)

        not_submitted = [idx for idx in range(length) if job['submit_count'][idx] == 0]
        not_submitted.remove(obj_id)
        if len(not_submitted) > 0:
            return self.redirect_url('/job', user_id=user_id, obj_id=not_submitted[0])
        else:
            return self.redirect_url('/job/status', user_id=user_id)


class JobReadOnlyPage(Page):
    def __init__(self, ):
        super(JobReadOnlyPage, self).__init__()

    def get_content(self, **kwargs):
        job_id = kwargs.pop('job_id')
        obj_id = try_int(kwargs.get('obj_id', 0), 0)
        if job_id is None:
            pass

    def process(self, **data):
        pass


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
        return self.fill(self.fields, {
            "JobStats": pd.DataFrame(
                stats
            ),
            "JobTasksStats": pd.DataFrame(
                tasks_stats
            ),
        })

    def process(self, **data):
        data = self.parse(self.fields, data)
        user_id = data.get('user_id')
        if user_id is None:
            return self.redirect_url('/login')

        return self.redirect_url("/job", user_id=user_id, obj_id=0)


class StatsPage(Page):
    def __init__(self, distributor):
        super(StatsPage, self).__init__()
        self.distributor = distributor

        self.fields = Navigation(VStack([
            OutputTableField("Stats")
        ]))
        self.fields.add_link("Login", "/login")
        self.fields.add_link("Stats", "/stats")

    def get_content(self, **kwargs):
        return self.fill(self.fields, {
            "Stats": self.create_df()
        })

    def create_df(self):
        result = self.distributor.stats()
        users = list(result.keys())
        dateindex = [r["date"].date().isoformat() for r in result[users[0]]]
        data = {user_id: list(map(lambda x: self.create_cell(x), result[user_id])) for user_id
                in users}
        data.update({"Date": dateindex})
        df = pd.DataFrame(columns=users + ["Date"], data=data)
        return df

    def create_cell(self, data):
        if "assigned_jobs" in data and "ended_jobs" in data:
            assigned_job_links = [self.create_link(f"Job {jid[:5]}...",
                                                   href=self.redirect_url("/view/job", job_id=jid))
                                  for jid in data['assigned_jobs']]
            ended_job_links = [self.create_link(f"Job {jid[:5]}...",
                                                href=self.redirect_url("/view/job", job_id=jid))
                               for jid in data['ended_jobs']]

            return f"""
<h5>Assigned job links: (total: {len(assigned_job_links)})</h5>
{'<br />'.join(assigned_job_links)}
<h5>Ended job links: (total: {len(ended_job_links)})</h5>
{'<br />'.join(ended_job_links)}
"""
        else:
            return f"""
Assigned: {data['assigned']}
<br />
Ended: {data['ended']}
"""

    def process(self, **data):
        return self.redirect_url("/login")


class Labelling(Web):
    def __init__(self,
                 name,
                 fields,
                 dataset,
                 saver,
                 distributor_fn,
                 db_name=None,
                 hook=lambda a, b: None):
        if db_name is None:
            db_name = name
        client = MongoClient()
        client.drop_database(db_name)
        db = client[db_name]
        self.dataset = dataset
        self.distributor = distributor_fn(db)
        self.fields = fields
        self.saver = saver

        super(Labelling, self).__init__({
            "job": JobPage(dataset=dataset,
                           distributor=self.distributor,
                           fields=fields,
                           saver=saver,
                           hook=hook),
            "view/job": JobReadOnlyPage(),
            "login": LoginPage(),
            "job/status": JobStatusPage(self.distributor, self.dataset),
            "finish": FinishJob(self.distributor),
            "stats": StatsPage(self.distributor),
        }, name=name)
