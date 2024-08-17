document.getElementById('chat-form').addEventListener('submit', async function (event) {
    event.preventDefault();
    const messageInput = document.getElementById('message');
    const categorySelect = document.getElementById('category');
    const message = messageInput.value;
    const category = categorySelect.value;

    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message, category }),
    });

    const data = await response.json();
    const chatHistory = document.getElementById('chat-history');
    chatHistory.innerHTML += `<div class="chat-entry user">${message}</div>`;
    chatHistory.innerHTML += `<div class="chat-entry bot">${data.response}</div>`;

    const audio = new Audio(data.audio);
    audio.play();

    messageInput.value = '';
});

document.getElementById('appointment-booking-form').addEventListener('submit', async function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData);

    const response = await fetch('/book-appointment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    const result = await response.json();
    alert(result.message);
});

document.getElementById('reference-details-form').addEventListener('submit', async function (event) {
    event.preventDefault();
    const referenceNumber = document.getElementById('reference-number').value;

    const response = await fetch(`/reference/${referenceNumber}`);
    const result = await response.json();
    alert(result.message);
});
