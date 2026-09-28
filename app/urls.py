from rest_framework.routers import DefaultRouter

from app.views import *

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('suppliers', SuppliersViewSet)
router.register('shifts', ShiftsViewSet)
router.register('positions', PositionsViewSet)
router.register('cities', CitiesViewSet)
router.register('payment_types', PaymentTypesViewSet)
router.register('genres', GenresViewSet)
router.register('books', BooksViewSet)
router.register('authors', AuthorsViewSet)
router.register('products', ProductsViewSet)
router.register('libraries', LibrariesViewSet)
router.register('library_books', LibraryBookViewSet)
router.register('payments', PaymentsViewSet)
router.register('chill_zones', ChillZonesViewSet)
router.register('category_chill_zones', CategoryChillZonesViewSet)
router.register('booking',ChillZoneBookingsViewSet)
router.register('orders',OrdersViewSet)
router.register('borrow_a_book',BorrowABooksViewSet)
router.register('borrow_one_book',BorrowABookViewSet)
router.register('receipts',ReceiptsViewSet)
router.register('receipt_products',ReceiptProductsViewSet)

urlpatterns = router.urls