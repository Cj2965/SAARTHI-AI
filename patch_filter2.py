import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's remove the whole block.
# We know it starts with <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; flex-wrap: wrap;">
# or similar. Let's just find the exact block and replace it using a regex that looks for schemeSearch and filterSector.

pattern = r'<div style="[^"]*">\s*<input type="text" id="schemeSearch"[^>]*>\s*<select id="filterSector"[^>]*>.*?</select>\s*<select id="sortSchemes"[^>]*>.*?</select>\s*</div>'

text = re.sub(pattern, '', text, flags=re.DOTALL)

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Filter bar removed via regex')
