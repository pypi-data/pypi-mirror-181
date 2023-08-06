# coding: utf8
import fpdf
import io
import os
from decimal import Decimal
from utils.templates import ColorSchema
from utils.fonts import fonts
from conf import settings


class TransPDF(fpdf.FPDF):
    def __init__(
            self,
            orientation='P',
            unit='mm',
            paper_format='A4',
            decimal_count=settings.API_ROUND_DECIMAL_FIELDS,
            title='',
            logo='',
            image_path='',
            sub_title='',
            empty=False,
            decimal_align='R',
            decimal_format='{:,.(decimal_count)f}'
    ):
        super().__init__(orientation, unit, paper_format)

        # There are widths of each character for some specific fonts (core fonts) in fPDF library.
        # And that library enforces text to encode into LATIN-1, which triggers error when there are Unicode chars.
        # After deleting helvetica core font, it accepts each char in the string has the width 500 (whatever unit).
        if 'helvetica' in self.core_fonts:
            del self.core_fonts['helvetica']

        self.font_cache_dir = settings.FONT_CACHE_DIR

        self.image_path = image_path
        self.logo = logo

        self.color = ColorSchema()

        self.decimal_count = decimal_count
        self.decimal_align = decimal_align
        self.decimal_format = decimal_format.replace('(decimal_count)', str(self.decimal_count))

        self.add_fonts()

        self.add_page()

        if not empty:
            self.add_header(title, sub_title)

        self.set_default_font()
        self.set_y(self.pixel(40))

    def add_fonts(self):
        if not os.path.exists(settings.FONT_CACHE_DIR):
            os.mkdir(settings.FONT_CACHE_DIR)

        for font in fonts[self.color.font]:
            current_font = fonts[self.color.font][font]
            self.add_font(
                current_font.get('name'),
                '',
                current_font.get('ttf'),
                uni=True
            )

    @staticmethod
    def pixel(pixel_value):
        """
            Converts pixels into mm
        """

        return pixel_value / 2.83

    def set_template(self, schema):
        self.color.schema = schema

    def add_paragraph(self, text, width=538, set_auto_font=True):
        if set_auto_font:
            self.set_default_font()

        self.multi_cell(self.pixel(width), self.font_size * 1.1, str(text), align="LEFT")

    def add_text(self, x, y, text):
        self.text(self.pixel(x), self.pixel(y), str(text))

    def add_multiline_text(self, x, y, width, texts, justify="J"):
        content = ''

        self.set_xy(self.pixel(x), self.pixel(y))
        self.set_text_html_color('#323232')

        for text in texts:
            text = text.replace('\n', '').strip()

            while '  ' in text:
                text = text.replace('  ', ' ')

            content += f'{text}\n'

        self.multi_cell(self.pixel(width), self.font_size * 1.1, content, align=justify)

    def set_header_font(self):
        self.set_default_font('bold', self.color.header_font_size, self.color.header)

    def add_header(self, title, sub_title):
        self.set_header_font()
        self.cell(self.pixel(40), self.pixel(self.font_size * 2), txt=str(title), ln=1, align='L')
        self.cell(self.pixel(40), self.pixel(self.font_size), txt=str(sub_title), ln=1, align='L')
        self.put_image(self.logo, x=150, y=8, w=50)

    def set_default_font(self, font_weight='regular', font_size=None, color=None):
        if font_size is None:
            font_size = self.color.font_size

        if font_weight == 'medium':
            font = self.color.medium_font
        elif font_weight == 'bold':
            font = self.color.bold_font
        else:
            font = self.color.font

        if color is not None:
            self.set_text_html_color(color)

        self.set_font(font, '', font_size)

    def add_line(self, x1, y1, x2, y2):
        self.line(self.pixel(x1), self.pixel(y1), self.pixel(x2), self.pixel(y2))

    @staticmethod
    def html_color_converter(html_color_code):
        if html_color_code is None:
            return None
        if html_color_code.startswith('#'):
            html_color_code = html_color_code[1:]

        return int(html_color_code[0:2], 16), \
            int(html_color_code[2:4], 16), \
            int(html_color_code[4:6], 16),

    def add_title(self, title, font_size=14, padding_bottom=2):
        y = self.get_y()

        self.set_y(y)

        self.set_default_font('bold', font_size, self.color.header)

        self.cell(
            self.pixel(220),
            self.pixel(10),
            txt=str(title),
            ln=1,
            align='L'
        )

        row_height = self.font_size
        self.set_default_font()

        self.set_y(y + padding_bottom * row_height)

    def set_text_html_color(self, color_code):
        self.set_text_color(*self.html_color_converter(color_code))

    def set_fill_html_color(self, color_code):
        self.set_fill_color(*self.html_color_converter(color_code))

    def set_draw_html_color(self, color_code):
        self.set_draw_color(*self.html_color_converter(color_code))

    def add_vertical_space(self, space):
        x = self.get_x()
        y = self.get_y()

        self.set_xy(x, y + self.pixel(space))

    def set_table_header(self, data, spacing, border, widths):
        self.set_fill_html_color(self.color.table_header_background_color)
        self.set_draw_html_color(self.color.table_header_border_color)

        x = self.get_x()

        self.set_default_font('bold', None, self.color.table_header_text)

        for index, header in enumerate(data.get('header', [])):
            y_before = self.get_y()

            self.multi_cell(
                int(widths[index]),
                4,
                txt=header.get('title', ''),
                border=border,
                fill=True,
                align=self.color.table_header_align,
            )

            x += widths[index]

            self.set_xy(x, y_before)

        self.set_default_font('regular')

        self.ln(self.font_size * spacing)

    def set_table_data(self, data, spacing, border, widths):
        self.set_text_html_color(self.color.table_row_text)
        self.set_fill_html_color(self.color.table_row_background)

        self.set_draw_html_color(self.color.table_row_border)

        fill_color = self.color.table_row_background

        for row in data.get('data', ()):
            if fill_color == self.color.table_row_background:
                fill_color = self.color.table_row_background_odd
            else:
                fill_color = self.color.table_row_background

            self.set_fill_html_color(fill_color)

            for index, column in enumerate(row):
                self.add_table_row(widths, index, column, spacing, border)

            self.ln(self.font_size * spacing)

    def set_table_footer(self, data, spacing, border, widths):
        self.set_fill_html_color(self.color.table_footer_background_color)
        self.set_draw_html_color(self.color.table_footer_border_color)

        self.set_default_font('bold', self.color.font_size, self.color.table_footer_text_color)

        for index, column in enumerate(data.get('footer', ())):
            self.add_table_row(widths, index, column, spacing, border)

        self.ln(self.font_size * spacing)

    @staticmethod
    def format_number(number, precision=2):
        # build format string
        format_str = '{{:,.{}f}}'.format(precision)

        # make number string
        number_str = format_str.format(number)

        # replace chars
        return number_str.replace(',', ' ')

    def add_table_row(self, widths, index, column, spacing, border):
        if index == 0 and self.color.table_first_row_is_bold:
            self.set_default_font('bold')
        else:
            self.set_default_font('regular')

        if type(column) in (float, Decimal, int):
            align = self.decimal_align

            if type(column) == int:
                column = self.format_number(column, 0)
            else:
                column = self.format_number(column)
        else:
            align = 'L'

        self.cell(
            widths[index],
            self.font_size * spacing,
            txt=str(column),
            border=border,
            fill=True,
            align=align,
        )

    def create_table(self, data, spacing=3, border=1):
        sum_of_widths = sum(item['width'] for item in data.get('header', []))

        rate_width = 190 / sum_of_widths

        widths = [float(i.get('width') * rate_width) for i in data.get('header', {})]

        self.set_default_font()
        self.set_table_header(data, spacing, border, widths)
        self.set_table_data(data, spacing, border, widths)
        self.set_table_footer(data, spacing, border, widths)

    def raw(self):
        return io.BytesIO(self.output())

    def put_image(self, image_file, x, y, w):
        try:
            self.image(f'{self.image_path}/{image_file}', self.pixel(x), self.pixel(y), self.pixel(w))
        except FileNotFoundError:
            print(f'File not found: {self.image_path}/{image_file}')

        return True
