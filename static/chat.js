const socket = io();
const username = window.currentUsername;  // make sure it's set in chat.html

const input = document.getElementById("msg");
const chatBox = document.getElementById("chat-box");

socket.on('message', data => {
    const p = document.createElement('p');
    p.innerHTML = `<strong>${data.user}:</strong> ${data.msg}`;
    chatBox.appendChild(p);
    chatBox.scrollTop = chatBox.scrollHeight;
});

input.addEventListener("keypress", function (e) {
    if (e.key === "Enter" && input.value.trim() !== "") {
        const messageData = {
            msg: input.value.trim(),
            user: username
        };
        console.log("Sending:", messageData);
        socket.emit("chat_message", messageData);
        input.value = "";
    }
});
