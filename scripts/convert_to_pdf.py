#!/usr/bin/env python3
"""
Convert markdown and text files to PDF format.
Uses reportlab for PDF generation.
"""

import os
import re
import sys
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def clean_text(text):
    """Clean text for PDF output, replacing special characters."""
    replacements = {
        '"': '"',
        '"': '"',
        ''': "'",
        ''': "'",
        '—': '-',
        '–': '-',
        '…': '...',
        '•': '*',
        '→': '->',
        '←': '<-',
        '↔': '<->',
        '✓': '[x]',
        '✗': '[ ]',
        '✅': '[x]',
        '❌': '[ ]',
        '📋': '[DOC]',
        '🏗': '[BUILD]',
        '📚': '[BOOK]',
        '🚀': '[ROCKET]',
        '📖': '[BOOK]',
        '🔧': '[TOOL]',
        '⚙': '[GEAR]',
        '📤': '[EXPORT]',
        '🎯': '[TARGET]',
        '🤖': '[BOT]',
        '🗄': '[DB]',
        '🧪': '[TEST]',
        '📝': '[NOTE]',
        '🙏': '',
        '╔': '+',
        '╗': '+',
        '╚': '+',
        '╝': '+',
        '═': '=',
        '║': '|',
        '├': '+',
        '└': '+',
        '┌': '+',
        '┐': '+',
        '│': '|',
        '─': '-',
        '┘': '+',
        '┴': '+',
        '┬': '+',
        '┼': '+',
        'ΒΊΒΛΟΣ ΛΌΓΟΥ': 'BIBLOS LOGOU',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # Handle Greek characters
    greek_map = {
        'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta',
        'ε': 'epsilon', 'ζ': 'zeta', 'η': 'eta', 'θ': 'theta',
        'ι': 'iota', 'κ': 'kappa', 'λ': 'lambda', 'μ': 'mu',
        'ν': 'nu', 'ξ': 'xi', 'ο': 'omicron', 'π': 'pi',
        'ρ': 'rho', 'σ': 'sigma', 'τ': 'tau', 'υ': 'upsilon',
        'φ': 'phi', 'χ': 'chi', 'ψ': 'psi', 'ω': 'omega',
    }
    for greek, latin in greek_map.items():
        text = text.replace(greek, latin)
        text = text.replace(greek.upper(), latin.upper())

    return text


def markdown_to_paragraphs(md_content):
    """Convert markdown content to list of paragraph data."""
    lines = md_content.split('\n')
    paragraphs = []
    current_para = []
    in_code_block = False
    in_table = False
    table_rows = []

    for line in lines:
        # Handle code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            if in_code_block and current_para:
                paragraphs.append(('text', ' '.join(current_para)))
                current_para = []
            continue

        if in_code_block:
            paragraphs.append(('code', line))
            continue

        # Handle tables
        if '|' in line and not line.strip().startswith('#'):
            if not in_table:
                if current_para:
                    paragraphs.append(('text', ' '.join(current_para)))
                    current_para = []
                in_table = True
                table_rows = []

            # Skip separator lines
            if re.match(r'^[\s|:-]+$', line):
                continue

            cells = [c.strip() for c in line.split('|')]
            cells = [c for c in cells if c]  # Remove empty cells
            if cells:
                table_rows.append(cells)
            continue
        elif in_table:
            if table_rows:
                paragraphs.append(('table', table_rows))
            in_table = False
            table_rows = []

        # Handle headers
        if line.startswith('#'):
            if current_para:
                paragraphs.append(('text', ' '.join(current_para)))
                current_para = []

            level = len(re.match(r'^#+', line).group())
            text = line.lstrip('#').strip()
            paragraphs.append((f'h{level}', text))
            continue

        # Handle horizontal rules
        if re.match(r'^[-=*]{3,}$', line.strip()):
            if current_para:
                paragraphs.append(('text', ' '.join(current_para)))
                current_para = []
            paragraphs.append(('hr', ''))
            continue

        # Handle list items
        if re.match(r'^\s*[-*+]\s', line) or re.match(r'^\s*\d+\.\s', line):
            if current_para:
                paragraphs.append(('text', ' '.join(current_para)))
                current_para = []
            # Remove list marker
            text = re.sub(r'^\s*[-*+\d.]+\s*', '* ', line)
            paragraphs.append(('list', text))
            continue

        # Handle empty lines
        if not line.strip():
            if current_para:
                paragraphs.append(('text', ' '.join(current_para)))
                current_para = []
            continue

        # Regular text
        current_para.append(line.strip())

    # Don't forget last paragraph
    if current_para:
        paragraphs.append(('text', ' '.join(current_para)))
    if in_table and table_rows:
        paragraphs.append(('table', table_rows))

    return paragraphs


def create_pdf(input_path, output_path):
    """Create PDF from markdown or text file."""
    print(f"Converting: {input_path}")

    # Read input file
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean content
    content = clean_text(content)

    # Get title from filename
    title = Path(input_path).stem

    # Create PDF document
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Get styles
    styles = getSampleStyleSheet()

    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=18,
        spaceAfter=20,
    )

    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=16,
        spaceBefore=15,
        spaceAfter=10,
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8,
    )

    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontSize=12,
        spaceBefore=10,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        spaceBefore=4,
        spaceAfter=4,
        leading=14,
    )

    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontSize=8,
        fontName='Courier',
        spaceBefore=2,
        spaceAfter=2,
        leftIndent=20,
    )

    list_style = ParagraphStyle(
        'CustomList',
        parent=styles['Normal'],
        fontSize=10,
        spaceBefore=2,
        spaceAfter=2,
        leftIndent=20,
    )

    # Parse content
    paragraphs = markdown_to_paragraphs(content)

    # Build story
    story = []

    # Add title
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 20))

    for para_type, para_content in paragraphs:
        try:
            if para_type == 'h1':
                story.append(Paragraph(para_content, h1_style))
            elif para_type == 'h2':
                story.append(Paragraph(para_content, h2_style))
            elif para_type in ('h3', 'h4', 'h5', 'h6'):
                story.append(Paragraph(para_content, h3_style))
            elif para_type == 'code':
                # Escape special characters for reportlab
                safe_content = para_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                story.append(Paragraph(safe_content, code_style))
            elif para_type == 'list':
                story.append(Paragraph(para_content, list_style))
            elif para_type == 'hr':
                story.append(Spacer(1, 10))
                story.append(Paragraph('-' * 60, body_style))
                story.append(Spacer(1, 10))
            elif para_type == 'table':
                # Create table
                table_data = para_content
                if table_data:
                    # Limit cell content length
                    for i, row in enumerate(table_data):
                        table_data[i] = [str(cell)[:50] for cell in row]

                    t = Table(table_data)
                    t.setStyle(TableStyle([
                        ('FONTSIZE', (0, 0), (-1, -1), 8),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ]))
                    story.append(t)
                    story.append(Spacer(1, 10))
            elif para_type == 'text' and para_content.strip():
                # Escape special characters
                safe_content = para_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                story.append(Paragraph(safe_content, body_style))
        except Exception as e:
            # If a paragraph fails, add it as plain text
            print(f"  Warning: Could not format paragraph: {str(e)[:50]}")
            try:
                safe = str(para_content)[:200].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                story.append(Paragraph(safe, body_style))
            except:
                pass

    # Build PDF
    doc.build(story)
    print(f"  Created: {output_path}")
    return True


def main():
    """Convert all relevant files to PDF."""

    # Create output directory
    pdf_dir = PROJECT_ROOT / 'pdf'
    pdf_dir.mkdir(exist_ok=True)

    # Files to convert
    files_to_convert = [
        # Main documentation
        PROJECT_ROOT / 'README.md',
        PROJECT_ROOT / 'MASTER_PLAN.md',
        PROJECT_ROOT / 'BIBLOS_LOGOU_EXPANDED_METHODOLOGY.md',
        PROJECT_ROOT / 'REFINED MASTER OUTLINE.md',

        # Docs folder
        PROJECT_ROOT / 'docs' / 'PROJECT_VISION.md',
        PROJECT_ROOT / 'docs' / 'PRODUCTION_METHOD.md',
        PROJECT_ROOT / 'docs' / 'MANDATES.md',
        PROJECT_ROOT / 'docs' / 'TANGIBLE_FACETS.md',
        PROJECT_ROOT / 'docs' / 'ABSTRACT_FACETS.md',
        PROJECT_ROOT / 'docs' / 'IMPLEMENTATION_GUIDE.md',
        PROJECT_ROOT / 'docs' / 'WORKFLOW_GUIDE.md',

        # Text files
        PROJECT_ROOT / 'Stratified.txt',
        PROJECT_ROOT / 'Hermeneutical.txt',
        PROJECT_ROOT / 'Biblical_Events_Complete_Orthodox_Canon.txt',
    ]

    converted = 0
    failed = 0

    for input_file in files_to_convert:
        if not input_file.exists():
            print(f"Skipping (not found): {input_file}")
            continue

        # Create output path
        output_name = input_file.stem + '.pdf'
        output_path = pdf_dir / output_name

        try:
            create_pdf(input_file, output_path)
            converted += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1

    print(f"\n{'=' * 50}")
    print(f"Conversion complete: {converted} succeeded, {failed} failed")
    print(f"PDFs saved to: {pdf_dir}")

    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
