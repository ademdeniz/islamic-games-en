# Otkrij skrivenu sliku -> Reveal the Hidden Picture (solo: right answers uncover 80 tiles over an animal picture;
# guess the animal for a bonus). Shared Ilmihal question bank (_ilmihal_bank.translate); the 68 animal pictures
# (name, description, kind – the kind is also the answer to “Which animal is hiding?”) are translated in transform().
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _ilmihal_bank  # noqa: E402

DELETE = ['<footer>Pripremio Abdo ef. Rekić • Radi bez interneta</footer>']

T = [
    ('<html lang="bs">', '<html lang="en">'),
    ('<title>Otkrij skrivenu sliku – Ilmihal</title>', '<title>Reveal the Hidden Picture</title>'),
    ('<h1>🧩 Otkrij skrivenu sliku</h1><p style="text-align:center">80 polja • pitanja iz Ilmihala</p>',
     '<h1>🧩 Reveal the Hidden Picture</h1><p style="text-align:center">80 tiles • questions from the Ilmihal</p>'),
    ('Odaberi nivo pitanja i broj slika. Svaki tačan odgovor otkriva jedno polje!', 'Choose the question level and the number of pictures. Every right answer uncovers one tile!'),
    ('<label>Nivo <select id="level"><option value="ALL">Svi nivoi</option>', '<label>Level <select id="level"><option value="ALL">All levels</option>'),
    ('<label>Slike <select', '<label>Pictures <select'), ('<option value="all">Sve</option>', '<option value="all">All</option>'),
    ('▶ Započni', '▶ Start'), ('⬇ Preuzmi HTML', '⬇ Download the game'),
    ('<div>Slika<b id="round">1/10</b></div><div>Bodovi<b id="points">0</b></div><div>Otkriveno<b id="opened">0/80</b></div>',
     '<div>Picture<b id="round">1/10</b></div><div>Points<b id="points">0</b></div><div>Uncovered<b id="opened">0/80</b></div>'),
    ('alt="Skrivena životinja"', 'alt="A hidden animal"'),
    ('<p class="hint" id="hint">Tačan odgovor otkriva jedno polje.</p>', '<p class="hint" id="hint">A right answer uncovers one tile.</p>'),
    ('🔎 Pogodi životinju', '🔎 Guess the animal'), ('⏭ Preskoči sliku', '⏭ Skip this picture'),
    ('<button id="mute" class="light">🔊 Zvuk</button>', '<button id="mute" class="light">🔊 Sound</button>'),
    ('<p>Koja se životinja krije na slici?</p>', '<p>Which animal is hiding in the picture?</p>'),
    ('alt="Otkrivena slika"', 'alt="The picture uncovered"'),
    ('<button id="next" class="gold">➡ Sljedeća slika</button><button id="home" class="light">🏠 Početak</button>',
     '<button id="next" class="gold">➡ Next picture</button><button id="home" class="light">🏠 Start page</button>'),
    ("'✅ Tačno! Otkriveno je jedno polje.'", "'✅ Correct! One tile is uncovered.'"),
    ("'❌ Netačno. Tačan odgovor: '+q.a[q.c]", "'❌ Wrong. The right answer: '+q.a[q.c]"),
    ("'Odgovaraj na pitanja i otkrij 80 polja.'", "'Answer the questions and uncover the 80 tiles.'"),
    ("solved?'🎉 Bravo, pogodio/la si!':'👀 Otkrivena slika'", "solved?'🎉 Well done, you got it!':'👀 The picture uncovered'"),
    ("'Bodovi: '+score+' • Otkrivena polja: '+shown+'/80'", "'Points: '+score+' • Tiles uncovered: '+shown+'/80'"),
    ("pos===queue.length-1?'🏆 Završni rezultat':'➡ Sljedeća slika'", "pos===queue.length-1?'🏆 Final result':'➡ Next picture'"),
    ("BANK.length+' pitanja • '+PICTURES.length+' slika'", "BANK.length+' questions • '+PICTURES.length+' pictures'"),
    ("sound?'🔊 Zvuk':'🔇 Bez zvuka'", "sound?'🔊 Sound':'🔇 No sound'"),
    ("'🏆 Završeno! Osvojeno bodova: '+score", "'🏆 All done! Your points: '+score"),
    ("a.download='otkrij-skrivenu-sliku-ilmihal.html'", "a.download='reveal-the-hidden-picture.html'"),
]

KIND = {'jež': 'hedgehog', 'kornjača': 'tortoise', 'pas': 'dog', 'mačka': 'cat', 'krava': 'cow', 'guska': 'goose', 'panda': 'panda',
        'magarac': 'donkey', 'vrana': 'crow', 'sova': 'owl', 'morski pas': 'shark', 'rak': 'lobster', 'roda': 'stork', 'paun': 'peacock',
        'tigar': 'tiger', 'žirafa': 'giraffe', 'vjeverica': 'squirrel', 'lisica': 'fox', 'deva': 'camel', 'lama': 'llama', 'patka': 'duck',
        'golub': 'pigeon', 'jelen': 'deer', 'koza': 'goat', 'ćuran': 'turkey', 'fazan': 'pheasant', 'gusjenica': 'caterpillar', 'zec': 'rabbit',
        'majmun': 'monkey', 'skakavac': 'grasshopper', 'leptir': 'butterfly', 'hobotnica': 'octopus', 'zebra': 'zebra', 'nosorog': 'rhino',
        'noj': 'ostrich', 'zmija': 'snake', 'krtica': 'mole', 'koala': 'koala', 'slon': 'elephant', 'bubamara': 'ladybird', 'pčela': 'bee',
        'medvjed': 'bear', 'leopard': 'leopard', 'polarni medvjed': 'polar bear', 'pingvin': 'penguin', 'delfin': 'dolphin', 'mrav': 'ant',
        'žaba': 'frog', 'pelikan': 'pelican'}
PICS = [
    ('Hedgehog', 'A little hedgehog spreads its paws and smiles happily.'), ('Tortoise', 'A green tortoise with a brown shell and big eyes.'),
    ('Puppy', 'A happy white and brown puppy sits and wags its tail.'), ('Kitten', 'A grey striped kitten with green eyes and white paws.'),
    ('Cow', 'A white and brown cow eats grass and wears a bell.'), ('Goose', 'A white goose stands by the water.'),
    ('Panda', 'A black and white panda sits among the bamboo.'), ('Donkey', 'A grey donkey stands happily in front of the barn.'),
    ('Cow on the farm', 'A brown and white cow stands in front of a red barn.'), ('Crow with a crown', 'A black bird with a golden crown sits on a branch.'),
    ('Owl', 'A brown owl with big eyes sits on a branch.'), ('Shark', 'A grey shark swims among little fish.'),
    ('Lobster', 'A red lobster with claws stands on the sea floor.'), ('Stork', 'A tall bird with long legs stands by the water.'),
    ('Peacock', 'A colourful peacock shows off its beautiful feathers.'), ('Tiger', 'An orange tiger with black stripes walks through the forest.'),
    ('Giraffe', 'A little giraffe with a long neck stands in a meadow.'), ('Squirrel on a branch', 'A brown squirrel sits on a tree branch.'),
    ('Fox', 'An orange fox peeks out from behind a tree.'), ('Camel', 'A camel with a hump stands among desert plants.'),
    ('Llama', 'A white llama stands in a green meadow.'), ('Duck', 'A duck with a green head swims on the water.'),
    ('Pigeon', 'A grey pigeon sits on a branch.'), ('Deer', 'A deer with antlers stands among the trees.'),
    ('Goat', 'A white goat stands on a rock in the mountains.'), ('Turkey', 'A turkey spreads its big fan-shaped tail.'),
    ('Pheasant', 'A colourful bird with a long tail stands in the grass.'), ('Hedgehog in the leaves', 'A brown hedgehog surrounded by autumn leaves.'),
    ('Hedgehog with apples', 'A little hedgehog carries apples on its spines.'), ('Squirrel with an acorn', 'A squirrel sits on a branch holding an acorn.'),
    ('Caterpillar on a branch', 'A green caterpillar smiles among the butterflies.'), ('Tortoise among the flowers', 'A green tortoise walks through a colourful flower meadow.'),
    ('Rabbit in its little house', 'A white rabbit looks out of the window of its little house.'), ('Kitten in the meadow', 'An orange kitten plays among the butterflies.'),
    ('Duckling on the lake', 'A yellow duckling swims on the lake.'), ('Monkey on a branch', 'A brown monkey hangs from a branch among the butterflies.'),
    ('Grasshopper', 'A green grasshopper sits on the grass by a bridge.'), ('Butterfly on a flower', 'A colourful butterfly lands on a pink flower.'),
    ('Octopus', 'An orange octopus has eight arms.'), ('Zebra among the butterflies', 'A little zebra sits in a flower meadow.'),
    ('Rhino', 'A grey rhino with a horn sits on the grass.'), ('Ostrich among the flowers', 'A tall bird with a long neck stands in a colourful garden.'),
    ('Snake', 'A colourful snake is curled up among the flowers.'), ('Zebra in the meadow', 'A black and white zebra stands among the trees.'),
    ('Fawn', 'A young fawn with white spots stands in a mountain meadow.'), ('Cow among the flowers', 'A white cow with dark patches stands in a meadow.'),
    ('Mole', 'A little grey mole sits among the flowers.'), ('Koala', 'A grey koala in a colourful cap sits in the garden.'),
    ('Ostrich in the meadow', 'A big bird with long legs stands in a green meadow.'), ('Elephant and squirrel', 'A little elephant plays with a squirrel in the forest.'),
    ('Ladybird', 'A red ladybird with black spots sits on a mushroom.'), ('Bee on a flower', 'A yellow bee flies up to a white flower.'),
    ('Bee with an umbrella', 'A happy bee carries a little basket and a colourful umbrella.'), ('Kitten in a basket', 'An orange kitten sits in a woven basket.'),
    ('Little elephant with balloons', 'A little grey elephant holds colourful balloons.'), ('Bunny with balloons', 'An orange bunny holds a few balloons.'),
    ('Teddy bear with balloons', 'A yellow teddy bear holds colourful balloons.'), ('Caterpillar on a leaf', 'A green caterpillar rests on a big leaf.'),
    ('Leopard', 'A big spotted cat rests on a branch.'), ('Bear with a fish', 'A brown bear sits holding a fish.'),
    ('Polar bears', 'A white mother bear and her cub sit on the ice.'), ('Penguins', 'A penguin stands with its chick on the ice.'),
    ('Dolphin', 'A grey dolphin jumps out of the blue water.'), ('Ant', 'A red ant carries a big piece of wood.'),
    ('Elephant in a boat', 'A grey elephant rows a red boat.'), ('Frog', 'A green frog sits on a water-lily leaf.'),
    ('Ostrich and butterflies', 'An ostrich walks through a flower meadow among the butterflies.'), ('Pelican', 'A pelican with a big orange beak stands on the seashore.'),
]


def transform(src):
    src = _ilmihal_bank.translate(src)
    i = src.index('const PICTURES=') + len('const PICTURES=')
    pics, end = json.JSONDecoder().raw_decode(src, i)
    assert len(pics) == len(PICS)
    for p, (name, desc) in zip(pics, PICS):
        p['name'], p['desc'], p['kind'] = name, desc, KIND[p['kind']]
    return src[:i] + _ilmihal_bank._dumps(pics, src[i:end]) + src[end:]
