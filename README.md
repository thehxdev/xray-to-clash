## How to use

- `app.py`:

```txt
usage: app.py [-h] -c CONFIG -t TEMPLATE

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        ABSOLUTE path to xray json config file.
  -t TEMPLATE, --template TEMPLATE
                        Template file for building clash config
                        for each user.
```

- `makeTmplateYaml.py`:

```txt
usage: makeTemplateYaml.py [-h] -c CONFIG [-s SERVER] [-d DOMAIN] -b BASE -n NAME

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        ABSOLUTE path to xray json config file.
  -s SERVER, --server SERVER
                        Your server's IP address.
  -d DOMAIN, --domain DOMAIN
                        Your domain name (If you have one).
  -b BASE, --base BASE  Base file for building clash config.
  -n NAME, --name NAME  Set the name of the proxy that will be in clash config file.
```
