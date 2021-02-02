import sys
import output # format and write output.
import parser # read config and parse jobs.
import send_request # send request for given job.

# Get path to config from command-line arguments.
if len(sys.argv) != 2:
    exit("Path to config not given!\n", "Programm closing...")
path = sys.argv[1]

# Parse config file. 
jobs = parser.parse_jobs(path)

# Handle jobs.
results = []
for job in jobs:
    # Execute job.
    try:
        r = send_request.send_req(job)
    except Exception as exc:
        print(exc, "\n")
        continue

    # Append formattet output for storing results.
    results.append(output.format(job, r))

# Save results to file ("results/path").
output.write(path, results)
