import json

# Converts job (verb, url, body) and response to be a json.
def format(job, response):
    result = {"url":job["url"], "verb":job["verb"], 
        "body":job["body"], "resp_status":response.status_code}
    # Remove trace, if exists, as it's making file completely unreadable.
    try:
        result["resp_body"] = response.json()
        if "trace" in result["resp_body"]:
            del result["resp_body"]["trace"]
    except Exception as exc:
        result["resp_body"] = ""
    return result

# Writes a list of results to a specified output file.
def write(path, results):
    result_path = path.replace("configs", "results")
    with open(result_path, "w") as result_file:
        json.dump(results, result_file, indent=4)
