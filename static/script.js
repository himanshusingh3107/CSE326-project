/* ==========================================================================
   CSE326 CA2 - Gym Management System
   Author: Student Project
   Description: JavaScript code for Form Validation, Member Table, Search, and BMI
   Compatibility: Universal (All Browsers, Mobile Touch & Desktop)
   ========================================================================== */

// Array to hold gym members data
let membersList = [];

// Initial sample data if no data exists
const defaultMembers = [
    {
        name: "Aman Kumar",
        mobile: "9876543210",
        age: 21,
        gender: "Male",
        plan: "Standard Plan",
        batch: "Morning (06:00 AM - 08:00 AM)",
        feeStatus: "Paid"
    },
    {
        name: "Simran Kaur",
        mobile: "9812345678",
        age: 20,
        gender: "Female",
        plan: "VIP Pro Plan",
        batch: "Evening (05:00 PM - 07:00 PM)",
        feeStatus: "Paid"
    },
    {
        name: "Rahul Verma",
        mobile: "9988776655",
        age: 23,
        gender: "Male",
        plan: "Basic Plan",
        batch: "Night (07:30 PM - 09:30 PM)",
        feeStatus: "Pending"
    }
];

// Load members and initialize animations when page loads
window.addEventListener("DOMContentLoaded", function() {
    loadMembers();
    setupMobileNav();
    initTypingAnimation();
    initTapAnimations();
});

// Dynamic Typing / Typewriter Animation for Hero Section
function initTypingAnimation() {
    const typingElement = document.getElementById("typingHeroText");
    if (!typingElement) return;

    const phrases = [
        "BUILD YOUR BODY, FORGE YOUR MIND",
        "DISCOVER YOUR TRUE STRENGTH",
        "TRAIN WITH CERTIFIED COACHES",
        "CRUSH YOUR FITNESS GOALS IN 2026"
    ];

    let phraseIndex = 0;
    let charIndex = phrases[0].length;
    let isDeleting = true;

    function typeLoop() {
        const currentPhrase = phrases[phraseIndex];

        if (isDeleting) {
            charIndex--;
            typingElement.textContent = currentPhrase.substring(0, charIndex);
        } else {
            charIndex++;
            typingElement.textContent = currentPhrase.substring(0, charIndex);
        }

        let delay = isDeleting ? 38 : 68;

        if (!isDeleting && charIndex === currentPhrase.length) {
            delay = 2400;
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            phraseIndex = (phraseIndex + 1) % phrases.length;
            delay = 350;
        }

        setTimeout(typeLoop, delay);
    }

    setTimeout(typeLoop, 2000);
}

// Tactile Tap & Ripple Feedback Animation
function initTapAnimations() {
    document.addEventListener("pointerdown", function(event) {
        const button = event.target.closest(".btn, .plan-card button, .nav-toggle-btn");
        if (!button) return;

        const rect = button.getBoundingClientRect();
        const ripple = document.createElement("span");
        ripple.className = "ripple-wave";

        const size = Math.max(rect.width, rect.height);
        const radius = size / 2;

        ripple.style.width = ripple.style.height = size + "px";
        ripple.style.left = (event.clientX - rect.left - radius) + "px";
        ripple.style.top = (event.clientY - rect.top - radius) + "px";

        const existing = button.querySelector(".ripple-wave");
        if (existing) existing.remove();

        button.appendChild(ripple);

        setTimeout(function() {
            if (ripple.parentNode === button) {
                ripple.remove();
            }
        }, 550);
    });
}

// 1. Mobile Navigation Toggle & Auto-Close
function toggleNav() {
    const nav = document.getElementById("navbarMenu");
    if (nav) {
        nav.classList.toggle("show-nav");
    }
}

function setupMobileNav() {
    const navLinks = document.querySelectorAll(".navbar a");
    const nav = document.getElementById("navbarMenu");
    navLinks.forEach(function(link) {
        link.addEventListener("click", function() {
            if (nav && nav.classList.contains("show-nav")) {
                nav.classList.remove("show-nav");
            }
        });
    });
}

// Check if running on HTTP server or local static file
const isHttpServer = window.location.protocol.startsWith("http");

// 2. Load members from Backend API (with LocalStorage fallback)
async function loadMembers() {
    if (isHttpServer) {
        try {
            const response = await fetch("/api/v1/members");
            if (response.ok) {
                const result = await response.json();
                if (result.success && Array.isArray(result.data)) {
                    membersList = result.data;
                    displayMembers(membersList);
                    saveMembers();
                    return;
                }
            }
        } catch (error) {
            console.warn("Backend API unavailable, using offline cache:", error);
        }
    }

    try {
        const saved = localStorage.getItem("gym_members");
        if (saved) {
            membersList = JSON.parse(saved);
        } else {
            membersList = defaultMembers.slice();
            saveMembers();
        }
    } catch (e) {
        membersList = defaultMembers.slice();
    }
    displayMembers(membersList);
}

// 3. Save members to LocalStorage (safe)
function saveMembers() {
    try {
        localStorage.setItem("gym_members", JSON.stringify(membersList));
    } catch (e) {
        console.warn("LocalStorage is disabled or unavailable:", e);
    }
}

// 4. Display members inside the HTML Table
function displayMembers(list) {
    const tableBody = document.getElementById("membersTableBody");
    const countSpan = document.getElementById("totalMembersCount");
    
    if (!tableBody) return;

    // Clear existing rows
    tableBody.innerHTML = "";

    // Update total count
    if (countSpan) {
        countSpan.innerText = list.length;
    }

    if (list.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="8" style="text-align:center; color: #888; padding: 20px;">No members found matching your search.</td></tr>';
        return;
    }

    // Loop through array and create rows
    for (let i = 0; i < list.length; i++) {
        const member = list[i];
        const statusClass = member.feeStatus === "Paid" ? "status-paid" : "status-pending";

        const row = `
            <tr>
                <td>${i + 1}</td>
                <td><strong>${escapeHtml(member.name)}</strong></td>
                <td>${escapeHtml(member.mobile)}</td>
                <td>${escapeHtml(String(member.age))} / ${escapeHtml(member.gender)}</td>
                <td>${escapeHtml(member.plan)}</td>
                <td>${escapeHtml(member.batch)}</td>
                <td><span class="${statusClass}">${escapeHtml(member.feeStatus)}</span></td>
                <td>
                    <button class="btn-delete" onclick="deleteMember(${i})" title="Remove Member">Delete</button>
                </td>
            </tr>
        `;
        tableBody.innerHTML += row;
    }
}

// Helper to escape HTML characters
function escapeHtml(str) {
    if (!str) return "";
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// 5. Form Submission and Validation
function handleRegistration(event) {
    event.preventDefault(); // Prevent page reload

    // Get input values safely
    const nameInput = document.getElementById("fullName");
    const mobileInput = document.getElementById("phoneNumber");
    const ageInput = document.getElementById("memberAge");
    const genderInput = document.getElementById("gender");
    const planInput = document.getElementById("membershipPlan");
    const batchInput = document.getElementById("shift");
    const feeStatusInput = document.getElementById("feeStatus");

    const name = nameInput ? nameInput.value.trim() : "";
    const mobile = mobileInput ? mobileInput.value.trim() : "";
    const age = ageInput ? ageInput.value.trim() : "";
    const gender = genderInput ? genderInput.value : "";
    const plan = planInput ? planInput.value : "";
    const batch = batchInput ? batchInput.value : "";
    const feeStatus = feeStatusInput ? feeStatusInput.value : "Pending";

    // Validation checks
    if (name.length < 3) {
        alert("Please enter a valid full name (minimum 3 letters).");
        if (nameInput) nameInput.focus();
        return;
    }

    if (mobile.length !== 10 || isNaN(mobile)) {
        alert("Please enter a valid 10-digit mobile number.");
        if (mobileInput) mobileInput.focus();
        return;
    }

    const ageNum = parseInt(age, 10);
    if (isNaN(ageNum) || ageNum < 15 || ageNum > 70) {
        alert("Age must be between 15 and 70 years.");
        if (ageInput) ageInput.focus();
        return;
    }

    if (gender === "") {
        alert("Please select gender.");
        if (genderInput) genderInput.focus();
        return;
    }

    if (plan === "") {
        alert("Please select a membership plan.");
        if (planInput) planInput.focus();
        return;
    }

    // Create new member object
    const newMember = {
        name: name,
        phone: mobile,
        mobile: mobile,
        age: ageNum,
        gender: gender,
        plan: plan,
        batch: batch,
        status: feeStatus,
        feeStatus: feeStatus
    };

    if (isHttpServer) {
        fetch("/api/v1/members", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newMember)
        })
        .then(function(res) { return res.json(); })
        .then(function(response) {
            if (!response.success) {
                const message = (response.error && response.error.message) ? response.error.message : "Registration failed.";
                alert("Error: " + message);
                return;
            }
            alert("Success! " + name + " has been registered successfully.");
            const form = document.getElementById("gymForm");
            if (form) form.reset();
            loadMembers();
            const membersSec = document.getElementById("members");
            if (membersSec) {
                membersSec.scrollIntoView({ behavior: "smooth" });
            }
        })
        .catch(function(err) {
            console.warn("Backend error, storing locally:", err);
            membersList.push(newMember);
            saveMembers();
            displayMembers(membersList);
            const form = document.getElementById("gymForm");
            if (form) form.reset();
            alert("Success! " + name + " has been registered successfully (offline mode).");
        });
        return;
    }

    // Offline / LocalStorage fallback
    membersList.push(newMember);
    saveMembers();
    displayMembers(membersList);

    const form = document.getElementById("gymForm");
    if (form) form.reset();
    alert("Success! " + name + " has been registered successfully.");

    const membersSec = document.getElementById("members");
    if (membersSec) {
        membersSec.scrollIntoView({ behavior: "smooth" });
    }
}

// 6. Delete Member
function deleteMember(index) {
    const targetMember = membersList[index];
    const memberName = targetMember ? targetMember.name : "this member";
    const confirmDelete = confirm("Are you sure you want to delete " + memberName + "?");
    if (!confirmDelete) return;

    if (isHttpServer && targetMember && targetMember.id) {
        fetch("/api/v1/members/" + targetMember.id, {
            method: "DELETE"
        })
        .then(function(res) { return res.json(); })
        .then(function(response) {
            if (response.success) {
                loadMembers();
            } else {
                alert("Could not delete member: " + (response.error ? response.error.message : "Error"));
            }
        })
        .catch(function(err) {
            console.warn("Delete API failed, falling back to local:", err);
            membersList.splice(index, 1);
            saveMembers();
            displayMembers(membersList);
        });
        return;
    }

    membersList.splice(index, 1);
    saveMembers();
    displayMembers(membersList);
}

// 7. Search Member by Name or Mobile
function searchMember() {
    const searchElem = document.getElementById("searchInput");
    const searchVal = searchElem ? searchElem.value.toLowerCase().trim() : "";
    
    const filteredList = membersList.filter(function(member) {
        const matchName = member.name.toLowerCase().indexOf(searchVal) !== -1;
        const matchPhone = String(member.mobile).indexOf(searchVal) !== -1;
        return matchName || matchPhone;
    });

    displayMembers(filteredList);
}

// 8. Auto-select plan from pricing card click
function selectPlan(planName) {
    const planDropdown = document.getElementById("membershipPlan");
    if (planDropdown) {
        planDropdown.value = planName;
    }
    alert("You selected " + planName + ". Please complete the admission form below!");
    const registerSec = document.getElementById("register");
    if (registerSec) {
        registerSec.scrollIntoView({ behavior: "smooth" });
    }
}

// 9. Interactive BMI Calculator
function calculateBMI() {
    const heightInput = document.getElementById("heightCm");
    const weightInput = document.getElementById("weightKg");

    const height = heightInput ? parseFloat(heightInput.value) : 0;
    const weight = weightInput ? parseFloat(weightInput.value) : 0;

    // Check valid inputs
    if (isNaN(height) || height <= 0 || height > 280) {
        alert("Please enter a valid height in cm (e.g. 170).");
        if (heightInput) heightInput.focus();
        return;
    }

    if (isNaN(weight) || weight <= 0 || weight > 350) {
        alert("Please enter a valid weight in kg (e.g. 65).");
        if (weightInput) weightInput.focus();
        return;
    }

    if (isHttpServer) {
        fetch("/api/v1/fitness/bmi", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ height_cm: height, weight_kg: weight })
        })
        .then(function(res) { return res.json(); })
        .then(function(response) {
            if (response.success && response.data) {
                const info = response.data;
                const resultBox = document.getElementById("bmiResult");
                const bmiNumber = document.getElementById("bmiNumber");
                const bmiCategory = document.getElementById("bmiCategory");
                const bmiAdvice = document.getElementById("bmiAdvice");

                if (bmiNumber) bmiNumber.innerText = info.bmi_score;
                if (resultBox) resultBox.style.display = "block";
                if (bmiCategory) {
                    bmiCategory.innerText = info.category + " (" + info.risk_level + ")";
                    bmiCategory.className = "bmi-status " + (info.category === "Normal" ? "status-normal" : "status-overweight");
                }
                if (bmiAdvice) {
                    bmiAdvice.innerText = "Target Healthy Weight: " + info.target_healthy_weight_min_kg + "kg - " + info.target_healthy_weight_max_kg + "kg. Workout: " + info.workout_advice + " Diet: " + info.dietary_advice;
                }
            }
        })
        .catch(function(err) {
            console.warn("API BMI calculation fallback:", err);
            renderClientBmi(height, weight);
        });
        return;
    }

    renderClientBmi(height, weight);
}

function renderClientBmi(height, weight) {
    const heightInMeters = height / 100;
    const bmi = (weight / (heightInMeters * heightInMeters)).toFixed(1);

    const resultBox = document.getElementById("bmiResult");
    const bmiNumber = document.getElementById("bmiNumber");
    const bmiCategory = document.getElementById("bmiCategory");
    const bmiAdvice = document.getElementById("bmiAdvice");

    if (bmiNumber) bmiNumber.innerText = bmi;
    if (resultBox) resultBox.style.display = "block";

    // Check Category
    if (bmi < 18.5) {
        if (bmiCategory) {
            bmiCategory.innerText = "Underweight";
            bmiCategory.className = "bmi-status status-underweight";
        }
        if (bmiAdvice) {
            bmiAdvice.innerText = "Recommendation: You are underweight. Eat a high-protein calorie-surplus diet and do weight training!";
        }
    } else if (bmi >= 18.5 && bmi <= 24.9) {
        if (bmiCategory) {
            bmiCategory.innerText = "Normal / Healthy Weight";
            bmiCategory.className = "bmi-status status-normal";
        }
        if (bmiAdvice) {
            bmiAdvice.innerText = "Recommendation: Great job! Your weight is in the healthy range. Maintain it with regular workouts!";
        }
    } else if (bmi >= 25.0 && bmi <= 29.9) {
        if (bmiCategory) {
            bmiCategory.innerText = "Overweight";
            bmiCategory.className = "bmi-status status-overweight";
        }
        if (bmiAdvice) {
            bmiAdvice.innerText = "Recommendation: You are overweight. Combine cardio, HIIT exercises, and a calorie-deficit diet!";
        }
    } else {
        if (bmiCategory) {
            bmiCategory.innerText = "Obese";
            bmiCategory.className = "bmi-status status-obese";
        }
        if (bmiAdvice) {
            bmiAdvice.innerText = "Recommendation: High health risk. Consult our personal gym trainer for a customized fat-loss workout!";
        }
    }
}
