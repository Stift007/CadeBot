import nextcord
import random

client = nextcord.AutoShardedClient()

@client.slash_command(name="rps", description="Play a Game of Rock, Paper, Scissor")
async def rps(interaction:nextcord.Interaction, action = nextcord.SlashOption(name="action",description="Your Action", required=True, choices={
    "Rock":"rock",
    "Paper":"paper",
    "Scissors":"scissors",})):
    
    cpu_choice = random.choice(["rock", "paper", "scissors"])
    if cpu_choice == action:
        resembed = nextcord.Embed(title="It's a Tie!")
        resembed.description = f'We both picked {action.capitalize()}'
    elif cpu_choice == "rock" and action == "paper":
        resembed = nextcord.Embed(title="You win!")
        resembed.description = f'You picked {action.capitalize()} and I chose {cpu_choice}'
        
    elif cpu_choice == "rock" and action == "scissors":
        resembed = nextcord.Embed(title="I win!")
        resembed.description = f'You picked {action.capitalize()} and I chose {cpu_choice}'
    
    elif cpu_choice == "paper" and action == "scissors":
        resembed = nextcord.Embed(title="You win!")
        resembed.description = f'You picked {action.capitalize()} and I chose {cpu_choice}'
        
    elif cpu_choice == "paper" and action == "rock":
        resembed = nextcord.Embed(title="I win!")
        resembed.description = f'You picked {action.capitalize()} and I chose {cpu_choice}'
    
    elif cpu_choice == "scissors" and action == "rock":
        resembed = nextcord.Embed(title="You win!")
        resembed.description = f'You picked {action.capitalize()} and I chose {cpu_choice}'
        
    elif cpu_choice == "scissors" and action == "paper":
        resembed = nextcord.Embed(title="I win!")
        resembed.description = f'You picked {action.capitalize()} and I chose {cpu_choice}'
    
    
    await interaction.response.send_message(embed = resembed)




client.run("OTEyNzQ1Mjc1NzcxMjE1OTUy.YZ0aRw.0MEWLF_9UZsTGacbxH91Zx1vu-g",reconnect=True)