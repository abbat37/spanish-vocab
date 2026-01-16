from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Dictionary of Spanish words by theme and type
WORD_DATABASE = {
    'cooking': {
        'verb': ['cocinar (to cook)', 'hornear (to bake)', 'freír (to fry)', 'hervir (to boil)', 'mezclar (to mix)',
                 'cortar (to cut)', 'pelar (to peel)', 'batir (to beat/whisk)', 'asar (to roast)', 'sazonar (to season)'],
        'noun': ['sartén (pan)', 'cuchillo (knife)', 'receta (recipe)', 'horno (oven)', 'ingrediente (ingredient)',
                 'olla (pot)', 'tabla (cutting board)', 'especias (spices)', 'sabor (flavor)', 'masa (dough)'],
        'adj': ['picante (spicy)', 'dulce (sweet)', 'salado (salty)', 'crujiente (crispy)', 'jugoso (juicy)',
                'amargo (bitter)', 'fresco (fresh)', 'cocido (cooked)', 'delicioso (delicious)', 'aromático (aromatic)']
    },
    'work': {
        'verb': ['trabajar (to work)', 'colaborar (to collaborate)', 'presentar (to present)', 'gestionar (to manage)',
                 'negociar (to negotiate)', 'capacitar (to train)', 'planificar (to plan)', 'delegar (to delegate)',
                 'coordinar (to coordinate)', 'evaluar (to evaluate)'],
        'noun': ['reunión (meeting)', 'proyecto (project)', 'equipo (team)', 'contrato (contract)', 'oficina (office)',
                 'plazo (deadline)', 'jefe (boss)', 'colega (colleague)', 'informe (report)', 'presupuesto (budget)'],
        'adj': ['eficiente (efficient)', 'productivo (productive)', 'profesional (professional)', 'urgente (urgent)',
                'complejo (complex)', 'exitoso (successful)', 'exigente (demanding)', 'flexible (flexible)',
                'responsable (responsible)', 'innovador (innovative)']
    },
    'sports': {
        'verb': ['entrenar (to train)', 'competir (to compete)', 'ganar (to win)', 'correr (to run)', 'saltar (to jump)',
                 'lanzar (to throw)', 'anotar (to score)', 'defender (to defend)', 'nadar (to swim)', 'patear (to kick)'],
        'noun': ['partido (match)', 'equipo (team)', 'entrenador (coach)', 'victoria (victory)', 'campeón (champion)',
                 'pelota (ball)', 'estadio (stadium)', 'jugador (player)', 'medalla (medal)', 'torneo (tournament)'],
        'adj': ['atlético (athletic)', 'rápido (fast)', 'fuerte (strong)', 'competitivo (competitive)', 'ágil (agile)',
                'resistente (resistant)', 'veloz (swift)', 'estratégico (strategic)', 'dinámico (dynamic)', 'hábil (skillful)']
    },
    'restaurant': {
        'verb': ['pedir (to order)', 'reservar (to reserve)', 'servir (to serve)', 'recomendar (to recommend)',
                 'probar (to taste)', 'pagar (to pay)', 'disfrutar (to enjoy)', 'elegir (to choose)',
                 'preparar (to prepare)', 'esperar (to wait)'],
        'noun': ['menú (menu)', 'mesero (waiter)', 'cuenta (bill)', 'propina (tip)', 'reservación (reservation)',
                 'plato (dish)', 'entrada (appetizer)', 'postre (dessert)', 'bebida (drink)', 'chef (chef)'],
        'adj': ['sabroso (tasty)', 'caro (expensive)', 'económico (affordable)', 'lento (slow)', 'rápido (fast)',
                'exquisito (exquisite)', 'tradicional (traditional)', 'moderno (modern)', 'acogedor (cozy)', 'popular (popular)']
    }
}

# Example sentences templates
SENTENCE_TEMPLATES = {
    'cooking': {
        'verb': [
            'Me gusta {word} todos los días para mi familia.',
            'Necesito {word} los ingredientes antes de empezar.',
            'Mi abuela sabe {word} platos increíbles.',
            'Voy a {word} algo especial esta noche.',
            'Es importante {word} con cuidado.'
        ],
        'noun': [
            'Necesito comprar un/una {word} nuevo/a para la cocina.',
            'El/La {word} está sobre la mesa.',
            'Mi {word} favorito/a es de acero inoxidable.',
            'No puedo encontrar el/la {word} que necesito.',
            'Este/a {word} es muy útil para cocinar.'
        ],
        'adj': [
            'La comida está muy {word} hoy.',
            'Prefiero los platos {word} en el verano.',
            'Este sabor es demasiado {word} para mí.',
            'La receta quedó perfectamente {word}.',
            'Me encanta cuando está {word} y caliente.'
        ]
    },
    'work': {
        'verb': [
            'Tengo que {word} con el equipo mañana.',
            'Vamos a {word} el nuevo proyecto.',
            'Es necesario {word} los recursos eficientemente.',
            'Quiero {word} mis habilidades profesionales.',
            'Debemos {word} antes del viernes.'
        ],
        'noun': [
            'Tenemos un/una {word} importante el lunes.',
            'El/La {word} requiere mucha atención.',
            'Mi {word} es muy colaborativo/a.',
            'Debo revisar el/la {word} antes de firmarlo/a.',
            'La {word} nueva está en el centro de la ciudad.'
        ],
        'adj': [
            'Este proceso es muy {word}.',
            'Necesitamos ser más {word} en nuestro trabajo.',
            'El ambiente es bastante {word}.',
            'Fue un proyecto muy {word} para todos.',
            'Tu actitud es muy {word} en la oficina.'
        ]
    },
    'sports': {
        'verb': [
            'Me gusta {word} todas las mañanas.',
            'El equipo va a {word} este fin de semana.',
            'Necesito {word} más para mejorar.',
            'Quiero {word} el balón con más fuerza.',
            'Vamos a {word} en el campeonato nacional.'
        ],
        'noun': [
            'El/La {word} fue muy emocionante.',
            'Nuestro/a {word} es el/la mejor de la liga.',
            'Conseguí un/una {word} de oro.',
            'El/La {word} está lleno/a de aficionados.',
            'Mi {word} favorito/a juega para el Barcelona.'
        ],
        'adj': [
            'Ese jugador es muy {word}.',
            'Necesitas ser más {word} en la cancha.',
            'El entrenamiento fue muy {word} hoy.',
            'Su estilo de juego es {word} y efectivo.',
            'Es un atleta {word} y dedicado.'
        ]
    },
    'restaurant': {
        'verb': [
            'Voy a {word} el pescado del día.',
            'Quiero {word} una mesa para dos.',
            'El mesero va a {word} el vino.',
            'Me gustaría {word} el plato especial.',
            'Debemos {word} unos minutos más.'
        ],
        'noun': [
            'El/La {word} tiene muchas opciones deliciosas.',
            'Llamé al/a la {word} para pedir la cuenta.',
            'La {word} fue muy razonable.',
            'Debo dejar una {word} generosa.',
            'Hice una {word} para las ocho.'
        ],
        'adj': [
            'Este restaurante es muy {word}.',
            'El plato estaba {word} y bien presentado.',
            'El servicio fue un poco {word} esta noche.',
            'La decoración es muy {word} y elegante.',
            'Es un lugar {word} entre los turistas.'
        ]
    }
}

# English translations for sentences
ENGLISH_TRANSLATIONS = {
    'cooking': {
        'verb': [
            'I like to {word} every day for my family.',
            'I need to {word} the ingredients before starting.',
            'My grandmother knows how to {word} incredible dishes.',
            'I\'m going to {word} something special tonight.',
            'It\'s important to {word} carefully.'
        ],
        'noun': [
            'I need to buy a new {word} for the kitchen.',
            'The {word} is on the table.',
            'My favorite {word} is stainless steel.',
            'I can\'t find the {word} I need.',
            'This {word} is very useful for cooking.'
        ],
        'adj': [
            'The food is very {word} today.',
            'I prefer {word} dishes in the summer.',
            'This flavor is too {word} for me.',
            'The recipe turned out perfectly {word}.',
            'I love when it\'s {word} and hot.'
        ]
    },
    'work': {
        'verb': [
            'I have to {word} with the team tomorrow.',
            'We\'re going to {word} the new project.',
            'It\'s necessary to {word} resources efficiently.',
            'I want to {word} my professional skills.',
            'We must {word} before Friday.'
        ],
        'noun': [
            'We have an important {word} on Monday.',
            'The {word} requires a lot of attention.',
            'My {word} is very collaborative.',
            'I must review the {word} before signing it.',
            'The new {word} is in the city center.'
        ],
        'adj': [
            'This process is very {word}.',
            'We need to be more {word} in our work.',
            'The environment is quite {word}.',
            'It was a very {word} project for everyone.',
            'Your attitude is very {word} in the office.'
        ]
    },
    'sports': {
        'verb': [
            'I like to {word} every morning.',
            'The team is going to {word} this weekend.',
            'I need to {word} more to improve.',
            'I want to {word} the ball with more force.',
            'We\'re going to {word} in the national championship.'
        ],
        'noun': [
            'The {word} was very exciting.',
            'Our {word} is the best in the league.',
            'I got a gold {word}.',
            'The {word} is full of fans.',
            'My favorite {word} plays for Barcelona.'
        ],
        'adj': [
            'That player is very {word}.',
            'You need to be more {word} on the court.',
            'The training was very {word} today.',
            'His playing style is {word} and effective.',
            'He\'s a {word} and dedicated athlete.'
        ]
    },
    'restaurant': {
        'verb': [
            'I\'m going to {word} the fish of the day.',
            'I want to {word} a table for two.',
            'The waiter is going to {word} the wine.',
            'I would like to {word} the special dish.',
            'We must {word} a few more minutes.'
        ],
        'noun': [
            'The {word} has many delicious options.',
            'I called the {word} to ask for the bill.',
            'The {word} was very reasonable.',
            'I should leave a generous {word}.',
            'I made a {word} for eight o\'clock.'
        ],
        'adj': [
            'This restaurant is very {word}.',
            'The dish was {word} and well presented.',
            'The service was a bit {word} tonight.',
            'The decoration is very {word} and elegant.',
            'It\'s a {word} place among tourists.'
        ]
    }
}

def generate_sentences(theme, word_type):
    """Generate 5 sentences with new Spanish words"""
    if theme not in WORD_DATABASE or word_type not in WORD_DATABASE[theme]:
        return []

    words = WORD_DATABASE[theme][word_type]
    templates_spanish = SENTENCE_TEMPLATES[theme][word_type]
    templates_english = ENGLISH_TRANSLATIONS[theme][word_type]

    # Select 5 random words
    selected_words = random.sample(words, min(5, len(words)))

    sentences = []
    for i, word in enumerate(selected_words):
        # Extract the Spanish word and English translation
        spanish_word = word.split(' (')[0]
        english_word = word.split('(')[1].rstrip(')')

        # Create Spanish sentence
        spanish_sentence = templates_spanish[i].replace('{word}', f'<mark>{spanish_word}</mark>')

        # Create English sentence
        english_sentence = templates_english[i].replace('{word}', f'<mark>{english_word}</mark>')

        sentences.append({
            'spanish': spanish_sentence,
            'english': english_sentence
        })

    return sentences

@app.after_request
def add_header(response):
    """Add headers to prevent caching during development"""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    sentences = []
    theme = ''
    word_type = ''

    if request.method == 'POST':
        theme = request.form.get('theme', '').lower()
        word_type = request.form.get('word_type', '').lower()

        if theme and word_type:
            sentences = generate_sentences(theme, word_type)

    return render_template('index.html', sentences=sentences, theme=theme, word_type=word_type)

if __name__ == '__main__':
    app.run(debug=True)
