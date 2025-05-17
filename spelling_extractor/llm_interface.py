# spelling_extractor/llm_interface.py
import subprocess

def run_phi_and_get_block(text, model='phi3'):
    """
    Sends the full newsletter text to Phi-3 and returns the exact block of spellings,
    including the title and bullet list as a single string.
    """
    prompt = f"""
Extract the list of next week's spellings from this newsletter text.\
Ignore the 'skeleton spellings:' words. Output including the title (e.g., "Words with ...") and each spelling preceded by a dash, one per line exactly as returned.

{text}
"""
    print("[LLM PROMPT]:")
    print(prompt)
    proc = subprocess.run(
        ['ollama', 'run', model],
        input=prompt.encode('utf-8'),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out = proc.stdout.decode('utf-8', errors='ignore')
    err = proc.stderr.decode('utf-8', errors='ignore')

    print("[PHI-3 OUTPUT]:")
    print(out)
    if err.strip():
        print("[PHI-3 ERROR]:", err)

    return out.strip()
