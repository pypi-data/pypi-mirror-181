import copy
from datetime import datetime
from ...cache import try_int
from ...fields.grid import VStack, HStack
from ...fields.inputs.hidden import InputHiddenField
from ...fields.navigation import Navigation
from ...fields.outputs.json import OutputJSONField
from ...page import Page


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
        if obj_id in not_submitted:
            not_submitted.remove(obj_id)
        if len(not_submitted) > 0:
            return self.redirect_url('/job', user_id=user_id, obj_id=not_submitted[0])
        else:
            return self.redirect_url('/job/status', user_id=user_id)
