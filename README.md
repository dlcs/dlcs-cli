# dlcs-cli

Command line interface for DLCS.

This is an experimental work in progress and will be updated.

You can do this kind of thing:

## Getting Started

You need to specify a `settings.py` file containing default values in the root of the repository. Sample file shown below:

```py
DLCS_ENTRY = 'https://api.dlcs' # the route of the API to call (e.g. https://api.dlcs.io)
DLCS_API_KEY = 'api-key' # username for basic auth
DLCS_SECRET = 'my-super-secret' # password for basic auth
DLCS_CUSTOMER_ID = 1 # customer to do operations on
DLCS_SPACE = 1 # space to do operations on
DLCS_ORIGIN = 'storage-origin' # bucket used to upload to (optional)
```

## Commands 

To make the CLI easier to manage commands are grouped, this allows commands to be in the format: `python dlcs.py <group> <command> <args>` 

Commands are listed below, unless otherwise stated, full output from DLCS is printed to stdout.

### Create customer

Create a new customer.

> Needs Admin credentials

`python dlcs.py customer create --name foo --display_name "Foo Bar"`

### Create API key

Create a new API key for customer. CustomerId taken from `settings.py`.

`python dlcs.py customer create_api_key`

### Create space

Create new space for customer. CustomerId taken from `settings.py`

`python dlcs.py customer create_space --name my-space`

### Ingest images from folder

Ingest a local folder full of images. `settings.DLCS_ORIGIN` property must be populated, with the name of an S3 bucket. All images will be uploaded to this bucket, then a batch will be created to ingest images from that location.

The ideal bucket to use is the DLCS 'origin bucket'. This is the bucket that the Portal will upload images to when uploaded via the UI. This is automatically configured as a 'optimised origin' so avoids the DLCS needing to make a copy.

Image Id is set to current filename. Images are uploaded in order.

Optional/Default args:

* `increment_number_field` (default of `n1`) - which specifies the metadata field to use to increment with image order.
* `profile` (default of `default`) - specifies which AWS profile to use for uploading images to bucket.
* Metadata fields: (`n1`, `n2`, `n3`, `s1`, `s2`, `s3`). Optional fields for specifying metadata. If a value is specified for the same field as `increment_number_field`, then `increment_number_field` wins.

> Current limitations - assumes eu-west-1 region. Assumes use of AWS profile for uploading.

`python dlcs.py ingest folder --dir /path/to/imgs/ --n2 99 --s1 string-value`

### Debug Settings

View current values in settings.py (API secret key masked)

`python dlcs.py debug settings`

## TODO

- Allow space/customer etc to be overriden in a per-command basis.