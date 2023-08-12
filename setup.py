import os
import site

from setuptools import setup
from setuptools.command.install import install


class PostInstall(install):
    @staticmethod
    def get_version(package_check):
        result_cmd = os.popen(f'{package_check} -v').read()
        result_cmd = result_cmd.replace('v', '')
        if len(result_cmd) == 0:
            return {
                'version_int': 0,
                'version': '0',
            }
        return {
            'version_int': int(result_cmd.split('.')[0]),
            'version': result_cmd,
        }

    # noinspection PyBroadException
    def run(self):
        node_result = self.get_version('node')
        npm_result = self.get_version('npm')
        if node_result['version_int'] == 0:
            raise Exception('Please install node (15.+)')
        if npm_result['version_int'] == 0:
            raise Exception('Please install npm (7.+)')
        if node_result['version_int'] < 15:
            raise Exception(
                'Needed node 15.+, '
                'actually installed is '
                f"{node_result['version']}",
            )
        if npm_result['version_int'] < 7:
            raise Exception(
                'Needed npm 7.+, '
                'actually installed is '
                f"{npm_result['version']}",
            )
        os.system('npm install')
        os.system('npm install --prefix newcalls/js/')
        if 'pip' in os.getcwd():
            print(
                'Copying files from '
                f'{os.getcwd()}/newcalls/'
                ' to '
                f'{site.getsitepackages()[0]}/newcalls/',
            )
            if os.path.exists(
                f'{site.getsitepackages()[0]}/newcalls',
            ):
                os.system(
                    'mkdir '
                    f'{site.getsitepackages()[0]}/newcalls',
                )
            if not os.path.exists(
                f'{site.getsitepackages()[0]}/newcalls/js',
            ):
                os.system(
                    'mkdir '
                    f'{site.getsitepackages()[0]}'
                    '/newcalls/js',
                )
            if os.path.exists(
                f'{site.getsitepackages()[0]}/newcalls/js/lib',
            ):
                os.system(
                    'rm -r '
                    f'{site.getsitepackages()[0]}'
                    '/newcalls/js/lib',
                )
            if os.path.exists(
                f'{site.getsitepackages()[0]}'
                '/newcalls/js/node_modules',
            ):
                os.system(
                    'rm -r '
                    f'{site.getsitepackages()[0]}'
                    '/newcalls/js/node_modules',
                )
            os.system(
                'cp -r '
                f'{os.getcwd()}/newcalls/js/lib '
                f'{site.getsitepackages()[0]}/newcalls/js/',
            )
            os.system(
                'cp -r '
                'newcalls/js/node_modules '
                f'{site.getsitepackages()[0]}/newcalls/js/',
            )
        install.run(self)


setup(
    cmdclass={
        'install': PostInstall,
    },
)