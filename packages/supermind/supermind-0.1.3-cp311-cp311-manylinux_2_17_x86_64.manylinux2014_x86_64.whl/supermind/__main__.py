# @Author: xiewenqian <int>
# @Date:   2022-10-24:10:33+08:00
# @Email:  wixb50@gmail.com
# @Last modified by:   int
# @Last modified time: 2022-10-24T16:27:14+08:00


import os
import shutil

from supermind.data.main import cli, click, setting


@cli.command()
@click.help_option('-h', '--help')
@click.option('-u', '--username', 'username', required=True, help="用户名")
@click.option('-p', '--password', 'password', required=True, help="密码")
def login(username, password):
    """用户登录
    """
    # make user root path
    rpath = setting.ROOT_PATH
    os.makedirs(rpath, exist_ok=True)
    shutil.copy(os.path.join(os.path.dirname(__file__), 'mod_config.yml'), rpath)
    # login supermind account
    from supermind.data.main import mg_api
    mg_api.login(username, password)
    click.echo('登录成功。')


@cli.command()
@click.help_option('-h', '--help')
def logout():
    """用户注销
    """
    from supermind.data.main import mg_api
    mg_api.logout()
    click.echo('注销成功。')


if __name__ == '__main__':
    cli()
