import datetime

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from purchase import utils


class ValidateDigitsNumber(RegexValidator):
    """
    指定された桁数の数字のみを受け付けるバリデータ
    args:
        length(int): 桁数
    params:
        regex(str): 正規表現
        message(str): エラーメッセージ
    """
    def __init__(self, length):
        self.length = length
        
        regex = rf'^\d{{{length}}}$'
        message = f'{length}桁の数字を入力してください'
        super().__init__(regex=regex, message=message)


def validate_expiration_date(str_month_year):
    """
    購入日と有効期限の比較を行うバリデータ
    
    args:
        str_month_year(str): MM/YY形式の文字列
    """
    expiration_date = utils.convert_expiration_string_to_date(str_month_year)
    if expiration_date < datetime.date.today():
        raise ValidationError('有効期限が切れています')