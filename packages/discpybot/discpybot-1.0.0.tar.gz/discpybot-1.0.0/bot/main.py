import typer
import os
import requests
from requests.structures import CaseInsensitiveDict

main_file = requests.get('https://raw.githubusercontent.com/DAARKKIBOI/bot-template/master/bot.py')
mod_file = requests.get('https://raw.githubusercontent.com/DAARKKIBOI/bot-template/master/cogs/moderation.py')
snipe_file = requests.get('https://raw.githubusercontent.com/DAARKKIBOI/bot-template/master/cogs/snipe.py')




app = typer.Typer()

@app.command()
def install_requirements():
    os.system('pip install -r requirements.txt')
    
    
@app.command()
def setup():
    print('Generating template...')
    os.mkdir('bot')
    if os.path.exists('./bot/cogs'):
        pass
    else:
        os.mkdir('./bot/cogs')
    with open('./bot/bot.py', 'w') as f:
        f.write(main_file.text)
    with open('./bot/cogs/moderation.py', 'w') as f:
        f.write(mod_file.text)
    with open('./bot/cogs/snipe.py', 'w') as f:
        f.write(snipe_file.text)
    
    
if __name__ == '__main__':
    app()