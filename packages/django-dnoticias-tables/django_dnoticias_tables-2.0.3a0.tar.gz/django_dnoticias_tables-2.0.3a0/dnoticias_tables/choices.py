from django.db import models


class FilterType:
    CONTAINS = "contains"
    ICONTAINS = "icontains"
    EXACT = "exact"
    IEXACT = "iexact"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    ISNULL = "isnull"
    STARTSWITH = "startswith"
    ISTARTSWITH = "istartswith"
    ENDSWITH = "endswith"
    IENDSWITH = "iendswith"
    YEAR = "year"
    MONTH = "month"
    DAY = "day"
    WEEK_DAY = "week_day"
    TIME = "time"
    DATE = "date"
    BLANK = "blank"



class YesNoChoices(models.IntegerChoices):
    NO = 0, "Não"
    YES = 1, "Sim"


class ActiveChoices(models.IntegerChoices):
    INACTIVE = 0, "Inativo"
    ACTIVE = 1, "Ativo"
