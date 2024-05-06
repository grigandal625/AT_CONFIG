import pathlib
import pkg_resources
import re


def new_requirement(req: str):
    if re.match(r'^(\w|-)*(\s|)@.+$', req):
        rest = req.split('@')[1:]
        pkg = re.sub(r'\s', '', req.split('@')[0])
        module = __import__(pkg.replace('-', '_'))
        new_pkg = f'{pkg}=={module.__version__}'
        new_req = '@'.join([new_pkg] + rest)
        return new_req
    return req
        

def fix_requirements():
    with pathlib.Path('requirements.txt').open() as requirements_txt:
        all_reqs = [
            str(requirement)
            for requirement
            in pkg_resources.parse_requirements(requirements_txt)
        ]
        new_reqs = [new_requirement(r) for r in all_reqs]
        requirements_txt.close()

    with pathlib.Path('requirements.txt').open(mode='w') as requirements_txt:
        requirements_txt.write('\n'.join(new_reqs))
        requirements_txt.close()


if __name__ == '__main__':
    fix_requirements()