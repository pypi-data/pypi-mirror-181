import os
import re
import subprocess

import click
from colorama import Back, Fore, Style


class MkGit:
    _PATH_MAIN = subprocess.getoutput('git rev-parse --show-toplevel').strip()
    _PATH_MAIN_CONFIG = f'{_PATH_MAIN}/.git/config'
    _PATH_SUB_LS = subprocess.getoutput(
        "git config --file .gitmodules --get-regexp path | awk '{ print $2 }'"
    ).splitlines()
    _PATH_SUB = list()
    _RESET = Style.RESET_ALL

    @classmethod
    def _get_submodules(cls):
        cls._PATH_SUB = [
            os.path.join(cls._PATH_MAIN, _) for _ in cls._PATH_SUB_LS
        ]

    @classmethod
    def _re_restores(cls, msg, restores):
        pattern = re.compile(r"(pathspec ')(.*)(')")
        for _ in pattern.findall(msg):
            restores.remove(_[1])

    @classmethod
    def add(cls, ignore):
        """ Auto add all files to git except submodules """
        cls._get_submodules()
        subprocess.run('git add .', shell=True)
        restores = ['git', 'restore', '--stage']

        if cls._PATH_SUB:
            restores.extend(cls._PATH_SUB_LS)

        if ignore:
            restores.extend(ignore)

        if len(restores) == 3:
            subprocess.run('git status', shell=True)
            return

        e = subprocess.run(restores, stderr=subprocess.PIPE, text=True).stderr
        if e:
            cls._re_restores(msg=e, restores=restores)
            subprocess.run(restores)

        subprocess.run('git status', shell=True)
        print(e or None)

    @staticmethod
    def _re_words(info):
        """
        e.q.
            From https://xxx.net/xxx/xx
             - [
               group1: (deleted)
               group2: (]         (none)     -> origin/)
               group3: (feature/michael/xxxx)

             - [deleted] (none) -> origin/feature/xxxx/add-advanced-task
             - [deleted] (none) -> origin/patch/michael/rename-success
        """
        pattern = re.compile(r'\[(.+)(\].+-> origin/)(.+)')
        info = pattern.sub(
            rf'[{Fore.CYAN}\1{Fore.RESET}\2{Fore.CYAN}\3{Fore.RESET}', info)
        return info

    @staticmethod
    def _re_branchs(msg):
        """ """
        pattern_remote = re.compile(r'(remotes[/\w]*)')
        pattern_now = re.compile(r'(\*)( )(.*)')
        msg = pattern_remote.sub(rf'{Fore.RED}\1{Fore.RESET}', msg)
        msg = pattern_now.sub(
            rf'{Fore.YELLOW}\1{Fore.RESET}\2{Fore.GREEN}\3{Fore.RESET}', msg)
        return msg

    @classmethod
    def fetch(cls, show=True):
        """ sort out current branchs """
        prefix = cls._get_color_prefix(color='LIGHTBLUE_EX',
                                       color_prefix=Fore.WHITE,
                                       prefix_msg='fetch')
        try:
            info = subprocess.getoutput('git fetch --prune')
        except Exception:
            print('No Git detect!')
            return

        msg = '--- Update ---' if info else 'Nothing To Update.'
        print(f'{prefix}{msg}')

        if not show and not info:
            return

        if 'deleted' in info:
            info = MkGit._re_words(info=info)
        print(info)

        # display branches
        click.echo('show branchs [y/N]: \n')
        show = click.getchar()
        if show == 'y':
            msg = cls._re_branchs(msg=subprocess.getoutput('git branch -a'))
            print(msg)

    @classmethod
    def _get_color_prefix(cls, color=None, color_prefix=None, prefix_msg=None):
        prefix = prefix_msg or os.path.basename(os.getcwd())
        color_prefix = color_prefix + getattr(Back, color) + Style.BRIGHT
        color = getattr(Fore, color, None)
        return (f'\n{color}'
                f'{color_prefix}{prefix}'
                f'{cls._RESET}'
                f'{color}'
                f'{cls._RESET} ')

    @classmethod
    def _checkout(cls, branch):
        colored_repo = cls._get_color_prefix(color='LIGHTBLACK_EX',
                                             color_prefix=Fore.WHITE)
        info = subprocess.getoutput(f'git checkout {branch}')
        try:
            if 'Already on' in info:
                status = f'Already on {Fore.CYAN}{branch}{cls._RESET}'

            elif 'Switched to' in info:
                status = f'Switched to {Fore.YELLOW}{branch}{cls._RESET}'

            else:
                status = f'Error on {Fore.RED}{branch}{cls._RESET}\n{info}'

        except Exception:
            status = f'Except Error on {Fore.RED}{branch}{cls._RESET}\n{info}'

        print(f'{colored_repo}{status}')

    @classmethod
    def _current_branch(cls):
        colored_repo = cls._get_color_prefix(color='LIGHTBLACK_EX',
                                             color_prefix=Fore.WHITE)
        try:
            output = str(
                subprocess.check_output(['git', 'branch'],
                                        cwd=os.getcwd(),
                                        universal_newlines=True))
            branch = [a for a in output.split('\n') if a.find('*') >= 0][0]
            current_branch = branch[branch.find('*') + 2:]
            status = f'Stay on {Fore.GREEN}{current_branch}{cls._RESET}'

        except Exception:
            status = f'Error on {Fore.RED}info{cls._RESET}\n{output}'

        print(f'{colored_repo}{status}')

    @classmethod
    def swap(cls, branch_name, ignore=list(), level='all'):
        """s branch_name
        swap current branch to target branch
        """
        if level == 'all' or level == '1':
            cls._checkout(branch=branch_name)

        if level == 'all' or level == '2':
            cls._get_submodules()
            if not cls._PATH_SUB:
                return
            for path in cls._PATH_SUB:
                try:
                    os.chdir(path)
                except Exception:
                    continue
                if branch_name in ignore:
                    cls._current_branch()
                cls._checkout(branch=branch_name)

    @classmethod
    def _init(cls):
        if not os.path.exists(cls._PATH_MAIN_CONFIG):
            print('No Git Config Found!')
            return
        cls._get_submodules()
        if not cls._PATH_SUB:
            return

        has_files = None
        for path in cls._PATH_SUB:
            try:
                os.chdir(path)
                has_files = False if not subprocess.getoutput('ls') else True
            except Exception:
                return
        if has_files:
            return

        color_prefix = cls._get_color_prefix(color='MAGENTA',
                                             color_prefix=Fore.WHITE,
                                             prefix_msg='init')
        print(f'{color_prefix}Git Submodeles')
        subprocess.run('git submodule update --init --recursive', shell=True)
        print(f'{color_prefix}Finished.\n')

    @staticmethod
    def _re_pull_words(replacement, info, color):
        pattern = re.compile(rf'([{replacement}]+)([\n-)])')
        return pattern.sub(rf'{color}\1{Fore.RESET}\2', info)

    @classmethod
    def _git_pull(cls):
        info = subprocess.getoutput('git pull')
        info = cls._re_pull_words(replacement='-', info=info, color=Fore.RED)
        info = cls._re_pull_words(replacement='+', info=info, color=Fore.GREEN)
        print(f'{info}\n')

    @classmethod
    def pull(cls):
        """ pull all file from Git repo """
        cls._init()

        os.chdir(cls._PATH_MAIN)
        cls.fetch(show=False)
        cls.swap(branch_name='develop', level='1')
        cls._git_pull()

        if not cls._PATH_SUB:
            return
        for path in cls._PATH_SUB:
            try:
                os.chdir(path)
            except Exception:
                continue
            cls.swap(branch_name='develop', level='1')
            cls._git_pull()
