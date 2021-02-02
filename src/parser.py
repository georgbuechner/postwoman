import yaml
import json  

# Reads config (yaml) from given path.
def read_config(path):
    with open(path, 'r') as stream:
        try: 
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            exit(exc, "\n", "Programm closing...")

# Generates verb, url and body for every job, by parsing url-/body-parameters into defaults.
def parse_jobs(path):
    config = read_config(path)
    # Handle jobs.
    for job in config["jobs"]:
        # Get URL from either job, or defaults and parse given parameters.
        job["url"] = handle_params(job.get("url", config["defaults"]["url"]), 
                job.get("url_params", []))
        job["verb"] = job.get("verb", config["defaults"].get("verb", "get"))
        # Get body from either job, or defaults and parse given parameters.
        job["body"] = handle_params(job.get("body", config["defaults"].get("body", "")), 
                job.get("body_params", [])) 
    return config["jobs"]

# Parses single job with given name, by reading config at given path.
def parse_job(path, job_name):
    config = read_config(path)
    job = {}
    try:
        job["verb"] = config[job_name]["verb"]
        job["url"] = config[job_name]["url"]
        job["body"] = config[job_name].get("body", "")
    except Exception:
        exit("job_name unkown, or verb or url missing.\n", "Program closing.")
    return job

# Parses given parameters into a template (might be body or URL with parameters).
def handle_params(string, params):
    if string == "" or len(params) == 0:
        return string
    return string.format(*params)

# Removes fields from response, which are set by config file.
def process_resp_before_forwarding(path, resp):
    config = read_config(path)
    for elem in config["remove"]:
        if elem in resp:
            del resp[elem]
    return resp


