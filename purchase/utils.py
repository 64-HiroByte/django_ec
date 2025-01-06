import calendar
import datetime


def convert_expiration_string_to_date(expiration):
        """
        'MM/YY'形式で入力した文字列の月末日でdate型に変換する

        Args:
            expiration (str): MM/YY形式で入力した月と年

        Returns:
            date: YYYY-MM-DD に変換された日付（DDは末日）
        """
        expiration_m, expiration_y = expiration.split('/')
        
        expiration_y = 2000 + int(expiration_y)
        expiration_m = int(expiration_m)
        expiration_d = calendar.monthrange(expiration_y, expiration_m)[1]
        expiration_date = datetime.date(expiration_y, expiration_m, expiration_d)
        return expiration_date