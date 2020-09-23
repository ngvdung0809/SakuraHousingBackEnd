class Error:
    code = "code"
    message = "message"


class ErrorCode:
    not_error = {
        Error.code: 0,
        Error.message: "成功"
    }
    unknown_error = {
        Error.code: 1,
        Error.message: "不明なエラーが発生しました。管理者に連絡してください。"
    }
    error_json_parser = {
        Error.code: 2,
        Error.message: "不明なエラーが発生しました。もう一度お試しください。"
    }
    wrong_email = {
        Error.code: 3,
        Error.message: 'メールが見つかりません',
    }
    account_has_exist = {
        Error.code: 4,
        Error.message: 'tai khoan da ton tai vui long tao tai khoan khac'
    }
    not_found_record = {
        Error.code: 5,
        Error.message: 'サーバーにデータが見つかりません'
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
    birthday_invalid_format = {
        Error.code: 9,
        Error.message: "ngay sinh k dung format"
    }
    birthday_invalid_date = {
        Error.code: 10,
        Error.message: "sai ngay sinh"
    }
    not_found_company = {
        Error.code: 11,
        Error.message: "khong tim thay company"
    }
    login_fail = {
        Error.code: 12,
        Error.message: 'メールアドレスまたはパスワードに誤りがあります'
    }
    has_exist_email = {
        Error.code: 13,
        Error.message: 'メールは、すでに使われています'
    }
    wrong_data = {
        Error.code: 14,
        Error.message: 'xac thuc that bai user khong ton tai hoac ma otp code sai'
    }
    otp_code_has_expired = {
        Error.code: 15,
        Error.message: 'xac thuc that bai OPT code het han, vui long tao lai tai khoan'
    }
