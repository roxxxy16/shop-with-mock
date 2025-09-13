Схема управления доступом (Access Control)

1. Основные сущности

| Сущность            | Описание                                                                      |
|---------------------|-------------------------------------------------------------------------------|
| **Role**            | Роль пользователя, определяет уровень доступа (guest, user, moderator, admin) |
| **Module**          | Модуль приложения, к которому применяются права (например: Catalog, Cart)     |
| **RolePermissions** | Набор разрешений роли для конкретного модуля                                  |
| **Users**           | Пользователи системы, каждый может иметь одну роль                            |

2. Роли и права доступа

| Роль          | Модуль    | Read  | Create | Update | Delete |
|---------------|-----------|-------|--------|--------|--------|
| **guest**     | Catalog   | ✔    | ❌     | ❌     | ❌    |
| **guest**     | Cart      | ❌   | ❌     | ❌     | ❌    |
| **user**      | Catalog   | ✔    | ❌     | ❌     | ❌    |
| **user**      | Cart      | ✔    | ✔      | ✔      | ✔     |
| **moderator** | Catalog   | ✔    | ❌     | ✔      | ❌    |
| **moderator** | Cart      | ✔    | ✔      | ✔      | ✔     |
| **admin**     | Catalog   | ✔    | ✔      | ✔      | ✔     |
| **admin**     | Cart      | ✔    | ✔      | ✔      | ✔     |

✔ — разрешено, ❌ — запрещено

3. Механизм проверки доступа

1. В каждом APIView указывается атрибут `module`, например:

class CatalogView(APIView):
    permission_classes = [HasModulePermission]
    module = "Catalog"

Класс HasModulePermission проверяет права пользователя: Если пользователь анонимный, ему присваивается роль guest. Получается RolePermissions для роли и модуля. В зависимости от HTTP-метода (GET, POST, PATCH, DELETE) проверяется соответствующее разрешение (read_permission, create_permission, update_permission, delete_permission). Если разрешение отсутствует → возвращается HTTP 403.

4. Структура базы данных
Role
 - id
 - name
 - description

Module
 - id
 - name
 - description

RolePermissions
 - id
 - role_id (FK -> Role)
 - module_id (FK -> Module)
 - read_permission
 - create_permission
 - update_permission
 - delete_permission

Users
 - id
 - email
 - password
 - role_id (FK -> Role)
 - -другие поля пользователя

5. Пример работы
Пользователь с ролью user делает POST /api/v1/catalog/ → 403 Forbidden (нет разрешения на создание товара). Пользователь с ролью admin делает POST /api/v1/catalog/ → 201 Created (товар создан). Анонимный пользователь делает GET /api/v1/catalog/ → 200 OK (только чтение).