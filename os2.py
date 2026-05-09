import re
import os
import matplotlib.pyplot as plt
from collections import deque

class ResourceManager:
    def __init__(self, total_resources=20 ):
        # Initialize all 20 resources as available (None means no process is using the resource)
        self.resources = {}
        self.resources_requests_not_aviable = {}
        for i in range(1, 21):  # Create 20 resources
            self.resources[f"R[{i}]"] = None
        self.resource_allocation = {}
    def request_resource_not_avialbe (self, resource_id, process):
        """Request a specific resource for a process but we not fond it."""
        self.resources_requests_not_aviable[resource_id] = process
    def release_resource_from_not_aviable(self, resource_id):
        """Release a specific resource."""
        if self.resources.get(resource_id) is not None:
            self.resources[resource_id] = None
    def request_resource(self, resource_id, process):
        """Request a specific resource for a process."""
        if self.resources.get(resource_id) is None:
            self.resources[resource_id] = process
            return True
        return False

    def release_resource(self, resource_id):
        """Release a specific resource."""
        if self.resources.get(resource_id) is not None:
            self.resources[resource_id] = None

    def is_available(self, resource_id):
        """Check if a specific resource is available."""
        return self.resources.get(resource_id) is None
    def release_resources_proceess(self, process):
        """Release all resources allocated to a process."""
        for resource_id in process.allocated_resources[:]:  # Iterate over a copy to avoid modification issues
            self.release_resource(resource_id)
            process.allocated_resources.remove(resource_id)
    ####
    def detect_deadlock(self, process, resource_id):
        """
        Check for potential deadlocks if a process requests a resource.

        Parameters:
            process (Process): The process making the request.
            resource_id (str): The resource being requested.

        Returns:
            bool: True if a deadlock is detected, False otherwise.
        """
        print("Checking for deadlock...")

        # Build the resource allocation graph
        graph = {}
        for res, holder in self.resources.items():
            if holder:
                if holder not in graph:
                    graph[holder] = []
                graph[holder].append(res)

        # Build the resource request graph
        request_graph = {}
        for proc in graph.keys():
            for req in proc.resource_requests:
                if req not in request_graph:
                    request_graph[req] = []
                request_graph[req].append(proc)

        # Add the current request to the request graph
        if resource_id not in request_graph:
            request_graph[resource_id] = []
        request_graph[resource_id].append(process)

        # Detect cycles in the combined graph
        visited = set()
        stack = set()

        def has_cycle(node):
            if node in stack:
                return True  # Cycle detected
            if node in visited:
                return False  # Already visited, no cycle
            visited.add(node)
            stack.add(node)

            # Check neighbors in the resource allocation graph
            if node in graph:
                for neighbor in graph[node]:
                    if has_cycle(neighbor):
                        return True

            # Check neighbors in the resource request graph
            if node in request_graph:
                for neighbor in request_graph[node]:
                    if has_cycle(neighbor):
                        return True

            stack.remove(node)
            return False

        # Check for cycles starting from each process in the graph
        for node in graph.keys():
            if has_cycle(node):
                return True  # Deadlock detected

        return False  # No deadlock detected
##############################################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
class Process:
    def __init__(self, pid, arrival_time, priority, bursts):
        self.pid = pid
        self.arrival_time = arrival_time
        self.priority = priority
        self.bursts = deque(bursts)
        ##########################
        self.resource_requests = []  # Resources the process is waiting for.
        self.allocated_resources = []   # Resources held by the process
        ################################
        self.waiting_time = 0
        self.turnaround_time = 0
        self.remaining_time = -1
        self.current_burst = None
        self.input_in_ready = 0
        self.taken=False
        self.end_execution_time=0
        #######################################
        self.type_of_waitng=1
        self.burst_waiting=0 #if type =0 is end of waiting time if it =1 resourse id
        ##########################################
        self.pointer_of_bursts = 0
        self.pointer_of_bursts_CPU = 0
        ##########################################
        self.executed=False
    @property
    def end_execution_time(self):
        return self._end_execution_time

    @end_execution_time.setter
    def end_execution_time(self, value):
        self._end_execution_time = value

    @property
    def resource_requests(self):
        return self._resource_requests  

    @resource_requests.setter
    def resource_requests(self, value):
        self._resource_requests = value

    @property
    def allocated_resources(self):
        return self._allocated_resources

    @allocated_resources.setter
    def allocated_resources(self, value):
        self._allocated_resources = value

    @property
    def waiting_time(self):
        return self._waiting_time

    @waiting_time.setter
    def waiting_time(self, value):
        self._waiting_time = value

    @property
    def turnaround_time(self):
        return self._turnaround_time

    @turnaround_time.setter
    def turnaround_time(self, value):
        self._turnaround_time = value

    @property
    def remaining_time(self):
        return self._remaining_time

    @remaining_time.setter
    def remaining_time(self, value):
        self._remaining_time = value

    @property
    def current_burst(self):
        return self._current_burst

    @current_burst.setter
    def current_burst(self, value):
        self._current_burst = value

    @property
    def input_in_ready(self):
        return self._input_in_ready

    @input_in_ready.setter
    def input_in_ready(self, value):
        self._input_in_ready = value

    @property
    def taken(self):
        return self._taken

    @taken.setter
    def taken(self, value):
        self._taken = value

    @property
    def type_of_waitng(self):
        return self._type_of_waitng

    @type_of_waitng.setter
    def type_of_waitng(self, value):
        self._type_of_waitng = value

    @property
    def burst_waiting(self):
        return self._burst_waiting

    @burst_waiting.setter
    def burst_waiting(self, value):
        self._burst_waiting = value

    @property
    def pointer_of_bursts(self):
        return self._pointer_of_bursts

    @pointer_of_bursts.setter
    def pointer_of_bursts(self, value):
        self._pointer_of_bursts = value

    @property
    def pointer_of_bursts_CPU(self):
        return self._pointer_of_bursts_CPU

    @pointer_of_bursts_CPU.setter
    def pointer_of_bursts_CPU(self, value):
        self._pointer_of_bursts_CPU = value

    @property
    def executed(self):
        return self._executed

    @executed.setter
    def executed(self, value):
        self._executed = value
    def set_waiting_type(self, waiting_type):
            """Set the type of waiting for the process."""
            self.type_of_waiting = waiting_type

    def set_burst_waiting(self, burst_waiting):
        """Set the burst waiting time or resource ID for the process."""
        self.burst_waiting = burst_waiting
    def remove_resource(self,Resource_id):
        if Resource_id in self.allocated_resources:
            self.allocated_resources.remove(Resource_id)
    def execute(self):
        """Mark the process as executed."""
        self.executed = True
    
##########################################################################################
def read_file(filename):
        try:
            with open(filename, 'r') as file:
                pass
        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{filename}' does not exist. Please provide a valid file path.")

        processes = []
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()  # Remove leading and trailing whitespace
                if not line or line.startswith("#"):  # Skip empty lines or comments
                    continue
                parts = line.split()
                if len(parts) < 4:  # Check if the line has the required number of fields
                    print(f"Skipping invalid line: {line}")
                    continue
                pid = int(parts[0])
                arrival_time = int(parts[1])
                priority = int(parts[2])
                burst=[]
                bursts = parse_bursts(' '.join(parts[3:]))
                processes.append(Process(pid, arrival_time, priority, bursts))
        return processes
##########################################################################################
def parse_bursts(data):
    """
    Parses CPU and IO bursts from a string.

    Args:
        data (str): A string containing bursts in the format 'CPU {value} IO {value} ...'.

    Returns:
        list: A list of formatted bursts as strings.
    """
    # Regex pattern to match all CPU and IO bursts
    pattern = re.compile(r'(CPU|IO)\s*\{([^}]+)\}')
    burst_parts = []  # List to store all burst matches

    # Find all matches of the pattern in the data
    matches = pattern.findall(data)
    if not matches:
        print("No bursts found in data.")
        return []
    
    # Process each match and append to the list
    for match in matches:
        burst_parts.append(f"{match[0]} [{match[1]}]")  # Format and add to list
    
    return burst_parts

##########################################################################################
def plot_gantt_chart(gantt_chart):
    fig, gantt_chart_plot = plt.subplots()
    executed_processes = set(entry[1] for entry in gantt_chart)
    # Group Gantt chart entries by process ID
    process_entries = {pid: [] for pid in executed_processes}
    for entry in gantt_chart:
        process_entries[entry[1]].append(entry)

    # Setting labels for x-axis and y-axis
    gantt_chart_plot.set_xlabel('Time')
    gantt_chart_plot.set_ylabel('Processes')

    # Setting ticks on y-axis
    y_ticks = list(range(len(process_entries)))
    y_labels = [f'P{pid}' for pid in process_entries.keys()]
    gantt_chart_plot.set_yticks(y_ticks)
    gantt_chart_plot.set_yticklabels(y_labels)

    # Setting graph limits
    gantt_chart_plot.set_xlim(0, max(entry[2] for entry in gantt_chart))
    gantt_chart_plot.set_ylim(-1, len(process_entries))

    # Plotting the Gantt chart
    for i, (pid, entries) in enumerate(process_entries.items()):
        for start_time, _, end_time in entries:
            gantt_chart_plot.broken_barh([(start_time, end_time - start_time)], (i - 0.4, 0.8), facecolors=('tab:blue'))
    plt.show()
##########################################################################################
def terminate_process(process,resource_manager,ready_queue,waiting_queue):
    """Terminate a process to resolve deadlock."""
    print(f"Terminating process {process.pid} to resolve deadlock.")
    resource_manager.release_resources_proceess(process)
    if process in ready_queue:
        ready_queue.remove(process)
    if process in waiting_queue:
        waiting_queue.remove(process)
    return
##########################################################################################
def main():
    try:
        filename = "input.txt"
        time_quantum = 5
        resource_manager = ResourceManager()  # Include the resource manager
        gantt_chart = []  # To store (start_time, process_id, end_time)
        ready_queue = []  # Processes ready for CPU (processes,time of input in ready queue)
        waiting_queue = []  # To store (process,time of input in wait, type of wait ,time of wait if its the type=0 io wait ,resource_id if its the type=2 resource wait) 
        current_time = 0  # Global clock
        processes =read_file(filename)
        print("Processes successfully loaded:")
        scheduler(processes, resource_manager, current_time, gantt_chart, ready_queue, waiting_queue ,time_quantum)
        total_waiting_time = sum(process.waiting_time for process in processes)
        print("_________________________________________________________")
        avg_waiting_time = total_waiting_time / len(processes)
        print(f"Average waiting time: {avg_waiting_time:.2f}")
        total_turnaround_time = sum(process.end_execution_time - process.arrival_time for process in processes)
        avg_turnaround_time = total_turnaround_time / len(processes)
        print(f"Average turnaround time: {avg_turnaround_time:.2f}")
        plot_gantt_chart(gantt_chart)
    except FileNotFoundError as e:
        print(e)
##########################################################################################
def scheduler(processes, resource_manager, current_time, gantt_chart, ready_queue, waiting_queue ,time_quantum):
    while True:
        for process in processes[:]:
            if process.arrival_time <= current_time and process.executed==False:
                if process not in waiting_queue and process not in ready_queue:
                    ready_queue.append(process)
                    if process.taken==False:
                        process.input_in_ready = process.arrival_time
                        process.taken=True
        while ready_queue :
            for process in processes[:]:
                if process.arrival_time <= current_time and process.executed==False:
                    if process not in waiting_queue and process not in ready_queue:
                        ready_queue.append(process)
                        if process.taken==False:
                            process.input_in_ready = process.arrival_time
                            process.taken=True
            check_waiting_queue(waiting_queue, ready_queue, current_time, resource_manager)
            
            # Sort the ready queue by priority and then by arrival time
            if ready_queue :
                ready_queue.sort(key=lambda process: (process.priority, process.arrival_time))
                process = ready_queue.pop(0)
                if process.executed ==True:
                    continue
                next_process = ready_queue[0] if ready_queue else None
                if process.bursts[process.pointer_of_bursts].startswith("CPU") and next_process and process.priority == next_process.priority:
                    #######schdule with round robin########
                    while next_process and process.priority == next_process.priority :
                        current_time= execute_process(process, gantt_chart, current_time, ready_queue, waiting_queue, resource_manager, round_robin=1,time_quantum=time_quantum)
                        check_waiting_queue(waiting_queue, ready_queue, current_time, resource_manager)
                        if process.executed ==True:
                            break
                        for new_process in processes[:]:
                            if new_process.arrival_time <= current_time and new_process.executed==False and new_process.taken==False:
                                new_process.taken=True

                                if new_process.priority > process.priority:
                                    ready_queue.insert(len(ready_queue),new_process)
                                    new_process.input_in_ready = new_process.arrival_time
                                if new_process.priority < ready_queue[0].priority:
                                    new_process.input_in_ready = new_process.arrival_time
                                    ready_queue.insert(0,new_process)
                                if new_process.priority == ready_queue[0].priority:
                                    enable=False
                                    for i in range(len(ready_queue)):
                                        if ready_queue[i].priority == new_process.priority:
                                            continue
                                        ready_queue.insert(i, new_process)
                                        new_process.input_in_ready = new_process.arrival_time
                                        enable=True
                                        break
                                    if not (enable):
                                        ready_queue.insert(i, new_process)
                                        new_process.input_in_ready = new_process.arrival_time
                        if ready_queue:
                            process = ready_queue.pop(0)
                            next_process = ready_queue[0]  if ready_queue else None
                        ########end round robin #########
                        else:
                            ready_queue.sort(key=lambda process: (process.priority, process.arrival_time))
                            break
                    

                next_process = ready_queue[0]  if ready_queue else None
                if next_process and process.priority == next_process.priority:
                    continue
                if  process==None :
                    continue
                if process.bursts[process.pointer_of_bursts].startswith("CPU") :
                    current_time= execute_process(process, gantt_chart, current_time, ready_queue, waiting_queue, resource_manager ,round_robin=0,time_quantum=time_quantum)
                    check_waiting_queue(waiting_queue,ready_queue,current_time,resource_manager,process1=None)
                    continue
                if process.bursts[process.pointer_of_bursts].startswith("IO") :
                    process.type_of_waiting=1
                    process.burst_waiting=(int(process.bursts[process.pointer_of_bursts].split("[")[1].split("]")[0])+current_time)
                    waiting_queue.append(process)
                    continue
                    
                    
        if not ready_queue and not waiting_queue and all(process.executed for process in processes):
                break
        current_time += 1
        check_waiting_queue(waiting_queue, ready_queue, current_time, resource_manager)   
        #waiting_queue = [] To store (process,time of input in wait,
        #type of wait ,time of wait if its the type=0 io wait or resource_id if its the type=1 resource wait)
##########################################################################################
def check_waiting_queue(waiting_queue, ready_queue, current_time, resource_manager, process1=None):
    """
    Check the waiting queue for processes that can now proceed and move them to the ready queue.
    
    Parameters:
        waiting_queue (list): The list of processes currently waiting.
        ready_queue (list): The list of processes ready to execute.
        current_time (int): The current simulation time.
        resource_manager (ResourceManager): The resource manager handling resources.
        process1 (Process, optional): Current process for priority comparison (if any).
    """
    for process in waiting_queue[:]:  # Iterate over a copy to avoid modification issues
        # Handle I/O wait (type_of_waiting = 1)
        if process.type_of_waiting == 1 and process.burst_waiting <= current_time:
            process.pointer_of_bursts += 1
            if process.pointer_of_bursts == len(process.bursts):  # Process has completed all bursts
                process.executed = True
                process.end_execution_time = current_time
            if not process.executed:
                if process1 is None:
                    ready_queue.append(process)
                else:
                    # Insert based on priority relative to process1
                    if process.priority > process1.priority:
                        ready_queue.append(process)
                    elif not ready_queue or process.priority <= ready_queue[0].priority:
                        ready_queue.insert(0, process)
                    else:
                        ready_queue.append(process)
                process.input_in_ready = process.burst_waiting
            waiting_queue.remove(process)  # Safely remove from waiting queue

        # Handle resource wait (type_of_waiting = 2)
        elif process.type_of_waiting == 2 and resource_manager.is_available(process.burst_waiting):
            print(f"Resource {process.burst_waiting} is available. Allocating to process {process.pid}.")
            resource_manager.request_resource(process.burst_waiting, process)
            process.allocated_resources.append(process.burst_waiting)
            ready_queue.append(process)
            process.input_in_ready = current_time
            waiting_queue.remove(process)  # Safely remove from waiting queue
            process.pointer_of_bursts_CPU += 1

    # Sort the ready queue by priority and arrival time
    if process1 is None:  # No round-robin or current process specified
        ready_queue.sort(key=lambda process: (process.priority, process.arrival_time))

    
##########################################################################################
def execute_process(process,gantt_chart, current_time,ready_queue ,waiting_queue,resource_manager,round_robin,time_quantum):
    process.waiting_time += (current_time - process.input_in_ready)
    """Execute a process, considering resource requirements."""
    # Use regex to match all items separated by commas, including nested brackets
    burst_list = re.findall(r'(R\[\d+\]|F\[\d+\]|\d+)', process.bursts[process.pointer_of_bursts])
    for burst in burst_list[process.pointer_of_bursts_CPU:]:
        if burst.startswith('R'):  # Request resource (e.g., "R[x]")
            resource_id = burst  # Keep full "R[x]" format to match ResourceManager keys
            # Check if the resource is available.
            if not resource_manager.is_available(resource_id):
                # Check for deadlock if the resource is unavailable.
                if resource_manager.detect_deadlock(process, resource_id):
                    print(f"Deadlock detected with Process {process.pid} requesting Resource {resource_id}. Terminating the process.")
                    terminate_process(process, resource_manager, ready_queue, waiting_queue)
                    return current_time
                # Add process to waiting queue.
                process.resource_requests.append(resource_id)
                process.type_of_waiting = 2  # Indicate waiting due to unavailable resource.
                process.burst_waiting = resource_id  # Set the resource ID as the waiting identifier.
                waiting_queue.append(process)
                print(f"Process {process.pid} added to waiting queue for Resource {resource_id}.")
                return current_time
            else:
                # Resource is available; allocate it to the process.
                if resource_manager.request_resource(resource_id, process):
                    process.allocated_resources.append(resource_id)  # Track allocated resource.
                    process.pointer_of_bursts_CPU += 1
                    print(f"Resource {resource_id} allocated to Process {process.pid}.")

        elif burst.startswith('F'):  # Free resource (e.g., "F[x]")
            process.pointer_of_bursts_CPU += 1
            resource_id = "R" + burst[1:]  # Convert "F[x]" → "R[x]" to match ResourceManager keys
            # Free the resource through the ResourceManager.
            if resource_id in process.allocated_resources:
                process.allocated_resources.remove(resource_id)
                resource_manager.release_resource(resource_id)
                print(f"Resource {resource_id} released by Process {process.pid}.")
                check_waiting_queue(waiting_queue, ready_queue, current_time, resource_manager)
            else:
                print(f"Warning: Process {process.pid} attempted to release unallocated Resource {resource_id}.")


        else:
            ##here i will edit the consept of time quantum how it will be used
            time = int(burst)
            if process.remaining_time == -1:
                process.remaining_time = time
            if round_robin == 1 and process.remaining_time > time_quantum :
                end_time = current_time + time_quantum
                gantt_chart.append((current_time, process.pid, end_time))
                current_time = end_time
                process.remaining_time = process.remaining_time - time_quantum
                ready_queue.insert(len(ready_queue),process)
                process.input_in_ready = current_time
                return current_time
            else:
                end_time = current_time + process.remaining_time
                gantt_chart.append((current_time, process.pid, end_time))
                current_time = end_time
                process.input_in_ready = current_time
                process.remaining_time = -1
                process.pointer_of_bursts_CPU += 1

    if process.pointer_of_bursts_CPU == len(burst_list):
        #if the process has finished all the bursts of type cpu then we move to the next burst
        process.pointer_of_bursts_CPU = 0
        process.pointer_of_bursts += 1
        if process.pointer_of_bursts == len(process.bursts):
            process.executed = True
            process.end_execution_time=current_time
    return current_time
##########################################################################################
main()