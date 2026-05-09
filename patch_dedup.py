"""
Remove the second stale chatWidget block added near end of file.
"""
import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find both floatingChatBtn positions
positions = [m.start() for m in re.finditer(r'id="floatingChatBtn"', content)]
print(f"floatingChatBtn at: {positions}")

if len(positions) == 2:
    # The second one is the stale widget near end - remove it and its associated chatWidget div
    second_pos = positions[1]
    # Go back to find the opening <button or <div before it
    chunk_start = content.rfind('\n    <', 0, second_pos)
    # Find end: next <script or </body
    chunk_end = content.find('<script src="app.js">', second_pos)
    if chunk_end == -1:
        chunk_end = content.find('</body>', second_pos)
    
    stale_block = content[chunk_start:chunk_end]
    print(f"Stale block to remove ({len(stale_block)} chars):")
    print(repr(stale_block[:200]))
    
    content = content[:chunk_start] + '\n\n    ' + content[chunk_end:]
    
    with open('frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Verify
    positions2 = [m.start() for m in re.finditer(r'id="floatingChatBtn"', content)]
    print(f"After fix - floatingChatBtn occurrences: {len(positions2)}")
    print("DONE!")
else:
    print(f"Expected 2, got {len(positions)} - no action needed")
