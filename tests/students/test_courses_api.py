import pytest

from rest_framework.test import APIClient
from students.models import Course, Student

from model_bakery import baker

base_url = '/api/v1/courses/'

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

# Проверка получения 1го курса (retrieve-логика) (по 1му курсу)
@pytest.mark.django_db
def test_retrieve(client, course_factory, quantity = 1):
    # Arrange
    courses = course_factory(_quantity = quantity)
    # Act
    list_of_responses = []
    for course in courses:
        response = client.get(base_url + str(course.id) + '/')
        list_of_responses.append(response)
    # Assert
    for index, response in enumerate(list_of_responses):
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == courses[index].name

# Проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_list(client, course_factory, quantity = 10):
    # Arrange
    courses = course_factory(_quantity = quantity)
    # Act
    response = client.get(base_url)
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert len(data) == len(courses)
    for index, course in enumerate(data):
        course['name'] == courses[index].name

# Проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_filter_id(client, course_factory, quantity = 10):
    # Arrange
    courses = course_factory(_quantity = quantity)
    # Act
    list_of_responses = []
    for course in courses:
        response = client.get(base_url + '?id=' + str(course.id))
        list_of_responses.append(response)
    # Assert
    for index, response in enumerate(list_of_responses):
        assert response.status_code == 200
        data = response.json()
        assert data[0]['name'] == courses[index].name

# Проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filter_name(client, course_factory, quantity = 10):
    # Arrange
    courses = course_factory(_quantity = quantity)
    # Act
    list_of_responses = []
    for course in courses:
        response = client.get(base_url + '?name=' + str(course.name))
        list_of_responses.append(response)
    # Assert
    for index, response in enumerate(list_of_responses):
        assert response.status_code == 200
        data = response.json()
        assert data[0]['name'] == courses[index].name

# Тест успешного создания курса
@pytest.mark.django_db
def test_post(client):
    # Arrange
    payload = {
        'name': 'course1',
        'student': 1
    }
    # Act
    response = client.post(base_url, data = payload)
    # Assert
    assert response.status_code == 201
    assert response.data['name'] == payload['name']

# Тест успешного обновления курса(курсов)
@pytest.mark.django_db
def test_patch(client, course_factory, quantity = 10):
    # Arrange
    courses = course_factory(_quantity = quantity)
    # Act
    list_of_responses = []
    for course in courses:
        payload = {
            'name': 'alter course'
        }
        response = client.patch(base_url + str(course.id) + '/', data = payload)
        list_of_responses.append(response)
    # Assert
    for index, response in enumerate(list_of_responses):
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == payload['name']

# Тест успешного удаления курса(курсов)
@pytest.mark.django_db
def test_del(client, course_factory, quantity = 10):
    # Arrange
    courses = course_factory(_quantity = quantity)
    # Act
    list_of_responses = []
    for course in courses:
        response = client.delete(base_url + str(course.id) + '/')
        # Assert
        assert response.status_code == 204