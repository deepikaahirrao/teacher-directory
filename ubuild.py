import os
from uranium import task_requires, current_build


current_build.config.set_defaults({
    "package_name": "teacher-directory",
    "module": "teacher_directory"
})


def main(build):
    build.packages.install(".", develop=True)

@task_requires("main")
def test(build):
    """ execute tests """
    build.packages.install("pytest")
    build.packages.install("pytest-cov")
    build.packages.install("httpretty", version="==0.8.10")
    basedir = os.path.abspath(os.path.dirname('__file__'))
    build.executables.run([
        "./bin/py.test", "{}/teacher_directory/tests".format(basedir),
        "--cov-report", "term-missing", "--cov=teacher_directory",
        "--cov-config=.coveragerc", "-W", "ignore::DeprecationWarning"
    ])


@task_requires("main")
def publish(build):
    """ construct a distribution of the package """
    build.packages.install("wheel")
    build.executables.run([
        "python", "setup.py", "sdist", "bdist_wheel"
    ])


'''
@task_requires("main")
def build_docs(build):
    build.packages.install("sphinx")
    build.executables.run(["bin/sphinx-apidoc", "--extensions", "ext-autodoc",
                           "-o", "./source", "./data_collector", "./teacher_directory/db/*",
                           "./data_collector/tests/*", "./teacher_directory/app.py", 
                           "./teacher_directory/config.py"])
    build.executables.run([
            "bin/sphinx-build", "./source", "./docs"
        ])
'''