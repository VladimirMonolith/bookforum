from typing import Optional

from fastapi import HTTPException, status


class MarketplaceException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ''

    def __init__(self, detail: Optional[str] = None):
        super().__init__(
            status_code=self.status_code, detail=detail or self.detail
        )


class ObjectAlreadyExistsException(MarketplaceException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Объект с указанными данными уже существует.'


class DatabaseErrorException(MarketplaceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = 'Произошла ошибка при работе с базой данных.'


class CannotProcessCSVException(MarketplaceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = 'Не удалось обработать CSV файл.'


class NotFoundException(MarketplaceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Данные не найдены.'

# Более специализированные классы для 500 ошибки,
#  заменены универсальным DatabaseErrorException

# class CannotAddDataToDatabase(MarketplaceException):
#     status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#     detail = ('Не удалось добавить тестовые данные в базу данных.'
#               'Проверьте корректность данных.')


# class CannotCreateData(MarketplaceException):
#     status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#     detail = 'Не удалось добавить запись в базу данных.'


# class CannotUpdateData(MarketplaceException):
#     status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#     detail = 'Не удалось обновить данные.'


# class CannotDeleteDataFromDatabase(MarketplaceException):
#     status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#     detail = 'Не удалось удалить запись из базы данных.'
