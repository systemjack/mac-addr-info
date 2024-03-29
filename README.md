# mac-addr-info
A client using the [macaddress.io](https://macaddress.io/) API to look up MAC address metadata.
## Prerequisites
### For command line use
To use this script directly from the command line the [requests](https://2.python-requests.org/en/master/) library needs to be installed:
```
pip install requests
```
### Building a docker image
A docker file is provided to build a runable image (in which case a separate install of **requests** is not required):
```
docker build -t mac-addr-info .
```
### An API key is required
You must have an existing account with [macaddress.io](https://macaddress.io/) in order to use this utility. 
The apiKey corresponding to your account must be provided by setting the **MACADDRESS_API_KEY** environment variable, or via the **key** command line parameter.
## Running the utility
### Example command line usage
The MAC address may be provided as the first argument or piped to **stdin**. Here are a couple examples:
```
./mac-addr-info.py 44:38:39:ff:ef:57

./mac-addr-info.py 443839ffef57 --key YOUR_API_KEY

echo '44-38-39-ff-ef-57' | ./mac-addr-info.py --output json
```
### Example Docker usage
The Docker container is configured to allow passing command line parameters directly.

Here is an example passing the apiKey into the container via environment variable: 

```
docker run -e "MACADDRESS_API_KEY=your_api_key" mac-addr-info 44:38:39:ff:ef:57
```
### Multiple MAC arguments
If more than one MAC address is supplied, the application will make a request for each MAC and print out the result on a separate line. Multiple addresses provided via standard input must be newline separated. Invalid MAC addresses will be skipped without interrupting the process.
Examples:
```
printf "44.38.39.ff.ef.57\n5c:f9:38:92:6d:30\n" | ./mac-addr-info.py

./mac-addr-info.py 443839ffef57 5c:f9:38:92:6d:30
```
### Controlling output
The **--output** parameter can be used to control the format of the query results.

The options available are: *vendor, json, xml, csv*.

The default *vendor* option provides only the company name as a result.
## Usage
Here are the detailed usage options:
```
usage: mac-addr-info.py [-h] [--key KEY] [--output {vendor,json,xml,csv}]
                        [--api API]
                        [mac [mac ...]]

positional arguments:
  mac                   mac address(es) to query

optional arguments:
  -h, --help            show this help message and exit
  --key KEY             your macaddress.io api key (defaults to
                        MACADDRESS_API_KEY environment variable)
  --output {vendor,json,xml,csv}
                        output format to request (default: vendor)
  --api API             api path (default: https://api.macaddress.io/v1)

note: accepts newline delimited mac addresses from stdin as well
```
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
## Acknowledgments
I borrowed the MAC address regex from [here](https://stackoverflow.com/a/7629690/3019685). Much faster and more vetted than coming up with it myself.
