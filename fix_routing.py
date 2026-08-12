import os

target_dir = r'C:\Tools\autesagent'
files_changed = 0

routing_fix_script = """
<script>
// Fix for statically scraped Remix/React Router SPA
document.addEventListener('click', function(e) {
    const a = e.target.closest('a');
    if (a && a.href && a.href.startsWith(window.location.origin) && !a.hasAttribute('target')) {
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        window.location.href = a.href;
    }
}, true);
</script>
"""

for root, dirs, files in os.walk(target_dir):
    if 'index.html' in files:
        filepath = os.path.join(root, 'index.html')
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'Fix for statically scraped Remix/React Router SPA' not in content:
            # Inject right after <head>
            content = content.replace('<head>', f'<head>\n{routing_fix_script}')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Fixed routing in {filepath}')
            files_changed += 1

print(f'Total files fixed: {files_changed}')
