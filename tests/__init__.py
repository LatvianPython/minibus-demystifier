patches = []


def setup_package():
    from unittest import mock
    from pathlib import Path
    from io import StringIO

    default_path = Path.cwd() / 'tests' / 'test_data'

    def mock_get(file_name):
        with open(default_path / file_name, mode='r', encoding='utf-8') as file:
            content = file.read()

        def get_handle():
            return StringIO(content)

        return get_handle

    routes_patch = mock.patch('minibus_routes.get_routes', mock_get('routes.txt'))
    stops_patch = mock.patch('minibus_stops.get_stops', mock_get('stops.txt'))

    patches.extend([routes_patch, stops_patch])

    for patch in patches:
        patch.start()


def teardown_package():
    for patch in patches:
        patch.stop()
