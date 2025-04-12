import discord
from discord.ext import commands
import asyncio

import os
TOKEN = os.getenv("TOKEN")  # 从环境变量读取 Bot Token  # ✅ 替换为你的真实 Token

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# 自动建房配置：点击创建频道的 ID
CREATE_RANK_CHANNEL_ID = 1360597969887563877  # 替换为“点击创建排位房”频道 ID
CREATE_MATCH_CHANNEL_ID = 1360598156492148858  # 替换为“点击创建匹配房”频道 ID

@bot.event
async def on_ready():
    print(f'✅ Bot 已上线：{bot.user}')

@bot.command(name="pw", aliases=["pp"])
async def create_room(ctx, *args):
    if len(args) == 0:
        await ctx.send("⚠️ 请输入人数信息，例如：`!pw 3=2` 或 `!pw 钻石超凡 3=2`")
        return

    if len(args) == 1:
        rank = "未指定"
        count = args[0]
    else:
        rank = args[0]
        count = args[1]

    author = ctx.author
    voice_channel = author.voice.channel if author.voice else None

    # 房间类型判断
    room_type = "匹配房" if ctx.invoked_with == "pp" else "排位房"

    # 自动识别频道类型
    def get_channel_type(name: str) -> str:
        if any(kw in name for kw in ["游戏", "game"]):
            return "🎮 游戏区"
        elif any(kw in name for kw in ["开黑", "组队", "黑"]):
            return "🧑‍🤝‍🧑 开黑房"
        elif "匹配" in name:
            return "🤖 匹配频道"
        elif "排位" in name:
            return "🏆 排位频道"
        return "🎧 语音频道"

    channel_type = get_channel_type(voice_channel.name) if voice_channel else "🎧 未加入"

    # 创建嵌入消息
    embed = discord.Embed(
        title=f"🎮 {room_type} - {rank} {count}",
        color=discord.Color.blurple(),
        description="———————————————\n点击下方按钮加入语音频道\n———————————————"
    )

    if author.avatar:
        embed.set_thumbnail(url=author.avatar.url)

    if voice_channel:
        embed.add_field(
            name=f"{channel_type}:",
            value=f"[🔊 {voice_channel.name}](https://discord.com/channels/{ctx.guild.id}/{voice_channel.id})",
            inline=False
        )

        members = [member.mention for member in voice_channel.members]
        embed.add_field(
            name="👥 当前成员:",
            value="\n".join(members) if members else "暂无其他成员",
            inline=False
        )
    else:
        embed.add_field(name="🎧 语音频道:", value="❌ 未加入语音频道", inline=False)

    embed.add_field(name="🙋 发起人:", value=author.mention, inline=True)
    embed.add_field(name="⏰ 使用时间:", value="刚刚", inline=True)

    view = discord.ui.View()
    if voice_channel:
        view.add_item(discord.ui.Button(label="🔊 加入语音频道", url=f"https://discord.com/channels/{ctx.guild.id}/{voice_channel.id}"))

    await ctx.send(embed=embed, view=view)

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is None or before.channel == after.channel:
        return

    if after.channel.id in [CREATE_RANK_CHANNEL_ID, CREATE_MATCH_CHANNEL_ID]:
        guild = member.guild
        if after.channel.id == CREATE_RANK_CHANNEL_ID:
            room_name = f"排位 - {member.display_name}"
        else:
            room_name = f"匹配 - {member.display_name}"

        new_channel = await guild.create_voice_channel(
            name=room_name,
            category=after.channel.category,
            bitrate=64000,
            user_limit=5
        )

        await member.move_to(new_channel)

        while True:
            await asyncio.sleep(30)
            if len(new_channel.members) == 0:
                await new_channel.delete()
                break

bot.run(TOKEN)
