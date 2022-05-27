class Job:
    def __init__(self, submit_time: int, id: int, user_id: int, estimated_runtime: int, instructions: int, disk_needed: int):
        self.submit_time = submit_time
        self.id = id
        self.user_id = user_id
        self.estimated_runtime = estimated_runtime
        self.instructions = instructions
        self.disk_needed = disk_needed
        self.completed_instructions = 0
        self.wait_start_time = None
        self.wait_end_time = None
        self.run_start_time = None
        self.run_end_time = None
    
    # returns True -> if completed, False otherwise
    def execute(self, number_of_instructions: int, current_time: int):
        self.completed_instructions += number_of_instructions
        if self.get_demand() <= 0:
            self.run_end_time = current_time
            return True
        return False

    def start_waiting(self, current_time: int):
        self.wait_start_time = current_time

    def start_executing(self, current_time: int):
        if self.wait_start_time == None:
            self.wait_start_time = current_time
        self.wait_end_time = current_time
        self.run_start_time = current_time

    def get_demand(self):
        return self.instructions - self.completed_instructions

    def get_stats(self):
        return [self.wait_end_time - self.wait_start_time, self.run_end_time - self.run_start_time]

    def get_submit_time(self):
        return self.submit_time