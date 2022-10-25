from rest_framework import viewsets, mixins


class ListCreateDeleteViewSet(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    """Вьюсет для получение списка, создание и удаление данных."""

    pass


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Вьюсет только для создания объекта."""

    pass
