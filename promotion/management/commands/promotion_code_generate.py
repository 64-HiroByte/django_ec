import random
import string

from django.core.management.base import BaseCommand

# from promotion.models import PromotionCode


class Command(BaseCommand):
    help = 'プロモーションコードと割引額を作成します'
    
    def add_arguments(self, parser):
        parser.add_argument('-l', '--lower', default=100, type=int, help='lower limit of discount')
        parser.add_argument('-u', '--upper', default=1000, type=int, help='upper limit of discount')
        parser.add_argument('-i', '--increment', default=10, type=int, help='discount increment')
        parser.add_argument('-c', '--count', default=7, type=int, help='number of characters in promotion code')
        parser.add_argument('-g', '--generate', default=10, type=int, help='number of promotion codes to generate')
    
    def handle(self, *args, **options):
        lower_limit = options.get('lower')
        upper_limit = options.get('upper')
        increment = options.get('increment')
        code_length = options.get('count')
        generate_num = options.get('generate')
        
        for _ in range(generate_num):
            chars = string.ascii_letters + string.digits
            generated_code = ''.join([random.choice(chars) for _ in range(code_length)])
            discount_amount = random.randrange(lower_limit, upper_limit + 1, increment)
            print(f'code: {generated_code}, discount amount: {discount_amount}')
        