import json
import sys
import output # format and write output.
import parser # read config and parse jobs.
import send_request # send request for given job.

# Get path to config from command-line arguments.
if len(sys.argv) != 3:
    exit("path to config, or uuid not given")
path = sys.argv[1]
uuid = sys.argv[2]

# Parse first job. 
job1 = parser.parse_job(path, "from")
job1["url"] = job1["url"] + uuid

# Send first request.
try:
    resp = send_request.send_req(job1)
except Exception as exc:
    print(exc, "\n")
    exit("Program closing...")

# Process request and then forward.
resp = parser.process_resp_before_forwarding(path, resp.json())
job2 = parser.parse_job(path, "to")
job2["body"] = json.dumps(resp)
try:
    resp2 = send_request.send_req(job2)
except Exception as exc:
    exit(exec, "\n", "Program closing...")
    output.write([])

# Print results to file.
output.write(path, [output.format(job2, resp2)])
