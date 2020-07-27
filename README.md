# dlcs-cli
Command line interface for dlcs

This is an experimental work in progress and only does one useful thing at the moment.

It borrows the dlcs-client classes, but they'll come out again once I see where thisis going.

You can do this kind of thing:

```
python dlcs.py ingest-image --image-id horse05 --image-location https://tomcrane.github.io/scratch/img/shire/DSCF6691.JPG --s1 horse --n2 4
```

...but I'd like image-location to allow _local_ files, and also upload whole folders with rules for incrementing metadata, naming etc.

## Getting Started

You need to specify a `settings.py` file containing default values in the root of the repository. Sample file shown below:

```py
DLCS_ENTRY = '' # the route of the API to call (e.g. https://api.dlcs.io)
DLCS_API_KEY = 'api-key' # username for basic auth
DLCS_SECRET = 'my-super-secret' # password for basic auth
DLCS_CUSTOMER_ID = 1 # customer to do operations on
DLCS_SPACE = 1 # space to do operations on
```