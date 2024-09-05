post_message_listener_src = '''
// Listen for messages from the iframe
window.addEventListener('message', function(event) {
    if (event.data.type === 'showMessage') {
        let error_message = document.getElementById('error-message')
        error_message.style.display = 'block';
        let heal_data = document.getElementById('heal_data')
        let content = JSON.stringify(event.data.content)
        heal_data.value = content
    }
});
'''