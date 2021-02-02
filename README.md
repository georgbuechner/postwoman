# Scheduler/ Forwarder
The _"Scheduler"_ and _"Forwarder"_ are both small python scripts designed to send 
HTTP-requests to given hosts. 
Both scripts execute "jobs". These jobs are specified in a config-file (yaml). Thus,
when running the scripts, one is in need to pass the path to the specific
config. (__NOTE__: _it is advised to use absolute paths_)
While the Scheduler is designed to send a number of similar requests to a single host,
the Forwarder is designed to execute only two jobs (get, then
forward). 

## Jobs 
Essentially both the Scheduler and the Forwarder work by executing so called
"jobs". What is a job? A job is merely a json, storing url, (HTTP-)verb and
eventually a function body. This might look something like this:
```yaml
url: "HTTP://127.0.0.1:9680/api/assets/location"
verb: "post"
body: '{"latitude":12.3456, "longitude":65.4321, "city":"Copenhagen"}'
```

## Output and response
The direct console-output will give you a sort summary of all sent requests
and the HTTP-return-code, looking something like this: 

```
HTTP://127.0.0.1:9680/api/assets/location: "post": <Response [200]>
```

In addition, a json is created with a complete print of all requests and their responses, so you
can easily copy and paste, if they are need for further requests. In the case
you use the Scheduler/ Forwarder in combination with a cronjob, you can have a
look once in a while, to assure yourself that everything is going as expected. 
These files are stored in the "results" folder. (The filename is identical with
the config-name.)


## Specific Scheduler/ Forwarder

### Scheduler 
The Scheduler is designed to easily send a series of requests to to one given
host. This is done by specifying a "default"-request. The jobs then merely parse
their specifics into the default URL/ body. Let's take a look at a possible
config:

```yaml
defaults:
    url: "HTTP://127.0.0.1:9680/api/assets/location"
    verb: "post"
    body: '{{"latitude":{0}, "longitude":{1}, "city":"{2}"}}'
```

What we essentially do, is specifying a URL, a verb and a _"template"_ for the
request-body. So in this example, what latitude, longitude and city might be, 
will be decided by every single job:

```yaml
jobs:
    - body_params: [60.54321, 60.65432, "Gladbach"]
    - body_params: [50.54321, 50.65432, "Dortmund"]
    - body_params: [40.54321, 40.65432, "Frankfurt am Main"]
```

And that's it! The Scheduler will parse the body-parameters into the template
which we specified in the defaults.

Of course this can also be done for get-request. Here is a complete working
example of a config to execute a series of get-requests:

```yaml
defaults:
    url: "HTTP://127.0.0.1:9680/api/assets/location/{0}"
    verb: "get"
jobs:
    - url_params: ["5bd99c2b-ee6e-4d13-83ea-b89fc40d70e4"]
    - url_params: ["76f43209-1a61-4227-b575-61532b263627"]
    - url_params: [""]
    - url_params: ["invalud uuid"]
    - url_params: ["76f43209-1a61-4227-b575-61532b263633"]
```

### Forwarder
The Forwarder's functionality is a lot "narrower" but has (in contrast to the
Scheduler) the ability to _use_ the first request made, which the scheduler does
not.
Also the Forwarder takes an additional command-line-argument specifying _what_ to
get.
The Scheduler is limited to two jobs being executed: The first gets some data,
the second forwards the data to a specified host. 
Again, lets have a look at a
config-file: 

```yaml
from: 
    url: "HTTP://127.0.0.1:9680/api/assets/location/"

to: 
    url: "HTTP://127.0.0.1:9680/api/assets/location"
    verb: "post"
```

The execution steps are:
- parse job A and add command-line-argument to URL
- execute job A
- parse job B and set the response of job A as body for job B 
- execute job B

__NOTE__: 
- Currently the first job is limited to the get-functionality. The script takes
  an _additional neccesary_ command-line-argument with the specified URL-parameter.
- Currently the forwarding can only modify the request _body_ not the URL.


## Advanced Usage
### Scheduler
One can overwrite the attributes `url`, `verb` and `body` for a single job for further
customizing ones config. One should however keep in mind, that a job never has
any knowledge of the job executed before.

### Forwarder
One might like to specify a few attributes not being forwarded. For this one can
specify the "remove-attribute": 

```yaml
from: 
    url: "HTTP://127.0.0.1:9680/api/assets/location/"
    verb: "get"

to: 
    url: "HTTP://127.0.0.1:9680/api/assets/location"
    verb: "post"

remove: 
    - "uuid"
```

Now the uuid will be removed, before forwarding. 
(__NOTE__ this is concurrently only working in the first-level of a json)
