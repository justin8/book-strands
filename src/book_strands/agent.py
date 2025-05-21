from strands import Agent
from strands_tools import http_request

from .tools import read_ebook_metadata, write_ebook_metadata


def agent(input_files: list[str], output_path: str, output_format: str):
    system_prompt = f"""
        You are in charge of making sure ebooks are tagged with the correct metadata.
        Use tools to gather the information required and then write it to the provided output folder ("{output_path}").
        The expected format and path of the output files is: "{output_format}"
        The list of books to process is: {input_files}
        Note that all series indexes should be in the format 1.0, 2.0, 2.5 etc based on common practice.
        """
    a = Agent(
        system_prompt=system_prompt,
        tools=[read_ebook_metadata, write_ebook_metadata, http_request],
    )
    return a("Perform the tasks as requested.")
