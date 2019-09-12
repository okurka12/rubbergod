import discord
from discord.ext import commands

import utils
from cogs import room_check
from features import acl
from config import config, messages
from repository import acl_repo

acl_repo = acl_repo.AclRepository()
acl = acl.Acl(acl_repo)
config = config.Config
messages = messages.Messages


class Acl(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.check = room_check.RoomCheck(bot)
        self.mod = None

    @commands.cooldown(rate=5, per=20.0, type=commands.BucketType.user)
    @commands.command()
    async def acl(self, ctx, *args):
        if self.mod is None:
            guild = self.bot.get_guild(config.guild_id)
            self.mod = discord.utils.get(guild.roles,
                                         name="Mod")
        if self.mod in ctx.author.roles:
            if not len(args):
                await ctx.send(
                    messages.acl_help
                    .format(user=utils.generate_mention(ctx.author.id)))
                return
            if args[0] == 'add':
                await acl.handle_add(ctx, args[1:])
            elif args[0] == 'del':
                await acl.handle_del(ctx, args[1:])
            elif args[0] == 'edit':
                await acl.handle_edit(ctx, args[1:])
            elif args[0] == 'list':
                await acl.handle_list(ctx, args[1:])
            else:
                await ctx.send(
                    messages.acl_help
                    .format(user=utils.generate_mention(ctx.author.id)))
                return
        else:
            await ctx.send(
                messages.missing_perms
                .format(user=utils.generate_mention(ctx.author.id)))
            return


def setup(bot):
    bot.add_cog(Acl(bot))
