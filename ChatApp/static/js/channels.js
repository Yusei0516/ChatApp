// open chat 要素の作成

const ul = document.querySelector(".channel-box");
channels.forEach(channel) 
{
const a = document.createElement("a");
const li = document.createElement("li");
const channelURL =`/channels/${open_chat_id}/messages`;
a.innerText = channnel.name;
a.setAttribute("href", channelURL);
li.appendChild(a);
}
