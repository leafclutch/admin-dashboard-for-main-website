# 📖 API Documentation (Intern Guide)

This guide explains how to use the Leafclutch Backend API. If you are building the Frontend, this is the only document you need to read!

---

## 🌍 1. The Basics
*   **Base URL**: `http://localhost:8000`
*   **Interactive Docs**: Go to `http://localhost:8000/docs` to test everything in your browser.

---

## 🔑 2. Authentication (Logging In)
Most "Admin" pages need you to be logged in.

1.  **Login**: Send a `POST` request to `/auth/login` with your email and password.
2.  **The Token**: You will get back an `access_token`.
3.  **Using the Token**: For every other request, you must add a header:
    `Authorization: Bearer YOUR_TOKEN_HERE`

---

## 📁 3. Projects & Feedback
Use these to manage the "Our Work" section.

*   **List Projects**: `GET /admin/projects` (Returns all projects).
*   **Create Project**: `POST /admin/projects`
    *   *Note*: You need to send `tech_ids` (a list of IDs from the Service Techs table).
*   **Add Feedback**: `POST /admin/projects/{project_id}/feedbacks`
    *   Use this to add a client review to a specific project.

---

## 💼 4. Opportunities (Jobs & Internships)
These are the hiring posts.

*   **List All**: `GET /api/admin/opportunities`
    *   *Search*: You can add `?search=React` to find specific titles.
    *   *Filter*: Use `?type=JOB` or `?type=INTERNSHIP`.
*   **Create**: `POST /api/admin/opportunities`
    *   **Important**: If the type is `JOB`, you **must** fill in `job_details`. If it's `INTERNSHIP`, fill in `internship_details`.

---

## 👥 5. Members (Team & Interns)
*   **All Members**: `GET /admin/members`
*   **Only Team**: `GET /admin/members/teams`
*   **Only Interns**: `GET /admin/members/interns`
*   **Update**: `PATCH /admin/members/{id}` (Use this to change a photo or position).

---

## 🛠 6. Services & Tech Stack
*   **Services**: `GET /admin/services` (Main services like Web Dev).
*   **Techs**: `GET /admin/service-techs` (List of tech names like "React", "Node").
*   **Offerings**: `GET /admin/service-offerings` (List of features like "SEO", "Cloud").

---

## 🎓 7. Training & Mentors
*   **Trainings**: `GET /admin/trainings` (Courses offered).
*   **Mentors**: `GET /admin/mentors` (The teachers).

---

## ⚠️ 8. Common Status Codes
*   **200 / 201**: Success! Everything worked.
*   **401**: Unauthorized. You forgot the Token or it expired.
*   **404**: Not Found. The ID you sent doesn't exist in the database.
*   **422**: Validation Error. You sent the wrong data format (e.g., sent a string where a number was expected).
