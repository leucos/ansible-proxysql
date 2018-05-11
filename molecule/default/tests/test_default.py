import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.fixture()
def AnsibleProxySqlAdminPort(Ansible):
    return Ansible("debug", "msg={{ proxysql_admin_port }}")["msg"]


@pytest.fixture()
def AnsibleProxySqlMysqlPort(Ansible):
    return Ansible("debug", "msg={{ proxysql_mysql_port }}")["msg"]


@pytest.fixture()
def AnsibleGetVar(Ansible, var):
    return Ansible("debug", "msg={{ %s }}" % var)["msg"]


def test_proxysql_listens_admin(host):
    bind = AnsibleGetVar(host.ansible, "proxysql_admin_interface")
    port = AnsibleGetVar(host.ansible, "proxysql_admin_port")
    sock = host.socket("tcp://{0}:{1}".format(bind, port))
    assert sock.is_listening


def test_proxysql_listens_mysql(host):
    bind = AnsibleGetVar(host.ansible, "proxysql_mysql_interface")
    port = AnsibleGetVar(host.ansible, "proxysql_mysql_port")
    sock = host.socket("tcp://{0}:{1}".format(bind, port))
    assert sock.is_listening


def test_proxysql_announces_proper_version(host):
    bind = AnsibleGetVar(host.ansible, "proxysql_admin_interface")
    port = AnsibleGetVar(host.ansible, "proxysql_admin_port")
    version = AnsibleGetVar(host.ansible, "proxysql_mysql_server_version")
    user = AnsibleGetVar(host.ansible, "proxysql_admin_user")
    password = AnsibleGetVar(host.ansible, "proxysql_admin_password")
    command = "mysql -h{0} -P{1} -u{2} -p{3} ".format(bind, port, user, password)
    command = command + "-e 'SELECT variable_value "
    command = command + "FROM runtime_global_variables "
    command = command + "WHERE variable_name=\"mysql-server_version\"'"
    assert version in host.check_output(command)
