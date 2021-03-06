from job import Job


class Node:
    def __init__(self, cpu_instructions_per_second: int, time_cost: int):
        self.cpu_instructions_per_second = cpu_instructions_per_second
        self.time_cost = time_cost
        self.job_queue = []
        self.current_job = None

    def add_job(self, job: Job, current_time: int):
        if self.current_job == None:
            self.current_job = job
            job.start_executing(current_time, self.time_cost)
        else:
            self.job_queue.append(job)
            job.start_waiting(current_time=current_time)

    def execute_jobs(self, current_time: int):
        instructions_left_in_cycle = self.cpu_instructions_per_second
        while instructions_left_in_cycle > 0:
            if self.current_job == None:
                if len(self.job_queue) == 0:
                    return 
                self.current_job = self.job_queue.pop(0)
                self.current_job.start_executing(current_time, self.time_cost)

            demand = self.current_job.get_demand()
            if demand < instructions_left_in_cycle:
                self.current_job.execute(demand, current_time)
                instructions_left_in_cycle -= demand
                self.current_job = None
            else:
                self.current_job.execute(instructions_left_in_cycle, current_time)
                instructions_left_in_cycle = 0
                
        return self.is_working()

    def is_working(self):
        return self.current_job != None or len(self.job_queue) > 0

