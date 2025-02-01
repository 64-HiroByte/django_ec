import random
import string
import sys

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

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
        try:
            lower_limit, upper_limit, increment, code_length, generate_num = self.arguments_validator(options)
        except CommandError as e:
            self.stderr.write(self.style.ERROR(e))
            sys.exit(1)
        
        for _ in range(generate_num):
            chars = string.ascii_letters + string.digits
            generated_code = ''.join(random.choices(chars, k=code_length))
            discount_amount = random.randrange(lower_limit, upper_limit + 1, increment)
            print(f'code: {generated_code}, discount amount: {discount_amount}')
        