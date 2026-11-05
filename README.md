# 🏋️‍♂️ Veer Batalion Elite Fitness Club - Gym Management System
**Course:** CSE326 - Internet Programming / Web Development  
**Assessment:** CA2 Project  
**Tech Stack:** HTML5, CSS3, JavaScript, Python (Flask)  
**Compatibility:** Universal (Mobile, Tablet, Laptop, Desktop | Windows, Mac, Linux, Android, iOS)

---

## 📌 Project Overview
Ye project ek **Universal Cross-Platform Gym Management System** web application hai jo gym ki daily operations aur member management ke liye banaya gaya hai. 

Ise **har tarah ke system, screen size, aur browser** ke compatible banaya gaya hai:
- 📱 **Mobile Phones** (Android, iPhone, screen width 320px - 480px)
- 📲 **Tablets & iPads** (Portrait aur Landscape 768px - 1024px)
- 💻 **Laptops & Desktops** (Windows, macOS, Linux, 1200px - 1920px+)
- 🌐 **All Browsers** (Google Chrome, Microsoft Edge, Mozilla Firefox, Apple Safari, Opera)

---

## 📱 Har System Ke Liye Kiye Gaye Compatibility Features

1. **Responsive Mobile Navigation (Hamburger Menu):**
   - Chhote phone screens par navigation bar lamba nahi hota; **`☰ MENU`** button aata hai jo tap karne par khulta hai aur link select karte hi auto-close ho jata hai.
2. **Horizontal Scrollable Tables (Touch Enabled):**
   - 8-column members directory aur weekly timetable chhote screens par squish nahi hote.
   - `-webkit-overflow-scrolling: touch;` ke sath smooth left-right swipe diya gaya hai.
3. **Universal System Font Stack:**
   - `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Ubuntu, Arial, sans-serif` use kiya hai taaki Windows par Segoe UI, Mac/iOS par San Francisco, aur Android par Roboto naturally sharp dikhe.
4. **iOS Safari Zoom Prevention:**
   - iPhone/iPad par form inputs par tap karne par unwanted auto-zoom nahi hota (inputs set to 16px).
5. **Private / Incognito Browsing Protection:**
   - Safari Private Mode ya strict privacy settings me `localStorage` band hone par bhi app crash nahi hota (`try/catch` safety).
6. **Local Wi-Fi Network Access (`host='0.0.0.0'`):**
   - Agar aap laptop me Flask server chalate hain, to apne mobile phone ya dusre PC se bhi same Wi-Fi par `http://<your-ip>:5000/` khol kar access kar sakte hain.
7. **Offline Standalone Mode:**
   - Internet ya Python na hone par bhi direct **`index.html`** par double click karke poora project smoothly chalega.

---

## 🎯 Key Project Features

1. **Header & Navigation Bar:**
   - Custom SVG Logo (Circle + Lightning Bolt).
   - Brand: **VEER BATALION ELITE FITNESS CLUB**.
   - Links: Home, Plans, Register, Members, BMI Calculator, Schedule, Contact.
2. **Moving Marquee:**
   - High-energy scrolling announcement ticker.
3. **Hero Section:**
   - Gym background image (`bg.jpg`) with dark overlay and quick action buttons.
4. **Membership Plans (3 Responsive Cards):**
   - Basic Plan (₹999), Standard Plan (₹1,799), VIP Pro Plan (₹2,999).
   - "Select Plan" button auto-selects the plan in the registration form.
5. **New Member Admission Form (JS Validation):**
   - Full Name, 10-digit Phone validation, Age limit (15 - 70), Gender, Plan, Shift, Fee Status.
6. **Live Members Directory (Table):**
   - Real-time search filter by Name or Mobile number.
   - Delete member option.
   - Data persists via browser `localStorage`.
7. **Interactive BMI Calculator:**
   - Real-time BMI score formula: `weight / (height/100)^2`.
   - Category display (*Underweight, Normal, Overweight, Obese*) with workout/diet recommendation.
8. **Weekly Workout Timetable:**
   - Monday to Saturday day-wise exercise split.
9. **Contact & Submission Details:**
   - Gym details, phone helpline, timings, aur academic info.

---

## 💻 Project Run Kaise Karein

### Method 1: Python Flask Server (Recommended)
1. Terminal / PowerShell kholein:
   ```bash
   python my_app\app.py
   ```
2. Apne computer ke browser me ye link kholein:
   ```
   http://127.0.0.1:5000/
   ```
   *(Local Wi-Fi par kisi dusre phone/laptop se access karne ke liye: `http://<Laptop-IP>:5000/`)*

### Method 2: Direct Double-Click (Zero Setup)
- Project folder me jakar **`index.html`** file par double-click karein. 
- Ye kisi bhi computer (Windows/Mac/Linux) me bina kisi server ya software ke direct Chrome/Edge/Safari me chal jayegi!

---

## 🎓 Teacher Viva Questions & Answers

| Question | Answer (Kya Bolna Hai) |
| :--- | :--- |
| **Q1. Website ko responsive aur har device compatible kaise banaya?** | Humne CSS Grid (`repeat(auto-fit, minmax(...))`), Flexbox, aur Media Queries (`@media (max-width: 768px)`) use kiye hain. Sath hi mobile ke liye hamburger menu aur table horizontal scroll diya hai. |
| **Q2. Mobile par table kaise manage kiya?** | Table ko `.table-container` wrapper me daala hai jisme `overflow-x: auto` aur `-webkit-overflow-scrolling: touch` diya hai taaki phone par columns cut na hon balki smoothly swipe hon. |
| **Q3. Form validation kaise kaam karti hai?** | `script.js` me JavaScript se empty fields, 10-digit mobile number (`length === 10 && !isNaN(mobile)`), aur age (15-70) validate ki gayi hai. |
| **Q4. BMI formula kya hai?** | `BMI = Weight (kg) / (Height in meters)^2`. Height (cm) ko meter me convert karne ke liye `height / 100` kiya hai. |
| **Q5. Data refresh karne par save kaise rehta hai?** | Browser ke `localStorage` me JSON string ke roop me data save hota hai, jise humne `try/catch` block se safe banaya hai. |
