# Importing the Necessary Libraries:

import os
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

instruction = "Behave like the best data scrapper and give the final data in the below csv format mentioned in the prompt. Give all the data present in the text extracted without any fail in the final data. Dont skip any data in the final data without any fail strictly. The final data needs to have all the data strictly."

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
    response_mime_type='text/plain',
    max_output_tokens=8192,
),safety_settings=safety,system_instruction=instruction)

input_prompt = """
Name,Email Address,Phone Number,Skills,Date Of Birth,Gender,Marital Status,Nationality,Total Experience,Companies Worked,Work Domain,Education Institution,Education Course,Education Branch,Graduation Year,Exams Percentage,Courses and Certifications,Project Names,Project description,Project Roles,Project Domain,Project Duration,Project Technologies,Languages

Extract the above details from the text extracted give the final data only in the csv format only. The final data should not contain unrelated data. It should have details that is present in the text extracted strictly and no unrelevant details should occur in the final data. If any data is not present, simply assign "NA" without thinking. If there is no details about Project Roles, Project Technologies, Project Domain, Project Duration in the text extracted, at that time simply assign "NA". Strictly no extra details should present in the Projects. Analyze the text extracted and assign properly with care. The Project details should not have references and responsibilities. The final data should be in the csv format. The Skills, Languages, Companies Worked, Work Domain, Educational Institution, Educational Course, Educational Branch, Graduation Year, Exams Percentage, Courses and Certifications, Project Names, Project Descriptions, Project Roles, Project Domains, Project Durations, Project Technologies should have list datatype strictly and compulsorily. The final order should be Name, Email Address, Phone Number, Skills, Date of Birth, Gender, Marital Status, Nationality, Total Experience, Companies Worked, Work Domain, Educational Institution, Educational Course, Educational Branch, Graduation Year, Exams Percentage, Courses and Certifications, Project Names, Project Descriptions, Project Roles, Project Domains, Project Durations, Project Technologies and Languages as mentioned above. The Companies worked should not contain the Project Names. The Project Description should be summarized and should not exceed more than 1 line. Dont assign anything if there is no Courses and Certifications in the text extracted. If there is no Project related section in the text extracted at that time dont assign anything. Dont skip any skills that is present in the text extracted. The work domain should be assigned from the text extracted only if the text extracted has the domain section and at that time dont skip those in that section. If there is no Work Domain section at that time assign most suitable only one domain from the text extracted. The work domain strictly should not contain skills name, tools name, technologies name and roles played in the companies such as java, sql, python, solution developer, technical consultant, software developer, etc. extract the work domain from the domain section only if it is present in the text extracted. If the text extracted has no domain section, at that time assign only one work domain on your own but not more than one and it should be relevant. The project roles should have only the roles played in the projects and it should not exceed 6 words. Dont skip any details regarding the education. If there is no value, at that time assign "NA" at that place. The work domain should not contain Roles played, tools, skills and technologies such as java, sql, python, Solution developer, Technical consultant etc. Dont change the order and pattern forever. Inside the list if there is empty value assign "NA" at that place. Dont skip the total experience. Dont assign any unrelated data strictly. Strictly The double quotes are allowed inside the list and not allowed outside the list datatype because list is important for multiple value never skip list datatype. Remove the new line characters present in the name, email address, Courses and Certifications, Project Descriptions. Strictly dont consider the list datatypes as string and dont enclose list in the double quotes at any cost. All the values other than list should be enclosed within double quotes. The header is very important so the first row should contain the header and second row should contain the value in the csv format. The Project Technologies should have list of list datatypes. All the list datatypes and list of list datatypes should end properly. Dont skip the list and list of list datatypes for multiple values strictly. Dont change the order and pattern. Follow all the commands in the prompt strictly. Dont skip any work domain if the domain section is present in the text extracted strictly and give the proper relevant. All the "NA" should have double quotes compulsorily.  All the string and "NA" datas should be enclosed with proper double quotes. Dont skip any education details strictly all the education details needs to be present in the final data without fail. Dont take any work domain from the Projects strictly. The final data should not have any extra symbols strictly. The work domain should not contain details ending in developer, consultant, analyst, program etc and give the revelant and suitable work domain only. Dont forget the list and list of list types. The Project duration can be present in the format of days also. The final data should follow the order and pattern compulsorily and it should display the data consistently. The Project Technologies should have list of list datatype like this [["data"],["data"]]. If the list of list datatype has pattern this [["data"],["data"]]] and simply remove the extra last square braces ']' and give the format as [["data"],["data"]]. Dont iterate the data, Give all the details only once. Each list should contain all the details of the same time. The languages known does not include the Programming languages. The languages means people speaking languages. Dont change the order strictly and give all the details in the final data without fail. If the work domain section is present in the text extracted, take all the work domain and if the section itself not present assign only one related domain from the text extracted. If the list is empty put "NA" in the list. Dont assign Reference and Responsibilities in the Projects. Dont skip any education details. Dont assign anything if there is no Projects in the text extracted. Strictly dont skip any list symbols [] in the final data and dont put double quotes outside the list because list is not string. The Work domain should not contain tools, methodologies and software names strictly. The Skills should have only tools and software names only. The Project Roles should have only 4 to 5 words. Dont skip anything if it is present in the text extracted. Dont skip any data in the final data without any fail strictly. The final data needs to have all the data strictly. I need all the data that is present in the text extracted in the final data. The final data should have only related and necessary data if present from the text extracted without skipping anything.
"""

text = text
input_prompt = input_prompt

prompt = """
Text Extracted: {0}

Input Prompt: {1}
""".format(text,input_prompt)

def get_response(prompt):
    response = model.generate_content(prompt,request_options={'retry': retry.Retry(predicate=retry.if_transient_error)})
    return response.text

details = get_response(prompt)
print(details)

with open('csvdata_pattern9.csv','w') as newfile:
    newfile.write(details)

print("Data Written Succesfully...")