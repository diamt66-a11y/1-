import json
import re

with open('posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

# category mapping
cat_map = {
    '일상': '기타 가이드',
    '기획': '비즈니스 전략',
    '일반': '기타 가이드',
    '비즈니스': '비즈니스 전략',
    'IT_자동화': 'IT 자동화 기획',
    '디지털_수익화': '디지털 수익화',
    '비즈니스_전략': '비즈니스 전략',
    '일반_메모': '기타 가이드'
}

for p in posts:
    old_cat = p.get('category', '비즈니스 전략')
    p['category'] = cat_map.get(old_cat, '비즈니스 전략')
    
    # Stoic post cleanup
    if '스토아' in p.get('title', '') or '스토아' in p.get('content', ''):
        content = p.get('content', '')
        # Remove [노코드], [로우코드], 활용 툴, 예상 비용
        content = re.sub(r'\[노코드\]|\[로우코드\]', '', content)
        content = re.sub(r'<p>.*?(활용 툴|무료 제공|비용).*?</p>', '', content)
        content = re.sub(r'<li>.*?(활용 툴|무료 제공|비용).*?</li>', '', content)
        p['content'] = content

with open('posts.json', 'w', encoding='utf-8') as f:
    json.dump(posts, f, ensure_ascii=False, indent=4)
print("posts.json cleaned successfully.")
