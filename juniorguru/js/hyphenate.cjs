/*
  This file is used by 'jg web post-process' to hyphenate
  the '.document' part of HTML files.
*/
const readline = require('node:readline');
const { stdin, stdout } = require('node:process');
const { hyphenateHTMLSync } = require("hyphen/cs");


const rl = readline.createInterface({ input: stdin, output: stdout });
lines = []
rl.on('line', (line) => {
  lines.push(line);
});
rl.on('close', () => {
  const html = lines.join('\n');
  console.log(hyphenateHTMLSync(html));
});
