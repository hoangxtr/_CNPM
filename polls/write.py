from django.utils import timezone


def writeOwnerReport(list_order_history, store):
    import xlwt
    from xlwt import Workbook

    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    row = 0
    col = 0
    sum_total = 0
    border_center = xlwt.easyxf('borders: top_color black, left_color black, bottom_color black, right_color black, '
                                ' top thin, left thin, bottom thin, right thin; align: vert centre, horiz centre')
    border = xlwt.easyxf('borders: top_color black, left_color black, bottom_color black, right_color black, '
                         ' top thin, left thin, bottom thin, right thin')
    border_top_bot = xlwt.easyxf('borders: top_color black, bottom_color black, top thin, bottom thin')
    time = str(timezone.now().day) + '-' + str(timezone.now().month) + '-' + str(timezone.now().year)
    sheet1.write(row, col, 'Báo Cáo Ngày: ' + time)
    sheet1.merge(row, row, col, col + 2)
    row = row + 2
    col = col + 2
    for orderHistory in list_order_history:
        if orderHistory.date_ordered.year == timezone.now().year and orderHistory.date_ordered.month == timezone.now().month and orderHistory.date_ordered.day == timezone.now().day and orderHistory.status == 3:
            list_order_item = OrderItem.objects.filter(order=orderHistory)
            sheet1.write(row, col, 'Mã Giao Dịch: ' + str(orderHistory.transaction_id), border_top_bot)
            sheet1.merge(row, row, col, col + 1, border_top_bot)
            sheet1.write(row, col + 2, '', border_top_bot)
            sheet1.write(row, col + 3, '', border_top_bot)
            sheet1.write(row, col + 4, '', border_top_bot)
            row = row + 2
            col = col + 1
            sheet1.write(row, col, 'Tên Món Ăn', border_center)
            sheet1.write(row, col + 1, 'Số Lượng', border_center)
            sheet1.write(row, col + 2, 'Giá Tiền (VND)', border_center)
            sheet1.write(row, col + 3, 'Thành Tiền (VND)', border_center)
            sum = 0
            for orderDetail in list_order_item:
                sheet1.write(row + 1, col, str(orderDetail.food.name), border_center)
                sheet1.write(row + 1, col + 1, orderDetail.quantity, border)
                sheet1.write(row + 1, col + 2, orderDetail.food.price, border)
                sheet1.write(row + 1, col + 3, orderDetail.get_total, border)
                sum = sum + orderDetail.get_total
                row = row + 1
            sheet1.write(row + 2, col - 1, 'Tổng Tiền', border_top_bot)
            sheet1.write(row + 2, col + 3, sum, border_top_bot)
            sheet1.write(row + 2, col, '', border_top_bot)
            sheet1.write(row + 2, col + 1, '', border_top_bot)
            sheet1.write(row + 2, col + 2, '', border_top_bot)
            sum_total = sum_total + sum
            row = row + 5
            col = 2
    sheet1.write(row, 0, 'Doanh Thu Ngày: ' + str(sum_total) + ' VND')
    sheet1.merge(row, row, 0, 2)
    wb.save('./media/' + store + '/' + time + '_report.xls')
    return time

def writeManReport(ven):
    import xlwt
    from xlwt import Workbook
    from system.models import Order, OrderItem
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    row = 0
    col = 0
    sum_total = 0
    border_center = xlwt.easyxf(
        'borders: top_color black, left_color black, bottom_color black, right_color black, '
        ' top thin, left thin, bottom thin, right thin; align: vert centre, horiz centre')
    border = xlwt.easyxf('borders: top_color black, left_color black, bottom_color black, right_color black, '
                         ' top thin, left thin, bottom thin, right thin')
    border_top_bot = xlwt.easyxf('borders: top_color black, bottom_color black, top thin, bottom thin')
    sheet1.write(row, col, 'Báo Cáo Tháng: ' + str(timezone.now().month) + ' năm ' + str(timezone.now().year))
    sheet1.merge(row, row, col, col + 2)
    row = 2
    col = 2
    for store in ven:
        write = True
        sumStore = 0
        list_order = Order.objects.filter(vendor=store)
        for order in list_order:
            if order.date_ordered.month == timezone.now().month and order.date_ordered.year == timezone.now().year and order.status == 3:
                quantity = 0
                sum = 0;
                list_order_item = OrderItem.objects.filter(order=order)
                if write:
                    sheet1.write(row, col - 1, str(order.store.name) + ':', border_top_bot)
                    sheet1.merge(row, row, col - 1, col + 2, border_top_bot)
                    row = row + 2;
                    sheet1.write(row, col, 'Ngày', border_center)
                    sheet1.write(row, col + 1, 'Số Lượng Đơn Hàng', border_center)
                    sheet1.write(row, col + 2, 'Doanh Thu (VND)', border_center)
                    write = False
                    row = row + 1
                for orderItem in list_order_item:
                    sum = sum + orderItem.get_total
                    quantity = quantity + 1
                sumStore = sumStore + sum
                sheet1.write(row, col, str(order.date_ordered.day), border_center)
                sheet1.write(row, col + 1, quantity, border)
                sheet1.write(row, col + 2, sum, border)
                row = row + 1
        sheet1.write(row + 1, col - 1, 'Tổng Doanh Thu Tháng', border_top_bot)
        sheet1.merge(row + 1, row + 1, col - 1, col, border_top_bot)
        sheet1.write(row + 1, col + 1, '', border_top_bot)
        sheet1.write(row + 1, col + 2, sumStore, border_top_bot)
        row = row + 4
        sum_total = sum_total + sumStore
    sheet1.write(row, col - 2, 'Doanh Thu Tháng Food Court: ' + str(sum_total) + ' VND')
    sheet1.merge(row, row, col - 2, col + 1)
    wb.save(str(timezone.now().month) + '-' + str(timezone.now().year) + '_report.xls')
