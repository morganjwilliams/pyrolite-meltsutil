def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    from pyrolite_meltsutil.download import install_melts
    from pyrolite_meltsutil.util.general import pyrolite_meltsutil_datafolder

    if not pyrolite_meltsutil_datafolder(subfolder="localinstall").exists():
        install_melts(local=True)  # install melts for example files etc
