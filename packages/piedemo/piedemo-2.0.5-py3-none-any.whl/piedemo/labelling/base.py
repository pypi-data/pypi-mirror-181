from pymongo import MongoClient

from ..page import PageWithError
from ..web import Web
from .pages.login import LoginPage
from .pages.job_status import JobStatusPage
from .pages.job import JobPage
from .pages.stats import StatsPage
from .pages.finish_job import FinishJob
from .pages.job_readonly import JobReadOnlyPage


class Labelling(Web):
    def __init__(self,
                 name,
                 fields,
                 view_fields,
                 dataset,
                 saver,
                 distributor_fn,
                 db_name=None,
                 hook=lambda a, b: None,
                 view_hook=lambda a, b: None):
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
            "view/job": JobReadOnlyPage(saver=saver,
                                        distributor=self.distributor,
                                        fields=view_fields,
                                        hook=view_hook),
            "login": LoginPage(),
            "job/status": PageWithError(JobStatusPage(self.distributor, self.dataset), "/login"),
            "finish": FinishJob(self.distributor),
            "stats": StatsPage(self.distributor),
        }, name=name)
