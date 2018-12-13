from communications.models import Communication


def get_profile_data(username, platform):
    communication = Communication.objects.create(
        method='profile_data',
    )
    communication = communication.communicate(platform=platform.name, username=username)
    if not communication.error:
        communication.create_player_stats()
    return communication


def get_match_history(account_id):
    communication = Communication.objects.create(
        method='match_history'
    )
    communication = communication.communicate(account_id=account_id)
    if not communication.error:
        communication.create_matches(account_id=account_id)
    return communication
