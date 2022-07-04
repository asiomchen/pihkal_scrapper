import sys
import re
import os
import datetime
import html
from bs4 import BeautifulSoup
from urllib.request import urlopen
from math import floor as round_down


def pihkal_scrapper(start_procedure: int = 1, end_procedure: int = 179)-> None:
    """
    Scraps the erowid pihkal DB and saves the synthesis data in separate txt files
    :param start_procedure:  start procedure number
    :param end_procedure:  end procedure number
    :return: None
    """

    time_sum = []
    # read url
    cwd = os.getcwd()
    for i in range(start_procedure, end_procedure):
        start_time = datetime.datetime.now()
        if i not in range(179):
            raise ValueError("Only 179 procedures available")
        i = str(i)

        # modifying number of synthesis to make correct url
        while True:
            if len(i) == 1:
                n = '00' + i
                break
            if len(i) == 2:
                n = '0' + i
                break
            if len(i) == 3:
                n = i
                break

        # erowid pihkal template as str
        page_template = f"https://erowid.org/library/books_online/pihkal/pihkal{n}.shtml"

        # opening and decoding of source html page
        try:
            page = urlopen(page_template)
            html_page = page.read().decode()
        except:
            raw_data_path = f'{cwd}/temp/problem_{i}'
            #raw_data_path = f"C:\\test\\temp\\PROBLEM {n}"
            os.makedirs(raw_data_path)
            complete_name = os.path.join(raw_data_path, "error" + ".txt")
            txt_output = open(complete_name, "w")
            txt_output.write(f"Decoding problem. Page url: {page_template}")
            continue

        # creating bs object from html
        soup = BeautifulSoup(html_page, "html.parser")

        # extracting procedure name from h2 tag
        try:
            synthesis_name = str(soup.find_all("h2", text=True))
            synthesis_name = synthesis_name.split(" ")
            synthesis_name = synthesis_name[1]
            synthesis_name = synthesis_name.replace("</h2>", "")
            synthesis_name = synthesis_name.replace("]", "")
        except:
            raw_data_path = f'{cwd}/temp/Procedure{i}'
            #raw_data_path = f"C:\\test\\temp\\Procedure{i}"
            os.makedirs(raw_data_path)
            complete_name = os.path.join(raw_data_path, "error" + ".txt")
            txt_output = open(complete_name, "w")
            txt_output.write("Synthesis name not found.")
            continue
        # extracting page text without html tags
        text = soup.find_all(text=True)
        page_output = ' '.join(text)

        # this step guaranties correct degree decoding
        page_output = html.unescape(page_output)

        # Searching for synthesis name using RegEx
        try:
            pattern = "SYNTHESIS.*?DOSAGE"
            match_results = re.search(pattern, page_output, re.DOTALL)
            txt = match_results.group()

            # Removing RegEx pattern from text
            txt = (txt[12:-11])
            txt = txt.replace("  ", " ")
        except:
            raw_data_path = f'{cwd}/temp/{synthesis_name }'
            #raw_data_path = f"C:\\test\\temp\\{synthesis_name}"
            os.makedirs(raw_data_path)
            complete_name = os.path.join(raw_data_path, synthesis_name + ".txt")
            txt_output = open(complete_name, "w")
            txt_output.write("Synthesis info not found.")
            continue

        # creating txt file with whole procedure
        try:
            raw_data_path = f'{cwd}/temp/{synthesis_name}'
            #raw_data_path = f"C:\\test\\temp\\{synthesis_name}"
            os.makedirs(raw_data_path)
            complete_name = os.path.join(raw_data_path, synthesis_name + ".txt")
            txt_output = open(complete_name, "w")
            txt_output.write(txt)
        except:
            raw_data_path = f'{cwd}/temp/Problem {n}'
            raw_data_path = f"C:\\test\\temp\\PROBLEM {n}"
            os.makedirs(raw_data_path)
            complete_name = os.path.join(raw_data_path, "error" + ".txt")
            txt_output = open(complete_name, "w")
            txt_output.write(f"Decoding problem. Page url: {page_template} ")
            continue

        # Splitting of original procedure into list of individual steps
        source_txt = txt.split("\n\n")
        step = 0
        file_name = "procedure.txt"

        # Looping over steps and separating into distill an non-distill procedures
        for paragraph in source_txt:
            step += 1
            if "distil" in paragraph or "Distil" in paragraph:
                synthesis_dir = f'{cwd}/distill_procedures/CY-ASi-ASi-PiHKAL_1991-cmp_{synthesis_name}_step-{step}'
                #synthesis_dir = f"C:\\test\\distill\\CY-ASi-ASi-PiHKAL_1991-cmp_{synthesis_name}_step-{step}"
                os.makedirs(synthesis_dir)
                complete_name = os.path.join(synthesis_dir, file_name)
                file = open(complete_name, "w")
                file.write(paragraph)
                file.close()
            else:
                synthesis_dir = f'{cwd}/non_distill_procedures/CY-ASi-ASi-PiHKAL_1991-cmp_{synthesis_name}_step-{step}'
                #synthesis_dir = f"C:\\test\\working_on\\CY-ASi-ASi-PiHKAL_1991-cmp_{synthesis_name}_step-{step}"
                os.makedirs(synthesis_dir)
                complete_name = os.path.join(synthesis_dir, file_name)
                file = open(complete_name, "w")
                file.write(paragraph)
                file.close()

        # time counter
        end_time = datetime.datetime.now()
        time_delta = (end_time - start_time)
        execution_time = time_delta.total_seconds()
        time_sum.append(execution_time)
        average_time = (sum(time_sum)) / (len(time_sum))
        etr = (average_time * (end_procedure - int(i)))
        if etr < 59:
            print(f"Script executed normally, compound name - {synthesis_name}, number of steps - {step}. "
                  f"Progress: {round(((int(i) - start_procedure + 1) / (end_procedure - start_procedure)) * 100, 3)}%. "
                  f"Estimated time: {round(etr, 0)} s.")
        else:
            etr_min = round_down(etr / 60)
            etr_s = round(etr % 60)
            print(f"Script executed normally, compound name - {synthesis_name}, number of steps - {step}. "
                  f"Progress: {round(((int(i) - start_procedure + 1) / (end_procedure - start_procedure)) * 100, 3)}%. "
                  f"Estimated time: {etr_min} min. {etr_s} s.")


if __name__ == "__main__":
    pihkal_scrapper()
