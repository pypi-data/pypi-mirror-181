## A named YAML file provider for octoDNS

An [octoDNS](https://github.com/octodns/octodns/) provider that targets a named YAML file.
Useful for sharing records between multiple zones.

### Installation

#### Command line

```
pip install octodns_namedfileyaml
```

#### requirements.txt/setup.py

Pinning specific versions or SHAs is recommended to avoid unplanned upgrades.

##### Versions

**Waiting for a new octodns release to support this**

```
# Start with the latest versions and don't just copy what's here
octodns==0.9.14
octodns_namedfileyaml==0.0.1
```

##### SHAs

```
# Start with the latest/specific versions and don't just copy what's here
-e git+https://git@github.com/octodns/octodns.git@af23c00b266c959f4001cd809b04511128a5602b#egg=octodns
-e git+https://git@github.com/octodns/octodns_namedfileyaml.git@ec9661f8b335241ae4746eea467a8509205e6a30#egg=octodns_namedfileyaml
```

### Configuration

Example for sharing email records between two domains managed at cloudflare:

```yaml
providers:
  zones:
    class: octodns_namedfileyaml.YamlProvider
    directory: ./zones
    enforce_order: False
    default_ttl: 300
  shared.email:
    class: octodns_namedfileyaml.NamedFileYamlProvider
    directory: ./shared
    filename: mail.yaml
  cloudflare:
    class: octodns_cloudflare.CloudflareProvider
    token: env/CLOUDFLARE_TOKEN
    strict_supports: true

zones:
  example.com.:
    sources:
      - zones
      - shared.email
    targets:
      - cloudflare
  example.net.:
    sources:
      - zones
      - shared.email
    targets:
      - cloudflare
```

### Support Information

#### Records

All octoDNS record types are supported.

#### Dynamic

NamedFileYamlProvider does not support dynamic records.

### Development

See the [/script/](/script/) directory for some tools to help with the development process. They generally follow the [Script to rule them all](https://github.com/github/scripts-to-rule-them-all) pattern. Most useful is `./script/bootstrap` which will create a venv and install both the runtime and development related requirements. It will also hook up a pre-commit hook that covers most of what's run by CI.
