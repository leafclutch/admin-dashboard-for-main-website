# 🖼️ Image Upload Flow - Developer Guide

This guide explains how to implement image uploads in the frontend. We use a **Direct-to-Cloudinary** approach to keep the backend fast and scalable.

---

## 💡 Why this design?
Instead of sending large image files to our backend, the frontend uploads them directly to **Cloudinary**. 
*   **Backend's Job**: Acts as a "Security Guard" to give you a signed permission slip (Signature).
*   **Frontend's Job**: Uploads the file to Cloudinary and gets a URL.
*   **Final Step**: Save that URL to our database.

---

## 🔄 The 3-Step Process

### Step 1: Get Upload Permission (Backend)
Before uploading, you must ask our backend for a secure signature.

*   **Endpoint**: `POST /admin/uploads/signature`
*   **Auth**: Requires Admin Bearer Token.
*   **Response Format**:
```json
{
    "cloud_name": "your_cloud_name",
    "api_key": "123456789012345",
    "timestamp": 1704710000,
    "signature": "abcd1234efgh5678...",
    "folder": "uploads"
}
```

---

### Step 2: Upload to Cloudinary (External)
Use the data from Step 1 to send the actual image file to Cloudinary.

*   **Cloudinary API**: `https://api.cloudinary.com/v1_1/{cloud_name}/image/upload`
*   **Method**: `POST` (Multipart Form Data)
*   **Body Fields**:
    1.  `file`: The actual image file.
    2.  `api_key`: (From Step 1)
    3.  `timestamp`: (From Step 1)
    4.  `signature`: (From Step 1)
    5.  `folder`: (From Step 1)

**Response**: Cloudinary will return a large JSON. You only need the `secure_url`.
```json
{
    "secure_url": "https://res.cloudinary.com/demo/image/upload/v1/uploads/sample.jpg",
    ...
}
```

---

### Step 3: Save the URL to our Database (Backend)
Now that you have the `secure_url`, send it to the relevant backend endpoint (e.g., creating a Project, Member, or Service).

*   **Example Payload**:
```json
{
    "title": "New Project",
    "photo_url": "https://res.cloudinary.com/demo/image/upload/v1/uploads/sample.jpg",
    ...
}
```

---

## 🛠️ Frontend Implementation Example (JavaScript)

```javascript
// 1. Get Signature from our Backend
const sigResponse = await fetch('/admin/uploads/signature', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` }
});
const signData = await sigResponse.json();

// 2. Upload directly to Cloudinary
const formData = new FormData();
formData.append('file', imageFile);
formData.append('api_key', sigData.api_key);
formData.append('timestamp', sigData.timestamp);
formData.append('signature', sigData.signature);
formData.append('folder', sigData.folder);

const cloudResponse = await fetch(`https://api.cloudinary.com/v1_1/${sigData.cloud_name}/image/upload`, {
    method: 'POST',
    body: formData
});
const cloudData = await cloudResponse.json();

// 3. Use the URL
const finalImageUrl = cloudData.secure_url;
console.log("Upload Success:", finalImageUrl);
```

---

## ⚠️ Important Rules
1.  **Don't send files to the backend**: The backend only accepts URLs (strings).
2.  **Signatures are temporary**: Get a fresh signature right before every upload.
3.  **Loading States**: Disable your "Save" button while the Cloudinary upload is in progress.
