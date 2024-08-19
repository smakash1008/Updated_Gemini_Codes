# Importing the Necessary Libraries:

import os
import json
from pdfminer.high_level import extract_text
import docx2txt
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
from google.api_core import retry

file_path = input("Enter the file path: ")
print(file_path)

def extract_file_extension(file_path):
    file_name_split = file_path.split(".",1)
    print(file_name_split)
    if len(file_name_split) == 2:
        return file_name_split[1]
    else:
        return None
    
file_extension = extract_file_extension(file_path)
print(file_extension)

def file_text_extract(file_extension):
    if file_extension == 'pdf':
        text = extract_text(file_path)
        return text
    elif file_extension == 'docx':
        text = docx2txt.process(file_path)
        return text
    else:
        return None
    
text = file_text_extract(file_extension)
print(text)

# Configuring the Gemini API KEY:
genai.configure(api_key=os.getenv("GOOGLE_API_KEY1"))

# Configuring the Gemini Model:

instruction = "Behave like the best data scrapper and give the final data in the below json format mentioned in the prompt. Give all the data present in the text extracted without any fail in the final data. Dont skip any data in the final data without any fail strictly."

safety = {
    'HATE':'BLOCK_NONE',
    'HARASSMENT':'BLOCK_NONE',
    'SEXUAL':'BLOCK_NONE',
    'DANGEROUS':'BLOCK_NONE'
}

model = genai.GenerativeModel(model_name="gemini-1.5-pro",generation_config=genai.GenerationConfig(
    temperature=1,
    top_p=0.95,
    top_k=64,
    response_mime_type='application/json',
    max_output_tokens=8192,
),safety_settings=safety,system_instruction=instruction)

prompt = f"""
Text Extracted : {text}

Extract the Name, Email Address, Phone Number, Skills, Total Years Of Experience, Work Domain, Companies Worked, Date of Birth, Gender, Marital Status, Nationality, Languages, Educational Institution, Education Course, Education Branch, Graduation Year, Exam Percentage, Courses and Certifications, Project Name, Project Description, Project Roles, Project Duration, Project Domain, Project Technologies from the above Text Extracted. Remove the New line characters present in the Name, Email, Courses and Certifications. Name the key as Work Experience for Companies Worked and give only the Companies_Worked and Dont give the Project Names in the Work_Experience strictly. The Work Experience should have only Companies Worked and strictly dont take any details from the Project Sections. Name the key as Education Details for Educational Institution, Education Course, Education Branch, Graduation Year, Exam Percentage and give the Education Details based on Education Course. Dont assign Courses and Certifications in the Education Details. Name the key as Project Details for Project Name, Project Description, Project Roles, Project Duration, Project Domain, Project Technologies. The final order should be Name, Email Address, Phone Number, Skills, Total Years Of Experience, Work Domain, Work Experience, Date of Birth, Gender, Marital Status, Nationality, Languages, Education Details, Courses and Certification and Project Details. Inside the Education Details the final order should be Educational Institution, Education Course, Education Branch, Graduation Year, Exam Percentage. Inside the Project Details the final order should be Project Name, Project Description, Project Roles, Project Duration, Project Domain, Project Technologies. Dont add the Reference and Responsibilities in the Project Details. The Project Description should be summarized in a way that it should not exceed 2 lines strcitly. Dont assign any variable to the final data. Dont change the order at any time. If the Work Domain is present take that only from the text and dont add extra details in it. If there is no details related to Work Domain try to assign only the domain related detail present in the text to the Work Domain at that situation only and dont try to analyze on your own. Dont try to assign unrelated details in Work Domain. Dont assign Skills, Tools, Technologies and Roles Played such as java, html, python, Software Developer, Solution Developer, Team Lead etc, in the Work Domain. Strictly the Work Domain should not contain Roles Played in the Company, Skills and Tools names strictly. Strictly no tools and skills names should be present in Work Domain. Dont skip any skills if present in the text and give all the skills. Dont give the language proficiency and if it is attached to the language remove the language proficiency and give only the language. If there is no details about Courses and Certifications in the text dont assign anything. Dont try to assign extra details which is not present in the text and try to extract details from the text. Dont assign any extra keys which is not mentioned and dont extract any extra information that is not mentioned in the prompt. The Work Domain should have only the domain, it should not have technologies, skills, tools and roles played in it strictly dont assign those. The final data should not be changed. The final order needs to show all the keys. The final data should not have escape characters. Use the list datatype for multiple values only. Give the Final data in the indented form. If there is no domain in the extracted text at that time give only one work domain strictly from the text extracted, dont give more than one work domain strictly. The list is very important for multiple values so dont try to skip list datatypes for multiple values and the list datatypes is compulsory. Extract the work domain from the domain section of the text extracted only. Assign NOT AVAILABLE for empty details. Compulsorily assign list datatype for the keys having multiple values in the Project Technologies, Courses and Certification strictly if the Project section is present in the text extracted. Strictly dont assign anything if there is no Project related section in the text extracted. Assign only the work domain present in the text extracted not anything related to the Projects section. The Work domain should not contain tools, methodologies and software names strictly. The Skills should have only tools and software names only. The Project Roles should have only 4 to 5 words. Dont skip anything if it is present in the text extracted. Read the entire prompt command fully and strictly follow all those in the prompt."""

def get_response(prompt):
    response = model.generate_content(prompt,request_options={'retry': retry.Retry(predicate=retry.if_transient_error)})
    return response.text

details = get_response(prompt)
print(details)

dict_data = json.loads(details)
print(dict_data)

with open('json_finaldata9.json','w') as newfile:
    newfile.write(details)

print("Data Written Succesfully...")