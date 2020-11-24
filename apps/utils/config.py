class PasswordRegex:
    password_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d!@#$%^&*?]{8,50}$"


class MailSubject:
    payment = 'Nhắc hẹn thanh toán'
    warning_payment = 'Nhắc nhở thanh toán quá hạn'
