"""Install a Reahl Linux Server

Use the InstallIt framework to rteinstallserver a Linux Server for a Reahl Application
"""

import argparse
from pathlib import Path

from beetools import beearchiver, beeutils, beescript
import configparserext
import installit

_PROJ_DESC = __doc__.split("\n")[0]
_PROJ_PATH = Path(__file__)
_PROJ_NAME = _PROJ_PATH.stem


class RteDbServer:
    """

    Parameters
    ----------

    Returns
    -------

    Examples
    --------
    # No proper doctest (<<<) because it is os dependent

    """

    def __init__(self, p_ini_pth):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        self.success = True
        self.ini_path = p_ini_pth
        self.ini = configparserext.ConfigParserExt(inline_comment_prefixes="#")
        self.ini.read([self.ini_path])

        self.batch_name_prefix = self.ini.get("General", "BatchNamePrefix")
        self.command_name_prefix = self.ini.get("General", "CommandNamePrefix")
        self.curr_os = beeutils.get_os()
        self.install_userid = self.ini.get("DEFAULT", "InstallUserId")
        self.mysql_rights_prefix = self.ini.get("General", "MySQLRightsPrefix")
        self.package_prefix = self.ini.get("General", "PackagePrefix")
        self.target_os = self.ini.get("General", "TargetOS")
        self.user_prefix = self.ini.get("General", "UserPrefix")

        self.inst_tls = installit.InstallIt()
        pass

    def configure_mysql_remote_access(self):
        admin = self.ini.get("MySQLUsers", "Admin", p_split=True)
        users = [
            x[1]
            for x in self.ini.get(
                "MySQLUsers", self.user_prefix, p_prefix=True, p_split=True
            )
        ]
        rights = [
            x[1]
            for x in self.ini.get(
                "MySQLUsers", self.mysql_rights_prefix, p_prefix=True, p_split=True
            )
        ]
        success = self.inst_tls.configure_mysql_remote_access(
            admin, [users[1]], [rights[2]], p_verbose=True
        )
        return success

    def create_linux_users(self):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        success = True
        if self.curr_os == beeutils.LINUX:
            users = [
                x[1]
                for x in self.ini.get(
                    "LinuxUsers", self.user_prefix, p_prefix=True, p_split=True
                )
            ]
            success = self.inst_tls.create_linux_users(users, p_verbose=True)
        return success

    def create_mysql_users(self):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        success = True
        admin = self.ini.get("MySQLUsers", "Admin", p_split=True)
        users = [
            x[1]
            for x in self.ini.get(
                "MySQLUsers", self.user_prefix, p_prefix=True, p_split=True
            )
        ]
        success = (
            self.inst_tls.create_mysql_users(admin, users, p_verbose=True) and success
        )
        rights = [
            x[1]
            for x in self.ini.get(
                "MySQLUsers", self.mysql_rights_prefix, p_prefix=True, p_split=True
            )
        ]
        success = (
            self.inst_tls.grant_mysql_user_rights(admin, rights, p_verbose=True)
            and success
        )
        return success

    def install(self):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        batch = [
            x[1]
            for x in self.ini.get(
                "{}01".format(self.batch_name_prefix),
                self.command_name_prefix,
                p_prefix=True,
                p_split=True,
            )
        ]
        beescript.exec_batch(batch, p_verbose=True)
        self.secure_mysql()
        self.start_firewall()
        batch = [
            x[1]
            for x in self.ini.get(
                "{}02".format(self.batch_name_prefix),
                self.command_name_prefix,
                p_prefix=True,
                p_split=True,
            )
        ]
        beescript.exec_batch(batch, p_verbose=True)
        self.create_linux_users()
        batch = [
            x[1]
            for x in self.ini.get(
                "{}03".format(self.batch_name_prefix),
                self.command_name_prefix,
                p_prefix=True,
                p_split=True,
            )
        ]
        self.create_mysql_users()
        self.configure_mysql_remote_access()
        self.install_system_prereq_packages()
        beescript.exec_batch(batch, p_verbose=True)
        pass

    def install_system_prereq_packages(self):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        script_cmds = []
        for package in self.ini.get(
            "SystemPreReqPackages", self.package_prefix, p_prefix=True, p_split=True
        ):
            if self.curr_os == beeutils.LINUX:
                script_cmds.append("sudo pip3 install {}".format(package[1][0]))
            else:
                script_cmds.append("pip3 rteinstallserver {}".format(package[1][0]))
        switches = []
        if self.curr_os == beeutils.LINUX:
            switches = ["-x"]
        beescript.exec_batch_in_session(
            script_cmds,
            p_script_name="InstallSystemPreReqPackages",
            p_switches=switches,
            p_verbose=True,
        )
        pass

    def run(self):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        if beeutils.get_os() == self.target_os:
            self.install()
        else:
            print(
                beearchiver.msg_error(
                    "Configuration not for this operating system\nTarget OS:\t{}\nCurrent OS:\t{}".format(
                        self.target_os, self.curr_os
                    )
                )
            )
        pass

    def secure_mysql(self):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        switches = []
        if self.curr_os == beeutils.LINUX:
            switches.append(["-x"])
        # script_name = 'secure_mysql'
        admin = self.ini.get("MySQLUsers", "Admin", p_split=True)
        # script_cmds = [ 'sudo mysql --user=root --password={} <<_EOF_'.format( admin[ 1 ])]
        script_cmds = self.inst_tls.make_sql_base_cmd(admin) + [
            "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '{}';".format(
                admin[1]
            )
        ]
        beescript.exec_cmd(script_cmds, p_verbose=True)
        script_cmds = self.inst_tls.make_sql_base_cmd(admin) + [
            "DELETE FROM mysql.user WHERE User='';"
        ]
        beescript.exec_cmd(script_cmds, p_verbose=True)
        script_cmds = self.inst_tls.make_sql_base_cmd(admin) + [
            "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"
        ]
        beescript.exec_cmd(script_cmds, p_verbose=True)
        script_cmds = self.inst_tls.make_sql_base_cmd(admin) + [
            "DROP DATABASE IF EXISTS test;"
        ]
        beescript.exec_cmd(script_cmds, p_verbose=True)
        script_cmds = self.inst_tls.make_sql_base_cmd(admin) + [
            "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"
        ]
        beescript.exec_cmd(script_cmds, p_verbose=True)
        script_cmds = self.inst_tls.make_sql_base_cmd(admin) + ["FLUSH PRIVILEGES;"]
        beescript.exec_cmd(script_cmds, p_verbose=True)
        pass

    def start_firewall(self):
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        # No proper doctest (<<<) because it is os dependent

        """
        if self.curr_os == beeutils.LINUX:
            switches = ["-x"]
            script_name = "start_firewall"
            script_cmds = [
                "sudo ufw allow OpenSSH",
                "sudo ufw allow 'Nginx HTTP'",
                "yes | sudo ufw enable",
                "sudo ufw status",
            ]
            beescript.exec_batch_in_session(
                script_cmds,
                p_script_name=script_name,
                p_verbose=True,
                p_switches=switches,
            )
        pass


# def project_desc():
#     return _PROJ_DESC


class Args:
    def __init__(self):
        arg_parser = argparse.ArgumentParser(description="Get configuration parameters")
        arg_parser.add_argument(
            "-c",
            "--config-path",
            help="Config file name",
            default=arg_parser.prog[: arg_parser.prog.find(".") + 1] + "ini",
        )
        args = arg_parser.parse_args()
        self.ini_path = args.config_path


if __name__ == "__main__":
    b_tls = beearchiver.Archiver(
        _PROJ_DESC,
        _PROJ_PATH,
        p_app_ini_file_name=Args().ini_path,
    )
    b_tls.print_header(p_cls=False)
    rhl_server = RteDbServer(Args().ini_path)
    if rhl_server.success:
        rhl_server.run()
    b_tls.print_footer()
