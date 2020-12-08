# dlcs-cli

Command line interface for DLCS.

This is an experimental work in progress and will be updated.

You can do this kind of thing:

## Getting Started

You need to create a `~/.dlcs-cli/credentials.json` file containing default values.

```json
{
  "key": "your_api_key",
  "secret": "your_secret",
  "api_url": "https://api.dlcs",
  "origin": "storage-origin",
  "customer": 2,
  "space": 7
}
```

- `api_key`: Username for basic auth
- `secret`: Password for basic auth
- `space`: Customer space to do operations on
- `api_url`: The route of the API to call (optional: defaults to 'api.dlcs.io')
- `origin`: Bucket used to upload to (optional: defaults to 'storage-origin')

### Installing

You can install this as a Python module in "edit mode" locally from the parent folder by:

```
pip3 install -e dlcs-cli
```

## Commands 

To make the CLI easier to manage commands are grouped, this allows commands to be in the format: 

`dlcs-cli <group> <command> <args>` 

Commands are listed below, unless otherwise stated, full output from DLCS is printed to stdout.

### Create customer

Create a new customer.

> Needs Admin credentials

`dlcs-cli customer create --name foo --display_name "Foo Bar"`

### Create API key

Create a new API key for customer. CustomerId taken from `settings.py`.

`dlcs-cli customer create_api_key`

### Create space

Create new space for customer. CustomerId taken from `settings.py`

`dlcs-cli customer create_space --name my-space`

### Ingest single image from remote origin

Ingest a single image that is currently in a remote origin (currently supports http* origins only)

`dlcs-cli ingest image --id image-from-cli --location https://images.io/my-image --s3 from-cli`

### Ingest images from folder

Ingest a local folder full of images. `origin` property must be populated, with the name of an S3 bucket. All images will be uploaded to this bucket, then a batch will be created to ingest images from that location.

The ideal bucket to use is the DLCS 'origin bucket'. This is the bucket that the Portal will upload images to when uploaded via the UI. This is automatically configured as a 'optimised origin' so avoids the DLCS needing to make a copy.

Image Id is set to current filename. Images are uploaded in order.

Optional/Default args:

* `increment_number_field` (default of `n1`) - which specifies the metadata field to use to increment with image order.
* `profile` (default of `default`) - specifies which AWS profile to use for uploading images to bucket.
* Metadata fields: (`n1`, `n2`, `n3`, `s1`, `s2`, `s3`). Optional fields for specifying metadata. If a value is specified for the same field as `increment_number_field`, then `increment_number_field` wins.

> Current limitations - assumes eu-west-1 region. Assumes use of AWS profile for uploading.

`dlcs-cli ingest folder --directory /path/to/imgs/ --n2 99 --s1 string-value`

### Debug Settings

View current values in settings.py (API secret key masked)

`dlcs-cli debug settings`

## TODO/Limitations

- Allow space/customer etc to be overriden in a per-command basis.
- Bulk uploads to non-S3 location
- Handle different AWS regions
- Handle different methods of AWS auth