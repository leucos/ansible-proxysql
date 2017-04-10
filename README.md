# ProxySQL Ansible role

This role will install proxysql on Ubuntu Xenial (16.04) from [sysown release](https://github.com/sysown/proxysql/releases).

## Requirements

None

## Role Handlers

| Name                     | Type    | Description                                                                 |
| ------------------------ | ------- | --------------------------------------------------------------------------- |
| Restart proxysql normal  | service | Restarts proxysql using service (SysV based) when proxysql_initial is False |
| Restart proxysql initial | command | Restarts proxysql in initial mode when proxysql_initial is True             |
| Restart proxysql         | Virtual | Calls all above handlers                                                    |

## Tags

| Name     | Description           |
| -------- | --------------------- |
| proxysql | Applies to whole role |


## Role Variables

| Name                       | Default   | Type   | Description                                                       |
| -----                      | -------   | ------ | -----------                                                       |
| proxysql_version           | 1.5.3     | String | ProxySQL version to install                                       |
| proxysql_admin_user        | admin     | String | Username for ProxySQL admin                                       |
| proxysql_admin_password    | admin     | String | Password for the above user                                       |
| proxysql_admin_interface   | 127.0.0.1 | String | Bind address for admin interface                                  |
| proxysql_admin_port        | 6032      | Number | Bind port for administrative interface                            |
| proxysql_initial           | False     | Bool   | Wipes existing config database when True (see --initial CLI flag) |
| proxysql_mysql_interface   | 127.0.0.1 | String | MySQL bind interface                                              |
| proxysql_mysql_port        | 6033      | Number | MySQL bind port                                                   |
| proxysql_mysql_query_rules | []        | Array  | Configuration-file query rules                                    |
| proxysql_mysql_servers     | []        | Array  | Configuration-file servers                                        |
| proxysql_mysql_users       | []        | Array  | Configuration-file users                                          |

## Example

### Requirements

```yaml
- src: git+ssh://git@github.com/leucos/ansible-proxysql.git
  version: origin/master
```
_Use a fixed tag instead of origin/master if possible_

### Playbook

```yaml
- hosts: proxylb
  roles:
    - role-proxysql
```

### Inventory

```yaml
proxysql_mysql_query_rules:
  - match_pattern: "^SELECT .* FOR UPDATE$"
    destination_hostgroup: 0
  - match_pattern: "^SELECT"
    destination_hostgroup: 1

proxysql_mysql_servers:
   - address: 1.2.3.4
     port: 3306
     hostgroup: 0
   - address: 5.6.7.8
     port: 3306
     hostgroup: 1
```

## Tests

To run tests locally in a Vagrant machine, just hit:

```bash
vagrant up
vagrant ssh -c specs
```

If you want to run the test playbook fast (i.e., without re-installing Ansible),
just run:

```bash
vagrant ssh -c 'specs -p'
```

## Notes

This role follows [Semantic Versionning](http://semver.org/)
conventions.

Besides proxysql, the `mysql-common` package will be installed by this role.

## License

MIT

## Author Information

@leucos

