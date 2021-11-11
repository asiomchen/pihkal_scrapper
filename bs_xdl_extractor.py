import os
import re
from urllib.request import urlopen
def xdl_extractor(RawDataPath: str):
    name = input("Enter name:")
    raw = open(RawDataPath, "r")
    txt = raw.read()
    txt = txt.split("\n\n")
    step = 0
    file_name = "procedure.txt"
    for paragraph in txt:
        step += 1
        if "distil" in paragraph or "Distil" in paragraph:
            dir= f"H:\script\distil\CY-ASi-ASi-PiHKAL_1991-cmp_{name}_step-{step}"
            os.makedirs(dir)
            completeName = os.path.join(dir, file_name)
            file = open(completeName,"w")
            file.write(paragraph)
            file.close()
        else:
            dir = f"H:\script\working_on\CY-ASi-ASi-PiHKAL_1991-cmp_{name}_step-{step}"
            os.makedirs(dir)
            completeName = os.path.join(dir, file_name)
            file = open(completeName,"w")
            file.write(paragraph)
            file.close()
    print(f"Script executed normally, number of steps - {step}")
def xdl_extractor2():
    url = "https://erowid.org/library/books_online/pihkal/pihkal001.shtml"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    SynthesisName = str(re.findall("<h2>.*</h2>", html))
    SynthesisName = SynthesisName.split(" ")
    SynthesisName = SynthesisName[1]
    pattern = "<b>SYNTHESIS.*?>.*?<b>DOSAGE.*?</b>"
    match_results = re.search(pattern, html, re.DOTALL)
    title = match_results.group()
    title = re.sub("<.*?>", "", title)
    print(title)

xdl_extractor2()