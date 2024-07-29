from database.orm import Todo


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_todos(client, mocker):
    mocker.patch("api.todo.get_todos", return_value=[
        Todo(id=1, contents="Fast API 0 section", is_done=True),
        Todo(id=2, contents="Fast API 1 section", is_done=False),
    ])

    asc_response = client.get("/todos")
    assert asc_response.status_code == 200

    desc_response = client.get("/todos?order=DESC")
    assert desc_response.status_code == 200
    assert asc_response.json()['todos'] == desc_response.json()['todos'][::-1]


def test_get_todo(client, mocker):
    # 200
    mocker.patch("api.todo.get_todo_by_todo_id",
                 return_value=Todo(id=1, contents="Fast API 0 section", is_done=True))

    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "Fast API 0 section", "is_done": True}

    # 404
    mocker.patch("api.todo.get_todo_by_todo_id", return_value=None)
    response = client.get("/todos/1")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_create_todo(client, mocker):
    create_spy = mocker.spy(Todo, "create")
    mocker.patch("api.todo.create_todo",
                 return_value=Todo(id=1, contents="Fast API 0 section", is_done=True))

    body = {
        "contents": "Fast API 0 section",
        "is_done": False
    }

    response = client.post("/todos", json=body)

    assert create_spy.spy_return.contents == body['contents']
    assert create_spy.spy_return.is_done == body['is_done']
    assert response.status_code == 201
    assert response.json() == {"id": 1, "contents": "Fast API 0 section", "is_done": True}

def test_update_todo(client, mocker):
    # 200
    mocker.patch("api.todo.get_todo_by_todo_id",
                 return_value=Todo(id=1, contents="Fast API 0 section", is_done=True))

    undone = mocker.patch.object(Todo, "undone")

    mocker.patch("api.todo.update_todo",
                 return_value=Todo(id=1, contents="Fast API 0 section", is_done=False))

    response = client.patch("/todos/1", json={"is_done": False})

    undone.assert_called_once_with()
    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "Fast API 0 section", "is_done": False}

    # 404
    mocker.patch("api.todo.get_todo_by_todo_id", return_value=None)
    response = client.patch("/todos/1", json={"is_done": True})

    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

def test_delete_todo(client, mocker):
    # 204
    mocker.patch("api.todo.get_todo_by_todo_id",
                 return_value=Todo(id=1, contents="Fast API 0 section", is_done=True))
    mocker.patch("api.todo.delete_todo", return_value=None)

    response = client.delete("/todos/1")
    assert response.status_code == 204

    # 404
    mocker.patch("api.todo.get_todo_by_todo_id", return_value=None)
    response = client.delete("/todos/1")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}
