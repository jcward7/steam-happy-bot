const { SlashCommandBuilder } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('server')
		.setDescription('Starts a server.'),
	async execute(interaction) {

		const { spawn } = require('child_process');
		//const batFilePath = 'C:\Users\moist\Desktop\steamhappy-bot';
		const child = spawn('cmd.exe', ['/k', 'runserver.bat'], {});

		await interaction.reply(`Server is now starting.`);

		child.stdout.on('data', (data) => {
			console.log(`${data}`);
		});

		child.stderr.on('data', (data) => {
			console.log(`ERROR: ${data}`);
		});

		child.on('close', (code) => {
			console.log(`child process exited with code ${code}`);
		});

	},
};
