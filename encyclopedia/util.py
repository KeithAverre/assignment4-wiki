import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))

def replace_entry(orginal_title, new_title, content):
    """
        Saves an encyclopedia entry, given its title and Markdown
        content. If an existing entry with the same title already exists,
        it is replaced.
        """
    filename_old = f"entries/{orginal_title}.md"
    filename_new = f"entries/{new_title}.md"
    if default_storage.exists(filename_old):
        default_storage.delete(filename_old)
    if default_storage.exists(filename_new):
        default_storage.delete(filename_new)
    default_storage.save(filename_new, ContentFile(content))
def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
