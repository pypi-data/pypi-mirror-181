[![Build status](https://github.com/odoopbx/pbx/actions/workflows/docker.yml/badge.svg)](https://github.com/odoopbx/pbx/actions)
[![Build status](https://github.com/odoopbx/pbx/actions/workflows/pypi.yml/badge.svg)](https://github.com/odoopbx/pbx/actions)

# PBX for Asterisk Plus odoo module
This repository contains PBX part for [Asterisk Plus] module.


Repository subfolders:

* `salt`: salt-formulas to install all OdooPBX components
  * `agent/files/etc` agent code
* `pillar`: configuration for salt-formulas
* `docker`: images for Docker Hub and docker-compose.yml example
* `cli`: management command-line tool [odoopbx]

## Agent
Agent is a middleware based on [saltstack] implementing the
API for [Asterisk Plus] to execute asterisk actions and an AMI proxy delivering asterisk events into [Asterisk Plus].

Find out more information at [docs.odoopbx.com](https://docs.odoopbx.com/).


[asterisk]: https://www.asterisk.org/
[odoo]: https://www.odoo.com/
[saltstack]: https://docs.saltproject.io/en/master/topics/salt_system_architecture.html
[Asterisk Plus]: https://github.com/odoopbx/addons
[odoopbx]: https://pypi.org/project/odoopbx/
