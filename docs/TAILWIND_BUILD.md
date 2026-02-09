# Tailwind CSS Build Process

This project uses Tailwind CSS v3 with a proper build process instead of the CDN.

## Quick Reference

### Development Commands

```bash
# Build CSS once (for development)
npm run build:css

# Watch for changes and rebuild automatically (recommended during development)
npm run watch:css

# Build minified CSS for production
npm run build:css:prod
```

## Setup (Already Done)

The Tailwind setup includes:

1. **Configuration File**: `tailwind.config.js`
   - Custom color palette (primary & calm colors)
   - Scans all HTML templates and JS files

2. **Input CSS**: `app/static/css/input.css`
   - Tailwind directives (@tailwind base, components, utilities)
   - Custom styles (highlight colors, focus states)

3. **Output CSS**: `app/static/css/output.css`
   - Generated file (don't edit manually)
   - In `.gitignore` (regenerated on each build)

## Development Workflow

### Option 1: Manual Build (Simple)
```bash
# After changing templates or adding new Tailwind classes:
npm run build:css
```

### Option 2: Watch Mode (Recommended)
```bash
# In a separate terminal, run:
npm run watch:css

# This automatically rebuilds CSS when you save template files
# Leave it running while you develop
```

### Option 3: One-Time Production Build
```bash
# Before deploying:
npm run build:css:prod
```

## How It Works

1. You write Tailwind classes in HTML templates (e.g., `class="bg-primary-500"`)
2. Tailwind scans all files in `app/templates/**/*.html`
3. It generates CSS **only for classes you actually use** (tree-shaking)
4. Output goes to `app/static/css/output.css`
5. Templates load: `<link rel="stylesheet" href="{{ url_for('static', filename='css/output.css') }}">`

## File Sizes

- **Development build**: ~25KB (readable, includes source maps)
- **Production build**: ~17KB (minified, optimized)
- **CDN (old method)**: 300KB+ (includes everything)

## Adding Custom Styles

### Method 1: Tailwind Config (Preferred)
Edit `tailwind.config.js` to add colors, spacing, etc:

```js
theme: {
  extend: {
    colors: {
      mycolor: '#abcdef',
    }
  }
}
```

### Method 2: Input CSS File
Add custom CSS to `app/static/css/input.css`:

```css
.my-custom-class {
  /* your styles */
}
```

## Deployment Considerations

### For EC2 Deployment:

1. **Install Node.js on EC2**:
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

2. **Update Deploy Script** (`.github/workflows/ci-cd.yml`):
   ```yaml
   - name: Build CSS
     run: |
       npm install
       npm run build:css:prod
   ```

3. **Or Build Locally Before Push**:
   ```bash
   npm run build:css:prod
   git add app/static/css/output.css
   git commit -m "Build production CSS"
   ```

   Then remove `app/static/css/output.css` from `.gitignore`

## Troubleshooting

### Classes not applying?
```bash
# Rebuild CSS
npm run build:css
# Refresh browser (Cmd+Shift+R / Ctrl+Shift+R)
```

### "Module not found" error?
```bash
# Reinstall dependencies
npm install
```

### CSS file too large?
```bash
# Make sure you're using the production build
npm run build:css:prod
```

### Changes not reflecting?
- Make sure Flask server restarted after CSS rebuild
- Hard refresh browser (clear cache)
- Check browser console for 404 errors

## Why This Is Better Than CDN

✅ **Smaller File Size**: Only includes CSS you actually use (17KB vs 300KB)
✅ **Faster Load Times**: Less data to download
✅ **Offline Development**: No internet required
✅ **Custom Configuration**: Your own color palette
✅ **Production Ready**: Proper build process
✅ **Version Control**: Lock exact Tailwind version

## Learning Resources

- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Customizing Colors](https://tailwindcss.com/docs/customizing-colors)
- [Configuration Guide](https://tailwindcss.com/docs/configuration)
