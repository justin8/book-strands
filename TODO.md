# To-do list

1. Split out filesystem checks to it's own separate agent flow - this should greatly reduce token usage since the file list won't stay in the conversation history. Or make it a fuzzy match file search instead?
2. Update the metadata agent to A) lookup metadata about a book but not write it out (leave that to the parent agent) B) cache the results; so it can be used to get data and structure the filename; then also to write metadata later. Although maybe the top level agent will know it has that info and not re-run it? let's find out.
3. Update cost measurements to account for sub-agents as well
4. Test using an agent-based approach instead of the current scraper for downloads
5. Add support for LiteLLM and/or Ollama models
