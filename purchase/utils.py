import calendar
import datetime

from django.shortcuts import redirect


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
    
    Args:
        purchaser (Purchaser): 購入者のインスタンス
        related_data_forms (list): 購入者に関連する情報のフォームのリスト
    """
    for related_data_form in related_data_forms:
        related_data = related_data_form.save(commit=False)
        related_data.purchaser = purchaser
        related_data.save()


def redirect_if_invalid(cart=None, purchaser_pk=None, redirect_url=None):
    """
    カートがない、または、数量が０の場合、または、購入者情報がない場合、リダイレクトする
    
    Args:
        cart (Cart): カートのインスタンス
        purchaser_pk (int): 購入者のプライマリーキー
        redirect_url (str): リダイレクト先のURL
    
    returns:
        redirect: リダイレクト先のURL
    """
    if (cart is None or getattr(cart, 'quantities', 0) == 0) or purchaser_pk is None:
        return redirect(redirect_url)
    return None


def delete_from_session(session, *models):
    """
    モデルのセッションキーが存在する場合に削除する

    Args:
        session (SessionBase): リクエストのセッション情報
        *models(Model): SESSION_KEYを持つモデルクラス
    """
    for model in models:
        session_key = getattr(model, 'SESSION_KEY', None)
        if session_key in session:
            del session[session_key]

def create_dict(keys, values):
    """
    キーと値のリスト（タプル）から辞書を作成する

    Args:
        keys (list or tuple): 辞書のキー
        values (list or tuple):辞書の値

    Returns:
        dict: 辞書を返す。キーと値の要素の長さが一致しない場合は例外（ValueError)が発生する
    """
    if len(keys) != len(values):
        raise ValueError('keysとvaluesの要素の長さが一致していません')

    return dict(zip(keys, values))

def create_information_dict(html_template_keys, mail_template_keys, values):
    """
    HTMLテンプレート、メールテンプレートで使用する情報をまとめた辞書を作成する

    Args:
        html_template_keys (list or tuple): HTMLテンプレートで使用する辞書のキー
        mail_template_keys (list or tuple): メールテンプレートで使用する辞書のキー
        values (list or tuple): HTML, メールテンプレートで使用する辞書の値

    Returns:
        dict: HTML, メールテンプレートで使用する情報をまとめた辞書
    """
    html_template_dict = create_dict(html_template_keys,values)
    mail_template_dict = create_dict(mail_template_keys, values)
    information_dict = {
        'html_template': html_template_dict,
        'mail_template': mail_template_dict
    }
    return information_dict


def get_template_dict(*models, attr_name=None, template_key=None):
    """
    モデルから指定した属性とキーを利用してテンプレート辞書を作成する

    Args:
        models(Model): テンプレート辞書を取得するモデル（可変長引数）
        attr_name (str): 取得する属性名。必須（None以外の属性名）
        template_key (str): テンプレート辞書のキー。必須。

    Raises:
        ValueError: attr_nameがNoneの場合
        AttributeError: モデルに指定したattr_nameが存在しない場合
        KeyError: 指定されたキーがattr_name内に存在しない場合
        TypeError: 指定されたキーの値が辞書型でない場合

    Returns:
        dict: モデルから取得したテンプレート辞書を連結した辞書
    """
    if attr_name is None:
        raise ValueError('引数 attr_nameに取得する属性を渡す必要があります')
    template_dict = {}
    for model in models:
        try:
            informations = getattr(model, attr_name, None)
            if informations is None:
                raise AttributeError(f'"{attr_name}"プロパティが{model.__class__.__name__}モデルに存在しません')
            
            if template_key not in informations:
                raise KeyError(f'{template_key} が {model.__class__.__name__}.{attr_name} に存在しません')
            
            template_value = informations[template_key]
            
            if not isinstance(template_value, dict):
                raise TypeError(f'{template_key}の値は辞書型である必要があります')
            
            template_dict.update(template_value)
            
        except (AttributeError, KeyError, TypeError) as err:
            raise type(err)(f'{err} (Model: {model.__class__.__name__}) from err')
        
    return template_dict