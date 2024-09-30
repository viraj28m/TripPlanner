// Get the tags and input elements from the DOM 
const tags = document.getElementById('tags'); 
const input = document.getElementById('input-tag'); 

function createTag(tagContent){
    // If the trimmed value is not an empty string 
    const tag = document.createElement('li'); 
    if (tagContent !== '') { 
    
        // Set the text content of the tag to  
        // the trimmed value 
        tag.innerText = tagContent; 

        tag.classList.add("location-preference-tag");

        // Add a delete button to the tag 
        tag.innerHTML += '<button class="delete-button">X</button>'; 
        
        // Append the tag to the tags list 
        tags.appendChild(tag); 
        
        // await new Promise(r => setTimeout(r, 50));
        // // Clear the input element's value 
        // await new Promise(r => setTimeout(r, 50));
        input.value = ''; 
    } 
}

// Add an event listener for keydown on the input element 
input.addEventListener('keydown', async function (event) { 

    // Check if the key pressed is 'Enter' 
    if (event.key === 'Enter') { 
    
        // Prevent the default action of the keypress 
        // event (submitting the form) 
        event.preventDefault(); 
    
        // Create a new list item element for the tag 
        const tag = document.createElement('li'); 

        tag.classList.add('location-preference-tag')
    
        // Get the trimmed value of the input element 
        const tagContent = input.value.trim(); 

        createTag(tagContent);
    } 
}); 

// Add an event listener for click on the tags list 
tags.addEventListener('click', function (event) { 

    // If the clicked element has the class 'delete-button' 
    if (event.target.classList.contains('delete-button')) { 
    
        // Remove the parent element (the tag) 
        event.target.parentNode.remove(); 
    } 
}); 