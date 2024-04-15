# GeminiHealth

GeminiHealth is a revolutionary healthcare platform designed to streamline medical record management, provide personalized health insights, and empower users to take control of their well-being whilst on the other hand helps food catering companies intelligently control their menu, store keeping, and orders. Built on cutting-edge technologies and powered by artificial intelligence , I meant Googles Gemini Model . Gemini Health offers a seamless integraton experience for both healthcare providers patients and catering companies.

## Key Features

- **Medical Profile Management**: Users can easily create and manage their medical profiles, including conditions, allergies, medications, and dietary preferences.

- **AI-Driven Insights**: Leveraging state-of-the-art AI algorithms, GeminiHealth provides personalized health insights and recommendations tailored to each user's unique medical history and lifestyle.


- **Recipe Generation**: Our platform generates customized recipes based on users' dietary preferences, allergies, and nutritional needs, making meal planning effortless and enjoyable.

- **Healthcare Provider Integration**: GeminiHealth seamlessly integrates with healthcare providers' systems, allowing for real-time sharing of medical records and facilitating collaboration between patients and providers.

- **Market Order Generation**: Using AI and information based on some company activities and meta data of users around their location gemini health is able to intelligently create 90% efficient market orders.

## Technologies Used

- Django: Backend framework for building robust and scalable web applications.
- React: Frontend library for creating dynamic and interactive user interfaces.
- Gemini: AI model used in development.
- PostgreSQL: Relational database management system for storing user data securely.

## Installation

To run GeminiHealth locally, follow these steps:

1. Clone the repository: 
```bash
   git clone https://github.com/ugochukwu-850/GeminiHealth.git
   ```
2. Navigate to the project directory: ```cd GeminiHealth```
3. Create an environment and activate it: 
```python 
   python venv -m geminienv
   source geminienv/bin/activate
   ```
4. Install dependencies: 
```bash
   pip install -r requirements.txt
   ```
5. Set up the database: 
```bash 
   python manage.py migrate
   ```
6. Populate some default models : 
```bash
   python manage.py populate ingredients 
   ```
7. Start the development server: 
```bash 
   python manage.py runserver
   ```

## Getting Started

Visit [GeminiHealth](http://localhost:8000) in your web browser to create an account or log in if you already have one. Explore the various features offered by the platform and start your journey towards better health today!

## Contributing

We welcome contributions from the community! Whether you're a developer, designer, or healthcare professional, there are many ways to get involved. Check out our [Contribution Guidelines](CONTRIBUTING.md) to learn how you can contribute to GeminiHealth.


## Support

If you have any questions, issues, or feedback, please don't hesitate to [contact us](mailto:ugochukwuchizaramoku@gmail.com). Our team is here to help and would love to hear from you!
