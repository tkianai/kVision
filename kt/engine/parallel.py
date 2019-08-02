"""This wraps some multiprocess job flow
"""

import multiprocessing as mp


class Parallel(object):

    def __init__(self, cores=None):

        if cores is None:
            cores = mp.cpu_count()
        
        self.cores = int(cores)
        self.res = []
        
    def run(self, job, data):
        """Run multiprocess jobss
        
        Arguments:
            job {function} -- the job
            data {list} -- list of tuple
        """

        pool = mp.Pool(processes=self.cores)
        for itm in data:
            self.res.append(pool.apply_async(job, itm))

        pool.close()
        pool.join()

    def fetch_results(self):

        res = []
        for itm in self.res:
            res.append(itm.get())

        # reset result
        self.res = []
        return res

        
