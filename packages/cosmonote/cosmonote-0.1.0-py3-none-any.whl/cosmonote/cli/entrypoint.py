from .main import main


def entrypoint():
    main(auto_envvar_prefix="HIMITSU")
