from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PaginationHandlerMixin(object):
    @property
    def paginator(self):
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_size_query_param = "limit"
    results_attr = "results"
    allow_inf = False

    def get_paginated_response(self, data):
        return Response({
            self.results_attr: data,
            "links": {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            },
            "count": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
        })

    def paginate_queryset(self, queryset, request, view=None):
        page_size = request.query_params.get(self.page_size_query_param, self.get_page_size(request))
        if page_size is None:
            return None

        if isinstance(page_size, str) and not page_size.isnumeric():
            if page_size != "inf":
                raise ValueError(f"Invalid {self.page_size_query_param} value")
            if not self.allow_inf:
                raise ValueError(f"Does not allow inf as {self.page_size_query_param} value")

        paginator = self.django_paginator_class(queryset, page_size if page_size != "inf" else len(queryset))

        page_number = 1
        if page_size != "inf":
            page_number = request.query_params.get(self.page_query_param, 1)

        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except Exception as exc:
            # Here it is
            raise exc

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    @classmethod
    def configure(cls, allow_limit_inf=False):
        class ConfiguredCustomPagination(cls):
            allow_inf = allow_limit_inf

        return ConfiguredCustomPagination
