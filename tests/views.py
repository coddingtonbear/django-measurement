from __future__ import unicode_literals

from dal import autocomplete

from .models import Product


class ProductAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_staff:
            return Product.objects.none()

        qs = Product.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
