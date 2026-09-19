"""
Management command для заполнения базы данных тестовыми данными:
категории, подкатегории, товары (с переводами EN/RU), пользователи
и отзывы к товарам.

Как использовать:
1. Положи этот файл в:
   avito_app/management/commands/seed_data.py

   Структура:
   avito_app/
       management/
           __init__.py
           commands/
               __init__.py
               seed_data.py

2. Запусти:
   python manage.py seed_data

Команда идемпотентна:
 - категории/подкатегории/товары — по уникальным полям (article и т.д.)
 - пользователи — по username
 - отзывы — по паре (пользователь, товар), т.е. один пользователь
   оставляет максимум один отзыв на товар (это и логично, и защищает
   от дублей при повторном запуске команды)
"""

from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from avito_app.models import Category, SubCategory, Product, UserProfile, Review
import itertools
import os
import random


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными: категории, товары, пользователи, отзывы (EN/RU)'

    def handle(self, *args, **options):
        self.stdout.write('Начинаю заполнение базы данных...')

        PLACEHOLDER_IMAGE_PATH = None  # например: 'seed_images/placeholder.jpg'

        def get_image_file(path):
            if path and os.path.exists(path):
                return ImageFile(open(path, 'rb'))
            return None

        # =================================================================
        # 1. КАТЕГОРИИ / ПОДКАТЕГОРИИ / ТОВАРЫ
        # =================================================================
        CATALOG = [
            {
                'category': ('Electronics', 'Электроника'),
                'subcategories': [
                    {
                        'name': ('Smartphones', 'Смартфоны'),
                        'brands': ['Apple', 'Samsung', 'Xiaomi', 'Honor', 'Realme', 'OnePlus'],
                        'items': [
                            ('Smartphone Pro', 'Смартфон Про', 45000, 95000),
                            ('Smartphone Lite', 'Смартфон Лайт', 15000, 35000),
                            ('Smartphone Ultra', 'Смартфон Ультра', 70000, 130000),
                        ],
                    },
                    {
                        'name': ('Laptops', 'Ноутбуки'),
                        'brands': ['Apple', 'ASUS', 'Lenovo', 'HP', 'Acer', 'Dell'],
                        'items': [
                            ('Laptop 14"', 'Ноутбук 14"', 40000, 90000),
                            ('Gaming Laptop', 'Игровой ноутбук', 80000, 180000),
                            ('Ultrabook', 'Ультрабук', 55000, 120000),
                        ],
                    },
                ],
            },
            {
                'category': ('Clothing', 'Одежда'),
                'subcategories': [
                    {
                        'name': ("Men's Wear", 'Мужская одежда'),
                        'brands': ['Zara', 'H&M', 'Nike', 'Adidas', "Levi's", 'Uniqlo'],
                        'items': [
                            ('Denim Jacket', 'Джинсовая куртка', 2500, 6000),
                            ('T-Shirt', 'Футболка', 800, 2500),
                            ('Jeans', 'Джинсы', 2000, 5500),
                            ('Sneakers', 'Кроссовки', 3500, 9000),
                        ],
                    },
                    {
                        'name': ("Women's Wear", 'Женская одежда'),
                        'brands': ['Zara', 'H&M', 'Mango', 'Bershka', 'Uniqlo'],
                        'items': [
                            ('Summer Dress', 'Летнее платье', 1800, 5000),
                            ('Blouse', 'Блузка', 1200, 3200),
                            ('Handbag', 'Сумка', 2500, 8000),
                        ],
                    },
                ],
            },
            {
                'category': ('Home & Garden', 'Дом и сад'),
                'subcategories': [
                    {
                        'name': ('Furniture', 'Мебель'),
                        'brands': ['IKEA', 'HomePro', 'ComfortHome', 'WoodLine'],
                        'items': [
                            ('Sofa', 'Диван', 15000, 45000),
                            ('Office Chair', 'Офисное кресло', 4000, 15000),
                            ('Coffee Table', 'Журнальный столик', 3000, 9000),
                        ],
                    },
                    {
                        'name': ('Kitchenware', 'Кухонная утварь'),
                        'brands': ['Tefal', 'Zwilling', 'Fissman', 'Bekker'],
                        'items': [
                            ('Frying Pan', 'Сковорода', 800, 3500),
                            ('Knife Set', 'Набор ножей', 1500, 6000),
                            ('Blender', 'Блендер', 2000, 7000),
                        ],
                    },
                ],
            },
            {
                'category': ('Sports', 'Спорт'),
                'subcategories': [
                    {
                        'name': ('Fitness', 'Фитнес'),
                        'brands': ['Nike', 'Adidas', 'Reebok', 'Puma'],
                        'items': [
                            ('Yoga Mat', 'Коврик для йоги', 600, 2000),
                            ('Dumbbells Set', 'Набор гантелей', 1500, 6000),
                            ('Running Shoes', 'Кроссовки для бега', 3000, 9000),
                        ],
                    },
                    {
                        'name': ('Outdoor', 'Активный отдых'),
                        'brands': ['Quechua', 'Columbia', 'The North Face', 'Salomon'],
                        'items': [
                            ('Tent', 'Палатка', 4000, 15000),
                            ('Backpack', 'Рюкзак', 2000, 8000),
                            ('Sleeping Bag', 'Спальный мешок', 1800, 6000),
                        ],
                    },
                ],
            },
            {
                'category': ('Beauty & Health', 'Красота и здоровье'),
                'subcategories': [
                    {
                        'name': ('Skincare', 'Уход за кожей'),
                        'brands': ['Nivea', 'La Roche-Posay', 'CeraVe', 'Garnier'],
                        'items': [
                            ('Face Cream', 'Крем для лица', 500, 3000),
                            ('Sunscreen', 'Солнцезащитный крем', 700, 2500),
                            ('Serum', 'Сыворотка', 900, 4000),
                        ],
                    },
                    {
                        'name': ('Haircare', 'Уход за волосами'),
                        'brands': ["L'Oreal", 'Pantene', 'Schwarzkopf', 'Dove'],
                        'items': [
                            ('Shampoo', 'Шампунь', 300, 1500),
                            ('Hair Dryer', 'Фен', 1500, 7000),
                            ('Hair Mask', 'Маска для волос', 400, 1800),
                        ],
                    },
                ],
            },
            {
                'category': ('Auto', 'Автотовары'),
                'subcategories': [
                    {
                        'name': ('Accessories', 'Аксессуары'),
                        'brands': ['Bosch', 'Philips', 'AutoPro', 'CarLife'],
                        'items': [
                            ('Car Vacuum Cleaner', 'Автопылесос', 1500, 5000),
                            ('Dash Cam', 'Видеорегистратор', 2000, 9000),
                            ('Car Charger', 'Автомобильное зарядное устройство', 400, 1500),
                        ],
                    },
                    {
                        'name': ('Tires & Wheels', 'Шины и диски'),
                        'brands': ['Michelin', 'Pirelli', 'Bridgestone', 'Continental'],
                        'items': [
                            ('Summer Tire', 'Летняя шина', 4000, 12000),
                            ('Winter Tire', 'Зимняя шина', 4500, 13000),
                            ('Alloy Wheel', 'Литой диск', 5000, 15000),
                        ],
                    },
                ],
            },
            {
                'category': ('Kids', 'Детские товары'),
                'subcategories': [
                    {
                        'name': ('Toys', 'Игрушки'),
                        'brands': ['LEGO', 'Hasbro', 'Mattel', 'Fisher-Price'],
                        'items': [
                            ('Building Blocks Set', 'Конструктор', 1000, 6000),
                            ('Plush Toy', 'Мягкая игрушка', 500, 2500),
                            ('Puzzle', 'Пазл', 400, 1800),
                        ],
                    },
                    {
                        'name': ('Baby Care', 'Товары для малышей'),
                        'brands': ['Pampers', 'Huggies', 'Avent', 'Chicco'],
                        'items': [
                            ('Stroller', 'Коляска', 8000, 25000),
                            ('Baby Bottle', 'Детская бутылочка', 300, 1000),
                            ('Diapers Pack', 'Упаковка подгузников', 800, 2500),
                        ],
                    },
                ],
            },
            {
                'category': ('Books', 'Книги'),
                'subcategories': [
                    {
                        'name': ('Fiction', 'Художественная литература'),
                        'brands': ['Eksmo', 'AST', 'Penguin', 'HarperCollins'],
                        'items': [
                            ('Novel', 'Роман', 300, 1200),
                            ('Short Story Collection', 'Сборник рассказов', 250, 900),
                            ('Poetry Book', 'Сборник стихов', 200, 800),
                        ],
                    },
                    {
                        'name': ('Non-Fiction', 'Нехудожественная литература'),
                        'brands': ['Alpina', 'MIF', 'Penguin', 'HarperCollins'],
                        'items': [
                            ('Business Guide', 'Бизнес-книга', 400, 1500),
                            ('Self-Help Book', 'Книга по саморазвитию', 350, 1300),
                            ('Textbook', 'Учебник', 500, 2000),
                        ],
                    },
                ],
            },
            {
                'category': ('Pets', 'Товары для животных'),
                'subcategories': [
                    {
                        'name': ('Dog Supplies', 'Товары для собак'),
                        'brands': ['Royal Canin', 'Pedigree', 'Trixie', 'Ferplast'],
                        'items': [
                            ('Dog Food', 'Корм для собак', 500, 3000),
                            ('Dog Leash', 'Поводок', 300, 1500),
                            ('Dog Bed', 'Лежанка для собаки', 800, 3500),
                        ],
                    },
                    {
                        'name': ('Cat Supplies', 'Товары для кошек'),
                        'brands': ['Whiskas', 'Purina', 'Trixie', 'Ferplast'],
                        'items': [
                            ('Cat Food', 'Корм для кошек', 400, 2500),
                            ('Cat Litter', 'Наполнитель для кошачьего туалета', 300, 1200),
                            ('Cat Scratching Post', 'Когтеточка', 800, 3000),
                        ],
                    },
                ],
            },
        ]

        DESC_EN = "{brand} {item} — reliable quality, great value for the price. A popular choice among customers."
        DESC_RU = "{brand} {item} — надёжное качество и отличное соотношение цены и качества. Популярный выбор среди покупателей."

        article_counter = itertools.count(1000001)
        created_categories = 0
        created_subcategories = 0
        created_products = 0
        all_products = []

        for cat_data in CATALOG:
            cat_en, cat_ru = cat_data['category']
            category, created = Category.objects.get_or_create(
                category_name_en=cat_en,
                defaults={'category_name_ru': cat_ru, 'category_name': cat_en},
            )
            if created:
                created_categories += 1
                img = get_image_file(PLACEHOLDER_IMAGE_PATH)
                if img:
                    category.category_image.save(os.path.basename(PLACEHOLDER_IMAGE_PATH), img, save=True)

            for sub_data in cat_data['subcategories']:
                sub_en, sub_ru = sub_data['name']
                subcategory, created = SubCategory.objects.get_or_create(
                    SubCategory_name_en=sub_en,
                    defaults={'SubCategory_name_ru': sub_ru, 'SubCategory_name': sub_en, 'category': category},
                )
                if created:
                    created_subcategories += 1
                    img = get_image_file(PLACEHOLDER_IMAGE_PATH)
                    if img:
                        subcategory.subcategory_image.save(os.path.basename(PLACEHOLDER_IMAGE_PATH), img, save=True)

                for item_en, item_ru, price_min, price_max in sub_data['items']:
                    for brand in sub_data['brands']:
                        article = next(article_counter)
                        name_en = f'{brand} {item_en}'
                        name_ru = f'{item_ru} {brand}'
                        price = round(random.uniform(price_min, price_max), 2)

                        product, created = Product.objects.get_or_create(
                            article=article,
                            defaults={
                                'subcategory': subcategory,
                                'product_name_en': name_en,
                                'product_name_ru': name_ru,
                                'product_name': name_en,
                                'description_en': DESC_EN.format(brand=brand, item=item_en),
                                'description_ru': DESC_RU.format(brand=brand, item=item_ru),
                                'description': DESC_EN.format(brand=brand, item=item_en),
                                'price': price,
                            },
                        )
                        if created:
                            created_products += 1
                        all_products.append(product)

        # =================================================================
        # 2. ПОЛЬЗОВАТЕЛИ
        # =================================================================
        USERS = [
            ('Айгуль', 'Асанова', 'aigul_asanova'),
            ('Бакыт', 'Жумабеков', 'bakyt_jumabekov'),
            ('Нурлан', 'Токтогулов', 'nurlan_toktogulov'),
            ('Динара', 'Сатылганова', 'dinara_satylganova'),
            ('Эрлан', 'Мамытов', 'erlan_mamytov'),
            ('Гульнара', 'Исаева', 'gulnara_isaeva'),
            ('Тимур', 'Абдыкадыров', 'timur_abdykadyrov'),
            ('Жамиля', 'Осмонова', 'jamilya_osmonova'),
            ('Руслан', 'Бекболотов', 'ruslan_bekbolotov'),
            ('Айжан', 'Курманова', 'aijan_kurmanova'),
            ('Максим', 'Иванов', 'maxim_ivanov'),
            ('Елена', 'Петрова', 'elena_petrova'),
            ('Сергей', 'Смирнов', 'sergey_smirnov'),
            ('Анна', 'Кузнецова', 'anna_kuznetsova'),
            ('Дмитрий', 'Соколов', 'dmitry_sokolov'),
            ('Ольга', 'Попова', 'olga_popova'),
            ('Азамат', 'Сыдыков', 'azamat_sydykov'),
            ('Чолпон', 'Дуйшеева', 'cholpon_duisheeva'),
            ('Бекзат', 'Орозов', 'bekzat_orozov'),
            ('Салтанат', 'Нурматова', 'saltanat_nurmatova'),
            ('Иван', 'Волков', 'ivan_volkov'),
            ('Мария', 'Новикова', 'maria_novikova'),
            ('Талант', 'Шергазиев', 'talant_shergaziev'),
            ('Венера', 'Абдразакова', 'venera_abdrazakova'),
            ('Куттубек', 'Раимкулов', 'kuttubek_raimkulov'),
            ('Жанна', 'Тыналиева', 'janna_tynalieva'),
            ('Алексей', 'Морозов', 'alexey_morozov'),
            ('Наталья', 'Васильева', 'natalya_vasilyeva'),
            ('Эмиль', 'Бекешов', 'emil_bekeshov'),
            ('Бермет', 'Джумашева', 'bermet_jumasheva'),
        ]

        statuses = ['simple', 'bronze', 'silver', 'gold']
        created_users = 0
        all_users = []

        for first_name, last_name, username in USERS:
            user, created = UserProfile.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': f'{username}@example.com',
                    'age': random.randint(18, 65),
                    'phone_number': f'+996{random.randint(500000000, 799999999)}',
                    'status': random.choice(statuses),
                },
            )
            if created:
                user.set_password('TestPass123!')
                user.save()
                created_users += 1
            all_users.append(user)

        # =================================================================
        # 3. ОТЗЫВЫ
        # =================================================================
        COMMENTS_BY_RATING = {
            5: [
                'Отличный товар, полностью соответствует описанию! Обязательно куплю ещё.',
                'Очень доволен покупкой, качество на высоте, рекомендую всем!',
                'Пришло быстро, упаковано хорошо, товар супер!',
                'Лучшая покупка за последнее время, спасибо продавцу!',
            ],
            4: [
                'Хороший товар, но есть небольшие нюансы. В целом доволен.',
                'Качество приятно удивило, цена адекватная. Рекомендую.',
                'Почти всё понравилось, разве что доставка немного задержалась.',
            ],
            3: [
                'Товар нормальный, ничего особенного. Соответствует цене.',
                'Среднее качество, но использовать можно.',
                'Ожидал большего, но в целом не разочарован.',
            ],
            2: [
                'Качество ниже среднего, есть нарекания.',
                'Не совсем то, что ожидал по описанию.',
                'Товар быстро потерял вид, не уверен, что куплю снова.',
            ],
            1: [
                'Очень разочарован покупкой, не рекомендую.',
                'Пришёл товар с браком, буду оформлять возврат.',
                'Качество ужасное, деньги на ветер.',
            ],
        }

        created_reviews = 0
        # Каждому товару назначаем случайное количество отзывов (0-4)
        # от случайных пользователей, без повторов пользователя на один товар.
        for product in all_products:
            num_reviews = random.randint(0, 4)
            if num_reviews == 0:
                continue
            reviewers = random.sample(all_users, min(num_reviews, len(all_users)))
            for user in reviewers:
                stars = random.choices(
                    population=[5, 4, 3, 2, 1],
                    weights=[40, 30, 15, 10, 5],  # больше положительных отзывов, как в реальной жизни
                    k=1,
                )[0]
                comment = random.choice(COMMENTS_BY_RATING[stars])

                review, created = Review.objects.get_or_create(
                    user=user,
                    product=product,
                    defaults={'comment': comment, 'stars': stars},
                )
                if created:
                    created_reviews += 1

        self.stdout.write(self.style.SUCCESS(
            f'Готово! Создано: категорий — {created_categories}, '
            f'подкатегорий — {created_subcategories}, товаров — {created_products}, '
            f'пользователей — {created_users}, отзывов — {created_reviews}.'
        ))