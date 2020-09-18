import click

from datetime import datetime


PARAGRAPH_DELIM = ' <end_of_paragraph> '


def get_now():
    return datetime.now()


def print_time(start_time, operation):
    delta = get_now() - start_time
    click.echo("{} took {}.{} seconds".format(
        operation, delta.seconds, delte.microseconds
    ))


def concat_paragraphs(paragraps):
    """Convert list of strings into one big string by concatenating each string
    by `PARAGRAPH_DELIM`.

    Parameters
    ----------
    paragraps : list of str
        A list of string

    Returns
    -------
    str
        A string where each string in `paragraps` is concatenated by
        PARAGRAPH_DELIM.
    """
    return PARAGRAPH_DELIM.join(paragraps)


def split_text_into_paragraphs(text):
    """Split text into paragraphs by `PARAGRAPH_DELIM`.

    Parameters
    ----------
    text : str
        A string to split into paragraphs.

    Returns
    -------
    list of str
        A list of paragraphs where each paragraph is a string.
    """
    return text.split(PARAGRAPH_DELIM)


def ask_admin_info():
    admin_name = click.prompt("Admin name")
    admin_password = click.prompt("Password", hide_input=True)
    return admin_name, admin_password


def admin_auth(db_interface, project_name):
    admin_name, admin_password = ask_admin_info()
    auth = db_interface.admin_authentication(
        project_name=project_name,
        admin_name=admin_name,
        admin_password=admin_password
    )
    return auth
