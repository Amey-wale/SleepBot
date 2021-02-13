# importing important libraries required
import discord
# for embedColour
import random
from discord.ext import commands
# for menus
from dpymenus import Page, PaginatedMenu
# for getting answers from codegrepper
import aiohttp
import typing
import json

class CodeHelp(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(name = 'ask',
        aliases = ['get', 'getcode'],
        help = 'Fetch code from CodeGrepper, Takes in No. of results (default 3) and the question.')
    async def ask(self,ctx, result_limit: typing.Optional[int] = 3, *, term: str=None):
        embedColour = random.randint(0, 0xffffff)
        if term!=None:
            googlequery=term
            q=googlequery.replace(" ","+")
            cq=googlequery.replace(" ","%20")
            searchurl='https://www.google.com/search?q='+q
            originurl='https://www.codegrepper.com/search.php?q='+cq
            # print(searchurl,q)

            # The initial embed which shows what you searched for
            startEmbed = discord.Embed(
                title ="You asked",
                description =f'{term} \n [source]({originurl})',
                colour=embedColour
            )
            startEmbed.set_author(name=ctx.message.author,icon_url=ctx.message.author.avatar_url)
            # print(term)
            # List which will contain the results
            results=[]
            # fetch results from codegrepper
            async with aiohttp.ClientSession() as session:
                async with session.get('https://www.codegrepper.com/api/search.php', params ={"q":term}) as r :
                    result = await r.json()
                results=result['answers']

                answerEmbed=discord.Embed(
                    title='Answers',
                    colour=embedColour
                )
            # print(len(results),'length')
            # embed.set_footer(text=f'{ctx.message}')
            print(len(results))
            # If less than 1 result stored, send notFoundEmbed
            if len(results)<1:
                notFoundEmbed=discord.Embed(
                    title="Answer Not Found",
                    description=f'''[Search yourself]({searchurl})
                    \nYou can also contribute to this by installing [codegrepper](https://www.codegrepper.com/) extension and marking an answer when you find it
                    ''',
                    colour=embedColour
                    
                )
                await ctx.send(embed=startEmbed)
                await ctx.send(embed=notFoundEmbed)
            # if there is exactly 1 result, send directly instead of using pages
            elif len(results)==1:
                print(len(results))
                await ctx.send(embed=startEmbed)
                data=results
                resultList = []
                for i in range(len(data)):
                    # print(i)
                    # print(i['answer'])
                    if i >= result_limit :
                        break
                    j=data[i]
                    ans = j['answer']
                    lang =j['language']
                    source=" "
                    source=j['source_url']
                    print(source,"source")
                    answer=f'```{lang}\n {ans}```'
                    answerEmbed=discord.Embed(
                        # name="name",
                        description=answer,
                        colour=embedColour
                    )
                notGotEmbed=discord.Embed(
                title=":frowning2: Did Not Find Your Answer?",
                description=f'''[Search yourself]({searchurl})
                \nYou can also contribute to this by installing [codegrepper](https://www.codegrepper.com/) extension and marking an answer when you find it
                ''',
                colour=embedColour
                )
                await ctx.send(embed=answerEmbed)
                await ctx.send(embed=notGotEmbed)
            # if more than or equal to 2 results, make multiple embeds and send a menu
            elif len(results)>=2:
                await ctx.send(embed=startEmbed)
                data=results
                resultList = []
                for i in range(len(data)):
                    # print(i)
                    # print(i['answer'])
                    if i >= result_limit :
                        break
                    j=data[i]
                    ans = j['answer']
                    lang =j['language']
                    source=" "
                    source=j['source_url']
                    print(source,"source")
                    answer=f'```{lang}\n {ans}```'
                    answerEmbed=discord.Embed(
                        # name="name",
                        description=answer,
                        colour=embedColour
                    )
                    # add the embed to resultList
                    resultList.append(answerEmbed)
                    #await ctx.send(embed=answerEmbed)
                notGotEmbed=discord.Embed(
                title=":frowning2: Did Not Find Your Answer?",
                description=f'''[Search yourself]({searchurl})
                \nYou can also contribute to this by installing [codegrepper](https://www.codegrepper.com/) extension and marking an answer when you find it
                ''',
                colour=embedColour
                )
                # page related stuff
                menu = PaginatedMenu(ctx)
                menu.add_pages(resultList)
                menu.set_timeout(30)
                menu.show_command_message()
                menu.persist_on_close()
                menu.show_page_numbers()
                menu.show_skip_buttons()
                menu.allow_multisession()
                await menu.open()
                print('menu opened')
                await ctx.send(embed=notGotEmbed)
            else:
                pass
        # if no argument is passed
        else:
            noargEmbed=discord.Embed(
                    title="Ask Something, it can't be blank",
                    description='''
                    something expected
                    `?ask what you want to ask`
                    ''',
                    colour=embedColour
                )
            await ctx.send(embed=noargEmbed)
        # await ctx.send(answer)


def setup(client):
    client.add_cog(CodeHelp(client))
