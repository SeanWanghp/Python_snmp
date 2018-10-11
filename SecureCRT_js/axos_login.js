var authour = 'sean_wang'
var command = ['idle-timeout 0', 'pag false', 'show file content core', 'show ala active']
var cli_in = 'cli'
var PROMPT = '# '
var ENTER = '\n'

crt.Screen.WaitForString(PROMPT);
crt.Screen.Send(cli_in + ENTER);
crt.Screen.WaitForString(PROMPT);

function main() {

	for (var i in command) {
		crt.Screen.Send (command[i] + ENTER);
		crt.Screen.WaitForString(PROMPT);
	  
	}
	crt.Sleep(1000)
}