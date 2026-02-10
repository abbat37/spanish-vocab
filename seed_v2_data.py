"""
Seed V2 Database
Creates sample vocabulary words and examples for testing
"""
from app import create_app
from app.shared.extensions import db
from app.shared.models import User
from app.v2.models import V2Word, V2GeneratedExample

app = create_app()

with app.app_context():
    # Get or create a test user
    user = User.query.filter_by(email='test@example.com').first()
    if not user:
        user = User(email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        print(f"Created test user: {user.email}")
    else:
        print(f"Using existing user: {user.email}")

    # Clear existing V2 data for this user
    V2Word.query.filter_by(user_id=user.id).delete()
    db.session.commit()

    # Seed data: 15 words with varied types and themes
    words_data = [
        # Content words
        {
            'spanish': 'cocinar',
            'english': 'to cook',
            'word_type': 'verb',
            'themes': 'food,home',
            'examples': [
                ('Me gusta cocinar con mi familia los domingos.', 'I like to cook with my family on Sundays.'),
                ('Ella sabe cocinar muy bien.', 'She knows how to cook very well.'),
                ('Voy a cocinar pasta esta noche.', 'I am going to cook pasta tonight.')
            ]
        },
        {
            'spanish': 'frío',
            'english': 'cold',
            'word_type': 'adjective',
            'themes': 'weather',
            'examples': [
                ('Hace mucho frío hoy.', 'It is very cold today.'),
                ('El agua está fría.', 'The water is cold.'),
                ('No me gusta el clima frío.', 'I don\'t like cold weather.')
            ]
        },
        {
            'spanish': 'casa',
            'english': 'house',
            'word_type': 'noun',
            'themes': 'home',
            'examples': [
                ('Mi casa es pequeña pero cómoda.', 'My house is small but comfortable.'),
                ('Vivo en una casa cerca del parque.', 'I live in a house near the park.'),
                ('La casa tiene tres dormitorios.', 'The house has three bedrooms.')
            ]
        },
        {
            'spanish': 'rápidamente',
            'english': 'quickly',
            'word_type': 'adverb',
            'themes': 'other',
            'examples': [
                ('Necesito terminar esto rápidamente.', 'I need to finish this quickly.'),
                ('El tiempo pasa rápidamente.', 'Time passes quickly.'),
                ('Ella camina muy rápidamente.', 'She walks very quickly.')
            ]
        },
        {
            'spanish': 'por cierto',
            'english': 'by the way',
            'word_type': 'phrase',
            'themes': 'other',
            'examples': [
                ('Por cierto, ¿has visto mi libro?', 'By the way, have you seen my book?'),
                ('Por cierto, mañana es mi cumpleaños.', 'By the way, tomorrow is my birthday.'),
                ('Por cierto, necesito hablar contigo.', 'By the way, I need to talk to you.')
            ]
        },
        # Function words (grammar)
        {
            'spanish': 'el',
            'english': 'the (masculine)',
            'word_type': 'function_word',
            'themes': 'other',
            'examples': [
                ('El gato es negro.', 'The cat is black.'),
                ('El sol brilla.', 'The sun shines.'),
                ('El libro está en la mesa.', 'The book is on the table.')
            ]
        },
        {
            'spanish': 'nuestro',
            'english': 'our',
            'word_type': 'function_word',
            'themes': 'other',
            'examples': [
                ('Nuestro coche es nuevo.', 'Our car is new.'),
                ('Este es nuestro proyecto.', 'This is our project.'),
                ('Nuestro equipo ganó el partido.', 'Our team won the game.')
            ]
        },
        # Numbers
        {
            'spanish': 'primero',
            'english': 'first',
            'word_type': 'number',
            'themes': 'other',
            'examples': [
                ('Es mi primer día de trabajo.', 'It is my first day of work.'),
                ('Llegó primero a la meta.', 'He arrived first at the finish line.'),
                ('El primer capítulo es interesante.', 'The first chapter is interesting.')
            ]
        },
        {
            'spanish': 'cinco',
            'english': 'five',
            'word_type': 'number',
            'themes': 'other',
            'examples': [
                ('Tengo cinco hermanos.', 'I have five siblings.'),
                ('Son las cinco de la tarde.', 'It is five in the afternoon.'),
                ('Necesitamos cinco sillas más.', 'We need five more chairs.')
            ]
        },
        # More content words
        {
            'spanish': 'trabajar',
            'english': 'to work',
            'word_type': 'verb',
            'themes': 'work',
            'examples': [
                ('Necesito trabajar mañana.', 'I need to work tomorrow.'),
                ('Ella trabaja en un hospital.', 'She works at a hospital.'),
                ('Me gusta trabajar en equipo.', 'I like to work in a team.')
            ]
        },
        {
            'spanish': 'sol',
            'english': 'sun',
            'word_type': 'noun',
            'themes': 'weather',
            'examples': [
                ('El sol sale por la mañana.', 'The sun rises in the morning.'),
                ('Hace sol hoy.', 'It is sunny today.'),
                ('Me gusta tomar el sol.', 'I like to sunbathe.')
            ]
        },
        {
            'spanish': 'lejos',
            'english': 'far away',
            'word_type': 'adverb',
            'themes': 'travel',
            'examples': [
                ('Mi casa está lejos del centro.', 'My house is far from downtown.'),
                ('No queda lejos de aquí.', 'It is not far from here.'),
                ('Vive muy lejos.', 'He/she lives very far away.')
            ]
        },
        {
            'spanish': 'fácil',
            'english': 'easy',
            'word_type': 'adjective',
            'themes': 'other',
            'examples': [
                ('Este ejercicio es fácil.', 'This exercise is easy.'),
                ('No es fácil aprender español.', 'It is not easy to learn Spanish.'),
                ('La pregunta era muy fácil.', 'The question was very easy.')
            ]
        },
        {
            'spanish': 'difícil',
            'english': 'difficult',
            'word_type': 'adjective',
            'themes': 'other',
            'examples': [
                ('Este problema es difícil.', 'This problem is difficult.'),
                ('Fue un día difícil.', 'It was a difficult day.'),
                ('Es difícil tomar una decisión.', 'It is difficult to make a decision.')
            ]
        },
        {
            'spanish': 'cerca',
            'english': 'close by, near',
            'word_type': 'adverb',
            'themes': 'travel',
            'examples': [
                ('La tienda está muy cerca.', 'The store is very close.'),
                ('Vivo cerca de la escuela.', 'I live near the school.'),
                ('El parque está cerca de aquí.', 'The park is close to here.')
            ]
        },
    ]

    # Create words and examples
    created_count = 0
    for word_data in words_data:
        word = V2Word(
            user_id=user.id,
            spanish=word_data['spanish'],
            english=word_data['english'],
            word_type=word_data['word_type'],
            themes=word_data['themes'],
            is_learned=False
        )
        db.session.add(word)
        db.session.flush()  # Get word.id

        # Add examples
        for spanish_sent, english_sent in word_data['examples']:
            example = V2GeneratedExample(
                word_id=word.id,
                spanish_sentence=spanish_sent,
                english_translation=english_sent
            )
            db.session.add(example)

        created_count += 1

    db.session.commit()
    print(f"\n✅ Successfully seeded {created_count} words with {created_count * 3} example sentences!")
    print(f"   User: {user.email}")
    print(f"   Password: password123")
    print(f"\n   Log in and visit /v2/ to see the vocabulary!")
