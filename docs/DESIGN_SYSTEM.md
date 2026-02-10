# Design System & UI Consistency Guide

**Purpose:** Maintain visual and terminology consistency across all versions of the Spanish Vocabulary Learning app.

---

## Core Principles

1. **Single Source of Truth**: V1 design is the baseline. All new versions must match or improve upon it.
2. **Consistency Over Novelty**: Use existing patterns before creating new ones.
3. **Test Before Deploy**: Visual regression tests catch styling drift.

---

## Brand Identity

### App Name
- **Primary**: "Spanish Learner"
- **Usage**: Always use in headers, titles, and user-facing text
- ❌ Don't use: "Spanish Vocabulary", "Spanish Word Learner", "Vocab App"

### Color Palette

#### Primary Colors (Indigo/Purple - Main Actions)
```css
primary-50:  #f0f4ff  /* Lightest backgrounds */
primary-100: #e0e9ff
primary-200: #c7d7fe
primary-300: #a5bbfc
primary-400: #8196f8
primary-500: #6366f1  /* Default buttons */
primary-600: #4f46e5  /* Hover states */
primary-700: #4338ca
primary-800: #3730a3
primary-900: #312e81  /* Darkest text */
```

#### Calm Colors (Neutral - Backgrounds, Text)
```css
calm-50:  #f8fafc  /* Page backgrounds */
calm-100: #f1f5f9  /* Section backgrounds */
calm-200: #e2e8f0  /* Borders */
calm-300: #cbd5e1
calm-400: #94a3b8
calm-500: #64748b
calm-600: #475569  /* Secondary text */
calm-700: #334155
calm-800: #1e293b
calm-900: #0f172a  /* Primary text */
```

#### Semantic Colors
```css
/* Success */
green-50:  #f0fdf4
green-800: #166534

/* Error */
red-50:  #fef2f2
red-800: #991b1b

/* Info (V2 Beta badges) */
blue-100: #dbeafe
blue-800: #1e40af
```

---

## Component Patterns

### 1. Primary Buttons (Call-to-Action)

**Usage:** Main actions like "Generate Sentences", "Try V2 Beta", form submissions

```html
<button class="w-full bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white font-semibold py-2.5 px-4 rounded-lg shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition duration-200">
    Button Text
</button>
```

**Key Features:**
- Gradient: `from-primary-500 to-primary-600`
- Hover elevation: `transform hover:-translate-y-0.5`
- Shadow depth increase on hover
- Font weight: `font-semibold`

### 2. Secondary Buttons (Less Prominent Actions)

**Usage:** "Sign Out", "Cancel", navigation links

```html
<a href="#" class="px-4 py-2 text-sm font-medium text-primary-600 hover:text-primary-700 hover:bg-primary-50 rounded-lg transition duration-200">
    Sign Out
</a>
```

**Key Features:**
- Colored text, no background fill
- Light background on hover: `hover:bg-primary-50`
- Slightly smaller: `text-sm`

### 3. Header/Navigation

**Logo:**
```html
<div class="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg">
    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
    </svg>
</div>
```

**Header Bar:**
```html
<header class="bg-calm-50 border-b border-calm-200 sticky top-0 z-50 shadow-sm">
    <!-- Content -->
</header>
```

### 4. Page Background

**All pages must use:**
```html
<body class="min-h-screen bg-gradient-to-br from-calm-100 via-calm-50 to-primary-50">
```

**Why:** Subtle gradient creates visual interest without distraction

---

## Typography

### Headings
```css
/* Page Title (H1) */
class="text-2xl sm:text-3xl font-bold text-calm-900 mb-2"

/* Section Title (H2) */
class="text-xl font-semibold text-calm-900 mb-3"

/* App Name in Header */
class="text-xl font-bold text-calm-900"
```

### Body Text
```css
/* Primary */
class="text-calm-900"

/* Secondary/Muted */
class="text-calm-600"

/* Small Text */
class="text-sm text-calm-600"
```

---

## Terminology Standards

### User-Facing Labels

| Context | Correct Term | ❌ Avoid |
|---------|-------------|----------|
| Exit account | **Sign Out** | Logout, Log Out |
| Enter account | **Login** | Sign In, Log In |
| App name | **Spanish Learner** | Spanish Vocabulary, Vocab App |
| New version | **V2 Beta** | Version 2, v2, V2.0 |
| Return to old | **Back to V1** | Return to V1, Go to V1 |

---

## Version-Specific UI Elements

### V1 Identifier
- **Location:** Only visible in base.html when NOT on v2
- **Visual**: None (v1 is default, no badge needed)

### V2 Beta Badge
```html
<span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded font-semibold">V2 Beta</span>
```

**Rules:**
- Always appears next to "Spanish Learner" title on V2 pages
- Never appears on V1 pages
- Uses semantic blue (not primary purple)

---

## Responsive Design

### Breakpoints
```css
sm:  640px  /* Small tablets */
md:  768px  /* Tablets and small laptops */
lg:  1024px /* Laptops */
xl:  1280px /* Desktops */
```

### Mobile Menu
- Hidden by default: `hidden md:hidden`
- Toggle with JavaScript: `menu.classList.toggle('hidden')`
- Border top separator: `border-t border-calm-200`

---

## Animation & Transitions

### Standard Duration
```css
transition duration-200  /* Most interactions */
```

### Button Hover Effects
```css
/* Elevation change */
transform hover:-translate-y-0.5

/* Shadow depth */
shadow-md hover:shadow-lg

/* Color shifts */
hover:from-primary-600 hover:to-primary-700
```

---

## Common Mistakes & How to Avoid

### ❌ Problem: Inconsistent button styling
```html
<!-- WRONG -->
<a href="/v2/" class="bg-blue-600 text-white px-3 py-2 rounded">
```

**✅ Solution:** Use primary button pattern
```html
<a href="/v2/" class="bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white font-semibold py-2.5 px-4 rounded-lg shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition duration-200">
```

### ❌ Problem: Wrong app name
```html
<!-- WRONG -->
<h1>Spanish Vocabulary</h1>
<h1>Spanish Word Learner</h1>
```

**✅ Solution:** Use official name
```html
<h1 class="text-xl font-bold text-calm-900">Spanish Learner</h1>
```

### ❌ Problem: Inconsistent auth terminology
```html
<!-- WRONG -->
<a href="/logout">Logout</a>
<a href="/logout">Log Out</a>
```

**✅ Solution:** Use standard term
```html
<a href="/logout">Sign Out</a>
```

### ❌ Problem: Different background colors
```html
<!-- WRONG -->
<body class="bg-gray-50">
<body class="bg-white">
```

**✅ Solution:** Use standard gradient
```html
<body class="min-h-screen bg-gradient-to-br from-calm-100 via-calm-50 to-primary-50">
```

---

## Testing for Consistency

### Pre-Commit Checklist
- [ ] App name is "Spanish Learner" everywhere
- [ ] Buttons use primary gradient (`from-primary-500 to-primary-600`)
- [ ] Auth links say "Sign Out" (not "Logout")
- [ ] Page background uses calm gradient
- [ ] Header has book icon logo
- [ ] Mobile menu works

### Automated Tests
See `/tests/test_phase1_version_management.py`:
- `test_v1_css_loads()` - Verifies CSS includes custom colors
- `test_tailwind_config_includes_all_template_paths()` - Ensures all templates are scanned

### Visual Regression
1. Take screenshot of v1 at `/v1/`
2. Take screenshot of v2 at `/v2/`
3. Compare headers - should be identical except "V2 Beta" badge
4. Compare button styling - should be identical

---

## When Adding New Features

### Before Writing Code:
1. **Check this doc first** - Does a pattern exist for this component?
2. **Copy from v1** - Don't reinvent existing components
3. **Update this doc** - Add new patterns if you create them

### Code Review Questions:
- Does this match existing button styles?
- Is the app name correct?
- Are auth labels consistent ("Sign Out" not "Logout")?
- Does the background use the standard gradient?
- Are colors from the design system palette?

---

## Files to Check

When ensuring consistency, verify these files match the design system:

### Templates
- `app/templates/base.html` - Shared header/footer (V2)
- `app/v1/templates/v1/index.html` - V1 main page
- `app/v2/templates/v2/index.html` - V2 pages
- `app/templates/login.html` - Auth pages
- `app/templates/register.html` - Auth pages

### Styles
- `tailwind.config.js` - Color palette definitions
- `app/static/css/input.css` - Global Tailwind directives

---

## Quick Reference Card

**Copy-paste these when building UI:**

```html
<!-- Primary Button -->
<button class="w-full bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white font-semibold py-2.5 px-4 rounded-lg shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition duration-200">

<!-- Secondary Button -->
<a class="px-4 py-2 text-sm font-medium text-primary-600 hover:text-primary-700 hover:bg-primary-50 rounded-lg transition duration-200">

<!-- Page Background -->
<body class="min-h-screen bg-gradient-to-br from-calm-100 via-calm-50 to-primary-50">

<!-- Section Card -->
<div class="bg-white rounded-xl shadow-sm border border-calm-200 p-6">

<!-- App Name -->
Spanish Learner

<!-- Auth Label -->
Sign Out
```

---

**Last Updated:** 2026-02-10 (Phase 1 implementation)
**Owner:** Development Team
**Review Schedule:** After each new version or major UI change
