# 📊 Database Design (Simple Guide)

This document explains how our backend stores data. Think of the database as a set of **Excel Sheets** that are connected to each other.

---

## 1. Admin & Security
*   **Admin Users**: Stores people who can log in to the dashboard (Email and Password).

## 2. Team & Members
*   **Members**: Stores everyone working at the company. 
    *   It has a `role` to tell if they are a **Team Member** or an **Intern**.
    *   Stores social media links, photos, and contact info.

## 3. Services (What we sell)
*   **Services**: The main services we offer (e.g., Web Development).
*   **Service Techs**: A list of technologies (like React, Python).
*   **Service Offerings**: Specific things included in a service (e.g., "SEO Optimization").
*   *Connection*: A Service can have many Techs and many Offerings.

## 4. Projects (Our Work)
*   **Projects**: Real-world projects we have finished.
*   **Project Feedbacks**: Reviews from clients for a specific project.
*   *Connection*: Each Feedback belongs to one Project.

## 5. Opportunities (Hiring)
*   **Opportunities**: This is one big table for both **Jobs** and **Internships**.
*   **Job Details**: Extra info only for Jobs (Salary, Type).
*   **Internship Details**: Extra info only for Internships (Duration, Stipend).
*   **Requirements**: A list of "Must-haves" for the position.
*   *Connection*: An Opportunity is either a Job or an Internship.

## 6. Training (Courses)
*   **Trainings**: Courses we offer.
*   **Benefits**: What the student gets from the course.
*   **Mentors**: The teachers for the courses.
*   *Connection*: One training can have many mentors and many benefits.

---

## 💡 Key Terms for Interns:
*   **ID (UUID)**: A long unique string like `eb6c607c...`. Every item has one. Use this to fetch or delete a specific item.
*   **Foreign Key**: A "link". For example, a Feedback has a `project_id` so it knows which project it belongs to.
*   **Enum**: A fixed list of choices (e.g., Type can ONLY be `JOB` or `INTERNSHIP`).
