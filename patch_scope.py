import re

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Expose openModal and loadTasks
if 'window.openModal = openModal;' not in js:
    js = js.replace("window.openSmallModal  = id => openModal(id);", 
                    "window.openSmallModal  = id => openModal(id);\n    window.openModal = openModal;")

# Find where loadTasks is defined and expose it
if 'window.loadTasks = loadTasks;' not in js:
    idx = js.find('async function loadTasks()')
    if idx != -1:
        # Just put it right after the function block or before it. Let's put it globally exposed anywhere.
        js = js.replace('async function loadTasks() {', 'window.loadTasks = loadTasks;\n    async function loadTasks() {')

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Exposed openModal and loadTasks globally")

