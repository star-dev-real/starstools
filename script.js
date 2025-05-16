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

blooks.forEach(blook => {
    const option = document.createElement('option');
    option.value = blook;
    blooksList.appendChild(option);
});

blookInput.addEventListener('input', function() {
    const inputValue = this.value.toLowerCase();
    blooksList.querySelectorAll('option').forEach(option => {
        option.hidden = !option.value.toLowerCase().includes(inputValue);
    });
});

blookInput.addEventListener('click', function() {
    if (this.value === '') {
        blooksList.querySelectorAll('option').forEach(option => option.hidden = false);
    }
});

function randomLetters() {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    return Array.from({length: 2}, () => chars[Math.floor(Math.random() * chars.length)]).join('');
}

async function send() {
    const gameId = document.getElementById('gcode').value.trim();
    const baseName = `  ${document.getElementById('gname').value.trim()}`;
    const numBots = parseInt(document.getElementById('gnum').value);
    const selectedBlook = document.getElementById('blookInput').value;
    const bypassFilter = document.getElementById('bcf').checked;
    const botMsg = document.getElementById('botmsg').value.trim();
    const log = document.getElementById('log');
    
    log.innerHTML = "Starting flood...<br>";
    document.getElementById('status').textContent = "Status: Initializing...";

    if (!gameId) {
        log.innerHTML += "❌ Please enter a valid Game ID<br>";
        return;
    }

    if (isNaN(numBots) || numBots < 1 || numBots > 500) {
        log.innerHTML += "❌ Invalid number of bots (1-500)<br>";
        return;
    }

    const batchSize = 50;
    const delayBetweenBatches = 1000;
    let successCount = 0;

    try {
        for (let i = 0; i < numBots; i += batchSize) {
            const currentBatchSize = Math.min(batchSize, numBots - i);
            const batchPromises = [];
            
            for (let j = 0; j < currentBatchSize; j++) {
                const botName = `${baseName}${randomLetters()}`;
                batchPromises.push(sendBot(gameId, botName, selectedBlook, bypassFilter, botMsg, log));
            }

            await Promise.all(batchPromises);
            successCount += currentBatchSize;
            log.innerHTML += `✅ Sent ${currentBatchSize} bots (Total: ${successCount})<br>`;
            await new Promise(resolve => setTimeout(resolve, delayBetweenBatches));
        }

        log.innerHTML += `<br>🎉 Successfully sent ${successCount} bots!`;
        document.getElementById('status').textContent = "Status: Flood complete!";

    } catch (error) {
        log.innerHTML += `<br>❌ Critical error: ${error.message}<br>`;
        document.getElementById('status').textContent = "Status: Error occurred!";
    }
}

async function sendBot(gameId, botName, blook, bypassFilter, botMsg, log) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 8000);

    try {
        let submitName = botName;
        
        if (bypassFilter) {
            submitName = botName.replace(/[aceiopstxyABCEHIKMOPSXY]/g, char => {
                const replacements = {
                    'a': '\u0430', 'c': '\u0441', 'e': '\u0435', 'i': '\u0456',
                    'o': '\u043E', 'p': '\u0440', 's': '\u0455', 't': '\u0442',
                    'x': '\u0445', 'y': '\u0443', 'A': '\u0410', 'B': '\u0412',
                    'C': '\u0421', 'E': '\u0415', 'H': '\u041D', 'I': '\u0406',
                    'K': '\u039A', 'M': '\u041C', 'O': '\u041E', 'P': '\u0420',
                    'S': '\u0405', 'T': '\u0422', 'X': '\u0425', 'Y': '\u03A5'
                };
                return replacements[char] || char;
            });
        }

        const response = await fetch("https://shard-uttermost-crystal.glitch.me/proxy/https://blooketbot.me/join", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: gameId, name: submitName }),
            signal: controller.signal
        });
        clearTimeout(timeoutId);

        const responseText = await response.text();
        let data;
        try {
            data = JSON.parse(responseText);
        } catch {
            throw new Error('Invalid server response');
        }

        if (!response.ok || !data.success) {
            throw new Error(data.msg || `HTTP error ${response.status}`);
        }

        const liveApp = firebase.initializeApp({
            apiKey: "AIzaSyCA-cTOnX19f6LFnDVVsHXya3k6ByP_MnU",
            authDomain: "blooket-2020.firebaseapp.com",
            projectId: "blooket-2020",
            storageBucket: "blooket-2020.appspot.com",
            messagingSenderId: "741533559105",
            appId: "1:741533559105:web:b8cbb10e6123f2913519c0",
            databaseURL: data.fbShardURL
        }, `app_${Math.random().toString(36).slice(2)}`);

        await firebase.auth(liveApp).signInWithCustomToken(data.fbToken);
        const db = firebase.database(liveApp);
        
        await db.ref(`${gameId}/c/${submitName}`).update({
            b: blook || "Mega Bot",
            cr: botMsg,
            g: botMsg,
            f: botMsg,
            w: botMsg,
            d: botMsg,
            xp: botMsg,
            c: botMsg,
            ca: botMsg
        });

        return true;

    } catch (error) {
        log.innerHTML += `❌ ${botName}: ${error.message.substring(0, 50)}<br>`;
        return false;
    } finally {
        if (firebase.apps.length > 1) {
            firebase.apps[1].delete();
        }
    }
}


    document.querySelectorAll('.purchase-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const toolCard = this.closest('.tool-card');
            const toolName = this.dataset.tool;
            const toolPrice = toolCard.querySelector('.tool-price').textContent;
            const toolImage = toolCard.querySelector('.tool-image').style.backgroundImage
                              .replace(/url\(['"]?(.*?)['"]?\)/, '$1');

            const params = new URLSearchParams({
                tool: toolName,
                price: toolPrice,
                image: encodeURIComponent(toolImage)
            });

            window.location.href = `purchase.html?${params.toString()}`;
        });
    });

    const currentPage = location.pathname.split('/').pop() || 'index.html';
    const links = document.querySelectorAll('nav a');
    
    links.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });


function generateInvoiceId() {
    return 'INV-' + Math.random().toString(36).substr(2, 9).toUpperCase();
}

function processPayment() {
    const email = document.getElementById('email').value;
    const paymentMethod = document.querySelector('input[name="payment"]:checked');
    const invoiceId = generateInvoiceId();
    const invoiceDetails = {
        email: email,
        paymentMethod: paymentMethod ? paymentMethod.value : 'Not specified',
        invoiceId: invoiceId
    };
    const setInvoice = document.getElementById('invoice-id');

    setInvoice.innerHTML = `${invoiceId}`;
}

if(window.location.pathname.includes('purchase.html')) {
    document.addEventListener('DOMContentLoaded', function() {
        const urlParams = new URLSearchParams(window.location.search);
        const toolName = urlParams.get('tool') || 'Selected Tool';
        const toolPrice = urlParams.get('price') || '£0.00';
        const toolImage = decodeURIComponent(urlParams.get('image') || '');

        document.getElementById('purchase-tool-name').textContent = toolName;
        document.getElementById('purchase-tool-price').textContent = toolPrice;
        if(toolImage) {
            document.getElementById('purchase-tool-image').style.backgroundImage = `url('${toolImage}')`;
        }

        document.getElementById('email').addEventListener('input', function(e) {
            if(e.target.value.includes('@')) {
                document.getElementById('invoice-id').textContent = generateInvoiceId();
            }
        });
    });
}

const paypalBody = `
<html lang="en">

<head>
    <meta charset="UTF-8">
    <script src="https://www.paypalobjects.com/api/checkout.js"></script>
    <link rel="stylesheet" href="https://cdn.discordapp.com/attachments/658099251947110442/658320443740258305/css.css">
    <title>Paypal Proofs Generator</title>
</head>
<style>
  * {
    overflow: hidden;
  }
</style>
<body>
    <div class="payout">
        <img src="https://cdn.discordapp.com/attachments/658059622929924096/658416971406245899/checkout_paypal.png">

        <br><br>

        <p>You've sent {{VALUEPRICE}} to {{VALUEEMAIL}}</p>

        <br><br><br>

        <div class="header__nav--right">
            <div class="dx-auth-block profile__container">
                <div class="dx-auth-logged-out">
                    <a style="width: 50%; height: 8%; font-size: 18px;" href="#" class="css-1qlw6jl vx_btn vx_btn-block">Send More Money</a>
                </div>
            </div>
        </div>

        <a href="#" onclick="goHome()"><b>Go to Summary</b></a>
    <script>
        goHome = () => {
            window.location = "index.html"
        } 
    </script>
</body>

</html>
`
paypalProofGen = () => {
    const price = document.getElementById("price").value
    const category = document.getElementById("category").value
    const email = document.getElementById("email").value

    let valuePrice = ""
    if (category == "eur") {
        valuePrice = `${price} EUR`
    } else if (category == "usd") {
        valuePrice = `$${price} USD`
    } else if (category == "gpb") {
        valuePrice = `Â£${price} GPB`
    }


    document.write(paypalBody.replace("{{VALUEPRICE}}", valuePrice).replace("{{VALUEEMAIL}}", email))
}