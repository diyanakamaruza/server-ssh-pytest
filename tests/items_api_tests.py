import time
import asyncio
from items_api import ItemsApi, environment


TIMESTAMP = int(time.time())
STRESSCOUNT = 100

api = ItemsApi(environment['docker'])


def verify_case(api_method, method_arg=None, expected_status=200, expected_keyword=None):

    if method_arg is None:
        api_response = api_method()
    else:
        api_response = api_method(method_arg)
    
    if expected_keyword is not None:
        assert expected_keyword in str(api_response.json())

    assert api_response.status_code == expected_status

    return True


def test_get_all_items():
    for i in range(5):
        assert verify_case(api.get_items, expected_status=200, expected_keyword=f'item_{i}')


def test_get_existing_item_by_name():
    assert verify_case(api.get_items_by_name, 'item_0', expected_status=200, expected_keyword='item_0')


def test_get_nonexisting_item_by_name():
    assert verify_case(api.get_items_by_name, 'noitem_999', expected_status=404, expected_keyword='not found')


def test_get_existing_item_by_param():
    assert verify_case(api.get_items_by_param, {'name': 'item_0'}, expected_status=200, expected_keyword='item_0')


def test_get_nonexisting_item_by_param():
    assert verify_case(api.get_items_by_param, {'noname': 'item_0'}, expected_status=200, expected_keyword='[]')
    assert verify_case(api.get_items_by_param, {'name': 'noitem_999'}, expected_status=200, expected_keyword='[]')


def test_add_new_item():
    initial_count = api.get_items_count()

    assert verify_case(api.add_item, {'name': f'item_{TIMESTAMP}'}, expected_status=201, expected_keyword=f'item_{TIMESTAMP}')
    assert verify_case(api.get_items_by_name, f'item_{TIMESTAMP}', expected_status=200, expected_keyword=f'item_{TIMESTAMP}')

    assert f'item_{TIMESTAMP}' in str(api.get_items().json())
    assert api.get_items_count() == initial_count + 1


def test_delete_existing_item():
    if api.get_items_by_name(f'item_{TIMESTAMP}').status_code != 200:
        api.add_item({'name': f'item_{TIMESTAMP}'})

    initial_count = api.get_items_count()

    verify_case(api.delete_item, f'item_{TIMESTAMP}', expected_status=204)
    verify_case(api.get_items_by_name, f'item_{TIMESTAMP}', expected_status=404, expected_keyword='not found')
    
    assert f'item_{TIMESTAMP}' not in str(api.get_items().json())
    assert api.get_items_count() == initial_count - 1


def test_delete_nonexisting_item():
    assert verify_case(api.delete_item, 'noitem_999', expected_status=404, expected_keyword='not found')


def test_stress_add_many_new_items_sequentially():
    initial_count = api.get_items_count()

    for i in range(STRESSCOUNT):
        assert api.add_item({'name': f'item_{TIMESTAMP}-s1-{i}'}).status_code == 201
        assert api.get_items_by_name(f'item_{TIMESTAMP}-s1-{i}').status_code == 200

    assert api.get_items_count() == initial_count + STRESSCOUNT


def test_stress_add_many_new_items_concurrently():
    initial_count = api.get_items_count()

    async def concurrent_tasks():

        def add_item(i):
            assert api.add_item({'name': f'item_{TIMESTAMP}-s2-{i}'}).status_code == 201
            assert api.get_items_by_name(f'item_{TIMESTAMP}-s2-{i}').status_code == 200
        
        reqs = []
        for i in range(STRESSCOUNT):
            reqs.append(asyncio.to_thread(add_item, i))
        await asyncio.gather(*reqs)

    async def verify():
        await concurrent_tasks()

    asyncio.run(verify())

    assert api.get_items_count() == initial_count + STRESSCOUNT


if __name__ == "__main__":
    import pytest
    pytest.main(["-sv", "--html=pytest-report.html", __file__])


"""
----------------------------------------------------------------------------------------------------
[GET]    /items/(?param=value)
Description
    List all items when no param given.
    Filter by param=value, for example /items/?tag=test
Response
    200    [{'name': 'item_1', ...}, ...]
----------------------------------------------------------------------------------------------------
[GET]    /items/<name>/
Description
    Get an item by name.
Response
    200    {'name': 'item_1', 'serial': '12345', ...}
    404    {'error': 'message'}
----------------------------------------------------------------------------------------------------
[POST]   /items/
Description
    Add new item.
Input
    {'name': 'item_name', 'email': 'test@ssh.com', ...}
Response
    201    {'name': 'item_name', ...}
    400    {'error': 'message'}
----------------------------------------------------------------------------------------------------
[DELETE] /items/<name>/
Description
    Delete an item by name.
Response
    204
    404    {'error': 'message'}
----------------------------------------------------------------------------------------------------
"""