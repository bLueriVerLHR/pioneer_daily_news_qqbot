import nonebot
import nonebot.adapters.onebot.v11 as obot
import nonebot.matcher
import nonebot.rule
import nonebot.params

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class DailyArticleInfo(BaseModel):
    name: str
    url: str
    time: str


vdb = []


async def user_checker(event: obot.Event) -> bool:
    return event.get_user_id() == "3465287429"


rule = nonebot.rule.Rule(user_checker)
matcher = nonebot.on_command("today", rule=rule)


@matcher.handle()
async def handle_first_receive(matcher: nonebot.matcher.Matcher, args: obot.Message = nonebot.params.CommandArg()):
    if len(vdb) > 0:
        await matcher.send(f"name:{vdb[-1]['name']}\nurl:{vdb[-1]['url']}\ntime:{vdb[-1]['time']}")


app: FastAPI = nonebot.get_app()


@app.post("/api/send_article")
async def update_item(item: DailyArticleInfo):
    json_compatible_item_data = jsonable_encoder(item)
    print(json_compatible_item_data)
    vdb.append(json_compatible_item_data)

