import nox

nox.options.sessions = ["format"]


@nox.session(
    # python=["3.10", "3.13", "pypy-7.3"],
    reuse_venv=True,
    venv_backend="uv|virtualenv",
)
def format(session: nox.Session) -> None:
    session.install("-U", "black")
    session.run("black", ".")


@nox.session
@nox.parametrize("version", ["5.3.0", "5.2.1", "5.1.1"])
def dont_run(session: nox.Session, version: str) -> None:
    session.install(f"analytix=={version}")
    session.run("python", "-m", "analytix")
