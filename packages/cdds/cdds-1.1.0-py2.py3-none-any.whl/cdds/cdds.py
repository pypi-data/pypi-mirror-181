"""Main module."""
def dojo_env_setup_instructions(only_summary=False, as_markdown=True):
	from IPython.display import Markdown, display
	with open("files/dojo-env-setup.md") as f:
		md = f.read()
	
	if only_summary:
		sections = md.split('__')
		summary_parts = [s for s in sections[1:] if "summary" in s.lower()]
		final_md = summary_parts.strip('\n\n')
	else:
		final_md = md
		
	if as_markdown:
		display(Markdown(final_md))
	else:
		print(final_md)
	