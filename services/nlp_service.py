def process_health_query(text: str):
    text = text.lower()

    # Fever
    if any(word in text for word in ["fever", "temperature"]):
        return (
            "If you have a fever, take rest, drink plenty of fluids, and monitor your temperature. "
            "If fever persists for more than two days, consult a doctor.",
            0.92
        )

    # Cough / Cold
    if any(word in text for word in ["cough", "cold", "sore throat"]):
        return (
            "For cough or cold, drink warm fluids and get enough rest. "
            "If symptoms worsen or last several days, seek medical advice.",
            0.90
        )

    # Headache
    if any(word in text for word in ["headache", "head pain"]):
        return (
            "A mild headache can improve with rest and hydration. "
            "If headaches are severe or frequent, consult a healthcare professional.",
            0.88
        )

    # Stomach pain
    if any(word in text for word in ["stomach pain", "abdominal pain", "stomach ache"]):
        return (
            "For mild stomach pain, eat light food and stay hydrated. "
            "If pain is severe or persistent, consult a doctor.",
            0.88
        )

    # Dehydration
    if any(word in text for word in ["dehydration", "dizzy", "dizziness"]):
        return (
            "Dehydration can cause dizziness. Drink water or oral rehydration fluids regularly. "
            "If symptoms continue, seek medical help.",
            0.89
        )

    # Diabetes awareness
    if "diabetes" in text or "sugar" in text:
        return (
            "If you have diabetes, monitor your blood sugar regularly and follow a balanced diet. "
            "Consult a doctor for personalized guidance.",
            0.87
        )

    # Blood pressure
    if any(word in text for word in ["blood pressure", "bp"]):
        return (
            "Maintaining healthy blood pressure involves a balanced diet, low salt intake, and regular activity. "
            "Consult a doctor for proper evaluation.",
            0.87
        )

    # Default fallback
    return (
        "Please describe your symptoms in more detail so I can provide general health guidance.",
        0.85
    )
