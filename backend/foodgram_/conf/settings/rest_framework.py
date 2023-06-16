from conf.settings.django import env

REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_AUTHENTICATION_CLASSES": ["api.authentication.UserApiTokenAuthentication"],
    # "EXCEPTION_HANDLER": "utils.exception_handler.custom_exception_handler",
    "PAGE_SIZE": env("PAGE_SIZE", default=10, cast=int),
}
