from pdf import TransPDF


def print_hi():
    pdf = TransPDF(
        logo="logo-transporeon.png",
        image_path='https://truck-static.s3.eu-central-1.amazonaws.com/static/pdf'
    )

    pdf.set_default_font('bold', 14, '#001A26')
    pdf.add_text(28, 270.92, 'Coverage of this report')

    pdf.set_default_font('regular', 12, '#323232')
    file = open("test.pdf", "wb")
    file.write(pdf.raw().read())
    file.close()
    print(pdf)


if __name__ == '__main__':
    print_hi()

