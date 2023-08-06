import copy
from ...cache import try_int
from ...fields.grid import VStack
from ...fields.inputs.choice import InputChoiceField
from ...fields.inputs.text import InputTextField
from ...fields.inputs.hidden import InputHiddenField
from ...fields.navigation import Navigation
from ...fields.outputs.json import OutputJSONField
from ...page import Page


class JobReadOnlyPage(Page):
    def __init__(self,
                 fields,
                 saver,
                 distributor,
                 hook=lambda a, b: None):
        super(JobReadOnlyPage, self).__init__()

        self.fields_no_user = Navigation(VStack([
            fields,
            OutputJSONField("params"),
        ]))

        self.fields = Navigation(VStack([
            fields,
            OutputJSONField("params"),
            InputChoiceField("CheckLabelledObject", ["True", "False"]),
            InputTextField("LeaveComment", default="", isArea=True),
            InputHiddenField("user_id", None),
            InputHiddenField("job_id", None),
            InputHiddenField("obj_id", None),
        ]))

        self.error_fields = OutputJSONField("Error")

        self.distributor = distributor
        self.saver = saver
        self.hook = hook

    def get_content(self, **kwargs):
        user_id = kwargs.get('user_id')
        job_id = kwargs.get('job_id')
        obj_id = try_int(kwargs.get('obj_id', 0), 0)
        if job_id is None:
            fields = copy.deepcopy(self.error_fields)
            return self.fill(fields, {"Error": {
                "Error": "Enter job id"
            }})
        job = self.distributor.get_job_by_id(job_id)
        if job is None:
            fields = copy.deepcopy(self.error_fields)
            return self.fill(fields, {"Error": {
                "Error": "Invalid job id"
            }})
        print("Job: ", job)
        idx = job['indices'][obj_id]
        length = len(job['indices'])

        if user_id is None:
            fields = copy.deepcopy(self.fields_no_user)
        else:
            fields = copy.deepcopy(self.fields)

        fields.add_link("Prev", self.redirect_url("/view/job",
                                                  job_id=job_id,
                                                  user_id=user_id,
                                                  obj_id=max(0, obj_id - 1)))
        fields.add_link("Next", self.redirect_url("/view/job",
                                                  job_id=job_id,
                                                  user_id=user_id,
                                                  obj_id=min(length - 1, obj_id + 1)))
        fields.add_link("Stats", self.redirect_url("/stats",
                                                   user_id=user_id))

        params = {
            "submit_count": job['submit_count'][obj_id],
            "durations": [(et - st).total_seconds() for st, et in zip(job['started_at'][obj_id], job['submit_at'][obj_id])],
            "user_id": job["user_id"],
            "comments": job["comments"][obj_id]
        }
        fields[1].set_output(params)
        if user_id is not None:
            fields[4].set_output(user_id)
            fields[5].set_output(job_id)
            fields[6].set_output(obj_id)

        self.fill(fields[0], self.saver.load(idx), inplace=True, generate=False,
                  hook=self.hook)
        return fields.generate()

    def process(self, **data):
        data = self.parse(self.fields, data)
        job_id = data.get('job_id')
        user_id = data.get('user_id')
        obj_id = data.get('obj_id')
        job = self.distributor.get_job_by_id(job_id)
        if job is None:
            return self.redirect_url("/stats", user_id=user_id)

        if user_id is not None or obj_id is not None:
            assert data["CheckLabelledObject"] in ["True", "False"]
            comment = data["LeaveComment"]
            checked = (data["CheckLabelledObject"] == "True")
            self.distributor.add_comment(job, obj_id, user_id, comment, checked)

        return self.redirect_url("/view/job", job_id=job_id,
                                 obj_id=obj_id,
                                 user_id=user_id)
