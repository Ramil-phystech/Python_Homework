import dataclasses
from dataclasses import dataclass, asdict, astuple
from string import ascii_letters, ascii_uppercase, ascii_lowercase
from uuid import (
    UUID,
    uuid4,
)

symbols = [str(x) for x in range(0, 10)] + list(ascii_letters)


@dataclass
class Person:
    """
    Информация о пользователе.

    Attrs:
        login: логин пользователя.
        password: пароль пользователя.
        username: имя пользователя.
        metadata: дополнительные сведения о пользователе.
    """

    login: str
    password: str
    username: str
    metadata: str = ""


class PersonDB:
    _database: dict[UUID, Person]
    _login_registry: set[str]
    _min_length_password = 10
    _min_length_login = 1

    def __init__(self) -> None:
        self._database = dict()
        self._login_registry = set()

    def create_person(self, person: Person) -> UUID:
        """
        Создает новую запись о пользователе в базе данных.

        Args:
            person: данные о пользователе, которые будут помещены в БД.

        Returns:
            UUID - идентификатор, который будет связан с созданной записью.

        Raises:
            ValueError, если логин или пароль не удовлетворяют требованиям.
        """
        if self._check_login(person.login) and self._check_password(person.password):
            uuid = uuid4()
            self._database[uuid] = person
            self._login_registry.add(person.login)

            return uuid

        raise ValueError

    def read_person_info(self, person_id: UUID) -> Person:
        """
        Читает актуальные данные пользователя из базы данных.

        Args:
            person_id: идентификатор пользователя в формате UUID.

        Returns:
            Данные о пользователе, упакованные в структуру Person.

        Raises:
            KeyError, если в базе данных нет пользователя с person_id.
        """
        if person_id in self._database:
            return self._database[person_id]

        raise KeyError

    def update_person_info(self, person_id: UUID, person_info_new: Person) -> None:
        """
        Обновляет данные о пользователе.

        Args:
            person_id: идентификатор пользователя в формате UUID.
            person_info_new: модель со значениями на обновление. Будут обновлены
                только те поля, чье значение отличается от пустой строки '',
                остальные поля будут оставлены без изменений.

        Raises:
            ValueError, если при обновлении логина или пароля логин или пароль
                не прошли этап валидации.
            KeyError, если в базе данных нет пользователя с person_id.
        """
        if person_id in self._database:
            login, password, username, metadata = dataclasses.astuple(person_info_new)
            old_login = self._database[person_id].login

            if password == "":
                password = self._database[person_id].password
            if metadata == "":
                metadata = self._database[person_id].metadata
            if login == "":
                login = old_login
            if username == "":
                username = self._database[person_id].username
            if ((login != old_login and self._check_login(login)) or login == old_login) and self._check_password(
                    password):
                if login != old_login:
                    self._login_registry.remove(old_login)

                self._database[person_id] = Person(password=password,
                                                   login=login,
                                                   username=username,
                                                   metadata=metadata
                                                   )
                self._login_registry.add(login)
            else:

                raise ValueError
        else:
            raise KeyError

    def delete_person(self, person_id: UUID) -> None:
        """
        Удаляет запись о пользователе.

        Args:
            person_id: идентификатор пользователя в формате UUID.

        Raises:
            KeyError, если в базе данных нет пользователя с person_id.
        """
        if person_id in self._database:
            self._login_registry.remove(self._database[person_id].login)
            del self._database[person_id]
        else:
            raise KeyError

    def _check_login(self, login: str) -> bool:
        """
        Проверяет, существует ли в базе данных данный login и является ли login корректным.

        Args:
            login: логин пользователя

        Returns:
            True, если login присутствует в базе данных логинов.
            False, если login отсутсвтует в базе данных логинов или не является корректным.
        """
        if login not in self._login_registry and all(x in symbols for x in login) and len(
                login) >= self._min_length_login:
            return True

        return False

    def _check_password(self, password: str) -> bool:
        """
        Проверяет, является ли password пользователя корректным.
        Пароль корректен, если:
            (conditions[0]) пароль содержит хотя бы одну цифру от 0 до 9
            (conditions[1]) пароль содержит хотя бы одну букву английского алфавита в нижнем регистре
            (conditions[2]) пароль содержит хотя бы одну букву английского алфавита в верхнем регистре
            (conditions[3]) пароль не содержит никаких символов, кроме разрешенных(ascii_letters and digits)
                            пароль состоит не менее чем из 10 символов

        Args:
            password: пароль пользователя

        Returns:
            True, если пароль является корректным.
            False, если пароль не является корректным.
        """
        conditions = [False] * 4
        conditions[3] = True
        if len(password) >= self._min_length_password:
            for x in password:
                if x.isdigit():
                    conditions[0] = True
                elif x.islower():
                    conditions[1] = True
                elif x.isupper():
                    conditions[2] = True
                conditions[3] *= x.isascii()
        else:
            return False

        return all(conditions) and password.isalnum()
