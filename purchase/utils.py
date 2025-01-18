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


def save_purchase_related_data(purchaser, related_data_forms):
    """
    購入者に関連する情報を保存する
    args:
        purchaser (Purchaser): 購入者のインスタンス
        related_data_forms (list or tuple): 購入者に関連する情報のフォームのリストまたはタプル
    """
    for related_data_form in related_data_forms:
        related_data = related_data_form.save(commit=False)
        related_data.purchaser = purchaser
        related_data.save()
