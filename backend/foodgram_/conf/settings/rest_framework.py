from conf.settings.django import env

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PERMISSION_CLASSES": (
        "api.permissions.BlockPermission",),
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.LimitOffsetPagination",),
    "PAGE_SIZE": env("PAGE_SIZE", default=10, cast=int),
}
