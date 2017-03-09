# taigabot
When you use Slack to communicate about Epics/Stories/Tasks/Issues and just mention tg#1 this tiny little bot will fetch you the details to Taiga Item#1. You don't have to care about wether it's an Epic, a Story, a Task or an Issue, just mention the Taiga item with this pattern (you can also choose to use TG#1, tG#1, Tg#1) and the bot replies with the details.

## Getting started
Just fill in the connection details in /resources/env.files and you are good to go.
- bot.env.tmpl shows the structure of the file Slack bot settings, copy it to bot.env and fill the details in
- taiga.env.tmpl shows the structure of the file for the Taiga connection, copy it to taiga.env and fill the details in
