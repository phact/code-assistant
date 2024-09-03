css_text = '''
    [contenteditable]:focus {
        outline: 0px solid transparent;
    }
    .container {
        margin: 3vw !important;
        width: 96vw !important;
        max-width: none !important;
    }
    .flex-container {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 2rem;
    }
    .flex-item {
        flex: 1;
        box-sizing: border-box;
    }
    .code-output {
        height:50vh;
        padding: 1rem;
        overflow-y: auto;
        margin-bottom: 1rem;
    }
    .spinner {
        display: none;
    }
    .spinner.visible {
        display: block;
    }
    .file-content {
        max-height: 50vh; 
        min-height: 500px;
        height: 100vh;
        margin-top: 1rem;
        padding: 1rem;
        width: 60vw;
        overflow-x: auto;
        overflow-y: auto;
    }
    .file-content.hidden {
        display: none;
    }
    pre {
        background: transparent !important;
        //height: 28px !important;
        overflow: hidden !important;
        width: fit-content;
    }
    pre>code {
        display: inline-block !important;
        padding: 0 !important;
    }
   .mockup-code pre:before {
       margin-right: 0;
       width: 0;
   }
   h1 {
       font-size: var(--pico-font-size) !important;
       margin-bottom: 1rem !important;
       font-weight: 400 !important;
       padding: 2vh !important;
   }
   .toggle{
       width: 3rem !important;
       height: 1.5rem !important;
   }
 
)
'''
