def construct_user_agent(class_name: str) -> str:
    from brambl import __version__ as brambl_version

    user_agent = 'brambl.py/{version}/{class_name}'.format(
        version=brambl_version,
        class_name=class_name,
    )
    return user_agent