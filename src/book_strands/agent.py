import logging

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands_tools import http_request  # type: ignore

from book_strands.constants import BOOK_HANDLING_PROMPT
from book_strands.utils import calculate_bedrock_cost  # type: ignore

from .tools import (
    download_ebook,
    file_move,
    metadata_agent,
    path_list,
)

log = logging.getLogger(__name__)


def agent(
    output_path: str,
    output_format: str,
    query: str,
):
    system_prompt = f"""
You are a book downloader, renamer, and metadata fixer agent.
Your task is to download ebooks, rename them according to the provided format ({output_format}), and fix their metadata.
The output ebooks should be saved in the specified output path ({output_path}).

Check the output directory for existing books by the same author to match that formatting.
Check if the ebook files for a particular book already exist in the output folder, and if so, skip downloading them.
If the ebook files do not exist, download them using the provided tools.

You can assume the author and title in the file names are correct without verifying the metadata.

From the input query, extract the list of book titles and authors to download.
If the query does not contain anything that can be resolved to a book title and/or author, return an error message indicating that no books were found.

{BOOK_HANDLING_PROMPT}
"""

    model = BedrockModel(model_id="us.amazon.nova-pro-v1:0")

    a = Agent(
        system_prompt=system_prompt,
        model=model,
        tools=[
            download_ebook,
            metadata_agent,
            file_move,
            path_list,
            http_request,
        ],
    )

    response = a(query)
    log.info(f"Accumulated token usage: {response.metrics.accumulated_usage}")

    total_cost = calculate_bedrock_cost(
        response.metrics.accumulated_usage,
        model,
    )
    log.info(f"Total cost: US${total_cost:.3f}")

    return response
