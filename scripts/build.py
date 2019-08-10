from pathlib import Path
from subprocess import run, PIPE


PROJECT_DIR = Path(__file__).parent.parent
BUILD_DIR = PROJECT_DIR / 'build'
PAGES_DIR = PROJECT_DIR / 'juniorguru' / 'pages'


print('Resetting the build directory')
run(['rm', '-r', BUILD_DIR], check=True)
run(['git', 'checkout', BUILD_DIR], check=True)

print('Building HTML')
pages = (
    item.name for item in PAGES_DIR.iterdir()
    if not item.name.startswith('_')
)
for page in pages:
    run(['python', '-m', f'juniorguru.pages.{page}'], check=True)

print('Building JS')
run(['npx', 'rollup', '--config'], check=True)

print('Minifying HTML')
html_minifier = ['npx', 'html-minifier', '--minify-css=true', '--minify-js=true',
                '--remove-comments', '--remove-attribute-quotes',
                '--remove-empty-attributes', '--remove-optional-tags',
                '--remove-redundant-attributes', '--use-short-doctype',
                '--collapse-whitespace', '--collapse-boolean-attributes',
                '--case-sensitive']
for html_path in BUILD_DIR.glob('**/*.html'):
    proc = run(html_minifier + [str(html_path)], check=True, stdout=PIPE)
    html_path.write_text(proc.stdout.decode('utf-8'))

print('Minifying JS')
for js_path in BUILD_DIR.glob('**/*.js'):
    proc = run(['npx', 'terser', str(js_path), '-c', '-m'], check=True, stdout=PIPE)
    js_path.write_text(proc.stdout.decode('utf-8'))

print('Minifying CSS')
for css_path in BUILD_DIR.glob('**/*.css'):
    proc = run(['npx', 'csso', str(css_path)], check=True, stdout=PIPE)
    css_path.write_text(proc.stdout.decode('utf-8'))

print('Minifying images')
for image in ['png', 'jpg', 'gif']:
    for image_path in BUILD_DIR.glob(f'**/*.{image}'):
        proc = run(['npx', 'imagemin', str(image_path)], check=True, stdout=PIPE)
        image_path.write_bytes(proc.stdout)
