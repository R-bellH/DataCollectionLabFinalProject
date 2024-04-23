from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import os

GOOGLE_API_KEY = 'Add your key here'
proj_dir = os.path.dirname(os.path.dirname(os.getcwd()))
data_path = proj_dir + "/data/countryNamesGemini"


def clean_reply(content):
    # remove "." from the text,
    content = content.replace(".", "")
    # remove repeated names
    names = content.split("\n")
    # remove digits and special characters
    # names = ["".join(filter(str.isalpha, name)) for name in names]
    names = list(set(names))
    return "\n".join(names)

llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7, cache=False,  google_api_key=GOOGLE_API_KEY)

languages_list = ['American', 'Australian', 'Brazilian', 'Canadian', 'Danish', 'Finnish', 'Israeli', 'Hindi', 'Egyptian', 'Turkish','Indonesian', 'Malaysian', 'Mexican', 'Norwegian', 'Pakistani', 'Saudi Arabian', 'South African', 'Swedish', 'Swiss', 'Ukrainian']
# 
for lang in languages_list:
    prompt =f"""give me a list of 1000 {lang} last names in English script, in the following format:
    last name 1
    last name 2
    ...
    only the last names
    no additional text or chars. do not number the last names"""
    firstReplyFromLLM = llm.invoke(prompt)
    firstReplyContent = firstReplyFromLLM.content
    names1=clean_reply(firstReplyContent)
    # print(firstReplyContent)
    secondPrompt="""give me another list of 1000 (or until character limit) """ + lang + """ last names in English script, in the following format:
    last names 1
    last names 2
    ...
    only the last names
    no additional text or chars. do not number the last names
    such that none of the last names appear in: {context}"""
    secondPrompt=ChatPromptTemplate.from_template(secondPrompt)
    secondPrompt = secondPrompt.format(context=names1)
    secondReplyFromLLM = llm.invoke(secondPrompt)
    secondReplyContent = secondReplyFromLLM.content
    # print(secondReplyContent)
    names = clean_reply(firstReplyContent + "\n" + secondReplyContent)

    # replyContent = replyContent.strip()
    with open(rf"{data_path}/{lang}.txt", "w", encoding="utf-8") as file:
        file.write(names)
    print(lang + " done")