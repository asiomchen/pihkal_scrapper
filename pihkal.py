from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import os
import datetime
import html

def parser(x, y, z):
    time_sum = []
    #read url
    for i in range(x, y):
        start_time = datetime.datetime.now()
        if i not in range(179) :
                raise ValueError("Only 179 procedures available")
        i = str(i)
        while True:
            if len(i) == 1:
                mod_1 = "0"
                n = mod_1 + i
                break
            if len(i) == 2:
                n = i
                break
        page_template = f"https://erowid.org/library/books_online/tihkal/tihkal{n}.shtml"
        try:
            page = urlopen(page_template)
            html_page = page.read().decode()
        except:
            RawDataPath = f"C:\script\\temp\PROBLEM {n}"
            os.makedirs(RawDataPath)
            completeName = os.path.join(RawDataPath, "error" + ".txt")
            txt_output = open(completeName, "w")
            txt_output.write(f"Decoding problem.Page url: {page_template}")
            txt_output.close
            continue
        #create bs object
        soup = BeautifulSoup(html_page, "html.parser")
        #extract procedure name
        try:
            SynthesisName = str(soup.find_all("h2", text=True))
            SynthesisName = SynthesisName.split(" ")
            SynthesisName = SynthesisName[z]
            SynthesisName = SynthesisName.replace("</h2>", "")
            SynthesisName = SynthesisName.replace("]", "")
        except:
            RawDataPath = f"C:\script\\temp\Procedure{i}"
            os.makedirs(RawDataPath)
            completeName = os.path.join(RawDataPath, "error" + ".txt")
            txt_output = open(completeName, "w")
            txt_output.write("Synthesis name not found.")
            txt_output.close
            continue
        #extract text without tags
        text = soup.find_all(text=True)

        page_output = ''
        blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        # there may be more elements you don't want, such as "style", etc.
        ]

        for t in text:
            if t.parent.name not in blacklist:
                page_output += '{} '.format(t)
        page_output = page_output.replace("<br/>","")
        page_output = html.unescape(page_output)

        try:
            pattern = "SYNTHESIS.*?DOSAGE"
            match_results = re.search(pattern, page_output, re.DOTALL)
            txt = match_results.group()
            txt = (txt[12:-11])
            txt = txt.replace("  ", " ")
        except:
            RawDataPath = f"C:\script\\temp\{SynthesisName}"
            os.makedirs(RawDataPath)
            completeName = os.path.join(RawDataPath, SynthesisName + ".txt")
            txt_output = open(completeName, "w")
            txt_output.write("Synthesis info not found.")
            txt_output.close
            continue
        


        try:
            RawDataPath = f"C:\script\\temp\{SynthesisName}"
            os.makedirs(RawDataPath)
            completeName = os.path.join(RawDataPath, SynthesisName + ".txt")
            txt_output = open(completeName, "w")
            txt_output.write(txt)
            txt_output.close
        except:
            RawDataPath = f"C:\script\\temp\PROBLEM {n}"
            os.makedirs(RawDataPath)
            completeName = os.path.join(RawDataPath, "error" + ".txt")
            txt_output = open(completeName, "w")
            txt_output.write(f"Decoding problem. Page url: {page_template} ")
            txt_output.close
            continue


        raw = open(completeName, "r")
        txtt = raw.read()
        print(completeName)
        txtt = txt.split("\n\n")
        step = 0
        file_name = "procedure.txt"


        for paragraph in txtt:
            step += 1
            if "distil" in paragraph or "Distil" in paragraph:
                dir= f"C:\script\distil\CY-AgZ-AgZ-TiHKAL_1997-cmp_{SynthesisName}_step-{step}"
                os.makedirs(dir)
                completeName = os.path.join(dir, file_name)
                file = open(completeName,"w")
                file.write(paragraph)
                file.close()
            else:
                dir = f"C:\script\working_on\CY-AgZ-AgZ-TiHKAL_1997-cmp_{SynthesisName}_step-{step}"
                os.makedirs(dir)
                completeName = os.path.join(dir, file_name)
                file = open(completeName,"w")
                file.write(paragraph)
                file.close()
        end_time = datetime.datetime.now()


        time_delta = (end_time - start_time)
        execution_time = time_delta.total_seconds()
        time_sum.append(execution_time)
        average_time = (sum(time_sum))/(len(time_sum))
        ETR_s = (average_time*(y-int(i)))
        ETR_m = ETR_s/60
        SSS = ETR_s - 60*round(ETR_m, 0)
        print(f"Script executed normally, number of steps - {step}. Progress: {round(((int(i)-x+1)/(y-x))*100, 3)}%. Estimated time: {round(ETR_m,0)} min.")
parser(7, 55, 2)