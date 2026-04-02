import django_rq


def get_queue(name='default', *args, **kwargs):
    return django_rq.get_queue(name, *args, **kwargs)


class TaskChain:
    """Chain of RQ jobs with dependencies."""

    def __init__(self, queue_name='default'):
        self.queue = get_queue(queue_name)
        self.jobs = []

    def then(self, func, *args, **kwargs):
        job = self.queue.enqueue(func, *args, depends_on=self.last_job, **kwargs)
        self.jobs.append(job)
        return self
    
    @property
    def last_job(self):
        return self.jobs[-1] if self.jobs else None