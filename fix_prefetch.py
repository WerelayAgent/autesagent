import os

target_dir = r'C:\Tools\autesagent'
files_changed = 0

fetch_fix_script = """
<script>
// Prevent Remix prefetch crashes
const _originalFetch = window.fetch;
window.fetch = async (...args) => {
    const url = typeof args[0] === 'string' ? args[0] : (args[0] ? args[0].url : '');
    if (url && (url.includes('?_data=') || url.includes('&_data='))) {
        return new Response('{}', { status: 200, headers: { 'Content-Type': 'application/json' } });
    }
    return _originalFetch(...args);
};
</script>
"""

for root, dirs, files in os.walk(target_dir):
    if 'index.html' in files:
        filepath = os.path.join(root, 'index.html')
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'Prevent Remix prefetch crashes' not in content:
            # Inject right after <head>
            content = content.replace('<head>', f'<head>\n{fetch_fix_script}')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Injected fetch interceptor in {filepath}')
            files_changed += 1

print(f'Total files fixed: {files_changed}')
