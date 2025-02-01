import random
import string
import sys

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db import transaction

from promotion.models import PromotionCode


class Command(BaseCommand):
    help = 'プロモーションコードと割引額を作成します'
    
    def add_arguments(self, parser):
        parser.add_argument('-l', '--lower', default=100, type=int, help='lower limit of discount')
        parser.add_argument('-u', '--upper', default=1000, type=int, help='upper limit of discount')
        parser.add_argument('-i', '--increment', default=10, type=int, help='discount increment')
        parser.add_argument('-c', '--count', default=7, type=int, help='number of characters in promotion code')
        parser.add_argument('-g', '--generate', default=10, type=int, help='number of promotion codes to generate')
    
    def arguments_validator(self, options):
        """
        オプションを入力した場合のバリデーションを行う

        Args:
            options (dict): カスタムコマンドで使用する引数と値の辞書

        Raises:
            CommandError: 不正な値が入力された場合に発生する

        Returns:
            tuple: バリデーションを通過した値のタプル
        """
        lower_limit = options.get('lower')
        upper_limit = options.get('upper')
        increment = options.get('increment')
        code_length = options.get('count')
        generate_num = options.get('generate')
        
        if lower_limit < PromotionCode.MIN_DISCOUNT_AMOUNT:
            raise CommandError(
                f'割引額の下限は、{PromotionCode.MIN_DISCOUNT_AMOUNT}以上の整数である必要があります'
            )
        if upper_limit > PromotionCode.MAX_DISCOUNT_AMOUNT:
            raise CommandError(
                f'割引額の上限は、{PromotionCode.MAX_DISCOUNT_AMOUNT}以下の整数である必要があります'
            )
            
        if lower_limit > upper_limit :
            raise CommandError(
                f'割引額の上限値({upper_limit})は、下限値({lower_limit})よりも大きい値である必要があります'
            )
        
        if increment < 1:
            raise CommandError(
                f'割引額の増分は、1以上の整数である必要があります'
            )
            
        if code_length < PromotionCode.MIN_CODE_LENGTH or PromotionCode.MAX_CODE_LENGTH < code_length :
            raise CommandError(
                f'生成するプロモーションコードの文字数は、{PromotionCode.MIN_CODE_LENGTH}文字以上、{PromotionCode.MAX_CODE_LENGTH}文字以下である必要があります'
            )
            
        if generate_num < 1:
            raise CommandError(
                f'生成するコードは、1以上の整数である必要があります'
            )
        
        return lower_limit, upper_limit, increment, code_length, generate_num
    
    def handle(self, *args, **options):
        # オプションで渡された値のバリデーションチェック
        try:
            lower_limit, upper_limit, increment, code_length, generate_num = self.arguments_validator(options)
        except CommandError as err:
            self.stderr.write(self.style.ERROR(err))
            sys.exit(1)
        
        # コードの生成に使用する文字列
        chars = string.ascii_letters + string.digits

        # DBに登録済みのプロモーションコードを取得
        existing_codes = set(PromotionCode.objects.values_list('code', flat=True))
        
        generated_codes = set()
        generated_promotions = []
        
        while len(generated_codes) < generate_num:
            # プロモーションコードの文字列を生成し、重複チェックする
            generated_code = ''.join(random.choices(chars, k=code_length))
            if generated_code in existing_codes | generated_codes:
                continue
            
            # 生成したプロモーションコードは重複チェックするため、setに追加する
            generated_codes.add(generated_code)
            
            # 割引額の決定
            discount_amount = random.randrange(lower_limit, upper_limit + 1, increment)
            
            # モデルのインスタンスをリストに追加
            generated_promotions.append(
                PromotionCode(code=generated_code, discount_amount=discount_amount)
            )
        
        # DBへ一括登録
        with transaction.atomic():
            PromotionCode.objects.bulk_create(generated_promotions)
        
        success_message = f'{generate_num}個のプロモーションコードを新規作成しました（割引額: {lower_limit} 〜 {upper_limit}）'
        self.stdout.write(self.style.SUCCESS(success_message))
        
        # 作成したコードの出力
        for generated_promotion in generated_promotions:
            self.stdout.write(f'code: {generated_promotion.code}, discount amount: {generated_promotion.discount_amount}')