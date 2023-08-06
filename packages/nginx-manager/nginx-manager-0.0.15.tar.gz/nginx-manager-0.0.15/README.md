# ngm

NGINX dynamic modules and websites manager.

## Managing your NGINX modules

The GetPageSpeed repository users have convenient access to over a hundred of NGINX module packages,
via [NGINX Extras collection](https://nginx-extras.getpagespeed.com/).

We realize the need of both our customers and users of other NGINX module collections, to
efficiently manage their installed set of NGINX modules.

The NGINX Manager utility (`ngm`) provides an easy way to list installed or available NGINX modules,
and look up their respective `load_module` directives.

## Usage

### List installed modules

```bash
ngm list
```

Sample output:

+--------------+---------------------------------------+-----------+-------------------------------------------------------------+
| Module ID    | Feature Summary                       | Enabled   | Load Directive used by "ngm enable <module id>"             |
|--------------+---------------------------------------+-----------+-------------------------------------------------------------|
| security     | Modsecurity v3 nginx connector        | No        | load_module modules/ngx_http_modsecurity_module.so;         |
| pagespeed    | Pagespeed dynamic module for nginx    | Yes       | load_module modules/ngx_pagespeed.so;                       |
| doh          | Serving dns-over-https (doh) requests | Yes       | load_module modules/ngx_http_doh_module.so;                 |
| headers-more | Nginx headers more dynamic module     | Yes       | load_module modules/ngx_http_headers_more_filter_module.so; |
| echo         | Nginx echo module                     | Yes       | load_module modules/ngx_http_echo_module.so;                |
+--------------+---------------------------------------+-----------+-------------------------------------------------------------+

Alternative, lengthier syntax to run the same is `ngm list installed`.

### Enable an installed module

```bash
ngm enable <module id>
```

For example:

```bash
ngm enable headers-more
```

This will do the following:

* Add respective `load_module` directive at the top of your `nginx.conf` configuration file
* Run `systemctl reload nginx`

### List installable modules

This command list modules available for installation via GetPageSpeed repositories:

```bash
ngm list available
```

## Installation

### CentOS/RHEL and other RPM-based systems

```bash
yum -y https://extras.getpagespeed.com/release-latest.rpm
yum -y install ngm
```

### Other systems

```bash
pip install nginx-manager
```

## Goals for future

### Modules 

* `ngm list enabled` to see what modules are enabled via `nginx -T` and parsing `load_module` directives
* `ngm disable <module-name>`
* auto-complete for modules
* `ngm compile --i-know-i-should-use-packages-instead github/blah`
* `ngm list` to display modules based on modules dir, then look up via `rpm -ql` all the `.so` instead of `.json` database
* `ngm list` should display latest versions `lastversion`, this requires look up URL: via `rpm`

### Websites

* Create sites from Jinja templates (absorb idea from https://github.com/dvershinin/pyNginx)
* `ngm sites list`
* `ngm sites create wordpress example.com`
* `ngs list` or `ngxs list`?

