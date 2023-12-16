with open("input.txt") as input_file:
    input_ = input_file.read() 

input_lines = input_.split('\n')

total_history = 0
total_future = 0
for line in input_lines:
        
    trace_raw = line.split()
    trace = [int(t) for t in trace_raw]

    last_numbers = []
    first_numbers = []

    done = False
    while(not done):
        new_trace = []
        last_numbers.append(trace[-1])
        first_numbers.append(trace[0])
        for i in range(len(trace) - 1):
            new_trace.append(trace[i+1] - trace[i])

        done = True
        for t in new_trace:
            done = (done and (t == 0))

        trace = new_trace

    total_history += sum(last_numbers)
    future = 0
    first_numbers.reverse()
    for no in first_numbers:
        future = no - future
    total_future += future

print(total_history)
print(total_future)