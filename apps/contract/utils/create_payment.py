from datetime import datetime
from dateutil.relativedelta import relativedelta

from apps.contract.models import HD2DichVus
from apps.payment.models import PaymentTransactions, ServiceTransactions


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
    list_time = payment_transaction(hd_thue.start_date, hd_thue.end_date, hd_thue.ky_tt)
    
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


def generate_service(service, start_date, end_date):
    list_obj = []
    for i in service:
        list_time = payment_transaction(start_date, end_date, i.ky_tt)
        for j in list_time:
            list_obj.append(ServiceTransactions(
                hd_2_dichvu=i,
                dot_thanh_toan="T{}".format(j.strftime("%m-%Y")),
                ngay_thanh_toan_du_kien=j,
            ))
    ServiceTransactions.objects.bulk_create(list_obj)
    return True


def create_hd2_dv(dich_vus, hd_thue):
    list_obj = [HD2DichVus(
        hd_thue=hd_thue,
        dich_vu_id=i['dich_vu'],
        ky_tt=i['ky_tt'],
        dinh_muc=i.get('dinh_muc', None),
        note=i.get('note', None)
    ) for i in dich_vus]
    list_instance = HD2DichVus.objects.bulk_create(list_obj)
    return list_instance
