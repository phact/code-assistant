scroll_script_src = '''
document.addEventListener('DOMContentLoaded', function() {
    // Function to auto-scroll chat to the bottom on new message
    function scrollToBottom() {
        const chatList = document.getElementById('chatlist');
        if (chatList) {
            chatList.scrollTop = chatList.scrollHeight;
        }
    }
    
    // Observe mutations in the chatlist to auto-scroll
    const chatListElement = document.getElementById('chatlist');
    if (chatListElement) {
        const observer = new MutationObserver(scrollToBottom);
        observer.observe(chatListElement, { childList: true });
    }
});
'''