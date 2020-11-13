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
