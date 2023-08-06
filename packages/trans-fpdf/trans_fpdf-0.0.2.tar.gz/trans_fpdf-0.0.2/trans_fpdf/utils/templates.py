class ColorSchema:
    def __init__(self):
        self.schemas = {
            'default': dict(
                table_first_row_is_bold=False,
                table_header_align='L',
                table_header_text='#ffffff',
                table_header_background_color='#657177',
                table_header_border_color='#657177',

                table_row_text='#657177',
                table_row_background='#ffffff',
                table_row_background_odd='#ebf7ff',
                table_row_border='#ffffff',

                table_footer_text_color='#657177',
                table_footer_background_color='#ffffff',
                table_footer_border_color='#ffffff',

                table_decimal_align='R',

                default='#323232',
                font_size=8,

                header_font_size=16,
                sub_header_font_size=12,
                header='#001A26',

            ),
            'overview': dict(
                table_first_row_is_bold=True,
                table_header_align='C',
                table_header_text='#D8E4EC',
                table_header_background_color='#008D89',
                table_header_border_color='#008D89',

                table_row_text='#000000',
                table_row_background='#FFFFFF',
                table_row_background_odd='#E5F8F6',
                table_row_border='#FFFFFF',

                table_footer_text_color='#000000',
                table_footer_background_color='#E5F8F6',
                table_footer_border_color='#E5F8F6',

                table_decimal_align='C',

                default='#008D89',
                font_size=8,

                header_font_size=16,
                sub_header_font_size=12,
                header='#001A26'
            ),
        }

    schema = 'default'

    @property
    def font(self):
        return 'helvetica'

    @property
    def medium_font(self):
        return 'helveticaM'

    @property
    def bold_font(self):
        return 'helveticaB'

    @property
    def font_size(self):
        return self.schemas[self.schema]['font_size']

    @property
    def header_font_size(self):
        return self.schemas[self.schema]['header_font_size']

    @property
    def sub_header_font_size(self):
        return self.schemas[self.schema]['sub_header_font_size']

    @property
    def default(self):
        return self.schemas[self.schema]['default']

    @property
    def header(self):
        return self.schemas[self.schema]['header']

    @property
    def table_first_row_is_bold(self):
        return self.schemas[self.schema]['table_first_row_is_bold']

    @property
    def table_header_align(self):
        return self.schemas[self.schema]['table_header_align']

    @property
    def table_decimal_align(self):
        return self.schemas[self.schema]['table_decimal_align']

    @property
    def table_header_text(self):
        return self.schemas[self.schema]['table_header_text']

    @property
    def table_header_background_color(self):
        return self.schemas[self.schema]['table_header_background_color']

    @property
    def table_header_border_color(self):
        return self.schemas[self.schema]['table_header_border_color']

    @property
    def table_row_text(self):
        return self.schemas[self.schema]['table_row_text']

    @property
    def table_row_background(self):
        return self.schemas[self.schema]['table_row_background']

    @property
    def table_row_background_odd(self):
        return self.schemas[self.schema]['table_row_background_odd']

    @property
    def table_row_border(self):
        return self.schemas[self.schema]['table_row_border']

    @property
    def table_footer_text_color(self):
        return self.schemas[self.schema]['table_footer_text_color']

    @property
    def table_footer_background_color(self):
        return self.schemas[self.schema]['table_footer_background_color']

    @property
    def table_footer_border_color(self):
        return self.schemas[self.schema]['table_footer_border_color']
