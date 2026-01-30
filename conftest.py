pytest_plugins = ["fixtures.driver", "fixtures.session"]

import pytest
from utils.artifacts import save_artifacts

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.failed and rep.when in ("setup", "call") and "driver" in item.fixturenames:
        drv = item.funcargs.get("driver")
        if drv:
            save_artifacts(drv, f"{item.name}_{rep.when}")
