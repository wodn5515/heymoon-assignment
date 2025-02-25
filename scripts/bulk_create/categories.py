from apps.products.models import Category

categories = [
    {
        "name": "패션",
        "subcategories": [
            {"name": "여성의류"},
            {"name": "남성의류"},
            {"name": "신발"},
            {"name": "가방"},
            {"name": "액세서리"},
        ],
    },
    {
        "name": "뷰티",
        "subcategories": [
            {"name": "스킨케어"},
            {"name": "메이크업"},
            {"name": "향수"},
            {"name": "헤어케어"},
            {"name": "바디케어"},
        ],
    },
    {
        "name": "가전/디지털",
        "subcategories": [
            {"name": "모바일"},
            {"name": "가전제품"},
            {"name": "컴퓨터"},
            {"name": "카메라"},
            {"name": "음향기기"},
        ],
    },
    {
        "name": "홈/리빙",
        "subcategories": [
            {"name": "가구"},
            {"name": "침구"},
            {"name": "인테리어"},
            {"name": "주방용품"},
            {"name": "생활용품"},
        ],
    },
    {
        "name": "식품",
        "subcategories": [
            {"name": "신선식품"},
            {"name": "가공식품"},
            {"name": "건강식품"},
            {"name": "음료"},
            {"name": "간식"},
        ],
    },
]


def create_categories():
    """카테고리 더미 데이터 생성"""
    print("=== 카테고리 더미 데이터 생성 시작 ===")
    category_list = []
    for category in categories:
        category_list.append(Category(name=category["name"]))
    Category.objects.bulk_create(category_list)
    category_list = []
    for category in categories:
        parent_category = Category.objects.get(name=category["name"])
        for sub_category in category["subcategories"]:
            category_list.append(
                Category(name=sub_category["name"], parent=parent_category)
            )
    Category.objects.bulk_create(category_list)
    print("=== 카테고리 더미 데이터 생성 완료 ===")
