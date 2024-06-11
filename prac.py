data = [
    {
        'title': 'Турман, Ума',
        'content': """У́ма Кару́на Ту́рман (англ. Uma Karuna Thurman; род. 29 апреля 1970, Бостон, США) — американская актриса и бывшая модель.
        
        Сыграла главные роли в различных кинолентах, от романтических комедий и драм до научно-фантастических фильмов и боевиков. После ранних ролей в таких фильмах, как «Опасные связи», она добилась международной известности в 1994 году, сыграв роль Мии Уоллес в «Криминальном чтиве» Квентина Тарантино, за которую была номинирована на премии «Оскар», «Золотой глобус» и BAFTA.""",
        'slug': 'slug-uma',
        'cat_id': 1,
    },
    {
        'title': 'Лопес, Дженнифер',
        'content': """Дже́ннифер Линн А́ффлек[1] (англ. Jennifer Lynn Affleck, ранее — Ло́пес (англ. Lopez) или Джей Ло (англ. J.Lo); род. 24 июля 1969, Бронкс, Нью-Йорк) — американская актриса, певица, танцовщица, модельер, продюсер и бизнесвумен. Впервые получила известность в 1991 году в качестве танцовщицы труппы Fly Girl[англ.] в телешоу In Living Color[англ.]. Она оставалась постоянной участницей коллектива до 1993 года, когда решила начать полноценную актёрскую карьеру. Свою первую главную роль Лопес получила в биографическом фильме о певице Селене в 1997 году. Эта роль принесла ей номинацию на «Золотой глобус». """,
        'slug': 'slug-lopec',
        'cat_id': 1,
    },
    {
        'title': 'Уинслет, Кейт',
        'content': """Кейт Эли́забет Уи́нслет (англ. Kate Elizabeth Winslet; род. 5 октября 1975, Рединг, Беркшир, Великобритания) — английская актриса[1] театра, кино, телевидения и озвучивания.

Актёрскую карьеру[англ.] Кейт Уинслет начала в 1991 году, дебютировав на британском телевидении. Дебютом в кино для Уинслет стала картина «Небесные создания» (1994), получившая положительные отзывы кинокритиков[2].""",
        'slug': 'slug-yinclet',
        'cat_id': 1,
    },
    {
        'title': 'Блэр Уолдорф',
        'content': """Блэр Корне́лия «Би» Уо́лдорф (англ. Blair Cornelia «B» Waldorf)[1] — главная героиня серии романов «Сплетница», написанных Сесилией фон Цигезар[2]. В телесериале по мотивам серии роль героини исполнила Лейтон Мистер[3].

Жизнь Блэр Уолдорф и других героев находится под постоянным взором таинственного, но известного блогера под ником «Сплетница».""",
        'slug': 'slug-yolderf',
        'cat_id': 1,
    },
    {
        'title': 'Лиза Трусова',
        'content': """крутая девчонка""",
        'slug': 'slug-try',
        'cat_id': 1,
    },

]
from string import ascii_letters, digits

password = 'fgdasfgasdgп'
chrs = f'{ascii_letters}{digits}-?!$#@_'

s = set(password) - set(f'{ascii_letters}{digits}-?!$#@_')
print(s)
if 1 or 2 \
    or 3:
    print(1)

# coding: utf-8
h1 = Husband.objects.create(name="Брэд Питт", age=59)
h2 = Husband.objects.create(name="Том Акерли", age=31)
h3 = Husband.objects.create(name="Дэниэл Модер")
h4 = Husband.objects.create(name="Кук Марони")
w1 = Women.objects.get(pk=2)
w1
w1.husband = h1



