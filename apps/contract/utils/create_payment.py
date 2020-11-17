from datetime import datetime
from dateutil.relativedelta import relativedelta

from apps.payment.models import PaymentTransactions


def payment_transaction(start_date, end_date, ky_tt):
    c = relativedelta(end_date, start_date)
    d = c.months + 12 * c.years
    
    z = round(d / ky_tt)
    
    a = [start_date]
    b = start_date
    
    for i in range(0, z):
        time = b + relativedelta(months=ky_tt)
        b = time
        a.append(time)
    return a


def generate_payment_hd(hd_thue, hd_moi_gioi, chu_nha):
    start_date = datetime.strptime('2020-11-11', '%Y-%m-%d')
    end_date = datetime.strptime('2022-11-11', '%Y-%m-%d')
    list_time = payment_transaction(start_date, end_date, 3)
    
    list_obj_hd_thue = [PaymentTransactions(
        hop_dong=hd_thue,
        dot_thanh_toan="T{}".format(i.strftime("%m-%Y")),
        start_date=i,
        end_date=i + relativedelta(days=7),
        ngay_thanh_toan_du_kien=i,
        so_tien=hd_thue.gia_thue_per_month * hd_thue.ky_tt,
        nguoi_gui=hd_thue.khach_thue,
        nguoi_nhan=chu_nha,
    ) for i in list_time]
    
    if hd_moi_gioi:
        PaymentTransactions.objects.create(
            hop_dong=hd_moi_gioi,
            dot_thanh_toan="Đợt thanh toán hợp đồng môi giới",
            start_date=hd_thue.start_date,
            end_date=hd_thue.start_date + relativedelta(days=7),
            ngay_thanh_toan_du_kien=hd_thue.start_date,
            so_tien=hd_moi_gioi.tien_moi_gioi,
            nguoi_gui=hd_thue.khach_thue,
            nguoi_nhan=chu_nha,
        )
    
    PaymentTransactions.objects.bulk_create(list_obj_hd_thue)
    return True
