"""
PAGINADORES PARA LISTADOS DE CATÁLOGO
"""

from rest_framework.pagination import PageNumberPagination


#* PAGINADOR PARA ADMIN
#28/06/25

class AdminPagination(PageNumberPagination):
    page_size = 10 #valor por defecto
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'
    allowed_page_sizes = [5, 10, 20, 30, 50, 100] #valores permitidos para la paginación

    #método para definir el tamaño de la paginación
    #28/06/25
    def get_page_size(self, request):
        try:
            page_size = int(request.query_params.get(self.page_size_query_param, self.page_size))
            if page_size in self.allowed_page_sizes:
                return page_size
        except (TypeError, ValueError):
            pass
        return self.page_size