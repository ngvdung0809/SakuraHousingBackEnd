class Error:
    code = "code"
    message = "message"


class ErrorCode:
    not_error = {
        Error.code: 0,
        Error.message: "Success"
    }
    unknown_error = {
        Error.code: 1,
        Error.message: "Đã có lỗi xảy trên trên server vui lòng liên hệ admin để kiểm tra"
    }
    error_json_parser = {
        Error.code: 2,
        Error.message: "Dữ liệu không hợp lệ"
    }
    account_has_exist = {
        Error.code: 4,
        Error.message: 'tai khoan da ton tai vui long tao tai khoan khac'
    }
    not_found_record = {
        Error.code: 5,
        Error.message: 'Không tìm thấy dữ liệu trên server'
    }
    error_not_auth = {
        Error.code: 6,
        Error.message: "Vui lòng đăng nhập để sử dụng chức năng này!"
    }
    invalid_auth = {
        Error.code: 7,
        Error.message: "Phiên đăng nhập đã hết hạn, vui lòng đăng nhập lại!"
    }
    password_invalid = {
        Error.code: 8,
        Error.message: "password khong dung yeu cau"
    }
    login_fail = {
        Error.code: 12,
        Error.message: 'Username hoặc password không chính xác vui lòng kiểm tra lại'
    }
    lock_account = {
        Error.code: 13,
        Error.message: 'Tai khoan bi khoa vui long lien he admin de biet them thong tin'
    }
    cant_delete_tenant = {
        Error.code: 14,
        Error.message: 'Khong the xoa tenant vi co tai khoan cua cong ty nay'
    }
    wrong_password = {
        Error.code: 15,
        Error.message: 'sai mat khau'
    }
    duplicate_password = {
        Error.code: 16,
        Error.message: 'Password cu va moi khong duoc giong nhau'
    }
    cant_delete_host = {
        Error.code: 17,
        Error.message: 'Khong the xoa chủ nha vi co căn hộ của chủ nhà này'
    }
    cant_delete_guest = {
        Error.code: 18,
        Error.message: 'Khong the xoa khach thue vi co hd thue lien quan'
    }
    cant_delete_canho = {
        Error.code: 19,
        Error.message: 'Khong the xoa can ho vi co hd group lien quan'
    }
    cant_delete_dv = {
        Error.code: 21,
        Error.message: 'Khong the xoa dich vu vi co hd thue lien quan'
    }
    cant_delete_building = {
        Error.code: 22,
        Error.message: 'Khong the xoa toa nha vi co can ho lien quan'
    }
    cant_delete_account = {
        Error.code: 23,
        Error.message: 'Khong the xoa toa nha vi co bo hop dong lien quan'
    }
