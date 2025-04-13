from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Item, PurchaseHeader, SellHeader, PurchaseDetail, SellDetail, SellAllocation
from .serializers import ItemSerializer, PurchaseHeaderSerializer, SellHeaderSerializer, PurchaseDetailSerializer, SellDetailSerializer
from datetime import datetime

class ItemViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Items.
    """
    queryset = Item.objects.filter(is_deleted=False)
    serializer_class = ItemSerializer
    lookup_field = 'code'

class PurchaseHeaderViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Purchase Headers.
    """
    queryset = PurchaseHeader.objects.filter(is_deleted=False)
    serializer_class = PurchaseHeaderSerializer
    lookup_field = 'code'

class SellHeaderViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Sell Headers.
    """
    queryset = SellHeader.objects.filter(is_deleted=False)
    serializer_class = SellHeaderSerializer
    lookup_field = 'code'

class PurchaseDetailListCreate(generics.ListCreateAPIView):
    """
    List and create Purchase Details under a specific header.
    """
    serializer_class = PurchaseDetailSerializer

    def get_queryset(self):
        """Filter details by header code, excluding deleted records."""
        header_code = self.kwargs['header_code']
        return PurchaseDetail.objects.filter(header__code=header_code, header__is_deleted=False, is_deleted=False)
    
    def get_serializer_context(self):
        """Pass header to serializer context."""
        context = super().get_serializer_context()
        context['header'] = PurchaseHeader.objects.get(code=self.kwargs['header_code'], is_deleted=False)
        return context

class SellDetailListCreate(generics.ListCreateAPIView):
    """
    List and create Sell Details under a specific header.
    """
    serializer_class = SellDetailSerializer

    def get_queryset(self):
        """Filter details by header code, excluding deleted records."""
        header_code = self.kwargs['header_code']
        return SellDetail.objects.filter(header__code=header_code, header__is_deleted=False, is_deleted=False)
    
    def get_serializer_context(self):
        """Pass header to serializer context."""
        context = super().get_serializer_context()
        context['header'] = SellHeader.objects.get(code=self.kwargs['header_code'], is_deleted=False)
        return context

class ReportView(APIView):
    """
    Generate a stock report for an item over a date range.
    """
    def get(self, request, item_code):
        # Parse query parameters
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
        
        # Fetch item
        try:
            item = Item.objects.get(code=item_code, is_deleted=False)
        except Item.DoesNotExist:
            return Response({"error": "Item not found."}, status=404)
        
        # Initialize stock state before start_date
        initial_purchases = PurchaseDetail.objects.filter(
            item=item,
            header__date__lt=start_date,
            header__is_deleted=False
        ).order_by('header__date')
        stock_queue = [(pd, pd.remaining_quantity) for pd in initial_purchases if pd.remaining_quantity > 0]

        # Fetch transactions within date range
        purchases = PurchaseDetail.objects.filter(
            item=item,
            header__date__gte=start_date,
            header__date__lte=end_date,
            header__is_deleted=False
        )
        sell_allocations = SellAllocation.objects.filter(
            sell_detail__item=item,
            sell_detail__header__date__gte=start_date,
            sell_detail__header__date__lte=end_date,
            sell_detail__header__is_deleted=False
        )

        # Create ordered list of events
        events = []
        for pd in purchases:
            events.append({
                'type': 'purchase',
                'date': pd.header.date,
                'description': pd.header.description,
                'code': pd.header.code,
                'detail': pd
            })
        for allocation in sell_allocations:
            events.append({
                'type': 'sell',
                'date': allocation.sell_detail.header.date,
                'description': allocation.sell_detail.header.description,
                'code': allocation.sell_detail.header.code,
                'allocation': allocation
            })
        events.sort(key=lambda x: x['date'])

        # Initialize report structure
        report = {
            'item_code': item.code,
            'name': item.name,
            'unit': item.unit,
            'transactions': [],
            'summary': {
                'in': {'qty': 0, 'total': 0},
                'out': {'qty': 0, 'total': 0},
                'stock': []
            }
        }

        # Current stock state
        current_stock = [
            {'qty': qty, 'price': float(pd.unit_price), 'total': float(qty * pd.unit_price)}
            for pd, qty in stock_queue if qty > 0
        ]

        # Process each event
        for event in events:
            if event['type'] == 'purchase':
                pd = event['detail']
                # Create transaction entry
                transaction = {
                    'date': event['date'].strftime('%Y-%m-%d'),
                    'description': event['description'],
                    'code': event['code'],
                    'in': {
                        'qty': pd.quantity,
                        'price': float(pd.unit_price),
                        'total': float(pd.quantity * pd.unit_price)
                    },
                    'out': {'qty': 0, 'price': 0, 'total': 0},
                    'stock': current_stock + [{
                        'qty': pd.quantity,
                        'price': float(pd.unit_price),
                        'total': float(pd.quantity * pd.unit_price)
                    }]
                }
                report['transactions'].append(transaction)
                # Update stock and summary
                current_stock.append({
                    'qty': pd.quantity,
                    'price': float(pd.unit_price),
                    'total': float(pd.quantity * pd.unit_price)
                })
                report['summary']['in']['qty'] += pd.quantity
                report['summary']['in']['total'] += float(pd.quantity * pd.unit_price)
            
            elif event['type'] == 'sell':
                allocation = event['allocation']
                pd = allocation.purchase_detail
                qty = allocation.quantity
                # Create transaction entry
                transaction = {
                    'date': event['date'].strftime('%Y-%m-%d'),
                    'description': event['description'],
                    'code': event['code'],
                    'in': {'qty': 0, 'price': 0, 'total': 0},
                    'out': {
                        'qty': qty,
                        'price': float(pd.unit_price),
                        'total': float(qty * pd.unit_price)
                    },
                    'stock': [stock for stock in current_stock if stock['qty'] > 0]
                }
                report['transactions'].append(transaction)
                # Update stock: reduce or remove depleted batch
                for stock in current_stock:
                    if stock['price'] == float(pd.unit_price):
                        if stock['qty'] >= qty:
                            stock['qty'] -= qty
                            stock['total'] = float(stock['qty'] * stock['price'])
                        else:
                            current_stock.remove(stock)
                        break
                # Update summary
                report['summary']['out']['qty'] += qty
                report['summary']['out']['total'] += float(qty * pd.unit_price)
            
        # Final stock in summary
        report['summary']['stock'] = [stock for stock in current_stock if stock['qty'] > 0]
        return Response(report)
