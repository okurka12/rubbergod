from disnake.ext.commands import Bot

from .cog import Latex


def setup(bot: Bot):
    bot.add_cog(Latex(bot))
