"""
Deployment validation tests
These tests verify that critical assets exist before deployment
"""
import os
import pytest


class TestDeploymentValidation:
    """Tests to run before/after deployment"""

    def test_css_output_file_exists(self):
        """Verify that output.css was generated"""
        css_path = os.path.join('app', 'static', 'css', 'output.css')
        assert os.path.exists(css_path), (
            f"CSS output file not found at {css_path}. "
            "Run 'npm run build:css:prod' to generate it."
        )

    def test_css_output_not_empty(self):
        """Verify that output.css has content"""
        css_path = os.path.join('app', 'static', 'css', 'output.css')

        if not os.path.exists(css_path):
            pytest.skip("CSS file doesn't exist, skipping size check")

        file_size = os.path.getsize(css_path)
        assert file_size > 1000, (
            f"CSS file is too small ({file_size} bytes). "
            "Expected at least 1KB. The build may have failed."
        )

    def test_css_contains_tailwind_classes(self):
        """Verify CSS contains expected Tailwind classes"""
        css_path = os.path.join('app', 'static', 'css', 'output.css')

        if not os.path.exists(css_path):
            pytest.skip("CSS file doesn't exist")

        with open(css_path, 'r') as f:
            css_content = f.read()

        # Check for custom colors we defined
        assert 'bg-primary-500' in css_content or '.from-primary-500' in css_content, (
            "CSS doesn't contain expected Tailwind classes. "
            "The build may have used wrong config."
        )

    def test_static_js_exists(self):
        """Verify JavaScript files exist"""
        js_path = os.path.join('app', 'static', 'js', 'mobile-menu.js')
        assert os.path.exists(js_path), f"JavaScript file not found at {js_path}"

    def test_templates_exist(self):
        """Verify critical templates exist"""
        # Shared templates (auth)
        shared_templates = [
            os.path.join('app', 'templates', 'login.html'),
            os.path.join('app', 'templates', 'register.html'),
            os.path.join('app', 'templates', 'base.html'),
        ]

        # V1 templates
        v1_templates = [
            os.path.join('app', 'v1', 'templates', 'v1', 'index.html'),
        ]

        # V2 templates
        v2_templates = [
            os.path.join('app', 'v2', 'templates', 'v2', 'index.html'),
        ]

        all_templates = shared_templates + v1_templates + v2_templates

        for template_path in all_templates:
            assert os.path.exists(template_path), f"Template not found: {template_path}"

    def test_package_json_exists(self):
        """Verify package.json exists for npm install"""
        assert os.path.exists('package.json'), "package.json not found"

    def test_tailwind_config_exists(self):
        """Verify tailwind.config.js exists"""
        assert os.path.exists('tailwind.config.js'), "tailwind.config.js not found"

    def test_requirements_txt_exists(self):
        """Verify requirements.txt exists for pip install"""
        assert os.path.exists('requirements.txt'), "requirements.txt not found"


class TestCSSContent:
    """Tests to verify CSS quality"""

    @pytest.fixture
    def css_content(self):
        """Load CSS content if file exists"""
        css_path = os.path.join('app', 'static', 'css', 'output.css')
        if not os.path.exists(css_path):
            pytest.skip("CSS file doesn't exist")

        with open(css_path, 'r') as f:
            return f.read()

    def test_css_is_minified_in_prod(self, css_content):
        """Production CSS should be minified (no unnecessary whitespace)"""
        # Skip in development - only validate in CI/production
        if os.getenv('CI') != 'true':
            pytest.skip("Minification check only runs in CI/production")

        # Check if this is a production build
        # Minified CSS has very few newlines
        newline_count = css_content.count('\n')
        total_length = len(css_content)

        # If it's very short with few newlines, it's minified
        if total_length > 5000:  # Only check if file is substantial
            newlines_per_kb = (newline_count / total_length) * 1000
            # Minified CSS should have < 5 newlines per KB
            # Non-minified has 20-50 newlines per KB
            assert newlines_per_kb < 10, (
                f"CSS appears to be non-minified ({newlines_per_kb:.1f} newlines/KB). "
                "Use 'npm run build:css:prod' for production."
            )

    def test_css_has_custom_colors(self, css_content):
        """Verify custom color palette is in CSS"""
        # Our custom colors should be in the generated CSS
        custom_indicators = [
            '#6366f1',  # primary-500
            '#f8fafc',  # calm-50
            'bg-calm',
            'bg-primary',
        ]

        found = any(indicator in css_content for indicator in custom_indicators)
        assert found, (
            "CSS doesn't contain custom colors. "
            "tailwind.config.js may not be loaded correctly."
        )
