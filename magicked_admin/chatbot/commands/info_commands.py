from chatbot.commands.command import Command
from server.player import Player
from utils.time import seconds_to_hhmmss
from utils.text import millify

import datetime


class CommandPlayers(Command):
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        message = ""

        for player in self.server.players:
            message += str(player) + " \n"
        message = message.strip()
        return message


class CommandGame(Command):
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        return str(self.server.game)

class CommandGameMap(Command):
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        return str(self.server.game.game_map)

class CommandHighWave(Command):
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        return "{} is the highest wave reached on this map."\
            .format(self.server.game.game_map.highest_wave)

class CommandHelp(Command):
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        return "Player commands:\n !me, !dosh, !kills, !server_dosh," \
               " !server_kills, !top_dosh, !top_kills, !stats, !info"


class CommandInfo(Command):
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        return "I'm a bot for ranked Killing Floor 2 servers. Visit:\n" \
            "github.com/th3-z/kf-magicked-admin/\n" + \
            "for information, source code, and credits."


class CommandMe(Command):
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

        stats_command = CommandStats(self.server, admin_only=False)
        return stats_command.execute("server", ["stats", username], admin=True)


class CommandStats(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        if len(args) < 2:
            return "Missing argument (username)"

        self.server.write_all_players()
        requested_username = " ".join(args[1:])

        player = self.server.get_player(requested_username)
        if player:
            now = datetime.datetime.now()
            elapsed_time = now - player.session_start
            session_time = elapsed_time.total_seconds()
        else:
            session_time = 0
            player = Player(requested_username, "no-perk")
            self.server.database.load_player(player)

        time = seconds_to_hhmmss(
            player.total_time + session_time
        )
        message = "Stats for {}:\n".format(player.username) +\
                  "Total play time: {} ({} sessions)\n"\
                      .format(time, player.total_logins) +\
                  "Total deaths: {}\n".format(player.total_deaths) +\
                  "Total kills: {}\n".format(millify(player.total_kills)) +\
                  "Total dosh earned: {}\n"\
                      .format(millify(player.total_dosh)) +\
                  "Dosh this game: {}".format(millify(player.game_dosh))

        return message
