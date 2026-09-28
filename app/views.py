from django.db import transaction
from django.db.models import Count, Q, F
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from app.models import Categories, Suppliers, Shifts, Positions, Cities, PaymentTypes, Genres, Books, Authors, Products, \
    Libraries, Payments, ChillZones, Orders, BorrowABooks, BorrowABook, Receipts, ReceiptProducts, ChillZoneBookings, \
    CategoryChillZones, LibraryBook
from app.pagination import Pagination
from app.permission import IsSameBranchOrSuperuser, IsSuperUserOrReadOnly, CanIssueBooks
from app.serializer.authors import AuthorsSerializer
from app.serializer.books import BooksWriteSerializer, BooksSerializer
from app.serializer.borrow_books import BorrowABooksWriteSerializer, BorrowABookClientSerializer, \
    BorrowABookStaffSerializer, BorrowABookSerializer
from app.serializer.category import CategorySerializer
from app.serializer.chill_zone import ChillZoneBookingWriteSerializer, \
    ChillZoneBookingSerializer, CategoryChillZonesSerializer, CategoryChillZonesWriteSerializer, \
    ChillZonesSerializer, ChillZonesWriteSerializer
from app.serializer.cities import CitiesSerializer
from app.serializer.genres import GenresSerializer
from app.serializer.libraries import LibrariesSerializer, LibraryBookCreateSerializer, LibraryBookSerializer, \
    StockAdjustSerializer
from app.serializer.order import OrdersWriteSerializer, OrdersSerializer
from app.serializer.payment import PaymentsSerializer
from app.serializer.payment_types import PaymentTypesSerializer
from app.serializer.positions import PositionSerializer
from app.serializer.products import ProductsSerializer
from app.serializer.receipt import ReceiptsSerializer, ReceiptProductsSerializer
from app.serializer.shifts import ShiftSerializer
from app.serializer.suppliers import SuppliersSerializer
from app.uttils import filter_by_branch


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Categories.objects.all().order_by('id')
    serializer_class = CategorySerializer
    pagination_class = Pagination


class SuppliersViewSet(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Suppliers.objects.all().order_by('id')
    serializer_class = SuppliersSerializer
    pagination_class = Pagination

    def get_queryset(self):
        qs = Suppliers.objects.all().order_by('id')
        search = self.request.query_params.get('search')
        if search:
            from django.db.models import Q
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(phone_number__icontains=search) |
                Q(email__icontains=search) |
                Q(about__icontains=search)
            )
        return qs


class ShiftsViewSet(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Shifts.objects.all().order_by('id')
    serializer_class = ShiftSerializer
    pagination_class = Pagination

class PositionsViewSet(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Positions.objects.all().order_by('id')
    serializer_class = PositionSerializer
    pagination_class = Pagination

class CitiesViewSet(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Cities.objects.all().order_by('id')
    serializer_class = CitiesSerializer
    pagination_class = Pagination

class PaymentTypesViewSet(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = PaymentTypes.objects.all().order_by('id')
    serializer_class = PaymentTypesSerializer
    pagination_class = Pagination

class GenresViewSet(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Genres.objects.all().order_by('id')
    serializer_class = GenresSerializer
    pagination_class = Pagination

class BooksViewSet(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Books.objects.all()
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return BooksWriteSerializer
        return BooksSerializer

    def get_queryset(self):
        qs = Books.objects.prefetch_related('author', 'genre').annotate(
            total_borrows=Count('borrow_book', distinct=True),
            currently_borrowed=Count(
                'borrow_book', filter=Q(borrow_book__returned_at__isnull=True), distinct=True))
        search = self.request.query_params.get('search')
        genre = self.request.query_params.get('genre')
        author = self.request.query_params.get('author')
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(author__name__icontains=search))
        if genre:
            qs = qs.filter(genre__name__icontains=genre)
        if author:
            qs = qs.filter(author__name__icontains=author)
        return qs.distinct().order_by('-total_borrows', 'id')

class AuthorsViewSet(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Authors.objects.all()
    serializer_class = AuthorsSerializer
    pagination_class = Pagination
    def get_queryset(self):
        qs = Authors.objects.annotate(
            total_borrows=Count('books__borrow_book', distinct=True),
            currently_borrowed=Count(
                'books__borrow_book',
                filter=Q(books__borrow_book__returned_at__isnull=True),
                distinct=True))
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(name__icontains=search)
        return qs.distinct().order_by('-total_borrows', 'id')

class ProductsViewSet(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Products.objects.all().order_by('id')
    serializer_class = ProductsSerializer
    pagination_class = Pagination
    def get_queryset(self):
        qs = Products.objects.prefetch_related('category', 'supplier').order_by('id')
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(category__name__icontains=search) |
                Q(supplier__name__icontains=search)
            ).distinct()
        return qs

class LibrariesViewSet(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Libraries.objects.select_related('city').prefetch_related('shift', 'payment_type', 'book').order_by('id')
    serializer_class = LibrariesSerializer
    pagination_class = Pagination
class PaymentsViewSet(ModelViewSet):
    queryset = Payments.objects.select_related('payment_type').order_by('id')
    serializer_class = PaymentsSerializer
    pagination_class = Pagination
    permission_classes = [IsAdminUser]

class ChillZonesViewSet(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = ChillZones.objects.all()
    serializer_class = ChillZonesSerializer
    library_field = 'library'
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return ChillZonesWriteSerializer
        return ChillZonesSerializer

    def get_queryset(self):
        base_qs = ChillZones.objects.select_related('library__city').prefetch_related(
            'category_chill_zones__category', 'library__shift', 'library__payment_type', 'library__book'
        ).annotate(orders_count=Count('orders', distinct=True)).order_by('id')
        return base_qs

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_superuser:
            serializer.save()
        else:
            serializer.save(library=user.employee_profile.library)

class CategoryChillZonesViewSet(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = CategoryChillZones.objects.all()
    library_field = 'chill_zone__library'
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return CategoryChillZonesWriteSerializer
        return CategoryChillZonesSerializer

    def get_queryset(self):
        qs = CategoryChillZones.objects.select_related(
            'category', 'chill_zone__library'
        ).order_by('id')
        return filter_by_branch(qs, self.request.user, library_field=self.library_field)

    def perform_create(self, serializer):
        user = self.request.user
        chill_zone = serializer.validated_data['chill_zone']

        if not user.is_superuser:
            employee = getattr(user, 'employee_profile', None)
            if not employee or not employee.library or chill_zone.library != employee.library:
                raise PermissionDenied('Нельзя добавлять категорию в чужой филиал.o(≧口≦)o')

        serializer.save()


class ChillZoneBookingsViewSet(ModelViewSet):
    queryset = ChillZoneBookings.objects.all()
    pagination_class = Pagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = ChillZoneBookings.objects.select_related('client', 'chill_zone__library').order_by('-id')
        user = self.request.user
        if user.is_superuser:
            return qs
        if not user.is_staff:
            return qs.filter(client=user)
        employee = getattr(user, 'employee_profile', None)
        if not employee or not employee.library:
            return qs.none()
        return qs.filter(chill_zone__library=employee.library)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ChillZoneBookingWriteSerializer
        return ChillZoneBookingSerializer

    def perform_create(self, serializer):
        chill_zone = serializer.validated_data['chill_zone']
        seats = serializer.validated_data['seats']
        with transaction.atomic():
            locked_zone = ChillZones.objects.select_for_update().get(pk=chill_zone.pk)
            if seats > locked_zone.free_seats:
                raise serializers.ValidationError({'seats': 'Not enough available spaces.༼ つ ◕_◕ ༽つ'})
            serializer.save(client=self.request.user)
            ChillZones.objects.filter(pk=locked_zone.pk).update(free_seats=F('free_seats') - seats)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if not booking.is_active:
            return Response({'detail': 'The reservation has already been cancelled.. (┬┬﹏┬┬)'}, status=status.HTTP_400_BAD_REQUEST)
        if booking.client != request.user and not request.user.is_superuser:
            return Response({'detail': 'Access denied.'}, status=status.HTTP_403_FORBIDDEN)
        with transaction.atomic():
            booking.is_active = False
            booking.save(update_fields=['is_active'])
            ChillZones.objects.filter(pk=booking.chill_zone_id).update(
                free_seats=F('free_seats') + booking.seats
            )
        return Response({'status': 'cancelled'})

class OrdersViewSet(ModelViewSet):
    queryset = Orders.objects.all()
    library_field = 'chill_zone__library'
    pagination_class = Pagination

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return [IsAdminUser(), IsSameBranchOrSuperuser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return OrdersWriteSerializer
        return OrdersSerializer

    def get_queryset(self):
        base_qs = Orders.objects.select_related(
            'client', 'employee__user', 'payment__payment_type', 'chill_zone__library').order_by('-id')
        user = self.request.user
        if not user.is_authenticated:
            return base_qs.none()
        if not user.is_staff:
            return base_qs.filter(client=user)
        return base_qs

    def perform_create(self, serializer):
        user = self.request.user
        chill_zone = serializer.validated_data['chill_zone']
        employee = getattr(user, 'employee_profile', None)

        if user.is_superuser:
            serializer.save()
            return

        if employee is not None:
            serializer.save(employee=employee)
            return

        if serializer.validated_data.get('client') != user:
            raise PermissionDenied('Читатель может оформить заказ только на своё имя. o(≧口≦)o')
        serializer.save(employee=None, client=user)

class BorrowABooksViewSet(ModelViewSet):
    queryset = BorrowABooks.objects.all()
    library_field = 'library'
    pagination_class = Pagination

    def get_permissions(self):
        if self.request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            return [IsAuthenticated(), IsSameBranchOrSuperuser(), CanIssueBooks()]
        return [IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        qs = BorrowABooks.objects.select_related(
            'library', 'employee__user', 'client_card', 'payment__payment_type'
        ).order_by('-id')
        user = self.request.user
        if not user.is_authenticated:
            return qs.none()
        if not user.is_staff:
            return qs.filter(client_card=user)
        return filter_by_branch(qs, user, library_field=self.library_field)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return BorrowABooksWriteSerializer
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return BorrowABookStaffSerializer
        return BorrowABookClientSerializer

    def perform_create(self, serializer):
        user = self.request.user
        library = serializer.validated_data['library']
        employee = getattr(user, 'employee_profile', None)

        if employee is not None:
            if employee.library and library != employee.library:
                raise PermissionDenied('Нельзя оформлять выдачу в чужом филиале.o(≧口≦)o')
            serializer.save(employee=employee, client_card=serializer.validated_data.get('client_card') or user)
            return

        if serializer.validated_data.get('client_card') not in (None, user):
            raise PermissionDenied('Читатель может оформить выдачу только на своё имя.（︶^︶）')
        serializer.save(employee=None, client_card=user)

    @action(detail=True, methods=['post'], url_path='return-book/(?P<book_id>[^/.]+)')
    def return_book(self, request, pk=None, book_id=None):
        borrow_batch = self.get_object()
        if borrow_batch.transaction_type == 'purchase':
            return Response({'detail': 'Purchased books are non-returnable.. （︶^︶）'}, status=status.HTTP_400_BAD_REQUEST)

        borrow_item = get_object_or_404(borrow_batch.borrow_book, book_id=book_id)
        if borrow_item.is_returned:
            return Response({'detail': 'This book has already been returned. （⊙ｏ⊙）'}, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            borrow_item.returned_at = timezone.now().date()
            borrow_item.save(update_fields=['returned_at'])
            LibraryBook.objects.filter(library=borrow_batch.library, book_id=book_id).update(
                quantity=F('quantity') + 1)
        return Response({'status': 'returned', 'returned_at': borrow_item.returned_at})

class BorrowABookViewSet(ReadOnlyModelViewSet):
    queryset = BorrowABook.objects.select_related(
        'borrow_at__library', 'borrow_at__client_card', 'book'
    ).order_by('id')
    serializer_class = BorrowABookSerializer
    pagination_class = Pagination
    permission_classes = [IsAdminUser]

class ReceiptsViewSet(ReadOnlyModelViewSet):
    queryset = Receipts.objects.all()
    library_field = 'order__chill_zone__library'
    serializer_class = ReceiptsSerializer
    pagination_class = Pagination
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        qs = Receipts.objects.select_related(
            'order__client', 'order__employee__user',
            'order__chill_zone__library', 'order__payment__payment_type'
        ).order_by('-id')
        user = self.request.user
        if not user.is_staff:
            return qs.filter(order__client=user)
        return qs

class ReceiptProductsViewSet(ReadOnlyModelViewSet):
    queryset = ReceiptProducts.objects.all()
    library_field = 'receipt__order__chill_zone__library'
    serializer_class = ReceiptProductsSerializer
    pagination_class = Pagination
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        qs = ReceiptProducts.objects.select_related(
            'product', 'receipt__order__client', 'receipt__order__chill_zone__library'
        ).prefetch_related('product__category', 'product__supplier').order_by('-id')

        user = self.request.user
        if not user.is_staff:
            return qs.filter(receipt__order__client=user)
        return filter_by_branch(qs, user, library_field=self.library_field)

class LibraryBookViewSet(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    queryset = LibraryBook.objects.all()
    library_field = 'library'
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LibraryBookCreateSerializer
        return LibraryBookSerializer

    def get_queryset(self):
        qs = LibraryBook.objects.select_related('library', 'book').order_by('id')
        book_id = self.request.query_params.get('book')
        library_id = self.request.query_params.get('library')
        if book_id:
            qs = qs.filter(book_id=book_id)
        if library_id:
            qs = qs.filter(library_id=library_id)
        return filter_by_branch(qs, self.request.user, library_field=self.library_field)

    def perform_create(self, serializer):
        user = self.request.user
        library = serializer.validated_data['library']

        if not user.is_superuser:
            employee = getattr(user, 'employee_profile', None)
            if not employee or not employee.library or library != employee.library:
                raise PermissionDenied('You cannot add books to someone else\'s branch. o((>ω< ))o')

        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser, IsSameBranchOrSuperuser])
    def adjust_stock(self, request, pk=None):
        link = self.get_object()
        serializer = StockAdjustSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        delta = serializer.validated_data['delta']

        with transaction.atomic():
            locked = LibraryBook.objects.select_for_update().get(pk=link.pk)
            if locked.quantity + delta < 0:
                raise serializers.ValidationError({'delta': 'The final quantity cannot be negative. (￣﹏￣；)'})
            LibraryBook.objects.filter(pk=locked.pk).update(quantity=F('quantity') + delta)

        link.refresh_from_db()
        return Response({'quantity': link.quantity})


