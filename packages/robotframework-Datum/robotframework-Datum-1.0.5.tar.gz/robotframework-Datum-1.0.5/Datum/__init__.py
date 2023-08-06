import json
from robot.api import logger
import os
from PyPDF2 import PdfFileWriter, PdfFileReader


class Datum():
    '''
    PDF Library is testing library for robotframework.
    '''
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0.5'

    def __init__(self, *args):       
        self.args = args

    def pdf_to_txt(
        self,
        File_Path: str,
        Txt_File_Name: str ="generatedtxtfile",
        Number_Of_Pages: int=1
        ):
        """Returns contents of the ``PDF file`` into a ``Text file``.

        Take as arguments, the file name and the path where the file exists.

        """
        pdffileobj = open(File_Path, 'rb')
        pdfreader = PdfFileReader(pdffileobj)
        file1=open(Txt_File_Name+".txt", "w")
        for i in range  (Number_Of_Pages):
            pageobj = pdfreader.getPage(i)
            text=pageobj.extract_text()
            file1.write(text)
        file1.close()


    def _decompose_pdf(self, 
        path_pdf: str,
        path_workspace: str,
        export_text: bool = False):
        """Returns every page in a single pdf file.

        Set to true if you would like to return every page
        in text format as well
        """
        list =[]
        fileName1, fileExtension1 = os.path.splitext(os.path.basename(path_pdf))
        input1pdf = PdfFileReader(open(path_pdf, "rb"))
        Npage_ref = input1pdf.numPages
        for i in range(input1pdf.numPages):
            output = PdfFileWriter()
            output.addPage(input1pdf.getPage(i))

            with open(path_workspace+str(fileName1)+"-page%s.pdf" % str(i+1), "wb") as outputStream:
                output.write(outputStream)
            
            if export_text==True:
                self.pdf_to_txt(path_workspace+str(fileName1)+"-page%s.pdf" % str(i+1),path_workspace+str(fileName1)+"-page%s" % str(i+1))
                list.append(path_workspace+str(fileName1)+"-page%s.txt" % str(i + 1))
        return Npage_ref,list


    def decompose_pdf(self, 
        path_pdf: str,
        path_workspace: str=os.curdir,
        export_text: bool = False):
        """Returns every page in a single pdf file.
        Set to true if you would like to return every page
        in text format as well.
        """
        list =[]
        fileName1, fileExtension1 = os.path.splitext(os.path.basename(path_pdf))
        input1pdf = PdfFileReader(open(path_pdf, "rb"))
        Npage_ref = input1pdf.numPages
        msg="File is decomposed successfuly to "+str(Npage_ref)+" pages"
        for i in range(input1pdf.numPages):
            output = PdfFileWriter()
            output.addPage(input1pdf.getPage(i))

            with open(path_workspace+str(fileName1)+"-page%s.pdf" % str(i+1), "wb") as outputStream:
                output.write(outputStream)
            
            if export_text==True:
                self.pdf_to_txt(path_workspace+str(fileName1)+"-page%s.pdf" % str(i+1),path_workspace+str(fileName1)+"-page%s" % str(i+1))
                list.append(path_workspace+str(fileName1)+"-page%s.txt" % str(i + 1))
        logger.info(str(msg))

    def compare_pdf_and_return_differences(self,
        path_pdf_ref: str,
        path_pdf_target: str,
        path_output_file: str=os.curdir):
        """Comparef two PDF files. This keyword split pdf files page by page and convert them to text.
        Then compare each page by its reference. Keyword type is function and returns text file that 
        contain the different strings.
        Takes as an argument:
        - _Path of PDF file reference
        - _Path of PDF file target
        - _Path of output text file which shows the difference
        """
        result = ''
        err = ''
        n_page_ref,list_ref = self._decompose_pdf(path_pdf_ref,path_output_file)
        n_page_target,list_target = self._decompose_pdf(path_pdf_target,path_output_file)
        if n_page_ref != n_page_target :
            err = "Number of pages in both pdf files is not equal, cannot compare"
        else:
            for i in range(n_page_ref):
                file_ref = open(list_ref[i], 'r')
                Lines_ref = file_ref.readlines()
                file_target = open(list_target[i], 'r')
                Lines_target = file_target.readlines()
                for n in range(max(len(Lines_ref),len(Lines_target))):
                    if Lines_ref[n] != Lines_target[n] :
                        if  Lines_ref[n] != '' or Lines_target[n] != '' :
                            err = "PDF files does not contain same text, check output file for more details"
                            result += "page "+str(i+1) +" : \n" +"----"+ str(Lines_ref[n])  +"++++"+ str(Lines_target[n])
        outputfile=open("Differences"+".txt",'w')
        outputfile.write(result)
        outputfile.close()
        if err!="":
            raise ValueError(err)
         

    def count_pdf_pages(self, Pdf_Path):
        """Returns the number of pages in a pdf document.
        """
        err=''
        try:
            inputfile = PdfFileReader(open(Pdf_Path, "rb"))
        except:
            err='No such file in the indicated directory, check the pdf file path'
            raise AssertionError(err)
        numberofpages = inputfile.numPages
        return  numberofpages


    def compare_json_files(file1, file2):
        """Fails if the given JSON files are not the same.
        
        """
        with open(file1) as f1:
            data1 = json.load(f1)
        with open(file2) as f2:
            data2 = json.load(f2)

        if data1 == data2:
            logger.info("JSON files are equal")
        else:
            for key in data1.keys():
                if data1[key] != data2[key]:
                    raise AssertionError("Differences found in: " f"{key}: {data1[key]} != {data2[key]}")


    
    def count_occurrences(string, paragraph, case_sensitive=True, ignore_punctuation=True):
        """Find the number of occurrences of a given string in a paragraph.

        By default the count method is case sensitive and it ignores punctuation"""
        if not ignore_punctuation:
            string = ''.join(ch for ch in string if ch not in string.punctuation)
            paragraph = ''.join(ch for ch in paragraph if ch not in string.punctuation)
        if not case_sensitive:
            string = string.lower()
            paragraph = paragraph.lower()
        return paragraph.count(string)