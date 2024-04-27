import re
import os

# Precompile regex patterns for efficiency
single_line_comment_re = re.compile(r"#.*")
multi_line_string_re = re.compile(r'(""".*?"""|\'\'\'.*?\'\'\')', flags=re.DOTALL)


def clean_code(code: str) -> str:
    """Removes comments and unnecessary whitespace from the code."""
    code = single_line_comment_re.sub("", code)
    code = multi_line_string_re.sub("", code)
    return os.linesep.join(
        [line.strip() for line in code.strip().splitlines() if line.strip()]
    )


def extract_first_code_block(markdown_text: str, language: str) -> str:
    """Extracts the first code block of the specified language from markdown text."""
    pattern = re.compile(rf"```{language}(.*?)```", re.DOTALL)
    match = pattern.search(markdown_text)
    return clean_code(match.group(1).strip()) if match else None
