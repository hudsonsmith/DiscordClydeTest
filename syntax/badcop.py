from syntax.cap import cap

def syntax_badcop(reply) -> str:
    reply = reply.replace("||", "")
    reply = cap(reply)
    reply = f"<:: {reply} ::>"
    print(reply)

    return reply