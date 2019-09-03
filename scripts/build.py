import sys
import shutil
from pathlib import Path
from subprocess import run, PIPE


PROJECT_DIR = Path(__file__).parent.parent
PAGES_DIR = PROJECT_DIR / 'juniorguru' / 'pages'
BUILD_DIR = PROJECT_DIR / 'build'


ALL_TARGETS = {'html', 'css', 'js'}
targets = frozenset(sys.argv[1:]) or ALL_TARGETS


if targets == ALL_TARGETS:
    print('Resetting the build directory')
    items = (
        shutil.rmtree(str(item)) for item in BUILD_DIR.iterdir()
        if item.name != 'now.json'
    )
    run(['git', 'checkout', BUILD_DIR], check=True)

if 'html' in targets:
    print('Building HTML')
    pages = (
        item.name for item in PAGES_DIR.iterdir()
        if not item.name.startswith('_')
    )
    for page in pages:
        run(['python', '-m', f'juniorguru.pages.{page}'], check=True)

if 'js' in targets:
    print('Building JS')
    run(['npx', 'rollup', '--config'], check=True)

if 'css' in targets:
    print('Building CSS')
    scss_path = str(PROJECT_DIR / 'juniorguru/css/main.scss')
    run(['npx', 'node-sass', scss_path, str(BUILD_DIR / 'bundle.css')], check=True)

print('Copying images')
images_dir = BUILD_DIR / 'images'
favicon_path = BUILD_DIR / 'favicon.ico'
shutil.rmtree(images_dir, ignore_errors=True)
shutil.rmtree(favicon_path, ignore_errors=True)
shutil.copytree(PROJECT_DIR / 'juniorguru/images', images_dir)
shutil.move(str(images_dir / 'favicon.ico'), favicon_path)

if targets == ALL_TARGETS:
    print('Minifying HTML')
    html_minifier = ['npx', 'html-minifier', '--minify-css=true',
                    '--minify-js=true', '--remove-comments',
                    '--remove-attribute-quotes', '--remove-empty-attributes',
                    '--remove-optional-tags', '--remove-redundant-attributes',
                    '--use-short-doctype', '--collapse-whitespace',
                    '--collapse-boolean-attributes', '--case-sensitive']
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

    for image_path in BUILD_DIR.glob(f'**/*.svg'):
        run(['npx', 'svgo', str(image_path)], check=True)
