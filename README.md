# <div align="center"><h1 style="color: red;">Numerical_Analysis_Summer_Internship_2025</h1></div>

# Development of an Interactive Web Platform for Teaching and Visualizing Numerical Analysis Concepts

---

## Project Overview

This repository contains a project designed to enhance the pedagogical approach to teaching **Numerical Analysis**. The project seeks to provide **interactive tools** and **educational content** to improve the understanding of core concepts in Numerical Analysis, including techniques such as solving systems of linear equations, linear and polynomial regression, root-finding algorithms, numerical integration, and differential equations. It utilizes **Manim** for animation generation and aims to deliver clear, beginner-friendly videos and interactive web-based applications to help students gain a deeper understanding of these mathematical methods.

**Project ID:** R&D NA N°2-4

### Supervisor:
    Afif Beji, Ing., M.Sc.
    - Role: Assistant Professor and Project Supervisor 
    - Institution: ESPRIT, School of Engineers

### Interns:
    * Sirine Dahmane
    - Role: Student
    - Institution: ESPRIT, School of Engineers

---

## Project Goals

This project is aimed at achieving the following objectives:

- **Enhance Pedagogical Support:**  
  Provide instructors with robust didactical resources, such as code examples, animations, and teaching aids, to better explain Numerical Analysis concepts in a classroom setting.

- **Support Student Learning:**  
  Facilitate students’ understanding of **core Numerical Analysis methods** through interactive and visual learning experiences. Students will be able to explore key concepts such as **numerical methods for solving equations, interpolation, numerical integration, and optimization** with hands-on examples.

- **Leverage Manim for Mathematical Visualizations:**  
  Create clear and engaging visualizations using **Manim**, an animation library, to demonstrate the inner workings of common Numerical Analysis algorithms. These animations will serve as a visual aid for both students and instructors.

- **Develop Beginner-Friendly Educational Videos:**  
  Produce a series of **explainable educational videos** that break down complex Numerical Analysis concepts into easy-to-understand, step-by-step guides. These videos will feature real-world applications to make the concepts more relatable to students with no prior advanced knowledge.

- **Build an Interactive Web Application:**  
  Develop an **interactive, web-based application** that allows students and users to experiment with Numerical Analysis methods. This application will provide users with the ability to manipulate algorithms, visualize results, and gain practical experience.

---

## Technologies and Tools Used

The project employs a variety of technologies to create a user-friendly and interactive experience:

- **Python:** The core programming language for implementing numerical methods and backend logic.
- **Manim:** A Python library for creating mathematical animations. Used for generating high-quality visualizations of Numerical Analysis algorithms.
<--- **Flask:** A lightweight web framework used for creating the web application interface. It will serve the interactive content to users.
- **JavaScript (or other Frameworks):** For frontend interactivity and dynamic visualizations on the web application.
- **HTML/CSS:** For structuring and styling the web application interface.--!>
- **Jupyter Notebooks:** Used for prototyping and testing various Numerical Analysis algorithms and code snippets.

---

## Key Features

### 1. **Mathematical Animations with Manim**
   - The project will include **animated tutorials** explaining key numerical methods, such as:
     - **Root-finding algorithms** (e.g., Bisection, Fixed-points, and Newton methods)
     - **Linear and polynomial regression**
     - **Numerical integration** (e.g., Simpson's rule, trapezoidal rule)
     - **Finite difference methods** for solving differential equations
     - **Optimization techniques** (e.g. Gradient Descent)
     - etc.
   - These animations will help students visually understand the step-by-step process behind each algorithm, improving retention and comprehension.

### 2. **Interactive Web Application**
   - A **user-friendly interface** where users can experiment with different Numerical Analysis algorithms.
   - **Interactive sliders** and input fields for adjusting parameters (e.g., tolerance levels, grid sizes).
   - Real-time visualizations of algorithm outputs and comparisons, enabling users to see how changes affect the results.
   - **Examples and use cases** that show practical applications of Numerical Analysis in real-world problems.
   - The ability to **save and share results**, allowing students to work on problems collaboratively.

### 3. **Educational Videos**
   - A series of **video tutorials** that explain:
     - The core principles of Numerical Analysis
     - Common methods used in Numerical Analysis
     - Real-world applications of these methods
   - The videos will be designed for a beginner audience, with easy-to-follow explanations and visual demonstrations.

### 4. **Code Examples and Documentation**
   - All code used in the project will be **well-documented** to provide clarity on how the algorithms work and how they can be used in different contexts.
   - Detailed **explanations** of the mathematical concepts behind each method.
   - Examples of how to implement these methods in a variety of scenarios.

---

## Project Structure

The project is organized into the following key components:

```bash
├── animations/               # Manim animation scripts and generated videos
├── app/                       # Web application code (Flask app)
├── docs/                      # Documentation, educational resources
├── videos/                    # Educational video tutorials
├── notebooks/                 # Jupyter notebooks with code examples
└── README.md                  # Project overview and setup instructions
