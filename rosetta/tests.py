import pytest

from rosetta import ServerManager

@pytest.fixture(scope="module")
def create_server_manager():
    test_server_manager = ServerManager()

    test_server_manager.env.load_config_file('$APP_DIR/data/test_config.yml')
    test_server_manager.create_all()

    return test_server_manager


def test_server_manager():
    server_manager = create_server_manager()
    assert(server_manager.app is not None)
