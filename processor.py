class Processor:

    def verify_steam_id(steam_id):
        # Verify that the Steam ID is a numeric string, typically 17 digits long
        return steam_id.isdigit() and len(steam_id) == 17