document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const nav = document.querySelector('nav');
    
    if (mobileMenuBtn && nav) {
        mobileMenuBtn.addEventListener('click', function() {
            nav.classList.toggle('show');
        });
    }


    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            nav.classList.remove('show');
        });
    });

    const purchaseBtns = document.querySelectorAll('.purchase-btn');
    const modal = document.getElementById('purchase-modal');
    const modalToolName = document.getElementById('modal-tool-name');
    const modalToolPrice = document.getElementById('modal-tool-price');
    const closeModal = document.querySelector('.close-modal');

    if (purchaseBtns.length && modal) {
        purchaseBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const toolName = this.getAttribute('data-tool');
                const toolPrice = this.parentElement.querySelector('.tool-price').textContent;
                
                modalToolName.textContent = toolName;
                modalToolPrice.textContent = toolPrice;
                modal.style.display = 'flex';
                document.body.style.overflow = 'hidden'; 
            });
        });

        closeModal.addEventListener('click', function() {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        });

        window.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    }

    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault(); 
            
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const statusEl = document.getElementById('statusContact');
            const formElements = contactForm.elements;

            submitBtn.disabled = true;
            statusEl.textContent = 'Sending message...';
            statusEl.style.color = 'var(--secondary-color)';

            try {
                const formData = {
                    name: formElements.name.value.trim(),
                    email: formElements.email.value.trim(),
                    message: formElements.message.value.trim()
                };

                if (!formData.name || !formData.email || !formData.message) {
                    throw new Error('Please fill in all required fields');
                }

                if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
                    throw new Error('Please enter a valid email address');
                }
                const response = await fetch('https://soulstoolsreal.pythonanywhere.com/api/v1/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });

                const responseText = await response.text();
                const data = responseText ? JSON.parse(responseText) : {};

                if (!response.ok) {
                    throw new Error(data.error || `Server error: ${response.status}`);
                }

                statusEl.textContent = `Message sent successfully! ID: ${data.id}`;
                statusEl.style.color = 'var(--success-color)';
                contactForm.reset();

            } catch (error) {
                statusEl.textContent = `Error: ${error.message}`;
                statusEl.style.color = 'var(--error-color)';
                console.error('Submission error:', error);
            } finally {
                submitBtn.disabled = false;
            }
        });
    }

    const currentPage = location.pathname.split('/').pop() || 'index.html';
    const links = document.querySelectorAll('nav a');
    
    links.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
});

const blooks = [
    "1#0#1#0#1$3#0#0#1#6#0#0$0", "Old Boot", "Jellyfish", "Clownfish", "Frog", "Crab", "Pufferfish", "Blobfish", "Octopus", "Narwhal", "Dolphin", "Baby Shark", "Megalodon", "Snowy Owl", "Polar Bear", "Arctic Fox", "Baby Penguin", "Penguin", "Arctic Hare", "Seal", "Walrus", "Snow Globe", "Holiday Gift", "Hot Chocolate", "Holiday Wreath", "Stocking", "Gingerbread Man", "Gingerbread House", "Reindeer", "Snowman", "Santa Claus", "Lil Bot", "Lovely Bot", "Angry Bot", "Happy Bot", "Watson", "Buddy Bot", "Brainy Bot", "Mega Bot", "Toast", "Cereal", "Yogurt", "Breakfast Combo", "Orange Juice", "Milk", "Waffle", "Pancakes", "French Toast", "Pizza", "Light Blue", "Black", "Red", "Purple", "Pink", "Orange", "Lime", "Green", "Teal", "Tan", "Maroon", "Gray", "Mint", "Salmon", "Burgandy", "Baby Blue", "Dust", "Brown", "Dull Blue", "Yellow", "Blue", "Amber", "Dino Egg", "Dino Fossil", "Stegosaurus", "Velociraptor", "Brontosaurus", "Triceratops", "Tyrannosaurus Rex", "Chick", "Chicken", "Cow", "Goat", "Horse", "Pig", "Sheep", "Duck", "Alpaca", "Bear", "Moose", "Fox", "Raccoon", "Squirrel", "Owl", "Hedgehog", "Deer", "Wolf", "Beaver", "Rainbow Jellyfish", "Blizzard Clownfish", "Lovely Frog", "Lucky Frog", "Spring Frog", "Poison Dart Frog", "Lucky Hamster", "Chocolate Rabbit", "Lemon Crab", "Pirate Pufferfish", "Donut Blobfish", "Crimson Octopus", "Rainbow Narwhal", "Frost Wreath", "Tropical Globe", "New York Snow Globe", "London Snow Globe", "Japan Snow Globe", "Egypt Snow Globe", "Paris Snow Globe", "Red Sweater Snowman", "Blue Sweater Snowman", "Elf Sweater Snowman", "Santa Claws", "Cookies Combo", "Chilly Flamingo", "Snowy Bush Monster", "Nutcracker Koala", "Sandwich", "Ice Slime", "Frozen Fossil", "Ice Crab", "Rainbow Panda", "White Peacock", "Tiger Zebra", "Teal Platypus", "Red Astronaut", "Orange Astronaut", "Yellow Astronaut", "Lime Astronaut", "Green Astronaut", "Cyan Astronaut", "Blue Astronaut", "Pink Astronaut", "Purple Astronaut", "Brown Astronaut", "Black Astronaut", "Lovely Planet", "Lovely Peacock", "Haunted Pumpkin", "Pumpkin Cookie", "Ghost Cookie", "Red Gummy Bear", "Blue Gummy Bear", "Green Gummy Bear", "Chick Chicken", "Chicken Chick", "Raccoon Bandit", "Owl Sheriff", "Vampire Frog", "Pumpkin King", "Anaconda Wizard", "Spooky Pumpkin", "Spooky Mummy", "Agent Owl", "Master Elf", "Party Pig", "Wise Owl", "Spooky Ghost", "Phantom King", "Tim the Alien", "Rainbow Astronaut", "Hamsta Claus", "Ice Bat", "Ice Bug", "Ice Elemental", "Rock Monster", "Dink", "Donk", "Bush Monster", "Yeti", "Witch", "Wizard", "Elf", "Fairy", "Slime Monster", "Jester", "Dragon", "Queen", "Unicorn", "King", "Dingo", "Echidna", "Koala", "Kookaburra", "Platypus", "Joey", "Kangaroo", "Crocodile", "Sugar Glider", "Dog", "Cat", "Rabbit", "Goldfish", "Hamster", "Turtle", "Kitten", "Puppy", "Panda", "Sloth", "Tenrec", "Flamingo", "Zebra", "Elephant", "Lemur", "Peacock", "Chameleon", "Lion", "Earth", "Meteor", "Stars", "Alien", "Planet", "UFO", "Spaceship", "Astronaut", "Pumpkin", "Swamp Monster", "Frankenstein", "Vampire", "Zombie", "Mummy", "Caramel Apple", "Candy Corn", "Werewolf", "Ghost", "Tiger", "Orangutan", "Cockatoo", "Parrot", "Anaconda", "Jaguar", "Macaw", "Toucan", "Panther", "Capuchin", "Gorilla", "Hippo", "Rhino", "Giraffe", "Two of Spades", "Eat Me", "Drink Me", "Alice", "Queen of Hearts", "Dormouse", "White Rabbit", "Cheshire Cat", "Caterpillar", "Mad Hatter", "King of Hearts", "Deckhand", "Buccaneer", "Swashbuckler", "Treasure Map", "Seagull", "Jolly Pirate", "Pirate Ship", "Kraken", "Captain Blackbeard"
       ];
   
       const blookInput = document.getElementById('blookInput');
       const blooksList = document.getElementById('blooksList');
   
       // Populate datalist with blook options
       blooks.forEach(blook => {
           const option = document.createElement('option');
           option.value = blook;
           blooksList.appendChild(option);
       });
   
       // Add input filtering
       blookInput.addEventListener('input', function() {
           const inputValue = this.value.toLowerCase();
           const options = blooksList.querySelectorAll('option');
           
           // Show matching options
           options.forEach(option => {
               if (option.value.toLowerCase().includes(inputValue)) {
                   option.hidden = false;
               } else {
                   option.hidden = true;
               }
           });
       });
   
       // Add click handler to show all options when clicked
       blookInput.addEventListener('click', function() {
           if (this.value === '') {
               const options = blooksList.querySelectorAll('option');
               options.forEach(option => option.hidden = false);
           }
       });
   
           function randomLetters() {
           const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
           let result = '';
           for (let k = 0; k < 2; k++) {
               result += chars.charAt(Math.floor(Math.random() * chars.length));
           }
           return result;
       }
   
       async function send() {
           const gameId = document.getElementById('gcode').value.trim();
           const baseName = `\x20` + `\x20` + document.getElementById('gname').value.trim();
           const numBots = parseInt(document.getElementById('gnum').value);
           const selectedBlook = document.getElementById('blookInput').value;
           const bypassFilter = document.getElementById('bcf').hasAttribute('checked');
           const botMsg = document.getElementById('botmsg').value.trim();
           
           const log = document.getElementById('log');
           log.innerHTML = "Starting flood...<br>";
           
           
           if (isNaN(numBots) || numBots < 1 || numBots > 500) {
               log.innerHTML += "❌ Please enter a valid number of bots (1-500).<br>";
               return;
           }
           
           document.getElementById('status').textContent = "Status: Flooding...";
           
           const batchSize = 50;
           const delayBetweenBatches = 500;
           
           for (let i = 0; i < numBots; i += batchSize) {
               const currentBatchSize = Math.min(batchSize, numBots - i);
               const batchPromises = [];
               
               for (let j = 0; j < currentBatchSize; j++) {
                   const botName = String.fromCharCode(32) + String.fromCharCode(32) + `${baseName}${randomLetters()}`;
                   batchPromises.push(sendBot(gameId, botName, selectedBlook, bypassFilter, botMsg, log));
               }
               
               await Promise.all(batchPromises);
               await new Promise(resolve => setTimeout(resolve, delayBetweenBatches));
           }
           
           log.innerHTML += `<br>🎉 Successfully sent ${numBots} bots to game ${gameId}!`;
           document.getElementById('status').textContent = "Status: Flood complete!";
       }
   
       async function sendBot(gameId, botName, blook, bypassFilter, botMsg, log) {
           try {
               let submitName = botName;
               
   if (bypassFilter) {
       submitName = botName
           .replace(/a/g, "\u0430")  // Cyrillic 'а'
           .replace(/c/g, "\u0441")  // Cyrillic 'с'
           .replace(/e/g, "\u0435")  // Cyrillic 'е'
           .replace(/i/g, "\u0456")  // Cyrillic 'і'
           .replace(/o/g, "\u043E")  // Cyrillic 'о'
           .replace(/p/g, "\u0440")  // Cyrillic 'р'
           .replace(/s/g, "\u0455")  // Cyrillic 'ѕ'
           .replace(/x/g, "\u0445")   // Cyrillic 'х'
           .replace(/y/g, "\u0443")   // Cyrillic 'у'
           .replace(/A/g, "\u0410")   // Cyrillic 'А'
           .replace(/B/g, "\u0412")   // Cyrillic 'В'
           .replace(/C/g, "\u0421")   // Cyrillic 'С'
           .replace(/E/g, "\u0415")   // Cyrillic 'Е'
           .replace(/H/g, "\u041D")   // Cyrillic 'Н'
           .replace(/I/g, "\u0406")   // Cyrillic 'І'
           .replace(/K/g, "\u039A")   // Greek 'Κ'
           .replace(/M/g, "\u041C")   // Cyrillic 'М'
           .replace(/O/g, "\u041E")   // Cyrillic 'О'
           .replace(/P/g, "\u0420")   // Cyrillic 'Р'
           .replace(/S/g, "\u0405")   // Cyrillic 'Ѕ'
           .replace(/T/g, "\u0422")   // Cyrillic 'Т'
           .replace(/X/g, "\u0425")   // Cyrillic 'Х'
           .replace(/Y/g, "\u03A5");  // Greek 'Υ'
   
   
   }
   
               const response = await fetch("https://shard-uttermost-crystal.glitch.me/proxy/https://blooketbot.me/join", {
                   method: "POST",
                   headers: { "Content-Type": "application/json" },
                   body: JSON.stringify({ 
                       id: gameId, 
                       name: submitName
                   })
               });
               
               const data = await response.json();
               
               if (data.success) {
                   const liveApp = firebase.initializeApp({
                       apiKey: "AIzaSyCA-cTOnX19f6LFnDVVsHXya3k6ByP_MnU",
                       authDomain: "blooket-2020.firebaseapp.com",
                       projectId: "blooket-2020",
                       storageBucket: "blooket-2020.appspot.com",
                       messagingSenderId: "741533559105",
                       appId: "1:741533559105:web:b8cbb10e6123f2913519c0",
                       databaseURL: data.fbShardURL
                   }, `app_${Math.random().toString(36).substring(7)}`);
                   
                   await firebase.auth(liveApp).signInWithCustomToken(data.fbToken);
                   const db = firebase.database(liveApp);            
                   await db.ref(`${gameId}/c/${submitName}`).set({ 
                       b: blook,
                       cr: botMsg,
                       g: botMsg,
                       f: botMsg,
                       w: botMsg,
                       d: botMsg,
                       xp: botMsg,
                       c: botMsg,
                       ca: botMsg,
                   });
                    if (blook) {                
                   await db.ref(`${gameId}/c/${submitName}`).set({ 
                       b: blook,
   
                   })} else { await db.ref(`${gameId}/c/${submitName}`).set({ 
                       b: "Mega Bot",
   
                   })};
   
   
                   
                   
                   log.innerHTML += `✅ ${botName} joined successfully<br>`;
               } else {
                   log.innerHTML += `⚠️ ${botName} failed: ${data.msg || "Unknown error"}<br>`;
               }
           } catch (error) {
               log.innerHTML += `❌ Error with ${botName}: ${error.message}<br>`;
           }
       }
