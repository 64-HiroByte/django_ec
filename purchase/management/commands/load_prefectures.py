from django.core.management.base import BaseCommand

from purchase.models import Prefecture


class Command(BaseCommand):
    help = '都道府県名を一括登録します'

    def handle(self, *args, **kwargs):
        """
        都道府県名を一括登録するコマンド
        
        how to use:
            開発環境あるいは本番環境で、以下のコマンドを実行する
            $ python manage.py load_prefectures
        """
        prefectures = [
            '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県',
            '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県',
            '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県',
            '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県',
            '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県',
            '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県',
            '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県'
        ]
        
        for prefecture_name in prefectures:
            Prefecture.objects.get_or_create(name=prefecture_name)
        