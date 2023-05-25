import asyncio

from handling_presentations import extract_text_from_presentation
from handling_api import api_request

CONTENT = "Text below from presentation slide give me short explanation about this topic \n"


async def main():
    file = open("my_lesson.txt", 'w')

    presentation_path = 'Tests.pptx'
    extracted_text = extract_text_from_presentation(presentation_path)

    res = '\n'.join(await asyncio.gather(*(api_request(CONTENT, text) for text in extracted_text)))
    file.write(res)


if __name__ == '__main__':
    asyncio.run(main())


