import nox


@nox.session(python=["3.10", "3.11"])  # type: ignore
def tests(session):
    session.install("-r", "requirements.txt")
    session.install("pytest", "coverage")
    session.run("coverage", "run", "-m", "pytest")
    session.run("coverage", "xml")
