def subprocess_run(args : list) -> bool:
    import subprocess
    success_flag = subprocess.run(args).returncode

    if success_flag == 0:    # ? A negative value -N indicates that the child was terminated by signal N. Aka, unsuccessful, https://docs.python.org/3/library/subprocess.html
        return True
    else: return False





# ? docx / doc to pdf
def docx2pdfConvert(doc_file_path, output_pdf_folder_path):
    ''' HOW TO USE :-
    docx = docx2pdfConvert(f'{os.getcwd()}/file name.docx', f'{os.getcwd()}/output_dir/')
    doc = docx2pdfConvert(f'{os.getcwd()}/file name.doc', f'{os.getcwd()}/output_dir/')
    '''

    success_status = False
    args = ['libreoffice', '--headless', '--convert-to', 'pdf', doc_file_path, '--outdir', output_pdf_folder_path]
    try:
        success_status = subprocess_run(args)
    except:
        try:
            args = ['/usr/bin/flatpak', 'run', 'org.libreoffice.LibreOffice', '--headless', '--convert-to', 'pdf', doc_file_path, '--outdir', output_pdf_folder_path]
            success_status = subprocess_run(args)
        except:
            try:
                args = ['/snap/bin/libreoffice', '--headless', '--convert-to', 'pdf', doc_file_path, '--outdir', output_pdf_folder_path]
                success_status = subprocess_run(args)
            except:
                success_status = False
                print('### libreoffice is not installed. Install it from distro repo or flatpak or snap ###')
    return success_status





# ? pptx / ppt to pdf
def pptx2pdfConvert(ppt_file_path, output_pdf_folder_path):
    ''' HOW TO USE :-
    pptx = pptx2pdfConvert(f'{os.getcwd()}/file name.pptx', f'{os.getcwd()}/output/')
    ppt = pptx2pdfConvert(f'{os.getcwd()}/file name.ppt', f'{os.getcwd()}/output/')
    '''
    success_status = docx2pdfConvert(doc_file_path = ppt_file_path, output_pdf_folder_path = output_pdf_folder_path)
    return success_status

    # args = ['libreoffice', '--headless', '--convert-to', 'pdf', ppt_file_path, '--outdir', output_pdf_folder_path]
    # try:
    #     success_status = subprocess_run(args)
    # except:
    #     try:
    #         args = ['/usr/bin/flatpak', 'run', 'org.libreoffice.LibreOffice', '--headless', '--convert-to', 'pdf', ppt_file_path, '--outdir', output_pdf_folder_path]
    #         success_status = subprocess_run(args)
    #     except:
    #         try:
    #             args = ['/snap/bin/libreoffice', '--headless', '--convert-to', 'pdf', ppt_file_path, '--outdir', output_pdf_folder_path]
    #             success_status = subprocess_run(args)
    #         except:
    #             success_status = False
    #             print('### libreoffice is not installed. Install it from distro repo or flatpak or snap ###')
    # return success_status





# ? jpeg to pdf
def img2pdfConvert(jpeg_file_path, output_pdf_file_path):
    '''
    jpeg = img2pdfConvert(f'{os.getcwd()}/file name.jpeg', f'{os.getcwd()}/output/file name.pdf')
    jpg = img2pdfConvert(f'{os.getcwd()}/file name.jpg', f'{os.getcwd()}/output/file name.pdf')
    png = img2pdfConvert(f'{os.getcwd()}/file name.png', f'{os.getcwd()}/output/file name.pdf')
    '''

    try:
        from img2pdf import convert as ConvertImg2PDF
        with open(output_pdf_file_path, 'wb') as newPdfFile:
            newPdfFile.write(ConvertImg2PDF(jpeg_file_path))
        return True

    except Exception as ex:
        print('### ', ex , ' ###')
        return False





# ? bmp to pdf
def bmp2pdfConvert(bmp_file_path, output_pdf_file_path):
    '''
    bmp = bmp2pdfConvert(f'{os.getcwd()}/file name.bmp', f'{os.getcwd()}/output/file name.pdf')
    '''
    try:
        from PIL import Image
        img = Image.open(bmp_file_path)
        img.save(output_pdf_file_path,'pdf')
        return True

    except Exception as ex:
        print('### ', ex , ' ###')
        return False





# ? txt to pdf
def txt2pdfConvert(txt_file_path, output_pdf_file_path):
    '''
    https://stackoverflow.com/a/64877141/16377463

    txt = txt2pdfConvert(f'{os.getcwd()}/file name.txt', f'{os.getcwd()}/output/file name.pdf')
    '''

    import textwrap
    from fpdf import FPDF
    from math import ceil, floor
    try:
        file = open(txt_file_path)
        text = file.read()
        file.close()

        a4_width_mm = 210
        pt_to_mm = 0.35
        fontsize_pt = 10
        fontsize_mm = fontsize_pt * pt_to_mm
        margin_bottom_mm = 10
        character_width_mm = 7 * pt_to_mm
        width_text = a4_width_mm / character_width_mm

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_auto_page_break(True, margin=margin_bottom_mm)
        pdf.add_page()
        pdf.set_font(family='Courier', size=fontsize_pt)
        # pdf.set_font(family='Times', size=fontsize_pt)
        splitted = text.split('\n')

        for line in splitted:
            # lines = textwrap.wrap(line, ceil(width_text))
            lines = textwrap.wrap(line, floor(width_text))

            if len(lines) == 0:
                pdf.ln()    # If a blank line exists then create an empty line

            for wrap in lines:
                pdf.cell(0, fontsize_mm, wrap, ln=1)
            pdf.ln()    # Add empty line below each line

        pdf.output(output_pdf_file_path, 'F')

        return True

    except Exception as ex:
        print('### ', ex , ' ###')
        return False





# https://stackoverflow.com/questions/3444645/merge-pdf-files

# ? Merge all pdf file to one pdf file
def mergePdfs(*pdf_paths : tuple, output_pdf_file_path):
    '''
    all_pdfs_path_tuple = (
                        f'{os.getcwd()}/file 1.pdf'
                        , f'{os.getcwd()}/file 2.pdf'
                        , f'{os.getcwd()}/file 2.pdf'
                        , f'{os.getcwd()}/file 3.pdf'
                        , f'{os.getcwd()}/file 4.pdf'
                        , f'{os.getcwd()}/file 5.pdf'
                    )
    merged = mergePdfs(*all_pdfs_path_tuple, output_pdf_file_path=f'{os.getcwd()}/output_merged_file.pdf')
    '''

    try:
        from PyPDF2 import PdfFileMerger, PdfMerger
        merger = PdfFileMerger()
        # merger = PdfMerger()
        [merger.append(pdf) for pdf in pdf_paths]
        with open(output_pdf_file_path, 'wb') as newPdfFile:
            merger.write(newPdfFile)
        return True

    except Exception as ex:
        print('### ', ex , ' ###')
        return False
