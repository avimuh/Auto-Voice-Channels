import cfg
import discord
import utils
import functions as func
from math import floor
from commands.base import Cmd
from time import time

help_text = [
    [
        ("Usage:", "```<PREFIX><COMMAND> @USER```" "```<PREFIX><COMMAND> @USER\nREASON```"),
        (
            "Description:",
            "Initiate a votekick to remove a user from your channel and prevent them from joining again. "
            "**More than half** of the remaining users must vote yes in order for the member to be kicked.\n\n"
            "If you wish to allow a kicked user to return to the channel, you will all have to leave and create a new "
            "channel instead, or if you are a server admin, manually edit the channel permissions.\n\n"
            "The person who initially created the channel cannot be kicked (unless they leave voluntarily and later "
            'return, in which case the "creator" of the channel is reassigned to the person who was at the top of the '
            "channel when they left.)",
        ),
        (
            "Examples:",
            "```<PREFIX><COMMAND> @pixaal```"
            "```<PREFIX><COMMAND> pixaal#1234\nBeing mean :(```"
            "```<PREFIX><COMMAND> pixaal\nSound board abuse```",
        ),
    ]
]


async def execute(ctx, params):
    if user == author:
        return False, "Please don't kick yourself :frowning:"

    if not channelcreator:
        participants = [m for m in vc.members if m not in [author, user] and not m.bot]
        required_votes = floor((len(participants) + 1) / 2) + 1
        try:
            text = (
                "‼ **Votekick** ‼\n"
                "{initiator} has initiated a votekick against {offender}.{reason}\n\n"
                "{participants}:\nVote by reacting with ✅ to kick {offender}, "
                "or ignore this message to vote **No**.\n\n"
                "You have **2 minutes** to vote. A majority vote ({req}/{tot}) is required.\n"
                "{initiator} your vote is automatically counted. Votes by users not in your channel will be ignored."
                "".format(
                    initiator=author.mention,
                    offender=user.mention,
                    reason=(" Reason: **{}**".format(reason) if reason else ""),
                    participants=' '.join([m.mention for m in participants]),
                    req=required_votes,
                    tot=len(participants) + 1
                )
            )
            if not participants:
                text = "..."
            m = await ctx['message'].channel.send(text)
        except discord.errors.Forbidden:
            return False, "I don't have permission to reply to your kick command."
        cfg.VOTEKICKS[m.id] = {
            "initiator": author,
            "participants": participants,
            "required_votes": required_votes,
            "offender": user,
            "reason": reason,
            "in_favor": [author],
            "voice_channel": vc,
            "message": m,
            "end_time": time() + 120
        }
        try:
            if participants:
                await m.add_reaction('✅')
        except discord.errors.Forbidden:
            pass
        await func.server_log(
            guild,
            "👢 {} (`{}`) initiated a votekick against **{}** (`{}`) in \"**{}**\". Reason: *{}*.".format(
                func.user_hash(author), author.id, func.user_hash(user), user.id, vc.name, reason
            ), 1, settings)
        return True, "NO RESPONSE"
    else:
        await name.move_to(None) #kicking try
        try:
            text = (
                "‼ **Kick Reminder** ‼\n"
                "{initiator} Kicked {offender} for {reason}\n\n"
                "".format(
                    initiator=author.mention,
                    offender=user.mention,
                    reason=(" Reason: **{}**".format(reason) if reason else ""),
                )
            )
            if not channelcreator:
                text = "wut the dog doin?"
            m = await ctx['message'].channel.send(text)
        except discord.errors.Forbidden:
            return False, "I don't have permission to reply to your kick command."
        try:
            print('kicking')
        except discord.errors.Forbidden:
            pass
        await func.server_log(
            guild,
            "👢 {} (`{}`) initiated a kick against **{}** (`{}`) in \"**{}**\". Reason: *{}*.".format(
                func.user_hash(author), author.id, func.user_hash(user), user.id, vc.name, reason
            ), 1, settings)
        return True, "NO RESPONSE"
        

command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=1,
    admin_required=False,
    voice_required=True,
)
