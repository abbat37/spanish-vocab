"""
Script to populate the database with Spanish vocabulary words and sentence templates
Run this once to initialize the database with data
"""
from database import db, VocabularyWord, SentenceTemplate

# Your existing word database
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

SENTENCE_TEMPLATES = {
    'cooking': {
        'verb': [
            ('Me gusta {word} todos los días para mi familia.', 'I like to {word} every day for my family.'),
            ('Necesito {word} los ingredientes antes de empezar.', 'I need to {word} the ingredients before starting.'),
            ('Mi abuela sabe {word} platos increíbles.', 'My grandmother knows how to {word} incredible dishes.'),
            ('Voy a {word} algo especial esta noche.', 'I\'m going to {word} something special tonight.'),
            ('Es importante {word} con cuidado.', 'It\'s important to {word} carefully.')
        ],
        'noun': [
            ('Necesito comprar un/una {word} nuevo/a para la cocina.', 'I need to buy a new {word} for the kitchen.'),
            ('El/La {word} está sobre la mesa.', 'The {word} is on the table.'),
            ('Mi {word} favorito/a es de acero inoxidable.', 'My favorite {word} is stainless steel.'),
            ('No puedo encontrar el/la {word} que necesito.', 'I can\'t find the {word} I need.'),
            ('Este/a {word} es muy útil para cocinar.', 'This {word} is very useful for cooking.')
        ],
        'adj': [
            ('La comida está muy {word} hoy.', 'The food is very {word} today.'),
            ('Prefiero los platos {word} en el verano.', 'I prefer {word} dishes in the summer.'),
            ('Este sabor es demasiado {word} para mí.', 'This flavor is too {word} for me.'),
            ('La receta quedó perfectamente {word}.', 'The recipe turned out perfectly {word}.'),
            ('Me encanta cuando está {word} y caliente.', 'I love when it\'s {word} and hot.')
        ]
    },
    'work': {
        'verb': [
            ('Tengo que {word} con el equipo mañana.', 'I have to {word} with the team tomorrow.'),
            ('Vamos a {word} el nuevo proyecto.', 'We\'re going to {word} the new project.'),
            ('Es necesario {word} los recursos eficientemente.', 'It\'s necessary to {word} resources efficiently.'),
            ('Quiero {word} mis habilidades profesionales.', 'I want to {word} my professional skills.'),
            ('Debemos {word} antes del viernes.', 'We must {word} before Friday.')
        ],
        'noun': [
            ('Tenemos un/una {word} importante el lunes.', 'We have an important {word} on Monday.'),
            ('El/La {word} requiere mucha atención.', 'The {word} requires a lot of attention.'),
            ('Mi {word} es muy colaborativo/a.', 'My {word} is very collaborative.'),
            ('Debo revisar el/la {word} antes de firmarlo/a.', 'I must review the {word} before signing it.'),
            ('La {word} nueva está en el centro de la ciudad.', 'The new {word} is in the city center.')
        ],
        'adj': [
            ('Este proceso es muy {word}.', 'This process is very {word}.'),
            ('Necesitamos ser más {word} en nuestro trabajo.', 'We need to be more {word} in our work.'),
            ('El ambiente es bastante {word}.', 'The environment is quite {word}.'),
            ('Fue un proyecto muy {word} para todos.', 'It was a very {word} project for everyone.'),
            ('Tu actitud es muy {word} en la oficina.', 'Your attitude is very {word} in the office.')
        ]
    },
    'sports': {
        'verb': [
            ('Me gusta {word} todas las mañanas.', 'I like to {word} every morning.'),
            ('El equipo va a {word} este fin de semana.', 'The team is going to {word} this weekend.'),
            ('Necesito {word} más para mejorar.', 'I need to {word} more to improve.'),
            ('Quiero {word} el balón con más fuerza.', 'I want to {word} the ball with more force.'),
            ('Vamos a {word} en el campeonato nacional.', 'We\'re going to {word} in the national championship.')
        ],
        'noun': [
            ('El/La {word} fue muy emocionante.', 'The {word} was very exciting.'),
            ('Nuestro/a {word} es el/la mejor de la liga.', 'Our {word} is the best in the league.'),
            ('Conseguí un/una {word} de oro.', 'I got a gold {word}.'),
            ('El/La {word} está lleno/a de aficionados.', 'The {word} is full of fans.'),
            ('Mi {word} favorito/a juega para el Barcelona.', 'My favorite {word} plays for Barcelona.')
        ],
        'adj': [
            ('Ese jugador es muy {word}.', 'That player is very {word}.'),
            ('Necesitas ser más {word} en la cancha.', 'You need to be more {word} on the court.'),
            ('El entrenamiento fue muy {word} hoy.', 'The training was very {word} today.'),
            ('Su estilo de juego es {word} y efectivo.', 'His playing style is {word} and effective.'),
            ('Es un atleta {word} y dedicado.', 'He\'s a {word} and dedicated athlete.')
        ]
    },
    'restaurant': {
        'verb': [
            ('Voy a {word} el pescado del día.', 'I\'m going to {word} the fish of the day.'),
            ('Quiero {word} una mesa para dos.', 'I want to {word} a table for two.'),
            ('El mesero va a {word} el vino.', 'The waiter is going to {word} the wine.'),
            ('Me gustaría {word} el plato especial.', 'I would like to {word} the special dish.'),
            ('Debemos {word} unos minutos más.', 'We must {word} a few more minutes.')
        ],
        'noun': [
            ('El/La {word} tiene muchas opciones deliciosas.', 'The {word} has many delicious options.'),
            ('Llamé al/a la {word} para pedir la cuenta.', 'I called the {word} to ask for the bill.'),
            ('La {word} fue muy razonable.', 'The {word} was very reasonable.'),
            ('Debo dejar una {word} generosa.', 'I should leave a generous {word}.'),
            ('Hice una {word} para las ocho.', 'I made a {word} for eight o\'clock.')
        ],
        'adj': [
            ('Este restaurante es muy {word}.', 'This restaurant is very {word}.'),
            ('El plato estaba {word} y bien presentado.', 'The dish was {word} and well presented.'),
            ('El servicio fue un poco {word} esta noche.', 'The service was a bit {word} tonight.'),
            ('La decoración es muy {word} y elegante.', 'The decoration is very {word} and elegant.'),
            ('Es un lugar {word} entre los turistas.', 'It\'s a {word} place among tourists.')
        ]
    }
}


def seed_vocabulary():
    """Populate vocabulary words table"""
    print("Seeding vocabulary words...")
    count = 0

    for theme, word_types in WORD_DATABASE.items():
        for word_type, words in word_types.items():
            for word_entry in words:
                # Parse "spanish_word (english translation)"
                spanish_word = word_entry.split(' (')[0]
                english_translation = word_entry.split('(')[1].rstrip(')')

                # Check if word already exists to avoid duplicates
                existing = VocabularyWord.query.filter_by(
                    theme=theme,
                    word_type=word_type,
                    spanish_word=spanish_word
                ).first()

                if not existing:
                    vocab = VocabularyWord(
                        theme=theme,
                        word_type=word_type,
                        spanish_word=spanish_word,
                        english_translation=english_translation
                    )
                    db.session.add(vocab)
                    count += 1

    db.session.commit()
    print(f"✓ Added {count} vocabulary words")


def seed_sentence_templates():
    """Populate sentence templates table"""
    print("Seeding sentence templates...")
    count = 0

    for theme, word_types in SENTENCE_TEMPLATES.items():
        for word_type, templates in word_types.items():
            for spanish_template, english_template in templates:
                # Check if template already exists to avoid duplicates
                existing = SentenceTemplate.query.filter_by(
                    theme=theme,
                    word_type=word_type,
                    spanish_template=spanish_template
                ).first()

                if not existing:
                    template = SentenceTemplate(
                        theme=theme,
                        word_type=word_type,
                        spanish_template=spanish_template,
                        english_template=english_template
                    )
                    db.session.add(template)
                    count += 1

    db.session.commit()
    print(f"✓ Added {count} sentence templates")


def seed_database():
    """Main function to seed the database - requires app context"""
    from app import app

    with app.app_context():
        # Check if database is already seeded
        existing_words = VocabularyWord.query.count()
        if existing_words > 0:
            print(f"Database already contains {existing_words} words.")
            response = input("Do you want to clear and reseed? (yes/no): ")
            if response.lower() != 'yes':
                print("Seeding cancelled.")
                return

            # Clear existing data
            print("Clearing existing data...")
            db.session.query(VocabularyWord).delete()
            db.session.query(SentenceTemplate).delete()
            db.session.commit()

        # Seed the database
        seed_vocabulary()
        seed_sentence_templates()

        print("\n✅ Database seeded successfully!")
        print(f"Total words: {VocabularyWord.query.count()}")
        print(f"Total templates: {SentenceTemplate.query.count()}")


if __name__ == '__main__':
    seed_database()
